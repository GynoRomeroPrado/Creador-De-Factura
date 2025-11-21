import React from 'react';
import { Document, Page, Tailwind } from '@htmldocs/react';

// Tipos para la factura
interface Item {
  cantidad: number;
  unidad: string;
  descripcion: string;
  precio_unitario: number;
  valor_venta: number;
  igv: number;
  precio_total: number;
}

interface Cuota {
  numero: number;
  fecha_vencimiento: string;
  monto: number;
}

interface DatosHotel {
  nombre_huesped: string;
  documento_huesped: string;
  fecha_checkin: string;
  fecha_checkout: string;
  num_noches: number;
  num_habitacion: string;
  tipo_habitacion: string;
}

interface DatosSeguro {
  numero_poliza: string;
  fecha_inicio_vigencia: string;
  fecha_fin_vigencia: string;
  tipo_seguro: string;
  placa_vehiculo?: string;
  marca_vehiculo?: string;
  modelo_vehiculo?: string;
  anio_vehiculo?: number;
}

interface FacturaData {
  // Datos del comprobante
  tipo_comprobante: string;
  serie: string;
  numero: string;
  fecha_emision: string;
  fecha_vencimiento?: string;
  moneda: string;
  tipo_cambio?: number;

  // Datos del emisor
  emisor_ruc: string;
  emisor_razon_social: string;
  emisor_nombre_comercial?: string;
  emisor_direccion: string;
  emisor_ubigeo?: string;
  emisor_departamento?: string;
  emisor_provincia?: string;
  emisor_distrito?: string;

  // Datos del receptor
  receptor_tipo_documento: string;
  receptor_numero_documento: string;
  receptor_razon_social: string;
  receptor_direccion?: string;

  // Items
  items: Item[];

  // Totales
  total_operaciones_gravadas: number;
  total_operaciones_exoneradas: number;
  total_operaciones_inafectas: number;
  total_igv: number;
  total_descuentos?: number;
  importe_total: number;
  importe_total_letras: string;

  // Forma de pago
  forma_pago: string;
  cuotas?: Cuota[];

  // Datos específicos opcionales
  datos_hotel?: DatosHotel;
  datos_seguro?: DatosSeguro;

  // Metadatos
  hash_cpe?: string;
  codigo_qr?: string;
}

// Componente para formatear moneda
const formatMoney = (amount: number, currency: string = 'PEN'): string => {
  const symbols: Record<string, string> = { PEN: 'S/', USD: '$', EUR: '€' };
  return `${symbols[currency] || currency} ${amount.toFixed(2)}`;
};

