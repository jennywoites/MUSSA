import os
import sys
sys.path.append("../..")

import unittest

#Archivos de test a ejecutar
from tests.TestAPIServicios.TestBuscarCarreras import TestBuscarCarreras
from tests.TestAPIServicios.TestBuscarMaterias import TestBuscarMaterias

#Ejecutar todos los tests
unittest.main()