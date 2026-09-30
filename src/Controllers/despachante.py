import threading


class Despachante:

    def __init__(self, pool):
        self.pool = pool
        self.total_solicitacoes = 0
        self.total_finalizadas = 0
        self.corridas_ativas = 0
        self.max_corridas_simultaneas = 0
        self.mutex = threading.Lock()
        self.ordem_evento = 0

    def _snapshot_metricas(self):
        return (
            f"solicitadas={self.total_solicitacoes} | "
            f"ativas={self.corridas_ativas} | "
            f"max_simultaneas={self.max_corridas_simultaneas} | "
            f"finalizadas={self.total_finalizadas}"
        )

    def _metricas(self):
        with self.mutex:
            return self._snapshot_metricas()

    def _registrar_log(self, mensagem):
        with self.mutex:
            self.ordem_evento += 1
            print(f"[{self.ordem_evento:04d}] {mensagem}")

    def solicitar_corrida(self, passageiro):
        with self.mutex:
            self.total_solicitacoes += 1
            metricas = self._snapshot_metricas()

        self._registrar_log(
            f"[DESPACHANTE] Solicitação recebida para passageiro {passageiro.id}. "
            f"Métricas: {metricas}"
        )

        resultado = self.pool.alocar(passageiro)

        if resultado:
            with self.mutex:
                self.corridas_ativas += 1
                self.max_corridas_simultaneas = max(
                    self.max_corridas_simultaneas,
                    self.corridas_ativas
                )
                metricas = self._snapshot_metricas()

            self._registrar_log(
                f"[DESPACHANTE] Passageiro {passageiro.id} alocado ao motorista "
                f"{passageiro.motorista.id}. Métricas: {metricas}"
            )
            return True

        with self.mutex:
            metricas = self._snapshot_metricas()

        self._registrar_log(
            f"[DESPACHANTE] Passageiro {passageiro.id} não pôde ser alocado agora. "
            f"Métricas: {metricas}"
        )
        return False

    def finalizar_corrida(self, passageiro):
        with self.mutex:
            if not passageiro.em_corrida:
                mensagem = (
                    f"[DESPACHANTE] Passageiro {passageiro.id} não estava em corrida. "
                )
                resultado = False
            else:
                motorista_id = passageiro.motorista.id if passageiro.motorista else None
                resultado = self.pool.finalizar(passageiro)

                if resultado:
                    self.corridas_ativas -= 1
                    self.total_finalizadas += 1
                    mensagem = (
                        f"[DESPACHANTE] Corrida encerrada: passageiro {passageiro.id} concluiu a viagem, "
                        f"motorista {motorista_id} foi liberado. "
                    )
                else:
                    mensagem = (
                        f"[DESPACHANTE] Não foi possível encerrar a corrida do passageiro {passageiro.id}. "
                    )

            metricas = self._snapshot_metricas()

        self._registrar_log(f"{mensagem}Métricas: {metricas}")
        return resultado