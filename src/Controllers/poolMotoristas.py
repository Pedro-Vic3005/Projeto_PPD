import threading

from src.schemas.motorista import Motorista


class PoolMotoristas:

    def __init__(self, quantidade):

        self.motoristas = [
            Motorista(i, f"Motorista {i}")
            for i in range(1, quantidade + 1)
        ]

        self.mutex = threading.Lock()
        self.semaforo = threading.Semaphore(quantidade)
        self.passageiros_ativos_por_motorista = {
            motorista.id: set() for motorista in self.motoristas
        }
        self.duplicidades = 0

    def alocar(self, passageiro):

        self.semaforo.acquire()

        with self.mutex:

            if passageiro.em_corrida:
                self.semaforo.release()
                return False

            for motorista in self.motoristas:

                if motorista.disponivel:

                    motorista.ocupar()
                    passageiros_ativos = self.passageiros_ativos_por_motorista[motorista.id]
                    if passageiros_ativos:
                        self.duplicidades += 1

                    passageiro.atribuir_motorista(motorista)
                    passageiros_ativos.add(passageiro.id)

                    return True

            self.semaforo.release()
            raise RuntimeError("Semáforo e pool inconsistentes")

    def finalizar(self, passageiro):

        with self.mutex:

            if not passageiro.em_corrida:
                return False

            motorista = passageiro.motorista
            if passageiro.finalizar_corrida():
                self.passageiros_ativos_por_motorista[motorista.id].discard(passageiro.id)

                self.semaforo.release()

                return True

            return False