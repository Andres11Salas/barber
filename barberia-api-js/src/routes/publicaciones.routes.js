const express = require('express');
const router = express.Router();
const publicacionesCtrl = require('../controllers/publicaciones.controller');

// GET todas las publicaciones
router.get('/', publicacionesCtrl.obtenerPublicaciones);

// GET publicaciones de un barbero específico
router.get('/barbero/:barbero_id', publicacionesCtrl.obtenerPublicacionesBarbero);

// POST crear publicación
router.post('/', publicacionesCtrl.crearPublicacion);

// PUT actualizar publicación
router.put('/:id', publicacionesCtrl.actualizarPublicacion);

// DELETE publicación
router.delete('/:id', publicacionesCtrl.eliminarPublicacion);

// POST agregar reacción (like/dislike)
router.post('/:publicacion_id/reacciones', publicacionesCtrl.agregarReaccion);

// POST agregar comentario
router.post('/:publicacion_id/comentarios', publicacionesCtrl.agregarComentario);

// DELETE comentario
router.delete('/comentarios/:comentario_id', publicacionesCtrl.eliminarComentario);

module.exports = router;
