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

4.  **Ejecutar el Generador (Fase 2)**
    Para generar el lote de 1,000 facturas con la nueva estructura plana y variabilidad, ejecuta:
    ```python
    !python main.py --cantidad 1000 --output facturas_fase2_final
    ```

5.  **Descargar los Resultados**
    Para descargar todas las facturas generadas en un archivo ZIP, ejecuta el siguiente bloque de código:
    ```python
    import shutil
    from google.colab import files

    # Comprimir la carpeta de salida
    shutil.make_archive('facturas_fase2_final', 'zip', 'facturas_fase2_final')

    # Descargar el archivo zip
    files.download('facturas_fase2_final.zip')
    ```

6.  **Generar Pruebas Rápidas**
    Si solo quieres verificar con un lote pequeño (ej. 15 facturas):
    ```python
    !python main.py --cantidad 15 --output pruebas_rapidas
    ```

## Notas Adicionales
- Los archivos generados se encuentran en la carpeta `facturas_finales` dentro del entorno de Colab.
- Puedes modificar los scripts `.py` directamente en Colab haciendo doble clic en ellos en el panel de archivos de la izquierda.
