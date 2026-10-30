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
