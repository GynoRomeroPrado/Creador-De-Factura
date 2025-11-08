"""
Script para Google Colab - Procesamiento y Aumento de Dataset de Facturas
Autor: Claude
Descripción: Renombra facturas y JSONs, luego genera variaciones mediante desplazamientos
"""

import os
import json
import shutil
from pathlib import Path
from typing import List, Tuple, Dict
import numpy as np
from PIL import Image
from pdf2image import convert_from_path
import io

# Instalación de dependencias necesarias
def install_dependencies():
    """Instala las librerías necesarias en Google Colab"""
    print("Instalando dependencias...")
    os.system('pip install -q pdf2image pillow')
    os.system('apt-get install -q poppler-utils')
    print("✓ Dependencias instaladas")


class InvoiceDatasetProcessor:
    """Clase para procesar y aumentar el dataset de facturas"""

    def __init__(self, drive_folder_path: str, output_folder_path: str = None):
        """
        Inicializa el procesador de facturas

        Args:
            drive_folder_path: Ruta a la carpeta de Drive con las facturas
            output_folder_path: Ruta de salida (si es None, usa la misma carpeta)
        """
        self.input_folder = Path(drive_folder_path)
        self.output_folder = Path(output_folder_path) if output_folder_path else self.input_folder

        # Crear subcarpetas organizadas
        self.organized_folder = self.output_folder / "organized"
        self.augmented_folder = self.output_folder / "augmented"

        self.organized_folder.mkdir(parents=True, exist_ok=True)
        self.augmented_folder.mkdir(parents=True, exist_ok=True)

    def get_invoice_pairs(self) -> List[Tuple[Path, Path]]:
        """
        Encuentra pares de facturas y sus JSON correspondientes

        Returns:
            Lista de tuplas (archivo_factura, archivo_json)
        """
        pairs = []

        # Buscar todos los archivos de imagen y PDF
        invoice_extensions = ['.jpg', '.jpeg', '.png', '.pdf']
        invoice_files = []

        for ext in invoice_extensions:
            invoice_files.extend(self.input_folder.glob(f'*{ext}'))
            invoice_files.extend(self.input_folder.glob(f'*{ext.upper()}'))

        # Para cada factura, buscar su JSON
        for invoice_file in invoice_files:
            # Buscar JSON con el mismo nombre base
            json_file = invoice_file.with_suffix('.json')

            if json_file.exists():
                pairs.append((invoice_file, json_file))
            else:
                print(f"⚠️  Advertencia: No se encontró JSON para {invoice_file.name}")

        return pairs

    def rename_and_organize(self) -> List[Tuple[Path, Path]]:
        """
        Renombra las facturas y JSONs de forma correlativa

        Returns:
            Lista de tuplas (nueva_factura, nuevo_json)
        """
        print("\n📋 Paso 1: Renombrando y organizando facturas...")

        pairs = self.get_invoice_pairs()
        organized_pairs = []

        for idx, (invoice_file, json_file) in enumerate(pairs, start=1):
            # Generar nombres correlativos
            extension = invoice_file.suffix
            new_invoice_name = f"factura_{idx:04d}{extension}"
            new_json_name = f"factura_{idx:04d}.json"

            new_invoice_path = self.organized_folder / new_invoice_name
            new_json_path = self.organized_folder / new_json_name

            # Copiar archivos con nuevos nombres
            shutil.copy2(invoice_file, new_invoice_path)

            # Actualizar JSON con el nuevo nombre de archivo
            with open(json_file, 'r', encoding='utf-8') as f:
                json_data = json.load(f)

            # Agregar/actualizar campo con nombre de archivo
            json_data['archivo_factura'] = new_invoice_name
            json_data['id_correlativo'] = f"factura_{idx:04d}"

            with open(new_json_path, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, ensure_ascii=False, indent=2)

            organized_pairs.append((new_invoice_path, new_json_path))
            print(f"  ✓ {invoice_file.name} → {new_invoice_name}")

        print(f"\n✓ {len(organized_pairs)} pares de facturas organizados")
        return organized_pairs

    def convert_pdf_to_image(self, pdf_path: Path) -> Image.Image:
        """
        Convierte la primera página de un PDF a imagen

        Args:
            pdf_path: Ruta al archivo PDF

        Returns:
            Imagen PIL de la primera página
        """
        images = convert_from_path(str(pdf_path), first_page=1, last_page=1)
        return images[0]

    def load_invoice_image(self, invoice_path: Path) -> Image.Image:
        """
        Carga una factura como imagen (PDF o imagen)

        Args:
            invoice_path: Ruta al archivo de factura

        Returns:
            Imagen PIL
        """
        if invoice_path.suffix.lower() == '.pdf':
            return self.convert_pdf_to_image(invoice_path)
        else:
            return Image.open(invoice_path)

    def apply_shift(self, image: Image.Image, shift_x: int, shift_y: int,
                    fill_color: tuple = (255, 255, 255)) -> Image.Image:
        """
        Aplica un desplazamiento a la imagen

        Args:
            image: Imagen PIL original
            shift_x: Desplazamiento en X (píxeles)
            shift_y: Desplazamiento en Y (píxeles)
            fill_color: Color de relleno para áreas vacías

        Returns:
            Nueva imagen desplazada
        """
        # Convertir a RGB si es necesario
        if image.mode != 'RGB':
            image = image.convert('RGB')

        # Crear nueva imagen
        width, height = image.size
        shifted_image = Image.new('RGB', (width, height), fill_color)

        # Aplicar desplazamiento
        shifted_image.paste(image, (shift_x, shift_y))

        return shifted_image

    def get_augmentation_configs(self, pixel_range: int = 10) -> List[Dict]:
        """
        Genera configuraciones de aumento de datos

        Args:
            pixel_range: Rango de píxeles para desplazamientos

        Returns:
            Lista de diccionarios con configuraciones de transformación
        """
        configs = []

        # Desplazamientos en 8 direcciones
        directions = [
            ("derecha", pixel_range, 0),
            ("izquierda", -pixel_range, 0),
            ("abajo", 0, pixel_range),
            ("arriba", 0, -pixel_range),
            ("diagonal_superior_derecha", pixel_range, -pixel_range),
            ("diagonal_superior_izquierda", -pixel_range, -pixel_range),
            ("diagonal_inferior_derecha", pixel_range, pixel_range),
            ("diagonal_inferior_izquierda", -pixel_range, pixel_range),
        ]

        for name, shift_x, shift_y in directions:
            configs.append({
                'name': name,
                'shift_x': shift_x,
                'shift_y': shift_y
            })

        # Desplazamientos intermedios (5 píxeles)
        medium_range = pixel_range // 2
        for name, shift_x, shift_y in directions:
            configs.append({
                'name': f"{name}_medio",
                'shift_x': shift_x // 2 if shift_x != 0 else 0,
                'shift_y': shift_y // 2 if shift_y != 0 else 0
            })

        return configs

    def augment_dataset(self, organized_pairs: List[Tuple[Path, Path]],
                       pixel_range: int = 10) -> int:
        """
        Aumenta el dataset aplicando transformaciones

        Args:
            organized_pairs: Lista de pares (factura, json)
            pixel_range: Rango de píxeles para desplazamientos

        Returns:
            Número total de facturas generadas
        """
        print(f"\n🔄 Paso 2: Aumentando dataset con desplazamientos de ±{pixel_range}px...")

        augmentation_configs = self.get_augmentation_configs(pixel_range)
        total_generated = 0

        for invoice_path, json_path in organized_pairs:
            # Leer JSON original
            with open(json_path, 'r', encoding='utf-8') as f:
                original_json = json.load(f)

            # Cargar imagen
            try:
                original_image = self.load_invoice_image(invoice_path)
                base_name = invoice_path.stem
                original_extension = invoice_path.suffix

                print(f"\n  Procesando: {invoice_path.name}")

                # Aplicar cada transformación
                for idx, config in enumerate(augmentation_configs, start=1):
                    # Generar nueva imagen
                    augmented_image = self.apply_shift(
                        original_image,
                        config['shift_x'],
                        config['shift_y']
                    )

                    # Guardar imagen aumentada
                    aug_name = f"{base_name}_aug_{idx:02d}_{config['name']}"
                    aug_image_path = self.augmented_folder / f"{aug_name}.png"
                    augmented_image.save(aug_image_path, 'PNG')

                    # Crear JSON aumentado
                    aug_json = original_json.copy()
                    aug_json['archivo_factura'] = f"{aug_name}.png"
                    aug_json['id_correlativo'] = aug_name
                    aug_json['augmentation'] = {
                        'original_file': invoice_path.name,
                        'transformation': config['name'],
                        'shift_x': config['shift_x'],
                        'shift_y': config['shift_y']
                    }

                    aug_json_path = self.augmented_folder / f"{aug_name}.json"
                    with open(aug_json_path, 'w', encoding='utf-8') as f:
                        json.dump(aug_json, f, ensure_ascii=False, indent=2)

                    total_generated += 1

                    if idx % 5 == 0:
                        print(f"    ✓ {idx} variaciones generadas...")

                print(f"  ✓ Completado: {len(augmentation_configs)} variaciones")

            except Exception as e:
                print(f"  ✗ Error procesando {invoice_path.name}: {str(e)}")
                continue

        return total_generated

    def generate_dataset_report(self) -> Dict:
        """
        Genera un reporte del dataset procesado

        Returns:
            Diccionario con estadísticas del dataset
        """
        organized_files = list(self.organized_folder.glob('factura_*.json'))
        augmented_files = list(self.augmented_folder.glob('*.json'))

        report = {
            'facturas_originales_organizadas': len(organized_files),
            'facturas_aumentadas_generadas': len(augmented_files),
            'total_facturas_dataset': len(organized_files) + len(augmented_files),
            'carpeta_organizadas': str(self.organized_folder),
            'carpeta_aumentadas': str(self.augmented_folder)
        }

        # Guardar reporte
        report_path = self.output_folder / 'dataset_report.json'
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

        return report


