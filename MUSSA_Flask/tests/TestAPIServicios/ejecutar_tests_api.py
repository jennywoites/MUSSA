import os
import sys
sys.path.append("../..")

import unittest

#Archivos de test a ejecutar
from tests.TestAPIServicios.TestBuscarCarreras import TestBuscarCarreras
from tests.TestAPIServicios.TestBuscarMaterias import TestBuscarMaterias
from tests.TestAPIServicios.TestObtenerMateria import TestObtenerMateria
from tests.TestAPIServicios.TestObtenerCarrerasDondeSeDictaLaMateria import TestObtenerCarrerasDondeSeDictaLaMateria
from tests.TestAPIServicios.TestObtenerMateriasCorrelativas import TestObtenerMateriasCorrelativas

#Ejecutar todos los tests
unittest.main()