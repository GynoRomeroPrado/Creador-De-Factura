"""
Renderer de facturas usando HTMLDocs
Integración Python con el sistema Node.js de HTMLDocs
"""

import json
import subprocess
import os
import tempfile
from pathlib import Path
from typing import Dict, Any, Optional


class HTMLDocsRenderer:
    """
    Renderizador de facturas PDF usando HTMLDocs (React/Tailwind).
    Requiere Node.js y las dependencias de htmldocs-invoices instaladas.
    """

    def __init__(self, htmldocs_dir: Optional[str] = None):
        """
        Inicializa el renderer.

        Args:
            htmldocs_dir: Directorio del proyecto HTMLDocs.
                          Por defecto usa 'htmldocs-invoices' en el directorio padre.
        """
        if htmldocs_dir:
            self.htmldocs_dir = Path(htmldocs_dir)
        else:
            # Directorio por defecto relativo al archivo actual
            self.htmldocs_dir = Path(__file__).parent.parent / 'htmldocs-invoices'

        self.generate_script = self.htmldocs_dir / 'generate-pdf.js'
        self._check_setup()

    def _check_setup(self) -> bool:
        """Verifica que HTMLDocs esté correctamente configurado."""
        if not self.htmldocs_dir.exists():
            raise FileNotFoundError(
                f"Directorio HTMLDocs no encontrado: {self.htmldocs_dir}\n"
                "Ejecuta: cd htmldocs-invoices && npm install"
            )

        if not self.generate_script.exists():
            raise FileNotFoundError(
                f"Script de generación no encontrado: {self.generate_script}"
            )

        # Verificar que node_modules existe
        node_modules = self.htmldocs_dir / 'node_modules'
        if not node_modules.exists():
            print("⚠️  node_modules no encontrado. Ejecutando npm install...")
            self._run_npm_install()

        return True

    def _run_npm_install(self):
        """Ejecuta npm install en el directorio HTMLDocs."""
        try:
            subprocess.run(
                ['npm', 'install'],
                cwd=self.htmldocs_dir,
                check=True,
                capture_output=True,
                text=True
            )
            print("✓ Dependencias instaladas correctamente")
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Error instalando dependencias: {e.stderr}")
        except FileNotFoundError:
            raise RuntimeError(
                "Node.js no encontrado. Instala Node.js para usar HTMLDocs.\n"
                "Descarga: https://nodejs.org/"
            )

    def render_factura(self, factura_data: Dict[str, Any], output_path: str) -> str:
        """
        Renderiza una factura a PDF usando HTMLDocs.

        Args:
            factura_data: Diccionario con los datos de la factura
            output_path: Ruta donde guardar el PDF generado

        Returns:
            Ruta del archivo PDF generado
        """
        # Crear archivo temporal con los datos JSON
        with tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.json',
            delete=False,
            encoding='utf-8'
        ) as temp_file:
            json.dump(factura_data, temp_file, ensure_ascii=False, indent=2)
            temp_json_path = temp_file.name

        try:
            # Ejecutar el script de generación
            result = subprocess.run(
                ['node', str(self.generate_script), temp_json_path, output_path],
                cwd=self.htmldocs_dir,
                capture_output=True,
                text=True,
                timeout=60  # 60 segundos timeout
            )

            if result.returncode != 0:
                raise RuntimeError(f"Error generando PDF: {result.stderr}")

            if not os.path.exists(output_path):
                raise RuntimeError(f"PDF no fue generado: {output_path}")

            return output_path

        except subprocess.TimeoutExpired:
            raise RuntimeError("Timeout: La generación del PDF tomó demasiado tiempo")
        finally:
            # Limpiar archivo temporal
            if os.path.exists(temp_json_path):
                os.remove(temp_json_path)

    def render_factura_from_json(self, json_path: str, output_path: str) -> str:
        """
        Renderiza una factura desde un archivo JSON existente.

        Args:
            json_path: Ruta al archivo JSON con datos de la factura
            output_path: Ruta donde guardar el PDF generado

        Returns:
            Ruta del archivo PDF generado
        """
        result = subprocess.run(
            ['node', str(self.generate_script), json_path, output_path],
            cwd=self.htmldocs_dir,
            capture_output=True,
            text=True,
            timeout=60
        )

        if result.returncode != 0:
            raise RuntimeError(f"Error generando PDF: {result.stderr}")

        return output_path

    def transformar_datos_factura(self, factura_dict: Dict[str, Any]) -> Dict[str, Any]:
        """
        Transforma los datos del formato interno al formato esperado por HTMLDocs.
        Útil para convertir facturas generadas por FacturaGenerator.

        Args:
            factura_dict: Datos de factura en formato interno

        Returns:
            Datos transformados para HTMLDocs
        """
        # Mapeo de campos del generador al formato HTMLDocs
        htmldocs_data = {
            # Datos del comprobante
            'tipo_comprobante': factura_dict.get('tipo_comprobante', 'FACTURA ELECTRÓNICA'),
            'serie': factura_dict.get('serie', 'F001'),
            'numero': factura_dict.get('numero', '00000001'),
            'fecha_emision': factura_dict.get('fecha_emision', ''),
            'fecha_vencimiento': factura_dict.get('fecha_vencimiento'),
            'moneda': factura_dict.get('moneda', 'PEN'),
            'tipo_cambio': factura_dict.get('tipo_cambio'),

            # Datos del emisor
            'emisor_ruc': factura_dict.get('emisor', {}).get('ruc', ''),
            'emisor_razon_social': factura_dict.get('emisor', {}).get('razon_social', ''),
            'emisor_nombre_comercial': factura_dict.get('emisor', {}).get('nombre_comercial'),
            'emisor_direccion': factura_dict.get('emisor', {}).get('direccion', ''),
            'emisor_ubigeo': factura_dict.get('emisor', {}).get('ubigeo'),
            'emisor_departamento': factura_dict.get('emisor', {}).get('departamento'),
            'emisor_provincia': factura_dict.get('emisor', {}).get('provincia'),
            'emisor_distrito': factura_dict.get('emisor', {}).get('distrito'),

            # Datos del receptor
            'receptor_tipo_documento': factura_dict.get('receptor', {}).get('tipo_documento', 'RUC'),
            'receptor_numero_documento': factura_dict.get('receptor', {}).get('numero_documento', ''),
            'receptor_razon_social': factura_dict.get('receptor', {}).get('razon_social', ''),
            'receptor_direccion': factura_dict.get('receptor', {}).get('direccion'),

            # Items - transformar al formato esperado
            'items': self._transformar_items(factura_dict.get('items', [])),

            # Totales
            'total_operaciones_gravadas': factura_dict.get('totales', {}).get('total_gravadas', 0),
            'total_operaciones_exoneradas': factura_dict.get('totales', {}).get('total_exoneradas', 0),
            'total_operaciones_inafectas': factura_dict.get('totales', {}).get('total_inafectas', 0),
            'total_igv': factura_dict.get('totales', {}).get('total_igv', 0),
            'total_descuentos': factura_dict.get('totales', {}).get('total_descuentos', 0),
            'importe_total': factura_dict.get('totales', {}).get('importe_total', 0),
            'importe_total_letras': factura_dict.get('totales', {}).get('importe_total_letras', ''),

            # Forma de pago
            'forma_pago': factura_dict.get('forma_pago', {}).get('tipo', 'Contado'),
            'cuotas': factura_dict.get('forma_pago', {}).get('cuotas', []),

            # Metadatos
            'hash_cpe': factura_dict.get('hash_cpe'),
            'codigo_qr': factura_dict.get('codigo_qr'),
        }

        # Datos específicos de hotel
        if 'datos_hotel' in factura_dict:
            htmldocs_data['datos_hotel'] = factura_dict['datos_hotel']

        # Datos específicos de seguro
        if 'datos_seguro' in factura_dict:
            htmldocs_data['datos_seguro'] = factura_dict['datos_seguro']

        return htmldocs_data

    def _transformar_items(self, items: list) -> list:
        """Transforma los items al formato esperado por HTMLDocs."""
        transformed = []
        for item in items:
            transformed.append({
                'cantidad': item.get('cantidad', 1),
                'unidad': item.get('unidad_medida', 'UND'),
                'descripcion': item.get('descripcion', ''),
                'precio_unitario': item.get('precio_unitario', 0),
                'valor_venta': item.get('valor_venta', 0),
                'igv': item.get('igv', 0),
                'precio_total': item.get('precio_total', 0),
            })
        return transformed


