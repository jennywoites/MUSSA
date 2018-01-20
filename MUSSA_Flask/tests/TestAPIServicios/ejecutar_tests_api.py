import sys
import unittest

sys.path.append("../..")

# Archivos de test a ejecutar

from tests.TestAPIServicios.TestCarreraServices.TestBuscarCarreras import TestBuscarCarreras
from tests.TestAPIServicios.TestCarreraServices.TestObtenerCarrerasDondeSeDictaLaMateria import \
    TestObtenerCarrerasDondeSeDictaLaMateria

from tests.TestAPIServicios.TestCursoServices.TestBuscarCursos import TestBuscarCursos
from tests.TestAPIServicios.TestCursoServices.TestObtenerDocentesCurso import TestObtenerDocentesCurso
from tests.TestAPIServicios.TestCursoServices.TestModificarCurso import TestModificarCurso

from tests.TestAPIServicios.TestDocenteServices.TestObtenerDocentes import TestObtenerDocentes

from tests.TestAPIServicios.TestMateriaServices.TestBuscarMaterias import TestBuscarMaterias
from tests.TestAPIServicios.TestMateriaServices.TestObtenerMateria import TestObtenerMateria
from tests.TestAPIServicios.TestMateriaServices.TestObtenerMateriasCorrelativas import TestObtenerMateriasCorrelativas

from tests.TestAPIServicios.TestTematicaServices.TestObtenerTematicasMaterias import TestObtenerTematicasMaterias

from tests.TestAPIServicios.TestEncuestaServices.TestObtenerPreguntasEncuesta import TestObtenerPreguntasEncuesta

#################################################
from tests.TestAPIServicios.TestAgregarMateriaAlumno import TestAgregarMateriaAlumno
from tests.TestAPIServicios.TestGuardarRespuestasEncuestaAlumno import TestGuardarRespuestasEncuestaAlumno
from tests.TestAPIServicios.TestModificarPadronAlumno import TestModificarPadronAlumno
from tests.TestAPIServicios.TestObtenerEncuestasAlumno import TestObtenerEncuestasAlumno
from tests.TestAPIServicios.TestObtenerMateriasAlumno import TestObtenerMateriasAlumno
from tests.TestAPIServicios.TestObtenerPadronAlumno import TestObtenerPadronAlumno
from tests.TestAPIServicios.TestObtenerRespuestasEncuestaAlumnoParaPreguntasEspecificas import \
    TestObtenerRespuestasEncuestaAlumnoParaPreguntasEspecificas

# Ejecutar todos los tests
unittest.main()
