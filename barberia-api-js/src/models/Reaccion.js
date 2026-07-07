const { DataTypes } = require('sequelize');
const db = require('../config/db');

const Reaccion = db.define('Reaccion', {
    id: { type: DataTypes.INTEGER, primaryKey: true, autoIncrement: true },
    publicacion_id: { type: DataTypes.INTEGER, allowNull: false },
    usuario_id: { type: DataTypes.INTEGER, allowNull: false },
    tipo: { type: DataTypes.ENUM('like', 'dislike'), allowNull: false },
    createdAt: { type: DataTypes.DATE, defaultValue: DataTypes.NOW }
}, { 
    tableName: 'reacciones',
    timestamps: false,
    indexes: [
        { fields: ['publicacion_id', 'usuario_id'], unique: true }
    ]
});

module.exports = Reaccion;
