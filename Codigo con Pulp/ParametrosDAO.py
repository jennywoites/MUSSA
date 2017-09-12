from MateriasDAO import get_materias, get_plan_carrera
from HorariosDAO import get_horarios, get_horarios_no_permitidos

CREDITOS_MINIMOS_ELECTIVAS = 0#5
NUM_EJEMPLO_MATERIAS = 5

class Parametros:

	def __init__(self):
		self.plan = get_plan_carrera(NUM_EJEMPLO_MATERIAS)
		self.materias = get_materias(NUM_EJEMPLO_MATERIAS)
		self.horarios = get_horarios(NUM_EJEMPLO_MATERIAS)
		self.horarios_no_permitidos = get_horarios_no_permitidos(NUM_EJEMPLO_MATERIAS)
		self.creditos_minimos_electivas = CREDITOS_MINIMOS_ELECTIVAS