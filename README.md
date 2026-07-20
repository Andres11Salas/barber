# Barbería - Sistema de Gestión

Sistema completo para gestión de barbería con **dos versiones** de API que comparten la misma base de datos PostgreSQL y el mismo frontend HTML.

## Estructura del proyecto

```
barber/
├── barberia-api-js/        # Versión Node.js (Express + Sequelize) — referencia
│   └── ...
├── barberia-api-py/        # Versión Python (Django + DRF) — activa/recomendada
│   ├── manage.py
│   ├── requirements.txt
│   ├── barberia/           # Configuración Django
│   ├── apps/               # Módulos: usuarios, servicios, citas, publicaciones, auth
│   └── public/             # Frontend HTML/CSS estático
├── .gitignore
├── README.md
└── LICENSE
```

## Versión activa: Python (barberia-api-py)

**Stack:** Django 5.1 + Django REST Framework 3.15 + PostgreSQL

### Requisitos

- Python 3.10+
- PostgreSQL (base de datos `barberia` existente con datos)
- pip

### Instalación y ejecución

```bash
cd barberia-api-py
pip install -r requirements.txt
python manage.py runserver
# Servidor en http://localhost:8000
```

### Configuración

Copia `.env.example` a `.env` y ajusta las credenciales de PostgreSQL.

### API Endpoints

| Método | Endpoint | Auth |
|--------|----------|------|
| POST | `/api/auth/login` | - |
| POST | `/api/auth/registro` | - |
| POST | `/api/auth/recuperar` | - |
| GET/POST | `/api/usuarios` | POST requiere Admin |
| GET/PUT/DELETE | `/api/usuarios/:id` | PUT/DELETE requieren Admin |
| GET | `/api/servicios` | - |
| POST/PUT/DELETE | `/api/servicios/:id` | Admin |
| GET/POST | `/api/citas` | - |
| DELETE | `/api/citas/cliente/:id` | Cliente (dueño) |
| GET/POST | `/api/publicaciones` | POST: Barbero/Admin |
| PUT/DELETE | `/api/publicaciones/:id` | Propietario |
| POST | `/api/publicaciones/:id/reacciones` | Auth requerido |
| POST | `/api/publicaciones/:id/comentarios` | Auth requerido |
| DELETE | `/api/publicaciones/comentarios/:id` | Propietario |

### Base de datos

PostgreSQL con tablas: `usuarios`, `servicios`, `citas`, `publicaciones`, `comentarios`, `reacciones`.
Los modelos Django mapean exactamente al schema existente (creado originalmente por Sequelize).
Migraciones aplicadas con `--fake-initial` para preservar datos.

### Roles

- **ADM** — Acceso total
- **BARBERO** — Crea/edita publicaciones, atiende citas
- **CLIENTE** — Agenda/cancela citas, comenta y reacciona

---

## Versión referencia: JavaScript (barberia-api-js)

**Stack:** Node.js + Express 5 + Sequelize + PostgreSQL

Código original conservado como referencia de la arquitectura anterior.
No requiere ejecución — la versión Python es la activa.

---

## Seguridad

- El archivo `.env` con credenciales está excluido vía `.gitignore`
- Las contraseñas en la base de datos se almacenan en texto plano (mejorable con bcrypt)
- Autenticación JWT con tokens de 2h de duración
- CORS habilitado para desarrollo
