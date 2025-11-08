"""
Generador de Facturas Ficticias
"""
from .utils import RUCGenerator, MontoLetras, DatosPersonas, GeneradorFechas, ItemsGenerator
from .generator import FacturaGenerator

# PDFFactura requiere reportlab, importar solo si está disponible
try:
    from .pdf_creator import PDFFactura
    __all__ = [
        'RUCGenerator',
        'MontoLetras',
        'DatosPersonas',
        'GeneradorFechas',
        'ItemsGenerator',
        'FacturaGenerator',
        'PDFFactura'
    ]
except ImportError:
    __all__ = [
        'RUCGenerator',
        'MontoLetras',
        'DatosPersonas',
        'GeneradorFechas',
        'ItemsGenerator',
        'FacturaGenerator'
    ]
