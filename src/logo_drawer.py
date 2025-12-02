from reportlab.lib import colors
from reportlab.graphics.shapes import Drawing, Rect, Circle, String, Group, Polygon, Line
from reportlab.graphics import renderPDF
import random

class LogoDrawer:
    """Clase para dibujar logos vectoriales dinámicos basados en la industria"""

    @staticmethod
    def draw_logo(c, x, y, size, company_name, industry_type="general"):
        """
        Dibuja un logo en el canvas en la posición (x, y) con tamaño especificado.
        El logo se genera proceduralmente basado en el nombre y la industria.
        """
        # Extraer iniciales
        words = company_name.split()
        initials = "".join([w[0] for w in words if len(w) > 2])[:2].upper()
        if not initials:
            initials = company_name[:2].upper()

        # Configuración por industria
        if industry_type == "construccion":
            color_primary = colors.orange
            color_secondary = colors.black
            shape_type = "hexagon"
        elif industry_type == "tech":
            color_primary = colors.HexColor("#007bff") # Azul brillante
            color_secondary = colors.HexColor("#17a2b8") # Cyan
            shape_type = "circuit"
        elif industry_type == "restaurante":
            color_primary = colors.HexColor("#dc3545") # Rojo
            color_secondary = colors.HexColor("#28a745") # Verde
            shape_type = "circle_organic"
        elif industry_type == "transporte":
            color_primary = colors.HexColor("#ffc107") # Amarillo
            color_secondary = colors.black
            shape_type = "arrow"
        elif industry_type == "hotel":
            color_primary = colors.HexColor("#d4af37") # Dorado
            color_secondary = colors.HexColor("#333333") # Gris oscuro
            shape_type = "crown"
        else:
            color_primary = colors.HexColor("#6c757d") # Gris
            color_secondary = colors.HexColor("#343a40") # Gris oscuro
            shape_type = "square"

        c.saveState()
        c.translate(x, y)
        
        # Dibujar fondo/forma base
        if shape_type == "hexagon":
            # Simular hexágono con polígono
            path = c.beginPath()
            path.moveTo(size*0.5, size)
            path.lineTo(size, size*0.75)
            path.lineTo(size, size*0.25)
            path.lineTo(size*0.5, 0)
            path.lineTo(0, size*0.25)
            path.lineTo(0, size*0.75)
            path.close()
            c.setFillColor(color_primary)
            c.drawPath(path, fill=1, stroke=0)
            
            # Detalle interno
            c.setFillColor(color_secondary)
            c.circle(size*0.5, size*0.5, size*0.25, fill=1, stroke=0)

        elif shape_type == "circuit":
            c.setFillColor(colors.white)
            c.setStrokeColor(color_primary)
            c.setLineWidth(2)
            c.rect(0, 0, size, size, fill=0, stroke=1)
            
            c.setFillColor(color_secondary)
            c.circle(size*0.2, size*0.8, size*0.1, fill=1, stroke=0)
            c.circle(size*0.8, size*0.2, size*0.1, fill=1, stroke=0)
            c.line(size*0.2, size*0.8, size*0.5, size*0.5)
            c.line(size*0.8, size*0.2, size*0.5, size*0.5)
            c.circle(size*0.5, size*0.5, size*0.15, fill=1, stroke=0)

        elif shape_type == "circle_organic":
            c.setFillColor(color_primary)
            c.circle(size*0.5, size*0.5, size*0.45, fill=1, stroke=0)
            c.setFillColor(colors.white)
            c.circle(size*0.5, size*0.5, size*0.35, fill=1, stroke=0)
            c.setFillColor(color_secondary)
            c.circle(size*0.5, size*0.5, size*0.25, fill=1, stroke=0)

        elif shape_type == "arrow":
            path = c.beginPath()
            path.moveTo(0, size*0.3)
            path.lineTo(size*0.6, size*0.3)
            path.lineTo(size*0.6, 0)
            path.lineTo(size, size*0.5)
            path.lineTo(size*0.6, size)
            path.lineTo(size*0.6, size*0.7)
            path.lineTo(0, size*0.7)
            path.close()
            c.setFillColor(color_primary)
            c.drawPath(path, fill=1, stroke=0)

        elif shape_type == "crown":
            path = c.beginPath()
            path.moveTo(0, size)
            path.lineTo(size*0.2, size*0.4)
            path.lineTo(size*0.5, size)
            path.lineTo(size*0.8, size*0.4)
            path.lineTo(size, size)
            path.lineTo(size, 0)
            path.lineTo(0, 0)
            path.close()
            c.setFillColor(color_primary)
            c.drawPath(path, fill=1, stroke=0)

        else: # Square/General
            c.setFillColor(color_primary)
            c.rect(0, 0, size, size, fill=1, stroke=0)
            c.setFillColor(color_secondary)
            c.rect(size*0.1, size*0.1, size*0.8, size*0.8, fill=1, stroke=0)

        # Dibujar Iniciales
        c.setFillColor(colors.white)
        if shape_type in ["circuit", "transporte"]:
            c.setFillColor(colors.black)
            
        c.setFont("Helvetica-Bold", size*0.4)
        c.drawCentredString(size*0.5, size*0.35, initials)

        c.restoreState()
