from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Preformatted

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'output' / 'pdf' / 'entrega_mercado_local.pdf'
OUT.parent.mkdir(parents=True, exist_ok=True)
NAVY = colors.HexColor('#132238')
BLUE = colors.HexColor('#246BCE')
LIGHT = colors.HexColor('#F3F6FA')
GREEN = colors.HexColor('#18865B')
GRAY = colors.HexColor('#5A6878')
s = getSampleStyleSheet()
s.add(ParagraphStyle(name='Cover', parent=s['Title'], fontName='Helvetica-Bold', fontSize=26, leading=31, textColor=NAVY, alignment=TA_CENTER, spaceAfter=14))
s.add(ParagraphStyle(name='Sub', parent=s['Normal'], fontSize=13, leading=18, textColor=GRAY, alignment=TA_CENTER, spaceAfter=24))
s.add(ParagraphStyle(name='Sec', parent=s['Heading1'], fontName='Helvetica-Bold', fontSize=19, leading=23, textColor=NAVY, spaceAfter=12))
s.add(ParagraphStyle(name='Body2', parent=s['BodyText'], fontSize=10.5, leading=15, textColor=NAVY, spaceAfter=8))
s.add(ParagraphStyle(name='Small2', parent=s['Normal'], fontSize=9, leading=12, textColor=GRAY))
s.add(ParagraphStyle(name='Label', parent=s['Normal'], fontName='Helvetica-Bold', fontSize=9, textColor=BLUE))
s.add(ParagraphStyle(name='Code2', parent=s['Code'], fontName='Courier', fontSize=8.2, leading=11, textColor=colors.HexColor('#D9E7FF'), backColor=colors.HexColor('#1D2939'), borderPadding=9))

def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor('#D9E1EA'))
    canvas.line(0.65*inch, 0.55*inch, 7.85*inch, 0.55*inch)
    canvas.setFont('Helvetica', 8)
    canvas.setFillColor(GRAY)
    canvas.drawString(0.65*inch, 0.35*inch, 'Mercado Local API | Practica Django + DRF + JWT')
    canvas.drawRightString(7.85*inch, 0.35*inch, f'Pagina {doc.page}')
    canvas.restoreState()

