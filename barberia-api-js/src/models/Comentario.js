const { DataTypes } = require('sequelize');
const db = require('../config/db');

const Comentario = db.define('Comentario', {
    id: { type: DataTypes.INTEGER, primaryKey: true, autoIncrement: true },
    publicacion_id: { type: DataTypes.INTEGER, allowNull: false },
    usuario_id: { type: DataTypes.INTEGER, allowNull: false },
    texto: { type: DataTypes.TEXT, allowNull: false },
    createdAt: { type: DataTypes.DATE, defaultValue: DataTypes.NOW }
}, { 
    tableName: 'comentarios',
    timestamps: false 
});

module.exports = Comentario;