// Componente principal de la factura
export default function Factura({ data }: { data: FacturaData }) {
  const currencySymbol = data.moneda === 'PEN' ? 'S/' : data.moneda === 'USD' ? '$' : '€';

  return (
    <Tailwind>
      <Document>
        <Page size="A4" className="p-8 font-sans text-sm">
          {/* Encabezado */}
          <div className="flex justify-between mb-6">
            {/* Datos del emisor */}
            <div className="flex-1">
              <h1 className="text-xl font-bold text-gray-800">
                {data.emisor_razon_social}
              </h1>
              {data.emisor_nombre_comercial && (
                <p className="text-gray-600 italic">{data.emisor_nombre_comercial}</p>
              )}
              <p className="text-gray-600 mt-2">{data.emisor_direccion}</p>
              {data.emisor_distrito && (
                <p className="text-gray-600">
                  {data.emisor_distrito}, {data.emisor_provincia}, {data.emisor_departamento}
                </p>
              )}
            </div>

            {/* Cuadro del comprobante */}
            <div className="border-2 border-blue-600 p-4 text-center min-w-[200px]">
              <p className="text-blue-600 font-bold">RUC: {data.emisor_ruc}</p>
              <p className="text-blue-600 font-bold mt-2">{data.tipo_comprobante}</p>
              <p className="text-blue-600 font-bold text-lg mt-1">
                {data.serie}-{data.numero}
              </p>
            </div>
          </div>

          {/* Datos del receptor */}
          <div className="border border-gray-300 p-4 mb-4">
            <div className="grid grid-cols-2 gap-2">
              <div>
                <span className="font-semibold">Fecha de Emisión:</span> {data.fecha_emision}
              </div>
              {data.fecha_vencimiento && (
                <div>
                  <span className="font-semibold">Fecha Vencimiento:</span> {data.fecha_vencimiento}
                </div>
              )}
              <div>
                <span className="font-semibold">{data.receptor_tipo_documento}:</span> {data.receptor_numero_documento}
              </div>
              <div>
                <span className="font-semibold">Moneda:</span> {data.moneda}
                {data.tipo_cambio && ` (TC: ${data.tipo_cambio})`}
              </div>
              <div className="col-span-2">
                <span className="font-semibold">Señor(es):</span> {data.receptor_razon_social}
              </div>
              {data.receptor_direccion && (
                <div className="col-span-2">
                  <span className="font-semibold">Dirección:</span> {data.receptor_direccion}
                </div>
              )}
            </div>
          </div>

          {/* Datos específicos de hotel */}
          {data.datos_hotel && (
            <div className="border border-gray-300 p-4 mb-4 bg-blue-50">
              <h3 className="font-bold text-blue-800 mb-2">Datos de Hospedaje</h3>
              <div className="grid grid-cols-2 gap-2 text-sm">
                <div><span className="font-semibold">Huésped:</span> {data.datos_hotel.nombre_huesped}</div>
                <div><span className="font-semibold">Documento:</span> {data.datos_hotel.documento_huesped}</div>
                <div><span className="font-semibold">Check-in:</span> {data.datos_hotel.fecha_checkin}</div>
                <div><span className="font-semibold">Check-out:</span> {data.datos_hotel.fecha_checkout}</div>
                <div><span className="font-semibold">Noches:</span> {data.datos_hotel.num_noches}</div>
                <div><span className="font-semibold">Habitación:</span> {data.datos_hotel.num_habitacion} ({data.datos_hotel.tipo_habitacion})</div>
              </div>
            </div>
          )}

          {/* Datos específicos de seguro */}
          {data.datos_seguro && (
            <div className="border border-gray-300 p-4 mb-4 bg-green-50">
              <h3 className="font-bold text-green-800 mb-2">Datos del Seguro</h3>
              <div className="grid grid-cols-2 gap-2 text-sm">
                <div><span className="font-semibold">N° Póliza:</span> {data.datos_seguro.numero_poliza}</div>
                <div><span className="font-semibold">Tipo:</span> {data.datos_seguro.tipo_seguro}</div>
                <div><span className="font-semibold">Vigencia:</span> {data.datos_seguro.fecha_inicio_vigencia} - {data.datos_seguro.fecha_fin_vigencia}</div>
                {data.datos_seguro.placa_vehiculo && (
                  <>
                    <div><span className="font-semibold">Placa:</span> {data.datos_seguro.placa_vehiculo}</div>
                    <div><span className="font-semibold">Vehículo:</span> {data.datos_seguro.marca_vehiculo} {data.datos_seguro.modelo_vehiculo} {data.datos_seguro.anio_vehiculo}</div>
                  </>
                )}
              </div>
            </div>
          )}

          {/* Tabla de items */}
          <table className="w-full border-collapse mb-4">
            <thead>
              <tr className="bg-blue-600 text-white">
                <th className="border p-2 text-center w-16">CANT.</th>
                <th className="border p-2 text-center w-16">U.M.</th>
                <th className="border p-2 text-left">DESCRIPCIÓN</th>
                <th className="border p-2 text-right w-24">P. UNIT.</th>
                <th className="border p-2 text-right w-24">V. VENTA</th>
              </tr>
            </thead>
            <tbody>
              {data.items.map((item, index) => (
                <tr key={index} className={index % 2 === 0 ? 'bg-gray-50' : ''}>
                  <td className="border p-2 text-center">{item.cantidad}</td>
                  <td className="border p-2 text-center">{item.unidad}</td>
                  <td className="border p-2">{item.descripcion}</td>
                  <td className="border p-2 text-right">{currencySymbol} {item.precio_unitario.toFixed(2)}</td>
                  <td className="border p-2 text-right">{currencySymbol} {item.valor_venta.toFixed(2)}</td>
                </tr>
              ))}
            </tbody>
          </table>

          {/* Totales */}
          <div className="flex justify-end mb-4">
            <div className="w-80">
              <div className="flex justify-between py-1 border-b">
                <span>Op. Gravadas:</span>
                <span>{formatMoney(data.total_operaciones_gravadas, data.moneda)}</span>
              </div>
              {data.total_operaciones_exoneradas > 0 && (
                <div className="flex justify-between py-1 border-b">
                  <span>Op. Exoneradas:</span>
                  <span>{formatMoney(data.total_operaciones_exoneradas, data.moneda)}</span>
                </div>
              )}
              {data.total_operaciones_inafectas > 0 && (
                <div className="flex justify-between py-1 border-b">
                  <span>Op. Inafectas:</span>
                  <span>{formatMoney(data.total_operaciones_inafectas, data.moneda)}</span>
                </div>
              )}
              {data.total_descuentos && data.total_descuentos > 0 && (
                <div className="flex justify-between py-1 border-b text-red-600">
                  <span>Descuentos:</span>
                  <span>-{formatMoney(data.total_descuentos, data.moneda)}</span>
                </div>
              )}
              <div className="flex justify-between py-1 border-b">
                <span>IGV (18%):</span>
                <span>{formatMoney(data.total_igv, data.moneda)}</span>
              </div>
              <div className="flex justify-between py-2 font-bold text-lg bg-gray-100 px-2">
                <span>IMPORTE TOTAL:</span>
                <span>{formatMoney(data.importe_total, data.moneda)}</span>
              </div>
            </div>
          </div>

          {/* Total en letras */}
          <div className="border border-gray-300 p-3 mb-4 bg-gray-50">
            <span className="font-semibold">SON: </span>
            <span className="italic">{data.importe_total_letras}</span>
          </div>

          {/* Forma de pago y cuotas */}
          <div className="border border-gray-300 p-3 mb-4">
            <span className="font-semibold">Forma de Pago: </span>
            <span>{data.forma_pago}</span>

            {data.cuotas && data.cuotas.length > 0 && (
              <div className="mt-2">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="bg-gray-200">
                      <th className="p-1 text-left">Cuota</th>
                      <th className="p-1 text-left">Fecha Vencimiento</th>
                      <th className="p-1 text-right">Monto</th>
                    </tr>
                  </thead>
                  <tbody>
                    {data.cuotas.map((cuota, index) => (
                      <tr key={index}>
                        <td className="p-1">Cuota {cuota.numero}</td>
                        <td className="p-1">{cuota.fecha_vencimiento}</td>
                        <td className="p-1 text-right">{formatMoney(cuota.monto, data.moneda)}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>

          {/* Pie de página con hash y QR */}
          <div className="mt-auto pt-4 border-t border-gray-300 text-xs text-gray-500">
            <div className="flex justify-between items-center">
              <div>
                {data.hash_cpe && (
                  <p>Hash: {data.hash_cpe}</p>
                )}
                <p className="mt-1">Representación impresa de la {data.tipo_comprobante}</p>
                <p>Autorizado mediante Resolución de Superintendencia</p>
              </div>
              {data.codigo_qr && (
                <div className="w-20 h-20 border flex items-center justify-center text-gray-400">
                  [QR]
                </div>
              )}
            </div>
          </div>
        </Page>
      </Document>
    </Tailwind>
  );
}

// Props por defecto para preview
Factura.defaultProps = {
  data: {
    tipo_comprobante: "FACTURA ELECTRÓNICA",
    serie: "F001",
    numero: "00000001",
    fecha_emision: "2025-01-15",
    moneda: "PEN",
    emisor_ruc: "20123456789",
    emisor_razon_social: "EMPRESA DEMO S.A.C.",
    emisor_direccion: "Av. Principal 123, Lima",
    receptor_tipo_documento: "RUC",
    receptor_numero_documento: "20987654321",
    receptor_razon_social: "CLIENTE DEMO E.I.R.L.",
    items: [
      { cantidad: 10, unidad: "UND", descripcion: "Producto de ejemplo", precio_unitario: 100.00, valor_venta: 1000.00, igv: 180.00, precio_total: 1180.00 }
    ],
    total_operaciones_gravadas: 1000.00,
    total_operaciones_exoneradas: 0,
    total_operaciones_inafectas: 0,
    total_igv: 180.00,
    importe_total: 1180.00,
    importe_total_letras: "MIL CIENTO OCHENTA CON 00/100 SOLES",
    forma_pago: "Contado"
  }
};
