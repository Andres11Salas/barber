const { Sequelize } = require('sequelize');
require('dotenv').config();

// Inicializamos Sequelize con las credenciales del .env
const sequelize = new Sequelize(
    process.env.DB_NAME, 
    process.env.DB_USER, 
    process.env.DB_PASSWORD, 
    {
        host: process.env.DB_HOST,
        dialect: 'postgres', // Le decimos qué motor de base de datos usar
        port: process.env.DB_PORT,
        logging: false // Pon esto en 'console.log' si quieres ver el SQL que Sequelize genera por detrás
    }
);

// Probamos la conexión
const conectarDB = async () => {
    try {
        await sequelize.authenticate();
        console.log('¡Conexión a PostgreSQL con Sequelize exitosa! 🚀');
    } catch (error) {
        console.error('Error conectando a la base de datos:', error);
    }
};

conectarDB();

module.exports = sequelize;