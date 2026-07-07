# 💈 Sistema de Gestión Integral para Barberías

Una plataforma web modular diseñada para optimizar la administración, el agendamiento y la comunicación dentro de una barbería. Este sistema digitaliza la experiencia tanto para el negocio como para sus clientes, centralizando reservas, pagos y mensajería en un solo lugar.

## ✨ Características Principales

* **📅 Control de Citas y Agendamientos:** Calendario interactivo para disponibilidad en tiempo real, reserva de turnos y recordatorios.
* **💳 Gestión de Pagos:** Registro de transacciones, historial de servicios pagados y control de ingresos.
* **💬 Módulo de Conversaciones:** Chat integrado para facilitar la comunicación directa y resolver dudas sobre cortes, estilos o cambios de horario.

## 👥 Roles del Sistema

La plataforma está diseñada con una arquitectura basada en permisos para tres perfiles principales:

1. **👑 Administrador:** Tiene control total del sistema. Puede gestionar sucursales, ver reportes financieros, administrar el catálogo de servicios/precios y supervisar a todo el personal.
2. **✂️ Barbero:** Accede a su agenda personal, confirma o reprograma citas, se comunica con sus clientes y visualiza su historial de servicios realizados.
3. **👤 Cliente:** Puede explorar los servicios, elegir a su barbero de preferencia, reservar turnos según disponibilidad, realizar pagos y chatear con el personal.

## 🛠️ Tecnologías Utilizadas

* **Backend:** Python (Django)
* **Frontend:** JavaScript, HTML5, CSS3
* **Base de Datos:** PostgreSQL / SQL Server
* **Control de Versiones:** Git & GitHub

## 🚀 Instalación y Configuración Local

Sigue estos pasos para levantar el entorno de desarrollo en tu máquina local:

### 1. Clonar el repositorio
```bash
git clone [https://github.com/tu-usuario/barber](https://github.com/tu-usuario/barber.git)
cd barber

# Crear un entorno virtual
python -m venv venv

# Activar el entorno virtual
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate

# Instalar las dependencias
pip install -r requirements.txt
