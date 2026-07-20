// src/models/index.js
const Usuario = require('./Usuario');
const Servicio = require('./Servicio');
const Cita = require('./Cita');
const Publicacion = require('./Publicacion');
const Comentario = require('./Comentario');
const Reaccion = require('./Reaccion');

// Relación 1: Una Cita pertenece a un Cliente (Usuario)
Cita.belongsTo(Usuario, { as: 'cliente', foreignKey: 'cliente_id' });
Usuario.hasMany(Cita, { foreignKey: 'cliente_id' });

// Relación 2: Una Cita es atendida por un Barbero (Usuario)
// Reutilizamos la tabla Usuario, pero con otro rol conceptual
Cita.belongsTo(Usuario, { as: 'barbero', foreignKey: 'barbero_id' });
Usuario.hasMany(Cita, { foreignKey: 'barbero_id' });

// Relación 3: Una Cita incluye un Servicio
Cita.belongsTo(Servicio, { as: 'servicio', foreignKey: 'servicio_id' });
Servicio.hasMany(Cita, { foreignKey: 'servicio_id' });

// Relación 4: Una Publicación pertenece a un Barbero
Publicacion.belongsTo(Usuario, { as: 'barbero', foreignKey: 'barbero_id' });
Usuario.hasMany(Publicacion, { as: 'publicaciones', foreignKey: 'barbero_id' });

// Relación 5: Un Comentario pertenece a una Publicación
Comentario.belongsTo(Publicacion, { as: 'publicacion', foreignKey: 'publicacion_id' });
Publicacion.hasMany(Comentario, { as: 'comentarios', foreignKey: 'publicacion_id' });

// Relación 6: Un Comentario lo realiza un Usuario
Comentario.belongsTo(Usuario, { as: 'usuario', foreignKey: 'usuario_id' });
Usuario.hasMany(Comentario, { as: 'comentarios_realizados', foreignKey: 'usuario_id' });

// Relación 7: Una Reacción pertenece a una Publicación
Reaccion.belongsTo(Publicacion, { as: 'publicacion', foreignKey: 'publicacion_id' });
Publicacion.hasMany(Reaccion, { as: 'reacciones', foreignKey: 'publicacion_id' });

// Relación 8: Una Reacción la realiza un Usuario
Reaccion.belongsTo(Usuario, { as: 'usuario', foreignKey: 'usuario_id' });
Usuario.hasMany(Reaccion, { as: 'reacciones_realizadas', foreignKey: 'usuario_id' });

// Exportamos todos los modelos ya relacionados
module.exports = {
    Usuario,
    Servicio,
    Cita,
    Publicacion,
    Comentario,
    Reaccion
};