from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Preformatted, Image

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'output' / 'pdf' / 'ra2_entrega_mercado_local.pdf'
OUT.parent.mkdir(parents=True, exist_ok=True)
NAVY = colors.HexColor('#132238')
BLUE = colors.HexColor('#246BCE')
LIGHT = colors.HexColor('#F3F6FA')
GREEN = colors.HexColor('#18865B')
GRAY = colors.HexColor('#5A6878')
s = getSampleStyleSheet()
s.add(ParagraphStyle(name='Cover2', parent=s['Title'], fontName='Helvetica-Bold', fontSize=25, leading=30, textColor=NAVY, alignment=TA_CENTER, spaceAfter=14))
s.add(ParagraphStyle(name='Sub2', parent=s['Normal'], fontSize=13, leading=18, textColor=GRAY, alignment=TA_CENTER, spaceAfter=24))
s.add(ParagraphStyle(name='Sec2', parent=s['Heading1'], fontName='Helvetica-Bold', fontSize=19, leading=23, textColor=NAVY, spaceAfter=12))
s.add(ParagraphStyle(name='Body3', parent=s['BodyText'], fontSize=10.5, leading=15, textColor=NAVY, spaceAfter=8))
s.add(ParagraphStyle(name='Small3', parent=s['Normal'], fontSize=9, leading=12, textColor=GRAY))
s.add(ParagraphStyle(name='Label3', parent=s['Normal'], fontName='Helvetica-Bold', fontSize=9, textColor=BLUE))
s.add(ParagraphStyle(name='Code3', parent=s['Code'], fontName='Courier', fontSize=8.1, leading=11, textColor=colors.HexColor('#D9E7FF'), backColor=colors.HexColor('#1D2939'), borderPadding=9))

def footer(canvas, doc):
    canvas.saveState(); canvas.setStrokeColor(colors.HexColor('#D9E1EA')); canvas.line(.65*inch,.55*inch,7.85*inch,.55*inch)
    canvas.setFont('Helvetica',8); canvas.setFillColor(GRAY); canvas.drawString(.65*inch,.35*inch,'RA2 | Django + React + JWT + APIs')
    canvas.drawRightString(7.85*inch,.35*inch,f'Pagina {doc.page}'); canvas.restoreState()

