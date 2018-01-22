HTTP = "http://"
IP = "localhost:"
PUERTO = "5000"
BASE_API = "/api/"
ADMIN = "admin/"

BASE_URL = HTTP + IP + PUERTO + BASE_API

# Requiere estar logueado
AGREGAR_CARRERA_ALUMNO_SERVICE = BASE_URL + "AgregarCarreraAlumno"
ELIMINAR_CARRERA_ALUMNO_SERVICE = BASE_URL + "EliminarCarreraAlumno"
AGREGAR_MATERIA_ALUMNO_SERVICE = BASE_URL + "AgregarMateriaAlumno"
ELIMINAR_MATERIA_ALUMNO_SERVICE = BASE_URL + "EliminarMateriaAlumno"
OBTENER_ENCUESTAS_ALUMNO_SERVICE = BASE_URL + "ObtenerEncuestasAlumno"
GUARDAR_RESPUESTAS_ENCUESTA_ALUMNO_SERVICE = BASE_URL + "GuardarRespuestasEncuestaAlumno"
ENCUESTA_ALUMNO_ESTA_COMPLETA_SERVICE = BASE_URL + 'EncuestaAlumnoEstaCompleta'
FINALIZAR_ENCUESTA_ALUMNO_SERVICE = BASE_URL + 'FinalizarEncuestaAlumno'
OBTENER_RESPUESTAS_ALUMNO_PARA_PREGUNTAS_ESPECIFICAS_SERVICE = (BASE_URL +
                                                                "ObtenerRespuestasEncuestaAlumnoParaPreguntasEspecificas")

# Requiere ser administrador
GUARDAR_HORARIOS_DESDE_ARCHIVO_PDF_SERVICE = BASE_URL + ADMIN + "GuardarHorariosDesdeArchivoPDF"