def main():
    """Función principal para ejecutar en Google Colab"""

    print("=" * 70)
    print("🚀 PROCESADOR DE DATASET DE FACTURAS")
    print("=" * 70)

    # Montar Google Drive
    from google.colab import drive
    drive.mount('/content/drive')

    # Instalar dependencias
    install_dependencies()

    # Configuración de rutas (AJUSTAR SEGÚN TU CARPETA DE DRIVE)
    INPUT_FOLDER = "/content/drive/MyDrive/Facturas"  # ⚠️ CAMBIAR ESTA RUTA
    OUTPUT_FOLDER = "/content/drive/MyDrive/Facturas_Procesadas"  # ⚠️ CAMBIAR ESTA RUTA

    print(f"\n📁 Carpeta de entrada: {INPUT_FOLDER}")
    print(f"📁 Carpeta de salida: {OUTPUT_FOLDER}")

    # Verificar que la carpeta existe
    if not os.path.exists(INPUT_FOLDER):
        print(f"\n❌ ERROR: La carpeta {INPUT_FOLDER} no existe")
        print("Por favor, ajusta la variable INPUT_FOLDER con la ruta correcta")
        return

    # Crear procesador
    processor = InvoiceDatasetProcessor(INPUT_FOLDER, OUTPUT_FOLDER)

    # Paso 1: Renombrar y organizar
    organized_pairs = processor.rename_and_organize()

    if not organized_pairs:
        print("\n❌ No se encontraron pares de facturas y JSONs")
        return

    # Paso 2: Aumentar dataset
    pixel_range = 10  # Puedes ajustar este valor
    total_generated = processor.augment_dataset(organized_pairs, pixel_range)

    # Generar reporte
    print("\n" + "=" * 70)
    print("📊 REPORTE FINAL")
    print("=" * 70)

    report = processor.generate_dataset_report()

    print(f"\n✓ Facturas originales organizadas: {report['facturas_originales_organizadas']}")
    print(f"✓ Facturas aumentadas generadas: {report['facturas_aumentadas_generadas']}")
    print(f"✓ Total facturas en dataset: {report['total_facturas_dataset']}")
    print(f"\n📁 Carpeta organizadas: {report['carpeta_organizadas']}")
    print(f"📁 Carpeta aumentadas: {report['carpeta_aumentadas']}")
    print(f"\n🎉 Proceso completado exitosamente!")


# Para uso en Google Colab
if __name__ == "__main__":
    main()
