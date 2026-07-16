const { Usuario } = require('../models');

// Función que ya tenías (POST)
const crearUsuario = async (req, res) => {
    try {
        const { nombre, email, password, rol } = req.body;
        const nuevoUsuario = await Usuario.create({ nombre, email, password, rol });
        res.status(201).json({ mensaje: 'Usuario creado', usuario: nuevoUsuario });
    } catch (error) {
        console.error(error);
        res.status(500).json({ error: 'Error al crear usuario' });
    }
};

// NUEVA Función (GET)
const obtenerUsuarios = async (req, res) => {
    try {
        // .findAll() es el equivalente de Sequelize a hacer un "SELECT * FROM usuarios"
        const usuarios = await Usuario.findAll();
        
        // Respondemos con código 200 (OK) y la lista de usuarios
        res.status(200).json(usuarios);
    } catch (error) {
        console.error(error);
        res.status(500).json({ error: 'Error al obtener los usuarios' });
    }
};

// NUEVA: Función para Actualizar (PUT)
const actualizarUsuario = async (req, res) => {
    try {
        const { id } = req.params; // Obtenemos el ID de la URL
        const { nombre, email, password, rol } = req.body; // Obtenemos los nuevos datos

        // Buscamos al usuario por su ID (Primary Key)
        const usuario = await Usuario.findByPk(id);
        
        if (!usuario) {
            return res.status(404).json({ error: 'Usuario no encontrado' });
        }

        // Actualizamos los datos
        await usuario.update({ nombre, email, password, rol });
        
        res.status(200).json({ mensaje: 'Usuario actualizado ✍️', usuario });
    } catch (error) {
        console.error(error);
        res.status(500).json({ error: 'Error al actualizar el usuario' });
    }
};

// NUEVA: Función para Eliminar (DELETE)
const eliminarUsuario = async (req, res) => {
    try {
        const { id } = req.params;

        const usuario = await Usuario.findByPk(id);
        
        if (!usuario) {
            return res.status(404).json({ error: 'Usuario no encontrado' });
        }

        // Eliminamos el registro de la base de datos
        await usuario.destroy();
        
        res.status(200).json({ mensaje: 'Usuario eliminado correctamente 🗑️' });
    } catch (error) {
        console.error(error);
        res.status(500).json({ error: 'Error al eliminar el usuario' });
    }
};

const obtenerUsuarioPorId = async (req, res) => {
    try {
        const { id } = req.params;
        const usuario = await Usuario.findByPk(id, {
            attributes: ['id', 'nombre', 'email', 'rol'] // Excluimos el password por seguridad
        });
        
        if (!usuario) return res.status(404).json({ error: 'Usuario no encontrado' });
        res.status(200).json(usuario);
    } catch (error) {
        res.status(500).json({ error: 'Error al obtener el perfil' });
    }
};

// No olvides exportarlas:
module.exports = {
    crearUsuario,
    obtenerUsuarios,
    obtenerUsuarioPorId,
    actualizarUsuario,
    eliminarUsuario
};