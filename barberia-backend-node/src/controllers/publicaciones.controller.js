const { Publicacion, Comentario, Reaccion, Usuario } = require('../models');

// GET todas las publicaciones (con barbero y reacciones/comentarios)
exports.obtenerPublicaciones = async (req, res) => {
    try {
        const publicaciones = await Publicacion.findAll({
            include: [
                { model: Usuario, as: 'barbero', attributes: ['id', 'nombre', 'email'] },
                { model: Comentario, as: 'comentarios', include: [{ model: Usuario, as: 'usuario', attributes: ['id', 'nombre'] }] },
                { model: Reaccion, as: 'reacciones', attributes: ['id', 'usuario_id', 'tipo'] }
            ],
            order: [['createdAt', 'DESC']]
        });
        res.json(publicaciones);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
};

// GET publicaciones de un barbero específico
exports.obtenerPublicacionesBarbero = async (req, res) => {
    try {
        const { barbero_id } = req.params;
        const publicaciones = await Publicacion.findAll({
            where: { barbero_id },
            include: [
                { model: Usuario, as: 'barbero', attributes: ['id', 'nombre', 'email'] },
                { model: Comentario, as: 'comentarios', include: [{ model: Usuario, as: 'usuario', attributes: ['id', 'nombre'] }] },
                { model: Reaccion, as: 'reacciones', attributes: ['id', 'usuario_id', 'tipo'] }
            ],
            order: [['createdAt', 'DESC']]
        });
        res.json(publicaciones);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
};

// POST crear publicación (solo barberos y admins)
exports.crearPublicacion = async (req, res) => {
    try {
        const { titulo, descripcion, contenido_json } = req.body;
        const token = req.headers.authorization?.split(' ')[1];
        if (!token) return res.status(401).json({ error: 'Token requerido' });

        const payload = JSON.parse(Buffer.from(token.split('.')[1], 'base64').toString());
        const barbero_id = payload.id;
        const rol = payload.rol;

        if (rol !== 'BARBERO' && rol !== 'ADM') {
            return res.status(403).json({ error: 'Solo barberos pueden crear publicaciones' });
        }

        if (!titulo) return res.status(400).json({ error: 'El título es obligatorio' });

        const pub = await Publicacion.create({
            barbero_id,
            titulo,
            descripcion: descripcion || '',
            contenido_json: contenido_json || {}
        });

        res.json({ mensaje: 'Publicación creada', publicacion: pub });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
};

// PUT actualizar publicación
exports.actualizarPublicacion = async (req, res) => {
    try {
        const { id } = req.params;
        const { titulo, descripcion, contenido_json } = req.body;
        const token = req.headers.authorization?.split(' ')[1];
        if (!token) return res.status(401).json({ error: 'Token requerido' });

        const payload = JSON.parse(Buffer.from(token.split('.')[1], 'base64').toString());
        const usuario_id = payload.id;

        const pub = await Publicacion.findByPk(id);
        if (!pub) return res.status(404).json({ error: 'Publicación no encontrada' });

        if (pub.barbero_id !== usuario_id) {
            return res.status(403).json({ error: 'No puedes editar esta publicación' });
        }

        pub.titulo = titulo || pub.titulo;
        pub.descripcion = descripcion !== undefined ? descripcion : pub.descripcion;
        pub.contenido_json = contenido_json || pub.contenido_json;
        await pub.save();

        res.json({ mensaje: 'Publicación actualizada', publicacion: pub });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
};

// DELETE publicación
exports.eliminarPublicacion = async (req, res) => {
    try {
        const { id } = req.params;
        const token = req.headers.authorization?.split(' ')[1];
        if (!token) return res.status(401).json({ error: 'Token requerido' });

        const payload = JSON.parse(Buffer.from(token.split('.')[1], 'base64').toString());
        const usuario_id = payload.id;

        const pub = await Publicacion.findByPk(id);
        if (!pub) return res.status(404).json({ error: 'Publicación no encontrada' });

        if (pub.barbero_id !== usuario_id) {
            return res.status(403).json({ error: 'No puedes eliminar esta publicación' });
        }

        // Eliminar comentarios y reacciones asociadas
        await Comentario.destroy({ where: { publicacion_id: id } });
        await Reaccion.destroy({ where: { publicacion_id: id } });
        await pub.destroy();

        res.json({ mensaje: 'Publicación eliminada' });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
};

// POST agregar reacción (like/dislike)
exports.agregarReaccion = async (req, res) => {
    try {
        const { publicacion_id } = req.params;
        const { tipo } = req.body; // 'like' o 'dislike'
        const token = req.headers.authorization?.split(' ')[1];
        if (!token) return res.status(401).json({ error: 'Token requerido' });

        const payload = JSON.parse(Buffer.from(token.split('.')[1], 'base64').toString());
        const usuario_id = payload.id;

        if (!['like', 'dislike'].includes(tipo)) {
            return res.status(400).json({ error: 'Tipo de reacción inválido' });
        }

        // Buscar si ya existe reacción del usuario
        let reaccion = await Reaccion.findOne({ where: { publicacion_id, usuario_id } });

        if (reaccion) {
            // Si existe y es la misma, eliminar
            if (reaccion.tipo === tipo) {
                await reaccion.destroy();
                return res.json({ mensaje: 'Reacción removida' });
            }
            // Si existe pero es diferente, actualizar
            reaccion.tipo = tipo;
            await reaccion.save();
        } else {
            // Crear nueva reacción
            reaccion = await Reaccion.create({ publicacion_id, usuario_id, tipo });
        }

        // Actualizar contadores en la publicación
        const pub = await Publicacion.findByPk(publicacion_id);
        const likes = await Reaccion.count({ where: { publicacion_id, tipo: 'like' } });
        const dislikes = await Reaccion.count({ where: { publicacion_id, tipo: 'dislike' } });
        pub.likes_count = likes;
        pub.dislikes_count = dislikes;
        await pub.save();

        res.json({ mensaje: 'Reacción registrada', reaccion });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
};

// POST agregar comentario
exports.agregarComentario = async (req, res) => {
    try {
        const { publicacion_id } = req.params;
        const { texto } = req.body;
        const token = req.headers.authorization?.split(' ')[1];
        if (!token) return res.status(401).json({ error: 'Token requerido' });

        const payload = JSON.parse(Buffer.from(token.split('.')[1], 'base64').toString());
        const usuario_id = payload.id;

        if (!texto || !texto.trim()) {
            return res.status(400).json({ error: 'El comentario no puede estar vacío' });
        }

        const comentario = await Comentario.create({
            publicacion_id,
            usuario_id,
            texto: texto.trim()
        });

        const comentarioConDatos = await Comentario.findByPk(comentario.id, {
            include: [{ model: Usuario, as: 'usuario', attributes: ['id', 'nombre'] }]
        });

        res.json({ mensaje: 'Comentario agregado', comentario: comentarioConDatos });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
};

// DELETE comentario
exports.eliminarComentario = async (req, res) => {
    try {
        const { comentario_id } = req.params;
        const token = req.headers.authorization?.split(' ')[1];
        if (!token) return res.status(401).json({ error: 'Token requerido' });

        const payload = JSON.parse(Buffer.from(token.split('.')[1], 'base64').toString());
        const usuario_id = payload.id;

        const comentario = await Comentario.findByPk(comentario_id);
        if (!comentario) return res.status(404).json({ error: 'Comentario no encontrado' });

        if (comentario.usuario_id !== usuario_id) {
            return res.status(403).json({ error: 'No puedes eliminar este comentario' });
        }

        await comentario.destroy();
        res.json({ mensaje: 'Comentario eliminado' });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
};
