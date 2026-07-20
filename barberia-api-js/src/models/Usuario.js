const { DataTypes } = require('sequelize');
const sequelize = require('../config/db');

const Usuario = sequelize.define('Usuario', {
    // El ID se crea automáticamente en Sequelize, pero si quieres controlarlo:
    id: {
        type: DataTypes.INTEGER,
        primaryKey: true,
        autoIncrement: true
    },
    nombre: {
        type: DataTypes.STRING,
        allowNull: false
    },
    email: {
        type: DataTypes.STRING,
        allowNull: false,
        unique: true
    },
    password: {
        type: DataTypes.STRING,
        allowNull: false
    },
    rol: {
        type: DataTypes.STRING,
        defaultValue: 'CLIENTE',
        // Validamos que solo acepte estos roles específicos
        validate: {
            isIn: [['ADM', 'BARBERO', 'CLIENTE']]
        }
    },
    estado: {
        type: DataTypes.STRING,
        defaultValue: 'ACTIVO', // Puede ser: ACTIVO, INACTIVO, BLOQUEADO
        // Validamos que solo acepte estos estados específicos
        validate: {
            isIn: [['ACTIVO', 'INACTIVO', 'BLOQUEADO']]
        }
    }
}, {
    timestamps: true, // Crea automáticamente las columnas createdAt y updatedAt
    tableName: 'usuarios'
});

module.exports = Usuario;