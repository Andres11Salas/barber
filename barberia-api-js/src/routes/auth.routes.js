const express = require('express');
const router = express.Router();
const { login, registrarCliente, recuperarPassword } = require('../controllers/auth.controller');

// Estas rutas son PÚBLICAS (No necesitan el middleware verificarToken)
router.post('/login', login);
router.post('/registro', registrarCliente);
router.post('/recuperar', recuperarPassword);

module.exports = router;