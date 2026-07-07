const express = require('express');
const router = express.Router();
const { crearUsuario, obtenerUsuarios, actualizarUsuario, eliminarUsuario, obtenerUsuarioPorId } = require('../controllers/usuarios.controller');
const { verificarToken, verificarRol } = require('../middlewares/auth.middleware'); // Importamos los guardias

router.get('/', obtenerUsuarios);
router.get('/:id', obtenerUsuarioPorId);

// Rutas protegidas solo para Administradores
router.post('/', verificarToken, verificarRol(['ADM']), crearUsuario);
router.put('/:id', verificarToken, verificarRol(['ADM']), actualizarUsuario);
router.delete('/:id', verificarToken, verificarRol(['ADM']), eliminarUsuario);

module.exports = router;