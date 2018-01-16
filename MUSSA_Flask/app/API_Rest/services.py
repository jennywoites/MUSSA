HTTP = "http://"
IP = "localhost:"
PUERTO = "5000"
BASE_API = "/api/"
ADMIN = "admin/"

BASE_URL = HTTP + IP + PUERTO + BASE_API

# No requiere autenticacion
BUSCAR_MATERIAS_SERVICE = BASE_URL + "BuscarMaterias"
OBTENER_MATERIAS_CORRELATIVAS_SERVICE = BASE_URL + "ObtenerMateriasCorrelativas"
BUSCAR_CURSOS_SERVICE = BASE_URL + "BuscarCursos"
OBTENER_PREGUNTAS_ENCUESTA_SERVICE = BASE_URL + "ObtenerPreguntasEncuesta"
OBTENER_DOCENTES_CURSO_SERVICE = BASE_URL + "ObtenerDocentesCurso"
OBTENER_TEMATICAS_MATERIAS = BASE_URL + "ObtenerTematicasMaterias"

# Requiere estar logueado
OBTENER_PADRON_ALUMNO_SERVICE = BASE_URL + "ObtenerPadronAlumno"
MODIFICAR_PADRON_ALUMNO_SERVICE = BASE_URL + "ModificarPadronAlumno"
AGREGAR_CARRERA_ALUMNO_SERVICE = BASE_URL + "AgregarCarreraAlumno"
OBTENER_CARRERAS_ALUMNO_SERVICE = BASE_URL + "ObtenerCarrerasAlumno"
ELIMINAR_CARRERA_ALUMNO_SERVICE = BASE_URL + "EliminarCarreraAlumno"
OBTENER_MATERIAS_ALUMNO_SERVICE = BASE_URL + "ObtenerMateriasAlumno"
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
MODIFICAR_CURSO_SERVICE = BASE_URL + ADMIN + "ModificarCurso"
