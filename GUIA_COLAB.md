# Guía de Uso en Google Colab

Este documento explica cómo ejecutar el generador de facturas masivas directamente en Google Colab.

## Pasos

1.  **Abrir Google Colab**
    Ve a [colab.research.google.com](https://colab.research.google.com/) y crea un "Nuevo cuaderno".

2.  **Clonar el Repositorio**
    En la primera celda de código, ejecuta el siguiente comando para descargar el código más reciente:
    ```python
    !git clone https://github.com/GynoRomeroPrado/Creador-De-Factura.git
    %cd Creador-De-Factura
    ```

3.  **Instalar Dependencias**
    Instala la librería necesaria (`reportlab`) ejecutando esta celda:
    ```python
    !pip install -r requirements.txt
    ```

4.  **Ejecutar el Generador**
    Para generar el lote de 20 facturas realistas, ejecuta:
    ```python
    !python generar_lote_final.py
    ```
    *Si deseas generar más facturas, puedes editar el archivo `generar_lote_final.py` o crear un script nuevo.*

5.  **Descargar los Resultados**
    Para descargar todas las facturas generadas en un archivo ZIP, ejecuta el siguiente bloque de código:
    ```python
    import shutil
    from google.colab import files

    # Comprimir la carpeta de salida
    shutil.make_archive('facturas_finales', 'zip', 'facturas_finales')

    # Descargar el archivo zip
    files.download('facturas_finales.zip')
    ```

## Notas Adicionales
- Los archivos generados se encuentran en la carpeta `facturas_finales` dentro del entorno de Colab.
- Puedes modificar los scripts `.py` directamente en Colab haciendo doble clic en ellos en el panel de archivos de la izquierda.
