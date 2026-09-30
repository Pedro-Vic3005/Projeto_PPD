import threading
import time

from src.schemas.passageiros import Passageiro
from src.Controllers.poolMotoristas import PoolMotoristas
from src.Controllers.despachante import Despachante


pool = PoolMotoristas(50)
despachante = Despachante(pool)


def executar_corrida(passageiro):
    despachante._registrar_log(f"[SIMULAÇÃO] Passageiro {passageiro.id} iniciou a solicitação de corrida.")

    if despachante.solicitar_corrida(passageiro):
        try:
            time.sleep(2)
        finally:
            despachante.finalizar_corrida(passageiro)
    else:
        despachante._registrar_log(f"[NEGADO] Passageiro {passageiro.id} não conseguiu uma corrida no momento.")


passageiros = [
    Passageiro(i, f"Passageiro {i}")
    for i in range(1, 501)
]

print("=" * 60)
print("INICIANDO SIMULAÇÃO DE CORRIDAS")
print(f"Total de passageiros: {len(passageiros)}")
print(f"Motoristas disponíveis no pool: {len(pool.motoristas)}")
print("=" * 60)

threads = []

for passageiro in passageiros:
    thread = threading.Thread(
        target=executar_corrida,
        args=(passageiro,),
        name=f"Thread-Passageiro-{passageiro.id}"
    )
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

print("=" * 60)
print("SIMULAÇÃO FINALIZADA COM SUCESSO!")
print(
    f"Resumo da simulação: solicitadas={despachante.total_solicitacoes} | "
    f"ativas={despachante.corridas_ativas} | finalizadas={despachante.total_finalizadas} | "
    f"duplicidades={pool.duplicidades}"
)
print("Todos os passageiros passaram pelo processo de alocação e encerramento.")
print("=" * 60)