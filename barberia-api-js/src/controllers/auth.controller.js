const { Usuario } = require('../models');
const jwt = require('jsonwebtoken');

// 1. Iniciar Sesión (La que ya tenías)
const login = async (req, res) => {
    try {
        const { email, password } = req.body;
        const usuario = await Usuario.findOne({ where: { email } });
        
        if (!usuario) return res.status(404).json({ error: 'Usuario no encontrado' });
        if (usuario.password !== password) return res.status(401).json({ error: 'Contraseña incorrecta' });

        const token = jwt.sign(
            { id: usuario.id, rol: usuario.rol }, 
            process.env.JWT_SECRET || 'mi_palabra_secreta_super_segura', 
            { expiresIn: '2h' }
        );

        res.status(200).json({ mensaje: `Bienvenido ${usuario.nombre}`, token, rol: usuario.rol });
    } catch (error) {
        res.status(500).json({ error: 'Error en el servidor' });
    }
};

// 2. NUEVA: Registro de Clientes
const registrarCliente = async (req, res) => {
    try {
        const { nombre, email, password } = req.body;
        
        // Verificamos que el correo no exista ya
        const existe = await Usuario.findOne({ where: { email } });
        if (existe) {
            return res.status(400).json({ error: 'Este correo ya está registrado.' });
        }

        // Creamos el usuario forzando el rol 'CLIENTE' para que nadie pueda hackear y crearse un 'ADM'
        const nuevoCliente = await Usuario.create({
            nombre,
            email,
            password,
            rol: 'CLIENTE'
        });

        res.status(201).json({ mensaje: '¡Cuenta creada con éxito! Ya puedes iniciar sesión.' });
    } catch (error) {
        console.error(error);
        res.status(500).json({ error: 'Error al registrar la cuenta.' });
    }
};

// 3. NUEVA: Recuperación de Contraseña (Versión Simulada)
const recuperarPassword = async (req, res) => {
    try {
        const { email } = req.body;
        const usuario = await Usuario.findOne({ where: { email } });
        
        if (!usuario) {
            return res.status(404).json({ error: 'No existe una cuenta con este correo.' });
        }

        /* 
         En un entorno real (producción), aquí usaríamos la librería "nodemailer" 
         para enviar un email con un link único. Para mantenerlo funcional hoy, 
         generaremos una contraseña temporal y la devolveremos en pantalla.
        */
        const passwordTemporal = Math.random().toString(36).slice(-8); // Genera algo como "a7b3c9d1"
        
        await usuario.update({ password: passwordTemporal });

        res.status(200).json({ 
            mensaje: 'Se ha restablecido tu acceso.',
            instruccion: `Tu contraseña temporal es: ${passwordTemporal}. Inicia sesión y cámbiala.` 
        });

    } catch (error) {
        console.error(error);
        res.status(500).json({ error: 'Error al procesar la recuperación.' });
    }
};

module.exports = { login, registrarCliente, recuperarPassword };