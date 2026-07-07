const { DataTypes } = require('sequelize');
const db = require('../config/db');

const Publicacion = db.define('Publicacion', {
    id: { type: DataTypes.INTEGER, primaryKey: true, autoIncrement: true },
    barbero_id: { type: DataTypes.INTEGER, allowNull: false },
    titulo: { type: DataTypes.STRING(255), allowNull: false },
    descripcion: { type: DataTypes.TEXT, allowNull: true },
    contenido_json: { type: DataTypes.JSON, allowNull: true }, // { "imagenes": [...], "videos": [...] }
    likes_count: { type: DataTypes.INTEGER, defaultValue: 0 },
    dislikes_count: { type: DataTypes.INTEGER, defaultValue: 0 },
    createdAt: { type: DataTypes.DATE, defaultValue: DataTypes.NOW }
}, { 
    tableName: 'publicaciones',
    timestamps: false 
});

module.exports = Publicacion;
