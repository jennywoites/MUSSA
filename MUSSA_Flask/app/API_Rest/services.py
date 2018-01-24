HTTP = "http://"
IP = "localhost:"
PUERTO = "5000"
BASE_API = "/api/"
ADMIN = "admin/"

BASE_URL = HTTP + IP + PUERTO + BASE_API

# Requiere estar logueado
AGREGAR_MATERIA_ALUMNO_SERVICE = BASE_URL + "AgregarMateriaAlumno"
ELIMINAR_MATERIA_ALUMNO_SERVICE = BASE_URL + "EliminarMateriaAlumno"
GUARDAR_RESPUESTAS_ENCUESTA_ALUMNO_SERVICE = BASE_URL + "GuardarRespuestasEncuestaAlumno"

# Requiere ser administrador
GUARDAR_HORARIOS_DESDE_ARCHIVO_PDF_SERVICE = BASE_URL + ADMIN + "GuardarHorariosDesdeArchivoPDF"
