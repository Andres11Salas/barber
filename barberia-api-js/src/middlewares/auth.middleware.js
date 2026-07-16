const jwt = require('jsonwebtoken');

// Guardia 1: Verifica que el usuario tenga un Token válido
const verificarToken = (req, res, next) => {
    // El frontend nos enviará el token en los "Headers" de la petición
    const token = req.header('Authorization');

    if (!token) {
        return res.status(401).json({ error: 'Acceso denegado. No hay token.' });
    }

    try {
        // Le quitamos la palabra "Bearer " que suele venir pegada al token
        const tokenLimpio = token.replace('Bearer ', '');

        // Desciframos el carnet usando la misma palabra secreta del login
        const decodificado = jwt.verify(tokenLimpio, process.env.JWT_SECRET || 'mi_palabra_secreta_super_segura');

        // Guardamos los datos del usuario en la petición (req) para usarlos después
        req.usuario = decodificado;

        next(); // ¡Todo en orden! Pasa al siguiente paso
    } catch (error) {
        res.status(401).json({ error: 'Token no válido o expirado' });
    }
};

// Guardia 2: Verifica que el usuario tenga el Rol necesario
const verificarRol = (rolesPermitidos) => {
    return (req, res, next) => {
        // req.usuario.rol viene del Guardia 1
        if (!req.usuario || !rolesPermitidos.includes(req.usuario.rol)) {
            return res.status(403).json({
                error: `Acceso denegado. Requiere uno de estos roles: ${rolesPermitidos.join(', ')}` 
            });
        }
        next(); // Tiene el rol correcto, ¡déjalo pasar!
    };
};

module.exports = { verificarToken, verificarRol };