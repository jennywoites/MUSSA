import os
import sys
sys.path.append("../..")

import unittest

#Archivos de test a ejecutar

# - servicios generales -
from tests.TestAPIServicios.TestBuscarCarreras import TestBuscarCarreras
from tests.TestAPIServicios.TestBuscarMaterias import TestBuscarMaterias
from tests.TestAPIServicios.TestObtenerMateria import TestObtenerMateria
from tests.TestAPIServicios.TestObtenerCarrerasDondeSeDictaLaMateria import TestObtenerCarrerasDondeSeDictaLaMateria
from tests.TestAPIServicios.TestObtenerMateriasCorrelativas import TestObtenerMateriasCorrelativas
from tests.TestAPIServicios.TestBuscarCursos import TestBuscarCursos

# - servicios de miembros -
#from tests.TestAPIServicios.TestAgregarMateriaAlumno import TestAgregarMateriaAlumno

# - servicios de administradores -
#from tests.TestAPIServicios.TestModificarCurso import TestModificarCurso


#Ejecutar todos los tests
unittest.main()