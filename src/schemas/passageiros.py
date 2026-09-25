class Passageiro:
    def __init__(self,id,nome):
        self.id = id
        self.motorista = None
        self.em_corrida = False #nao esta em uma corrida
        pass

    def atribuir_motorista(self, motorista):
        if self.em_corrida == False:
            self.motorista = motorista
            self.em_corrida = True
            return True
        return False
    
    def finalizar_corrida(self):
        if self.em_corrida and self.motorista is not None:
            self.em_corrida = False
            self.motorista.liberar()
            self.motorista = None
            return True
        return False
    
    def exibir_status(self):
        print(f"Passageiro: {self.id}")
        print(f"Status: {self.em_corrida}")

        if self.motorista is not None:
            print(f"Motorista: {self.motorista.id}")