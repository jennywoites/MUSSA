import sys
import unittest

sys.path.append("../..")

# Archivos de test a ejecutar

# - servicios generales -
from tests.TestAPIServicios.TestBuscarCarreras import TestBuscarCarreras
from tests.TestAPIServicios.TestBuscarMaterias import TestBuscarMaterias
from tests.TestAPIServicios.TestObtenerMateria import TestObtenerMateria
from tests.TestAPIServicios.TestObtenerCarrerasDondeSeDictaLaMateria import TestObtenerCarrerasDondeSeDictaLaMateria
from tests.TestAPIServicios.TestObtenerMateriasCorrelativas import TestObtenerMateriasCorrelativas
from tests.TestAPIServicios.TestBuscarCursos import TestBuscarCursos
from tests.TestAPIServicios.TestObtenerDocentesCurso import TestObtenerDocentesCurso
from tests.TestAPIServicios.TestObtenerDocentes import TestObtenerDocentes

# - servicios de miembros -
from tests.TestAPIServicios.TestAgregarMateriaAlumno import TestAgregarMateriaAlumno
from tests.TestAPIServicios.TestObtenerPadronAlumno import TestObtenerPadronAlumno
from tests.TestAPIServicios.TestModificarPadronAlumno import TestModificarPadronAlumno
from tests.TestAPIServicios.TestObtenerMateriasAlumno import TestObtenerMateriasAlumno
from tests.TestAPIServicios.TestObtenerEncuestasAlumno import TestObtenerEncuestasAlumno

# - servicios de administradores -
from tests.TestAPIServicios.TestModificarCurso import TestModificarCurso

# Ejecutar todos los tests
unittest.main()
