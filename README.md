# Barbería - Sistema de Gestión

Backend migrado de Node.js (Express + Sequelize) a **Python Django + Django REST Framework**.

## Tecnologías

- **Python 3.14** / Django 5.1
- **Django REST Framework** 3.15
- **PostgreSQL** (base de datos existente)
- **JWT** (autenticación con djangorestframework-simplejwt)
- **CORS** habilitado

## Requisitos

- Python 3.10+
- PostgreSQL (con la base de datos `barberia` existente)
- pip

## Instalación

```bash
cd barberia-backend
pip install -r requirements.txt
```

## Configuración

1. Copia `.env.example` a `.env` y ajusta las credenciales:

```env
SECRET_KEY=genera-una-clave-segura
DEBUG=True
DB_NAME=barberia
DB_USER=postgres
DB_PASSWORD=tu_contraseña
DB_HOST=localhost
DB_PORT=5432
JWT_SECRET=tu_palabra_secreta
```

2. Las tablas ya existen en PostgreSQL (creadas por Sequelize). Los migrations están
   marcados como aplicados con `--fake-initial` para respetar el schema existente.

## Ejecución

```bash
cd barberia-backend
python manage.py runserver
```

Servidor en `http://localhost:8000`

## API Endpoints

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| POST | `/api/auth/login` | Iniciar sesión | - |
| POST | `/api/auth/registro` | Registrar cliente | - |
| POST | `/api/auth/recuperar` | Recuperar contraseña | - |
| GET | `/api/usuarios` | Listar usuarios | - |
| GET | `/api/usuarios/:id` | Detalle usuario | - |
| POST | `/api/usuarios` | Crear usuario | Admin |
| PUT | `/api/usuarios/:id` | Actualizar usuario | Admin |
| DELETE | `/api/usuarios/:id` | Eliminar usuario | Admin |
| GET | `/api/servicios` | Listar servicios | - |
| POST | `/api/servicios` | Crear servicio | Admin |
| PUT | `/api/servicios/:id` | Actualizar servicio | Admin |
| DELETE | `/api/servicios/:id` | Eliminar servicio | Admin |
| GET | `/api/citas` | Listar citas | - |
| POST | `/api/citas` | Crear cita | - |
| DELETE | `/api/citas/cliente/:id` | Cancelar cita (cliente) | Cliente |
| GET | `/api/publicaciones` | Listar publicaciones | - |
| GET | `/api/publicaciones/barbero/:id` | Pub. por barbero | - |
| POST | `/api/publicaciones` | Crear publicación | Barbero/Admin |
| PUT | `/api/publicaciones/:id` | Actualizar publicación | Propietario |
| DELETE | `/api/publicaciones/:id` | Eliminar publicación | Propietario |
| POST | `/api/publicaciones/:id/reacciones` | Reaccionar (like/dislike) | Auth |
| POST | `/api/publicaciones/:id/comentarios` | Comentar | Auth |
| DELETE | `/api/publicaciones/comentarios/:id` | Eliminar comentario | Propietario |

## Estructura del proyecto

```
barberia-backend/
├── manage.py
├── requirements.txt
├── .env
├── barberia/                  # Configuración Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── apps/
│   ├── usuarios/              # Modelo Usuario + CRUD
│   ├── servicios/             # Modelo Servicio + CRUD
│   ├── citas/                 # Modelo Cita + CRUD
│   ├── publicaciones/         # Publicacion, Comentario, Reaccion
│   └── authentication/        # Login, Registro, Recuperar
├── public/                    # Frontend HTML estático
└── static/                    # Archivos estáticos Django
```
