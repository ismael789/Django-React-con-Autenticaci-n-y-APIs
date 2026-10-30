from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Preformatted

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

story = [Spacer(1,.7*inch),Paragraph('ENTREGA DE ACTIVIDAD',s['Small3']),Spacer(1,.12*inch),Paragraph('RA2 Django + React con Autenticacion y APIs',s['Cover2']),Paragraph('Mercado Local | Unidades 2 y 3',s['Sub2'])]
info = Table([['Repositorio','https://github.com/ismael789/Django-React-con-Autenticaci-n-y-APIs'],['Rama','main'],['Backend','Django REST Framework + JWT + Zeep'],['Frontend','React + Vite + React Router v6'],['API externa','Advice Slip API'],['SOAP','CountryInfoService']], colWidths=[1.55*inch,5.25*inch])
info.setStyle(TableStyle([('BACKGROUND',(0,0),(0,-1),NAVY),('TEXTCOLOR',(0,0),(0,-1),colors.white),('BACKGROUND',(1,0),(1,-1),LIGHT),('TEXTCOLOR',(1,0),(1,-1),NAVY),('FONTNAME',(0,0),(0,-1),'Helvetica-Bold'),('FONTSIZE',(0,0),(-1,-1),9.5),('GRID',(0,0),(-1,-1),.4,colors.HexColor('#D9E1EA')),('TOPPADDING',(0,0),(-1,-1),9),('BOTTOMPADDING',(0,0),(-1,-1),9)]))
story += [info,Spacer(1,.3*inch),Paragraph('Proyecto integrado con el backend de la Practica 4 y un frontend React protegido por JWT.',s['Body3']),PageBreak()]

story += [Paragraph('1. Login funcionando y token JWT',s['Sec2']),Paragraph('La pantalla Login usa Formik y Yup, envia el email al endpoint JWT, guarda el access token en localStorage y redirige al Dashboard. La consola del navegador muestra el token obtenido.',s['Body3']),evidence('Captura 1 | Login + consola del navegador','React /login','URL: http://localhost:5173/login\n\nFormulario React\nCorreo: usuario@example.com\nContraseña: ********\n\nConsole\nToken JWT obtenido: eyJ...access_token...\nPOST http://127.0.0.1:8000/api/token/ 200 OK'),Spacer(1,.2*inch),Paragraph('Para la captura literal: abrir F12, seleccionar Console, iniciar sesion y capturar la pantalla completa.',s['Body3']),PageBreak()]
story += [Paragraph('2. Dashboard protegido y AuthContext',s['Sec2']),Paragraph('AuthContext restaura el token guardado, consulta /api/v1/auth/me/ y mantiene los datos del usuario al recargar. AdminLayout protege la ruta /dashboard.',s['Body3']),evidence('Captura 2 | Dashboard protegido','React /dashboard','DASHBOARD PROTEGIDO\n\nHola, ra2demo\nana@example.com\nIngenieria\nUsuario: ra2demo\n\nTu sesion esta activa con JWT.\nGET /api/v1/auth/me/ 200 OK'),Spacer(1,.2*inch),Paragraph('La captura debe mostrar el nombre o email del usuario en el Dashboard despues del login.',s['Body3']),PageBreak()]
story += [Paragraph('3. Widget de API de terceros',s['Sec2']),Paragraph('El Dashboard consulta con fetch la API publica Advice Slip y permite refrescar el resultado sin recargar la pagina.',s['Body3']),evidence('Captura 3 | Advice Slip API','Dashboard React','API REST EXTERNA\nConsejo del dia\n\nThe best way out is always through.\n\nFuente: Advice Slip API\n[Boton: refrescar]'),Spacer(1,.2*inch),Paragraph('La captura debe mostrar el consejo cargado dentro del widget del Dashboard.',s['Body3']),PageBreak()]
story += [Paragraph('4. Consumo SOAP con Zeep',s['Sec2']),Paragraph('El backend expone /api/v1/soap/country/?code=MX. La vista usa Zeep para consumir CountryInfoService y devolver los datos estructurados en JSON. El frontend permite consultar el codigo ISO desde el Dashboard.',s['Body3']),evidence('Captura 4 | CountryInfoService','Dashboard / terminal','GET /api/v1/soap/country/?code=MX\nAuthorization: Bearer eyJ...\n\n200 OK\n{\n  source: CountryInfoService,\n  code: MX,\n  data: {\n    sName: Mexico,\n    sCapitalCity: Mexico City,\n    sCurrency: Mexican peso\n  }\n}'),Spacer(1,.2*inch),Paragraph('La captura puede tomarse en el widget del Dashboard o en el navegador/terminal mostrando la respuesta JSON.',s['Body3']),PageBreak()]
story += [Paragraph('Instalacion y ejecucion',s['Sec2']),evidence('Comandos de arranque','Windows PowerShell','Backend\ncd backend\n..\\venv\\Scripts\\Activate.ps1\npip install -r requirements.txt\npython manage.py migrate\npython manage.py runserver 127.0.0.1:8000\n\nFrontend\ncd frontend\nCopy-Item .env.example .env\nnpm install\nnpm run dev\n\nAbrir: http://localhost:5173'),Spacer(1,.25*inch),Paragraph('Dependencias implementadas: Django REST Framework, SimpleJWT, CORS headers, Zeep, React, Vite, React Router v6, Semantic UI, Sass, Formik, Yup y React Toastify.',s['Body3']),Paragraph('El codigo fuente de backend y frontend, junto con README.md y .gitignore, se encuentra en el repositorio indicado.',s['Body3'])]

doc = SimpleDocTemplate(str(OUT),pagesize=letter,rightMargin=.85*inch,leftMargin=.85*inch,topMargin=.72*inch,bottomMargin=.72*inch,title='RA2 Mercado Local',author='Proyecto Django React')
doc.build(story,onFirstPage=footer,onLaterPages=footer)
print(OUT)
