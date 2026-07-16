const { Servicio } = require('../models');

const crearServicio = async (req, res) => {
    try {
        const { nombre, descripcion, precio, duracion_minutos } = req.body;
        const nuevoServicio = await Servicio.create({ nombre, descripcion, precio, duracion_minutos });
        res.status(201).json({ mensaje: 'Servicio creado ✂️', servicio: nuevoServicio });
    } catch (error) {
        console.error(error);
        res.status(500).json({ error: 'Error al crear servicio' });
    }
};

const obtenerServicios = async (req, res) => {
    try {
        const servicios = await Servicio.findAll();
        res.status(200).json(servicios);
    } catch (error) {
        console.error(error);
        res.status(500).json({ error: 'Error al obtener los servicios' });
    }
};

const actualizarServicio = async (req, res) => {
    try {
        const { id } = req.params;
        const { nombre, descripcion, precio, duracion_minutos } = req.body;

        const servicio = await Servicio.findByPk(id);
        if (!servicio) {
            return res.status(404).json({ error: 'Servicio no encontrado' });
        }

        await servicio.update({ nombre, descripcion, precio, duracion_minutos });
        res.status(200).json({ mensaje: 'Servicio actualizado ✏️', servicio });
    } catch (error) {
        console.error(error);
        res.status(500).json({ error: 'Error al actualizar el servicio' });
    }
};

const eliminarServicio = async (req, res) => {
    try {
        const { id } = req.params;

        const servicio = await Servicio.findByPk(id);
        if (!servicio) {
            return res.status(404).json({ error: 'Servicio no encontrado' });
        }

        await servicio.destroy();
        res.status(200).json({ mensaje: 'Servicio eliminado correctamente 🗑️' });
    } catch (error) {
        console.error(error);
        res.status(500).json({ error: 'Error al eliminar el servicio' });
    }
};

// Exportar funcionalidades para usarlas en las rutas
module.exports = {
    crearServicio,
    obtenerServicios,
    actualizarServicio,
    eliminarServicio
};