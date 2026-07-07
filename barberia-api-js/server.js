const express = require('express');
const { Usuario, Servicio, Cita, Publicacion, Comentario, Reaccion } = require('./src/models'); // Importa los modelos y la conexión a la base de datos

// 1. Inicializamos la aplicación
const app = express();

// 2. Middleware (Esto permite que el servidor entienda datos en formato JSON)
app.use(express.json());

const path = require('path');
// Le decimos a Express que la carpeta "public" contiene nuestros archivos visuales
app.use(express.static(path.join(__dirname, 'public')));

// 3. Importar rutas
const usuariosRoutes = require('./src/routes/usuarios.routes');
const serviciosRoutes = require('./src/routes/servicios.routes');
const citasRoutes = require('./src/routes/citas.routes');
const authRoutes = require('./src/routes/auth.routes');
const publicacionesRoutes = require('./src/routes/publicaciones.routes');


// 4. Usar las rutas
app.use('/api/usuarios', usuariosRoutes);
app.use('/api/servicios', serviciosRoutes);
app.use('/api/citas', citasRoutes);
app.use('/api/auth', authRoutes);
app.use('/api/publicaciones', publicacionesRoutes);

// Ruta de prueba
app.get('/', (req, res) => {
    res.send('¡Servidor de la Barbería en línea! 💈');
});

// 5. Encender el servidor y conectar base de datos
const PORT = process.env.PORT || 3000;

// Sincronizamos los modelos (crea las tablas si no existen) y luego levantamos el servidor
const sequelize = require('./src/config/db'); // Importamos la instancia de sequelize
sequelize.sync({ alter: true }) 
    .then(() => {
        console.log('Modelos sincronizados con la base de datos de PostgreSQL. 📦');
        app.listen(PORT, () => {
            console.log(`Servidor corriendo en el puerto ${PORT} 🚀`);
        });
    })
    .catch(err => console.error('Error al sincronizar la base de datos:', err));



