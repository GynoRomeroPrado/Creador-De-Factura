/**
 * Script para generar PDFs de facturas usando HTMLDocs
 * Uso: node generate-pdf.js <archivo_json> <archivo_salida.pdf>
 */

import { render } from '@htmldocs/render';
import { readFileSync, writeFileSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

async function generatePDF(jsonPath, outputPath) {
  try {
    // Leer datos de la factura desde JSON
    const facturaData = JSON.parse(readFileSync(jsonPath, 'utf-8'));

    // Renderizar el documento a PDF
    const pdf = await render({
      document: 'factura',
      props: { data: facturaData },
      documentsDir: join(__dirname, 'documents'),
    });

    // Guardar el PDF
    writeFileSync(outputPath, pdf);
    console.log(`PDF generado exitosamente: ${outputPath}`);

    return { success: true, path: outputPath };
  } catch (error) {
    console.error('Error generando PDF:', error.message);
    return { success: false, error: error.message };
  }
}

// Ejecutar desde línea de comandos
const args = process.argv.slice(2);
if (args.length >= 2) {
  generatePDF(args[0], args[1]);
} else if (args.length === 1 && args[0] === '--help') {
  console.log(`
Generador de PDFs de Facturas con HTMLDocs

Uso:
  node generate-pdf.js <archivo_json> <archivo_salida.pdf>

Ejemplo:
  node generate-pdf.js ../facturas_json/factura_001.json ../facturas_pdf/factura_001.pdf

El archivo JSON debe contener los datos de la factura según el esquema definido.
  `);
} else {
  console.log('Uso: node generate-pdf.js <archivo_json> <archivo_salida.pdf>');
  console.log('Use --help para más información');
}

export { generatePDF };
