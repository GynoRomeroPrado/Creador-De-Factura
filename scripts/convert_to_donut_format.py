#!/usr/bin/env python3
"""
Script de conversión de datos al formato Donut

Convierte JSONs de facturas + imágenes al formato requerido por Donut:
- metadata.jsonl
- Estructura de carpetas train/val/test
- Validación de datos

Uso:
    python scripts/convert_to_donut_format.py \
        --input-json "Datos extraidos de Originales/anotaciones" \
        --input-images "Datos extraidos de Originales/facturas_procesadas" \
        --output "dataset_donut" \
        --split 0.8 0.1 0.1
"""

import argparse
import json
import shutil
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import random
from datetime import datetime


class DonutDatasetConverter:
    """Conversor de datos al formato Donut"""

    def __init__(
        self,
        input_json_dir: str,
        input_images_dir: str,
        output_dir: str,
        train_ratio: float = 0.8,
        val_ratio: float = 0.1,
        test_ratio: float = 0.1,
        seed: int = 42
    ):
        self.input_json_dir = Path(input_json_dir)
        self.input_images_dir = Path(input_images_dir)
        self.output_dir = Path(output_dir)

        self.train_ratio = train_ratio
        self.val_ratio = val_ratio
        self.test_ratio = test_ratio
        self.seed = seed

        # Validar ratios
        assert abs(train_ratio + val_ratio + test_ratio - 1.0) < 0.01, \
            "Los ratios deben sumar 1.0"

        random.seed(seed)

    def convert(self, schema_level: str = "intermedio"):
        """
        Convertir dataset completo

        Args:
            schema_level: "basico" (20 campos), "intermedio" (50 campos), "completo" (97 campos)
        """
        print("🍩 Conversión a formato Donut")
        print(f"   Esquema: {schema_level}")
        print(f"   Input JSONs: {self.input_json_dir}")
        print(f"   Input Imágenes: {self.input_images_dir}")
        print(f"   Output: {self.output_dir}")
        print()

        # 1. Crear estructura de directorios
        self._create_directories()

        # 2. Cargar y procesar datos
        data_pairs = self._load_data_pairs()
        print(f"✓ Encontrados {len(data_pairs)} pares JSON-Imagen")

        # 3. Aplicar transformación según nivel de esquema
        transformed_data = self._transform_schema(data_pairs, schema_level)
        print(f"✓ Datos transformados a esquema '{schema_level}'")

        # 4. Validar datos
        valid_data = self._validate_data(transformed_data)
        print(f"✓ Validados {len(valid_data)} pares (descartados {len(transformed_data) - len(valid_data)})")

        # 5. Split en train/val/test
        splits = self._split_data(valid_data)
        print(f"✓ Split: {len(splits['train'])} train, {len(splits['val'])} val, {len(splits['test'])} test")

        # 6. Guardar en formato Donut
        self._save_donut_format(splits)
        print(f"✓ Dataset guardado en {self.output_dir}")

        # 7. Generar estadísticas
        self._generate_statistics(splits)

        print("\n✅ Conversión completada!")

    def _create_directories(self):
        """Crear estructura de directorios"""
        for split in ["train", "validation", "test"]:
            (self.output_dir / split / "images").mkdir(parents=True, exist_ok=True)

    def _load_data_pairs(self) -> List[Dict]:
        """Cargar pares de JSON + Imagen"""
        pairs = []

        # Buscar todos los JSONs
        json_files = list(self.input_json_dir.glob("*.json"))

        for json_file in json_files:
            # Cargar JSON
            with open(json_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Buscar imagen correspondiente
            image_path = self._find_corresponding_image(json_file)

            if image_path:
                pairs.append({
                    "json_path": json_file,
                    "image_path": image_path,
                    "data": data
                })
            else:
                print(f"⚠️  No se encontró imagen para {json_file.name}")

        return pairs

    def _find_corresponding_image(self, json_file: Path) -> Optional[Path]:
        """Encontrar imagen correspondiente al JSON"""
        # El nombre del JSON debe coincidir con el de la imagen (sin extensión)
        base_name = json_file.stem

        # Buscar con diferentes extensiones
        for ext in [".pdf", ".jpg", ".jpeg", ".png"]:
            image_path = self.input_images_dir / f"{base_name}{ext}"
            if image_path.exists():
                return image_path

        return None

    def _transform_schema(self, data_pairs: List[Dict], level: str) -> List[Dict]:
        """
        Transformar esquema según nivel de complejidad

        Args:
            data_pairs: Lista de pares JSON-Imagen
            level: "basico", "intermedio", "completo"
        """
        transformed = []

        for pair in data_pairs:
            data = pair["data"]

            if level == "basico":
                transformed_data = self._transform_to_basic(data)
            elif level == "intermedio":
                transformed_data = self._transform_to_intermediate(data)
            else:  # completo
                transformed_data = data  # Ya está en formato completo

            transformed.append({
                **pair,
                "transformed_data": transformed_data
            })

        return transformed

    def _transform_to_basic(self, data: Dict) -> Dict:
        """Transformar a esquema básico (20 campos)"""
        return {
            "tipo_documento": data.get("tipo_documento"),
            "serie_completa": data.get("serie_completa"),
            "fecha_emision": data.get("fecha_emision"),
            "moneda": data.get("moneda"),

            "emisor": {
                "ruc": data.get("emisor_ruc"),
                "razon_social": data.get("emisor_razon_social")
            },

            "receptor": {
                "numero_doc": data.get("receptor_numero_doc"),
                "razon_social": data.get("receptor_razon_social")
            },

            "totales": {
                "subtotal": data.get("subtotal"),
                "igv": data.get("igv"),
                "total": data.get("importe_total")
            },

            "items": [
                {
                    "item": item.get("item"),
                    "descripcion": item.get("descripcion"),
                    "cantidad": item.get("cantidad"),
                    "precio_unitario": item.get("precio_unitario"),
                    "importe_total": item.get("importe_total_item")
                }
                for item in data.get("items", [])
            ]
        }

    def _transform_to_intermediate(self, data: Dict) -> Dict:
        """Transformar a esquema intermedio (50 campos)"""
        return {
            "documento": {
                "tipo": data.get("tipo_documento"),
                "serie_completa": data.get("serie_completa"),
                "fecha_emision": data.get("fecha_emision"),
                "fecha_vencimiento": data.get("fecha_vencimiento"),
                "moneda": data.get("moneda")
            },

            "emisor": {
                "ruc": data.get("emisor_ruc"),
                "razon_social": data.get("emisor_razon_social"),
                "nombre_comercial": data.get("emisor_nombre_comercial"),
                "direccion": data.get("emisor_direccion"),
                "departamento": data.get("emisor_departamento"),
                "provincia": data.get("emisor_provincia"),
                "distrito": data.get("emisor_distrito"),
                "telefono": data.get("emisor_telefono"),
                "email": data.get("emisor_email"),
                "web": data.get("emisor_web")
            },

            "receptor": {
                "tipo_doc": data.get("receptor_tipo_doc"),
                "numero_doc": data.get("receptor_numero_doc"),
                "razon_social": data.get("receptor_razon_social"),
                "direccion": data.get("receptor_direccion"),
                "departamento": data.get("receptor_departamento"),
                "provincia": data.get("receptor_provincia"),
                "distrito": data.get("receptor_distrito"),
                "contacto": data.get("receptor_contacto")
            },

            "importes": {
                "subtotal": data.get("subtotal"),
                "descuento": data.get("descuento"),
                "subtotal_con_descuento": data.get("subtotal_con_descuento"),
                "igv": data.get("igv"),
                "isc": data.get("isc"),
                "otros_cargos": data.get("otros_cargos"),
                "total": data.get("importe_total"),
                "detraccion_monto": data.get("detraccion_monto"),
                "detraccion_porcentaje": data.get("detraccion_porcentaje")
            },

            "referencias": {
                "orden_compra": data.get("orden_compra"),
                "guia_remision": data.get("guia_remision"),
                "numero_contrato": data.get("numero_contrato"),
                "condicion_pago": data.get("condicion_pago"),
                "forma_pago": data.get("forma_pago")
            },

            "items": [
                {
                    "item": item.get("item"),
                    "codigo": item.get("codigo"),
                    "descripcion": item.get("descripcion"),
                    "cantidad": item.get("cantidad"),
                    "unidad_medida": item.get("unidad_medida"),
                    "precio_unitario": item.get("precio_unitario"),
                    "valor_venta": item.get("valor_venta"),
                    "tipo_igv": item.get("tipo_igv"),
                    "igv_item": item.get("igv_item"),
                    "importe_total": item.get("importe_total_item"),
                    "observacion": item.get("observacion_item")
                }
                for item in data.get("items", [])
            ],

            "cuotas": [
                {
                    "numero": cuota.get("numero"),
                    "monto": cuota.get("monto"),
                    "fecha_vencimiento": cuota.get("fecha_vencimiento")
                }
                for cuota in data.get("cuotas", [])
            ]
        }

    def _validate_data(self, data_pairs: List[Dict]) -> List[Dict]:
        """Validar pares de datos"""
        valid_pairs = []

        for pair in data_pairs:
            try:
                # Validar que existan campos mínimos
                data = pair["transformed_data"]

                # Campos obligatorios según esquema
                required_fields = ["tipo_documento", "moneda"]

                # Validar presencia
                for field in required_fields:
                    if field not in str(data):
                        raise ValueError(f"Campo obligatorio faltante: {field}")

                # Validar imagen existe
                if not pair["image_path"].exists():
                    raise ValueError("Imagen no existe")

                valid_pairs.append(pair)

            except Exception as e:
                print(f"⚠️  Validación fallida para {pair['json_path'].name}: {e}")

        return valid_pairs

    def _split_data(self, data_pairs: List[Dict]) -> Dict[str, List[Dict]]:
        """Dividir datos en train/val/test"""
        # Mezclar datos
        random.shuffle(data_pairs)

        total = len(data_pairs)
        train_end = int(total * self.train_ratio)
        val_end = train_end + int(total * self.val_ratio)

        return {
            "train": data_pairs[:train_end],
            "val": data_pairs[train_end:val_end],
            "test": data_pairs[val_end:]
        }

    def _save_donut_format(self, splits: Dict[str, List[Dict]]):
        """Guardar en formato Donut"""

        for split_name, data_pairs in splits.items():
            # Mapear nombre de split
            split_dir_name = "validation" if split_name == "val" else split_name
            split_dir = self.output_dir / split_dir_name

            # Crear metadata.jsonl
            metadata_file = split_dir / "metadata.jsonl"

            with open(metadata_file, "w", encoding="utf-8") as f:
                for i, pair in enumerate(data_pairs):
                    # Nombre de archivo de imagen
                    image_ext = pair["image_path"].suffix
                    new_image_name = f"{split_name}_{i:05d}{image_ext}"

                    # Copiar imagen
                    src_image = pair["image_path"]
                    dst_image = split_dir / "images" / new_image_name

                    shutil.copy2(src_image, dst_image)

                    # Crear línea de metadata
                    ground_truth = {
                        "gt_parse": pair["transformed_data"]
                    }

                    metadata_line = {
                        "file_name": new_image_name,
                        "ground_truth": json.dumps(ground_truth, ensure_ascii=False)
                    }

                    f.write(json.dumps(metadata_line, ensure_ascii=False) + "\n")

    def _generate_statistics(self, splits: Dict[str, List[Dict]]):
        """Generar estadísticas del dataset"""
        stats = {
            "total": sum(len(pairs) for pairs in splits.values()),
            "train": len(splits["train"]),
            "val": len(splits["val"]),
            "test": len(splits["test"]),
            "created_at": datetime.now().isoformat(),
            "seed": self.seed
        }

        # Guardar estadísticas
        stats_file = self.output_dir / "dataset_statistics.json"
        with open(stats_file, "w", encoding="utf-8") as f:
            json.dump(stats, f, indent=2, ensure_ascii=False)

        print("\n📊 Estadísticas del Dataset:")
        print(f"   Total: {stats['total']}")
        print(f"   Train: {stats['train']} ({stats['train']/stats['total']*100:.1f}%)")
        print(f"   Val: {stats['val']} ({stats['val']/stats['total']*100:.1f}%)")
        print(f"   Test: {stats['test']} ({stats['test']/stats['total']*100:.1f}%)")


def main():
    parser = argparse.ArgumentParser(
        description="Convertir datos de facturas al formato Donut"
    )

    parser.add_argument(
        "--input-json",
        type=str,
        required=True,
        help="Directorio con JSONs de anotaciones"
    )

    parser.add_argument(
        "--input-images",
        type=str,
        required=True,
        help="Directorio con imágenes de facturas"
    )

    parser.add_argument(
        "--output",
        type=str,
        required=True,
        help="Directorio de salida para dataset Donut"
    )

    parser.add_argument(
        "--schema",
        type=str,
        default="intermedio",
        choices=["basico", "intermedio", "completo"],
        help="Nivel de esquema a usar (default: intermedio)"
    )

    parser.add_argument(
        "--split",
        type=float,
        nargs=3,
        default=[0.8, 0.1, 0.1],
        metavar=("TRAIN", "VAL", "TEST"),
        help="Ratios de split (default: 0.8 0.1 0.1)"
    )

    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Seed para reproducibilidad (default: 42)"
    )

    args = parser.parse_args()

    # Crear conversor
    converter = DonutDatasetConverter(
        input_json_dir=args.input_json,
        input_images_dir=args.input_images,
        output_dir=args.output,
        train_ratio=args.split[0],
        val_ratio=args.split[1],
        test_ratio=args.split[2],
        seed=args.seed
    )

    # Ejecutar conversión
    converter.convert(schema_level=args.schema)


if __name__ == "__main__":
    main()
