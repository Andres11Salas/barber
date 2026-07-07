const express = require('express');
const router = express.Router();
const { crearServicio, obtenerServicios, actualizarServicio, eliminarServicio } = require('../controllers/servicios.controller');

// Importamos a nuestros guardias de seguridad
const { verificarToken, verificarRol } = require('../middlewares/auth.middleware');

// El GET está libre, cualquiera puede ver el catálogo
router.get('/', obtenerServicios);

// Las rutas que modifican la base de datos ahora están protegidas
// Primero pasan por verificarToken, luego por verificarRol, y si todo sale bien, ejecutan el controlador
router.post('/', verificarToken, verificarRol(['ADM']), crearServicio);
router.put('/:id', verificarToken, verificarRol(['ADM']), actualizarServicio);
router.delete('/:id', verificarToken, verificarRol(['ADM']), eliminarServicio);

module.exports = router;