# Mercado Local API

API REST de una tienda en línea desarrollada con Django REST Framework. El proyecto usa un usuario personalizado que inicia sesión con correo electrónico y agrega el campo `carrera`.

## Instalación

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

La documentación Swagger está disponible en `http://127.0.0.1:8000/api/swagger/` y el esquema OpenAPI en `/api/schema/`.

## Endpoints principales

- `POST /api/usuarios/`: alta de usuario con `email`, `password` y `carrera`.
- `POST /api/token/`: obtiene `access` y `refresh` usando email y contraseña.
- `POST /api/token/refresh/`: renueva el token de acceso.
- `GET /api/usuarios/datos-personales/`: devuelve los datos personales del usuario autenticado.
- `GET|POST|PUT|PATCH|DELETE /api/usuarios/<id>/`: CRUD protegido de usuarios.
- `GET|POST|PUT|PATCH|DELETE /api/products/`: CRUD protegido de productos.
- `GET|POST|PUT|PATCH|DELETE /api/categories/`: CRUD protegido de categorías.

## Correcciones de seguridad

- `password` es un campo `write_only`; nunca aparece en ninguna respuesta, incluido datos personales.
- En una actualización, la contraseña solo se modifica cuando el campo `password` viene explícitamente en la petición.
- El token de acceso dura 30 minutos (`ACCESS_TOKEN_LIFETIME`).

## Pruebas

```powershell
python manage.py test
```

Incluye pruebas de token por email, ausencia del hash y conservación de contraseña al editar sin enviarla.
# django-project

## RA2 Django + React con autenticacion y APIs

La actividad de cierre conserva el backend de Mercado Local y agrega un frontend React con Vite, autenticacion JWT, consumo de una API REST externa y un servicio SOAP publico.

### Arrancar el backend

```powershell
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 127.0.0.1:8000
```

Endpoints RA2:

- `POST /api/v1/auth/register/`: registro publico con contrasena cifrada.
- `POST /api/token/`: login con email y contrasena.
- `GET /api/v1/auth/me/`: datos del usuario autenticado con Bearer JWT.
- `GET /api/v1/soap/country/?code=MX`: consulta CountryInfoService mediante Zeep.
- `GET /api/swagger/`: documentacion OpenAPI.

### Arrancar el frontend

En otra terminal:

```powershell
cd frontend
Copy-Item .env.example .env
npm install
npm run dev
```

Abrir `http://localhost:5173`. El archivo `.env` usa `VITE_BASE_API_URL=http://127.0.0.1:8000` y `VITE_TOKEN_STORAGE_KEY=mercado_local_access_token`.

El frontend incluye las rutas modulares `routes.admin`, `routes.client`, `routes.common` y `Navigation`, los layouts `AdminLayout`, `ClientLayout` y `CommonLayout`, las pantallas de login, registro, catalogo y dashboard protegido, el widget Advice Slip y el formulario SOAP.

### Capturas para el PDF

1. Login funcionando y consola del navegador mostrando el token JWT.
2. Dashboard protegido mostrando el usuario cargado por `AuthContext`.
3. Widget de Advice Slip con un consejo y el boton de refrescar.
4. Consulta SOAP con el codigo `MX` y la respuesta visible.