class HTMLDocsAPI:
    """
    Cliente para la API REST de HTMLDocs Cloud.
    Para uso con templates publicados en la nube.
    """

    def __init__(self, api_key: str, base_url: str = "https://api.htmldocs.com"):
        """
        Inicializa el cliente de API.

        Args:
            api_key: API key de HTMLDocs
            base_url: URL base de la API
        """
        self.api_key = api_key
        self.base_url = base_url

    def render_pdf(self, template_id: str, data: Dict[str, Any]) -> bytes:
        """
        Renderiza un PDF usando la API de HTMLDocs Cloud.

        Args:
            template_id: ID del template publicado
            data: Datos para el template

        Returns:
            Bytes del PDF generado
        """
        import urllib.request
        import urllib.error

        url = f"{self.base_url}/v1/render/{template_id}"
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }

        request_data = json.dumps(data).encode('utf-8')
        req = urllib.request.Request(url, data=request_data, headers=headers)

        try:
            with urllib.request.urlopen(req) as response:
                return response.read()
        except urllib.error.HTTPError as e:
            raise RuntimeError(f"Error de API: {e.code} - {e.read().decode()}")


# Funciones de conveniencia
def crear_pdf_factura(factura_data: Dict[str, Any], output_path: str) -> str:
    """
    Función de conveniencia para crear un PDF de factura.

    Args:
        factura_data: Datos de la factura
        output_path: Ruta de salida del PDF

    Returns:
        Ruta del PDF generado
    """
    renderer = HTMLDocsRenderer()
    datos_transformados = renderer.transformar_datos_factura(factura_data)
    return renderer.render_factura(datos_transformados, output_path)


def instalar_htmldocs():
    """Instala las dependencias de HTMLDocs."""
    htmldocs_dir = Path(__file__).parent.parent / 'htmldocs-invoices'

    if not htmldocs_dir.exists():
        raise FileNotFoundError(f"Directorio no encontrado: {htmldocs_dir}")

    print(f"Instalando dependencias en {htmldocs_dir}...")
    subprocess.run(['npm', 'install'], cwd=htmldocs_dir, check=True)
    print("✓ Instalación completada")


if __name__ == '__main__':
    # Test del módulo
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == '--install':
        instalar_htmldocs()
    else:
        print("HTMLDocs Renderer para Facturas Peruanas")
        print("=" * 40)
        print("\nUso:")
        print("  python htmldocs_renderer.py --install  # Instalar dependencias")
        print("\nDesde código:")
        print("  from htmldocs_renderer import crear_pdf_factura")
        print("  crear_pdf_factura(datos_factura, 'factura.pdf')")
