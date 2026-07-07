const { DataTypes } = require('sequelize');
const sequelize = require('../config/db');

const Cita = sequelize.define('Cita', {
    id: {
        type: DataTypes.INTEGER,
        primaryKey: true,
        autoIncrement: true
    },
    fecha: {
        type: DataTypes.DATEONLY, // DATEONLY guarda solo la fecha (YYYY-MM-DD)
        allowNull: false
    },
    hora: {
        type: DataTypes.TIME, // Guarda solo la hora
        allowNull: false
    },
    estado: {
        type: DataTypes.STRING,
        defaultValue: 'PENDIENTE',
        validate: {
            isIn: [['PENDIENTE', 'COMPLETADA', 'CANCELADA']]
        }
    }
}, {
    timestamps: true,
    tableName: 'citas'
});

module.exports = Cita;