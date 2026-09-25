class Motorista:

    def __init__(self, id, nome):
        self.id = id
        self.disponivel = True

    def ocupar(self):
        if self.disponivel:
            self.disponivel = False
            return True

        return False

    def liberar(self):
        self.disponivel = True

    def exibir_status(self):
        status = "Livre" if self.disponivel else "Ocupado"
        print(f"Motorista: {self.id}")
        print(f"Status: {status}")