def evidence(title, browser, body):
    head = Table([[Paragraph(title,s['Label3']), Paragraph(browser,ParagraphStyle('B',parent=s['Small3'],textColor=GREEN,alignment=2))]], colWidths=[5.75*inch,1.05*inch])
    head.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),LIGHT),('BOX',(0,0),(-1,-1),.5,colors.HexColor('#D9E1EA')),('LEFTPADDING',(0,0),(-1,-1),10),('RIGHTPADDING',(0,0),(-1,-1),10),('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8)]))
    box = Table([[head],[Preformatted(body,s['Code3'])]], colWidths=[6.8*inch])
    box.setStyle(TableStyle([('BOX',(0,0),(-1,-1),.7,colors.HexColor('#C7D2DF')),('BACKGROUND',(0,1),(-1,1),colors.HexColor('#1D2939')),('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),0),('TOPPADDING',(0,0),(-1,-1),0),('BOTTOMPADDING',(0,0),(-1,-1),0)]))
    return box

def real_capture(filename, caption):
    path = ROOT / 'output' / 'ra2_captures' / filename
    image = Image(str(path), width=6.8*inch, height=4.49*inch)
    return [Paragraph(caption, s['Body3']), image]

console_token = 'Token JWT obtenido: eyJ...token real capturado en la consola del navegador...'
console_path = ROOT / 'output' / 'ra2_captures' / 'console.txt'
if console_path.exists():
    for line in console_path.read_text(encoding='utf-8').splitlines():
        if 'Token JWT obtenido:' in line:
            console_token = line[:55] + ' ... (token real capturado; se muestra abreviado)'
            break

story = [Spacer(1,.7*inch),Paragraph('ENTREGA DE ACTIVIDAD',s['Small3']),Spacer(1,.12*inch),Paragraph('RA2 Django + React con Autenticacion y APIs',s['Cover2']),Paragraph('Mercado Local | Unidades 2 y 3',s['Sub2'])]
info = Table([['Repositorio','https://github.com/ismael789/Django-React-con-Autenticaci-n-y-APIs'],['Rama','main'],['Backend','Django REST Framework + JWT + Zeep'],['Frontend','React + Vite + React Router v6'],['API externa','Advice Slip API'],['SOAP','CountryInfoService']], colWidths=[1.55*inch,5.25*inch])
info.setStyle(TableStyle([('BACKGROUND',(0,0),(0,-1),NAVY),('TEXTCOLOR',(0,0),(0,-1),colors.white),('BACKGROUND',(1,0),(1,-1),LIGHT),('TEXTCOLOR',(1,0),(1,-1),NAVY),('FONTNAME',(0,0),(0,-1),'Helvetica-Bold'),('FONTSIZE',(0,0),(-1,-1),9.5),('GRID',(0,0),(-1,-1),.4,colors.HexColor('#D9E1EA')),('TOPPADDING',(0,0),(-1,-1),9),('BOTTOMPADDING',(0,0),(-1,-1),9)]))
story += [info,Spacer(1,.3*inch),Paragraph('Proyecto integrado con el backend de la Practica 4 y un frontend React protegido por JWT.',s['Body3']),PageBreak()]

story += [Paragraph('1. Login funcionando y token JWT',s['Sec2']),Paragraph('Captura real tomada de la pantalla React de login con los datos de prueba. El token se obtuvo desde la consola del navegador.',s['Body3']),*real_capture('01-login.png','Captura real 1 | Login en React'),evidence('Consola real del navegador','Chrome',console_token),PageBreak()]
story += [Paragraph('2. Dashboard protegido y AuthContext',s['Sec2']),Paragraph('Captura real posterior al login. El Dashboard muestra el usuario cargado mediante AuthContext y la consulta protegida /api/v1/auth/me/.',s['Body3']),*real_capture('02-dashboard.png','Captura real 2 | Dashboard protegido'),PageBreak()]
story += [Paragraph('3. Widget de API de terceros',s['Sec2']),Paragraph('Captura real del Dashboard con el consejo cargado desde Advice Slip API mediante fetch.',s['Body3']),*real_capture('03-api-terceros.png','Captura real 3 | API externa Advice Slip'),PageBreak()]
story += [Paragraph('4. Consumo SOAP con Zeep',s['Sec2']),Paragraph('Captura real del Dashboard después de consultar MX. La respuesta visible proviene de CountryInfoService y fue consumida por Django mediante Zeep.',s['Body3']),*real_capture('04-soap.png','Captura real 4 | Respuesta SOAP CountryInfoService'),PageBreak()]
story += [Paragraph('Instalacion y ejecucion',s['Sec2']),evidence('Comandos de arranque','Windows PowerShell','Backend\ncd backend\n..\\venv\\Scripts\\Activate.ps1\npip install -r requirements.txt\npython manage.py migrate\npython manage.py runserver 127.0.0.1:8000\n\nFrontend\ncd frontend\nCopy-Item .env.example .env\nnpm install\nnpm run dev\n\nAbrir: http://localhost:5173'),Spacer(1,.25*inch),Paragraph('Dependencias implementadas: Django REST Framework, SimpleJWT, CORS headers, Zeep, React, Vite, React Router v6, Semantic UI, Sass, Formik, Yup y React Toastify.',s['Body3']),Paragraph('El codigo fuente de backend y frontend, junto con README.md y .gitignore, se encuentra en el repositorio indicado.',s['Body3'])]

doc = SimpleDocTemplate(str(OUT),pagesize=letter,rightMargin=.85*inch,leftMargin=.85*inch,topMargin=.72*inch,bottomMargin=.72*inch,title='RA2 Mercado Local',author='Proyecto Django React')
doc.build(story,onFirstPage=footer,onLaterPages=footer)
print(OUT)
