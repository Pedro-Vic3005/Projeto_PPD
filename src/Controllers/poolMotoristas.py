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

    def alocar(self, passageiro):

        self.semaforo.acquire()

        with self.mutex:

            if passageiro.em_corrida:
                self.semaforo.release()
                return False

            for motorista in self.motoristas:

                if motorista.disponivel:

                    motorista.ocupar()
                    passageiro.atribuir_motorista(motorista)

                    return True

            self.semaforo.release()
            raise RuntimeError("Semáforo e pool inconsistentes")

    def finalizar(self, passageiro):

        with self.mutex:

            if not passageiro.em_corrida:
                return False

            if passageiro.finalizar_corrida():

                self.semaforo.release()

                return True

            return False