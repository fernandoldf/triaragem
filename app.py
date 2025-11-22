from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from datetime import datetime

# Estruturas de dados
from estrutura_dados.priority_queue import PriorityQueue
from estrutura_dados.stack import Stack

# Serviços
from services.triagem_service import TriagemService
from services.atendimento_service import AtendimentoService

app = Flask(__name__)
app.secret_key = "sua_chave_secreta_aqui"

# Instâncias globais
fila_atendimento = PriorityQueue()
historico_atendimentos = Stack()

# Serviços
triagem_service = TriagemService()
atendimento_service = AtendimentoService(fila_atendimento, historico_atendimentos)


# PÁGINA PRINCIPAL

@app.route("/")
def index():
    paciente_atual = atendimento_service.get_atual()
    paciente_anterior = atendimento_service.get_anterior()
    fila = fila_atendimento.to_list()

    return render_template(
        "index.html",
        paciente_atual=paciente_atual,
        paciente_anterior=paciente_anterior,
        fila=fila,
        total_fila=len(fila),
        total_historico=historico_atendimentos.size
    )


# ZERAR SISTEMA (TESTES)

@app.route("/zerar")
def zerar():
    global fila_atendimento, historico_atendimentos

    fila_atendimento = PriorityQueue()
    historico_atendimentos = Stack()

    atendimento_service.set_atual(None)
    atendimento_service.set_anterior(None)

    return redirect(url_for("index"))


# HISTÓRICO

@app.route("/historico")
def historico():
    historico_list = historico_atendimentos.get_history()

    return render_template(
        "historico.html",
        historico=historico_list,
        total_fila=fila_atendimento.size,
        total_historico=len(historico_list)
    )


# CADASTRO DE PACIENTE

@app.route("/cadastro")
def cadastro():
    return render_template(
        "cadastro.html",
        total_fila=fila_atendimento.size,
        total_historico=historico_atendimentos.size
    )



# ADICIONAR PACIENTE

@app.route("/adicionar_paciente", methods=["POST"])
def adicionar_paciente():
    try:
        dados = {
            "nome": request.form.get("nome"),
            "cpf": request.form.get("cpf"),
            "idade": request.form.get("idade"),
            "contato": request.form.get("contato"),
            "prioridade": request.form.get("prioridade", "normal"),
            "sintomas": request.form.get("sintomas", "")
        }

        paciente = triagem_service.processar_dados(dados)

        fila_atendimento.enqueue(paciente)

        return redirect(url_for("index"))

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400


# CHAMAR PRÓXIMO

@app.route("/chamar_proximo", methods=["POST"])
def chamar_proximo():
    try:
        atendimento_service.chamar_proximo()
        return jsonify({"success": True})

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400


# VOLTAR AO ANTERIOR

@app.route("/voltar_anterior", methods=["POST"])
def voltar_anterior():
    try:
        atendimento_service.voltar_anterior()
        return jsonify({"success": True})

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400


# API – Fila

@app.route("/api/fila")
def api_fila():
    return jsonify({
        "fila": fila_atendimento.to_list(),
        "total": fila_atendimento.size
    })


# API – Status

@app.route("/api/status")
def api_status():
    return jsonify({
        "paciente_atual": atendimento_service.get_atual(),
        "total_fila": fila_atendimento.size,
        "total_historico": historico_atendimentos.size
    })

# EXECUTAR

if __name__ == "__main__":
    app.run(debug=True, port=5000)