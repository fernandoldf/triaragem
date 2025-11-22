from datetime import datetime
from flask import session

class AtendimentoService:

    def __init__(self, fila, historico):
        self.fila = fila
        self.historico = historico
    
  # CONTROLE DE SESSÃO

    def get_atual(self):
        return session.get('paciente_atual')

    def set_atual(self, paciente):
        if paciente:
            session['paciente_atual'] = paciente
        else:
            session.pop('paciente_atual', None)

    def get_anterior(self):
        return session.get('paciente_anterior')

    def set_anterior(self, paciente):
        if paciente:
            session['paciente_anterior'] = paciente
        else:
            session.pop('paciente_anterior', None)



    def chamar_proximo(self): 

        atual = self.get_atual()
        proximo = self.fila.dequeue()

        if not proximo:
            raise ValueError("Fila vazia")

        atendimento = {
            **proximo,
            "hora_atendimento": datetime.now().strftime("%H:%M:%S"),
            "data_atendimento": datetime.now().strftime("%d/%m/%Y")
        }

        self.historico.push(atendimento)

        self.set_anterior(atual)
        self.set_atual(proximo)


    def voltar_anterior(self):

        atual = self.get_atual()
        anterior = self.get_anterior()

        if not atual and not anterior:
            raise ValueError("Não há paciente anterior")


        if atual:
            self.fila.add_first(atual)
            self.historico.pop()

        self.set_atual(anterior)

        if self.historico.size < 2:
            self.set_anterior(None)
        else:
            self.set_anterior(self.historico.peek().prev.data)