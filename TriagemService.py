from datetime import datetime

class TriagemService:

    PRIORIDADES_VALIDAS = ["normal", "urgente", "emergência"]

    def processar_dados(self, dados):

        try:
            idade = int(dados.get('idade'))
        except:
            raise ValueError("Idade inválida")

        prioridade = dados.get('prioridade', 'normal')

        if prioridade not in self.PRIORIDADES_VALIDAS:
            prioridade = "normal"

        paciente = {
            'nome': dados.get('nome'),
            'cpf': dados.get('cpf'),
            'idade': idade,
            'contato': dados.get('contato'),
            'prioridade': prioridade,
            'sintomas': dados.get('sintomas', ''),
            'hora_cadastro': datetime.now().strftime('%H:%M:%S'),
            'data_cadastro': datetime.now().strftime('%d/%m/%Y')
        }

       
        if not all([paciente['nome'], paciente['cpf'], paciente['contato']]):
            raise ValueError("Preencha todos os campos obrigatórios")

        return paciente