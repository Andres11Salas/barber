const { Cita, Usuario, Servicio } = require('../models');

// 1. FUNCIÓN PARA CREAR UNA CITA
const crearCita = async (req, res) => {
    try {
        const { cliente_id, barbero_id, servicio_id, fecha, hora } = req.body;
        
        const nuevaCita = await Cita.create({
            cliente_id,
            barbero_id,
            servicio_id,
            fecha,
            hora
        });

        res.status(201).json({ mensaje: 'Cita creada con éxito', cita: nuevaCita });
    } catch (error) {
        console.error(error);
        res.status(500).json({ error: 'Error al agendar la cita' });
    }
};

// 2. FUNCIÓN PARA OBTENER TODAS LAS CITAS (Con nombres de clientes y barberos)
const obtenerCitas = async (req, res) => {
    try {
        const citas = await Cita.findAll({
            include: [
                { model: Usuario, as: 'cliente', attributes: ['id', 'nombre', 'email'] },
                { model: Usuario, as: 'barbero', attributes: ['id', 'nombre', 'email'] },
                { model: Servicio, as: 'servicio', attributes: ['id', 'nombre', 'precio'] }
            ]
        });
        res.status(200).json(citas);
    } catch (error) {
        console.error(error);
        res.status(500).json({ error: 'Error al obtener las citas' });
    }
};

// 3. FUNCIÓN PARA CANCELAR CITA (Regla de 6 horas)
const cancelarCitaCliente = async (req, res) => {
    try {
        const { id } = req.params;
        const cita = await Cita.findByPk(id);

        if (!cita) return res.status(404).json({ error: 'Cita no encontrada.' });
        
        // Seguridad: Verificar que la cita le pertenece al usuario que la intenta borrar
        if (cita.cliente_id !== req.usuario.id) {
            return res.status(403).json({ error: 'No tienes permiso para cancelar esta cita.' });
        }

        // Lógica de las 6 horas
        const fechaCita = new Date(`${cita.fecha}T${cita.hora}`);
        const ahora = new Date();
        
        const horasDiferencia = (fechaCita - ahora) / (1000 * 60 * 60);

        if (horasDiferencia < 6) {
            return res.status(400).json({ 
                error: 'Debes cancelar con al menos 6 horas de anticipación. Por favor, comunícate con la barbería.' 
            });
        }

        await cita.destroy();
        res.status(200).json({ mensaje: 'Tu cita ha sido cancelada exitosamente.' });
    } catch (error) {
        console.error(error);
        res.status(500).json({ error: 'Error al cancelar la cita.' });
    }
};

// EXPORTAMOS TODO AL FINAL
module.exports = {
    crearCita,
    obtenerCitas,
    cancelarCitaCliente
};