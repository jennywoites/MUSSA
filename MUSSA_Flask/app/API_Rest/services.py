HTTP = "http://"
IP = "localhost:"
PUERTO = "5000"
BASE_API = "/api/"
ADMIN = "admin/"

BASE_URL = HTTP + IP + PUERTO + BASE_API

#No requiere autenticacion
BUSCAR_CARRERAS_SERVICE = BASE_URL + "BuscarCarreras"
BUSCAR_MATERIAS_SERVICE = BASE_URL + "BuscarMaterias"
OBTENER_MATERIA_SERVICE = BASE_URL + "ObtenerMateria"
OBTENER_MATERIAS_CORRELATIVAS_SERVICE = BASE_URL + "ObtenerMateriasCorrelativas"
OBTENER_CARRERAS_DONDE_SE_DICTA_LA_MATERIA_SERVICE = BASE_URL + "ObtenerCarrerasDondeSeDictaLaMateria"
BUSCAR_CURSOS_SERVICE = BASE_URL + "BuscarCursos"

#Requiere estar logueado
OBTENER_PADRON_ALUMNO = BASE_URL + "ObtenerPadronAlumno"
MODIFICAR_PADRON_ALUMNO = BASE_URL + "ModificarPadronAlumno"
AGREGAR_CARRERA_ALUMNO = BASE_URL + "AgregarCarreraAlumno"
OBTENER_CARRERAS_ALUMNO = BASE_URL + "ObtenerCarrerasAlumno"
ELIMINAR_CARRERA_ALUMNO = BASE_URL + "EliminarCarreraAlumno"

#Requiere ser administrador
GUARDAR_HORARIOS_DESDE_ARCHIVO_PDF_SERVICE = BASE_URL + ADMIN + "GuardarHorariosDesdeArchivoPDF"
MODIFICAR_CURSO = BASE_URL + ADMIN + "ModificarCurso"