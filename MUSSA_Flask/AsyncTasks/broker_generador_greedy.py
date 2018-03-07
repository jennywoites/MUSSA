from celery import  Celery
from time import  sleep

broker_generador_greedy = Celery('broker', broker='redis://localhost')
broker_generador_greedy.conf.update({
    'task_reject_on_worker_lost': True,
    'task_acks_late': True,
})
#broker_generador_greedy.conf.broker_transport_options = {'visibility_timeout': 40}


@broker_generador_greedy.task(acks_late=True)
def generar_plan_greedy(parametros):
    print("Estoy generando un plan con %s" % parametros)
    sleep(30)
    print("Termine de generar el plan %s"  % parametros)