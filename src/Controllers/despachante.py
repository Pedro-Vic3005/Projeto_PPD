class Despachante:

    def __init__(self, pool):
        self.pool = pool

    def solicitar_corrida(self, passageiro):

        resultado = self.pool.alocar(passageiro)

        if resultado:
            print(
                f"Passageiro {passageiro.id} "
                f"alocado ao motorista "
                f"{passageiro.motorista.id}"
            )

            return True

        return False

    def finalizar_corrida(self, passageiro):

        if not passageiro.em_corrida:
            return False

        resultado = self.pool.finalizar(passageiro)

        if resultado:
            print(
                f"Corrida do passageiro "
                f"{passageiro.id} finalizada."
            )

            return True

        return False