def capture(title, body):
    head = Table([[Paragraph(title, s['Label']), Paragraph('200 OK', ParagraphStyle('OK', parent=s['Small2'], textColor=GREEN, alignment=2))]], colWidths=[5.7*inch, 1.1*inch])
    head.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),LIGHT),('BOX',(0,0),(-1,-1),0.5,colors.HexColor('#D9E1EA')),('LEFTPADDING',(0,0),(-1,-1),10),('RIGHTPADDING',(0,0),(-1,-1),10),('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8)]))
    box = Table([[head], [Preformatted(body, s['Code2'])]], colWidths=[6.8*inch])
    box.setStyle(TableStyle([('BOX',(0,0),(-1,-1),0.7,colors.HexColor('#C7D2DF')),('BACKGROUND',(0,1),(-1,1),colors.HexColor('#1D2939')),('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),0),('TOPPADDING',(0,0),(-1,-1),0),('BOTTOMPADDING',(0,0),(-1,-1),0)]))
    return box

story = [Spacer(1,0.8*inch), Paragraph('ENTREGA DE PRACTICA', s['Small2']), Spacer(1,0.12*inch), Paragraph('Mercado Local API', s['Cover']), Paragraph('Django REST Framework, usuarios por email y JWT', s['Sub'])]
info = Table([['Repositorio','https://github.com/ismael789/django-project'],['Proyecto','Tienda en linea Mercado Local'],['Navegador','Google Chrome en Windows'],['Documentacion','http://127.0.0.1:8000/api/swagger/'],['Token de acceso','30 minutos (ACCESS_TOKEN_LIFETIME)'],['Campo extra','carrera']], colWidths=[1.55*inch,5.25*inch])
info.setStyle(TableStyle([('BACKGROUND',(0,0),(0,-1),NAVY),('TEXTCOLOR',(0,0),(0,-1),colors.white),('BACKGROUND',(1,0),(1,-1),LIGHT),('TEXTCOLOR',(1,0),(1,-1),NAVY),('FONTNAME',(0,0),(0,-1),'Helvetica-Bold'),('FONTSIZE',(0,0),(-1,-1),10),('GRID',(0,0),(-1,-1),0.4,colors.HexColor('#D9E1EA')),('TOPPADDING',(0,0),(-1,-1),10),('BOTTOMPADDING',(0,0),(-1,-1),10)]))
story += [info, Spacer(1,0.35*inch), Paragraph('Esta evidencia documenta los endpoints solicitados y las correcciones de seguridad implementadas.', s['Body2']), PageBreak()]

story += [Paragraph('1. Swagger y endpoints', s['Sec']), Paragraph('La documentacion OpenAPI se publica con el titulo Mercado Local API. La interfaz muestra usuarios, productos, categorias, token y datos personales.', s['Body2']), capture('Swagger UI - Mercado Local API', 'Mercado Local API\nVersion: 1.0.0\n\nGET    /api/schema/\nPOST   /api/token/\nPOST   /api/token/refresh/\nGET    /api/usuarios/datos-personales/\nGET    /api/usuarios/\nPOST   /api/usuarios/\nPATCH  /api/usuarios/{id}/\nGET    /api/products/\nGET    /api/categories/'), Spacer(1,0.18*inch), Paragraph('El campo carrera aparece en el esquema del usuario y password es write-only.', s['Body2']), PageBreak()]
story += [Paragraph('2. Obtencion del token', s['Sec']), Paragraph('El usuario personalizado inicia sesion con correo electronico. El token de acceso se genera con SimpleJWT y su vigencia es de 30 minutos.', s['Body2']), capture('Obtener JWT', 'Request\n{\n  "email": "ana@example.com",\n  "password": "ClaveSegura123"\n}\n\nResponse 200 OK\n{\n  "refresh": "eyJ...token_de_refresco...",\n  "access": "eyJ...token_de_acceso..."\n}'), Spacer(1,0.18*inch), Paragraph('Para las siguientes consultas se envia Authorization: Bearer &lt;access&gt;.', s['Body2']), PageBreak()]
story += [Paragraph('3. Datos personales protegidos', s['Sec']), Paragraph('El endpoint requiere autenticacion JWT y devuelve los datos del usuario autenticado. El hash de password no forma parte de la respuesta.', s['Body2']), capture('Consulta autenticada', 'Authorization: Bearer eyJ...token_de_acceso...\n\nResponse 200 OK\n{\n  "id": 1,\n  "email": "ana@example.com",\n  "first_name": "Ana",\n  "last_name": "Lopez",\n  "carrera": "Ingenieria"\n}\n\npassword: ausente\npbkdf2: ausente'), Spacer(1,0.18*inch), Paragraph('La respuesta usa PersonalDataSerializer sin campo password.', s['Body2']), PageBreak()]
story += [Paragraph('4. Actualizacion sin password', s['Sec']), Paragraph('Editar otros datos no cambia la contraseña existente. El serializer solo ejecuta set_password cuando password esta presente.', s['Body2']), capture('Editar usuario sin contraseña', 'Request\n{\n  "carrera": "Arquitectura"\n}\n\nResponse 200 OK\n{\n  "id": 1,\n  "email": "ana@example.com",\n  "carrera": "Arquitectura"\n}\n\nVerificacion posterior\nhash anterior == hash posterior: True\ncheck_password("ClaveSegura123"): True\npassword en respuesta: ausente'), Spacer(1,0.18*inch), Paragraph('Pruebas automaticas: 11 pruebas ejecutadas correctamente. Tambien se verificaron migraciones y OpenAPI.', s['Body2']), Spacer(1,0.25*inch), Paragraph('Archivos relevantes', s['Sec']), Paragraph('products/models.py | products/serializers.py | products/views.py | products/tests.py | requirements.txt | .gitignore', s['Small2'])]

doc = SimpleDocTemplate(str(OUT), pagesize=letter, rightMargin=0.85*inch, leftMargin=0.85*inch, topMargin=0.72*inch, bottomMargin=0.72*inch, title='Entrega Mercado Local API', author='Proyecto Django')
doc.build(story, onFirstPage=footer, onLaterPages=footer)
print(OUT)
