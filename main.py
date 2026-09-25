import threading
import time

from src.schemas.passageiros import Passageiro
from src.Controllers.poolMotoristas import PoolMotoristas
from src.Controllers.despachante import Despachante


pool = PoolMotoristas(50)
despachante = Despachante(pool)


def executar_corrida(passageiro):

    if despachante.solicitar_corrida(passageiro):

        try:
            time.sleep(2)

        finally:
            despachante.finalizar_corrida(passageiro)

passageiros = [
    Passageiro(i,f"Passageiro {i}")
    for i in range(1, 501)
]

threads = []

for passageiro in passageiros:

    thread = threading.Thread(
        target=executar_corrida,
        args=(passageiro,)
    )

    threads.append(thread)
    thread.start()


for thread in threads:
    thread.join()

print("Simulação finalizada!")