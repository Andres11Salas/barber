const express = require('express');
const router = express.Router();

// 1. IMPORTAMOS LOS CONTROLADORES (Deben coincidir con los nombres del module.exports)
const { 
    crearCita, 
    obtenerCitas, 
    cancelarCitaCliente 
} = require('../controllers/citas.controller');

// 2. IMPORTAMOS LOS GUARDIAS DE SEGURIDAD
const { verificarToken, verificarRol } = require('../middlewares/auth.middleware');

// 3. DEFINIMOS LAS RUTAS
router.get('/', obtenerCitas);
router.post('/', crearCita); // ¡Aquí es donde Node.js se estaba quejando!
router.delete('/cliente/:id', verificarToken, verificarRol(['CLIENTE']), cancelarCitaCliente);

module.exports = router;