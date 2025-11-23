from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from datetime import datetime
from estrutura_dados import PriorityQueue, Stack

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui_mude_em_producao'

# Instâncias globais (em produção, usar banco de dados)
fila_atendimento = PriorityQueue()
historico_atendimentos = Stack()

def get_paciente_atual():
    """Retorna paciente atual da sessão"""
    return session.get('paciente_atual')

def set_paciente_atual(paciente):
    """Define paciente atual na sessão"""
    if paciente:
        session['paciente_atual'] = paciente
    else:
        session.pop('paciente_atual', None)

def get_paciente_anterior():
    """Retorna paciente anterior da sessão"""
    return session.get('paciente_anterior')

def set_paciente_anterior(paciente):
    """Define paciente anterior na sessão"""
    if paciente:
        session['paciente_anterior'] = paciente
    else:
        session.pop('paciente_anterior', None)



@app.route('/')
def index():
    """Tela principal - fila de atendimento"""
    paciente_atual = get_paciente_atual()
    paciente_anterior = get_paciente_anterior()
    fila = fila_atendimento.to_list()
    
    return render_template('index.html', 
                         paciente_atual=paciente_atual,
                         paciente_anterior=paciente_anterior,
                         fila=fila,
                         total_fila=len(fila),
                         total_historico=historico_atendimentos.size)


@app.route('/zerar')
def zerar():
    """Zera fila e histórico (para testes)"""
    global fila_atendimento, historico_atendimentos
    fila_atendimento = PriorityQueue()
    historico_atendimentos = Stack()
    set_paciente_atual(None)
    set_paciente_anterior(None)
    return redirect(url_for('index'))

@app.route('/historico')
def historico():
    """Tela de histórico de atendimentos"""
    historico_list = historico_atendimentos.get_history()
    
    return render_template('historico.html',
                         historico=historico_list,
                         total_fila=fila_atendimento.size,
                         total_historico=len(historico_list))


@app.route('/cadastro')
def cadastro():
    """Tela de cadastro de paciente"""
    return render_template('cadastro.html',
                         total_fila=fila_atendimento.size,
                         total_historico=historico_atendimentos.size)


@app.route('/adicionar_paciente', methods=['POST'])
def adicionar_paciente():
    """Adiciona paciente à fila"""
    try:
        paciente = {
            'nome': request.form.get('nome'),
            'cpf': request.form.get('cpf'),
            'idade': int(request.form.get('idade')),
            'contato': request.form.get('contato'),
            'prioridade': request.form.get('prioridade', 'normal'),
            'sintomas': request.form.get('sintomas', ''),
            'hora_cadastro': datetime.now().strftime('%H:%M:%S'),
            'data_cadastro': datetime.now().strftime('%d/%m/%Y')
        }
        print(paciente)
        
        # Validações básicas
        if not all([paciente['nome'], paciente['cpf'], paciente['idade'], paciente['contato']]):
            return jsonify({'success': False, 'message': 'Preencha todos os campos obrigatórios'}), 400
        
        fila_atendimento.enqueue(paciente)
        print(fila_atendimento.to_list())
        return redirect(url_for('index'))
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400


@app.route('/chamar_proximo', methods=['POST'])
def chamar_proximo():
    """Chama próximo paciente da fila"""
    try:
        # Salvar paciente atual no histórico se existir
        paciente_atual = get_paciente_atual()
        
        # Pegar próximo da fila
        proximo = fila_atendimento.dequeue()
        
        if proximo:
            print('Chamando próximo paciente:', proximo)
            atendimento = {
                **proximo,
                'hora_atendimento': datetime.now().strftime('%H:%M:%S'),
                'data_atendimento': datetime.now().strftime('%d/%m/%Y')
            }
            historico_atendimentos.push(atendimento)
            print('colocou no histórico:', atendimento)
            set_paciente_anterior(paciente_atual)
            print('anterior setado como:', paciente_atual)
            set_paciente_atual(proximo)
            print('atual setado como:', proximo)
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'message': 'Fila vazia'}), 400
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400


@app.route('/voltar_anterior', methods=['POST'])
def voltar_anterior():
    """Volta para o paciente anterior"""
    try:
        paciente_anterior = get_paciente_anterior()
        paciente_atual = get_paciente_atual()

        if not paciente_anterior and not paciente_atual:
            return jsonify({'success': False, 'message': 'Não há paciente anterior'}), 400
        
        paciente_atual = get_paciente_atual()
        
        # Retorna paciente atual para a fila
        if paciente_atual:
            fila_atendimento.add_first(paciente_atual)
            historico_atendimentos.pop()  # Remove do histórico
            print(f"removido histórico: {paciente_atual}")
            print(paciente_atual)
        
        # Restaura paciente anterior
        set_paciente_atual(paciente_anterior)
        print('atual setado como:', paciente_anterior)

        set_paciente_anterior(None if historico_atendimentos.size < 2 else historico_atendimentos.peek().prev.data)
        print('anterior setado como:', None if historico_atendimentos.size < 2 else historico_atendimentos.peek())
        
        return jsonify({'success': True})
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400


@app.route('/api/fila')
def api_fila():
    """API para obter fila atualizada"""
    return jsonify({
        'fila': fila_atendimento.to_list(),
        'total': fila_atendimento.size
    })


@app.route('/api/status')
def api_status():
    """API para status geral do sistema"""
    return jsonify({
        'paciente_atual': get_paciente_atual(),
        'total_fila': fila_atendimento.size,
        'total_historico': historico_atendimentos.size
    })


@app.route('/remover_paciente', methods=['POST'])
def remover_paciente():
    """Remove paciente da fila pelo CPF"""
    try:        
        cpf = request.json.get('cpf')
        fila_atendimento.remove_by_cpf(cpf)
        return jsonify({'success': True})   
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400



# Rota para baixar histórico em CSV
import csv
from flask import Response

@app.route('/historico/download')
def download_historico():
    historico_list = historico_atendimentos.get_history()
    # Define colunas que aparecem na tabela
    fieldnames = ['nome', 'contato', 'prioridade', 'data_atendimento', 'hora_atendimento']
    def generate():
        yield ','.join(fieldnames) + '\n'
        for atendimento in historico_list:
            row = [str(atendimento.get(col, '')) for col in fieldnames]
            yield ','.join(row) + '\n'
    return Response(generate(), mimetype='text/csv', headers={
        'Content-Disposition': 'attachment; filename=historico.csv'
    })


@app.route('/historico/stats')
def historico_stats():
    """Retorna estatísticas simples do histórico: contagem por prioridade e top sintomas."""
    historico_list = historico_atendimentos.get_history()

    # Contagem por prioridade
    prioridade_counts = {'emergência': 0, 'urgente': 0, 'normal': 0}

    # Contagem de sintomas (string inteira como chave)
    sintomas_counts = {}

    for atendimento in historico_list:
        p = atendimento.get('prioridade', 'normal')
        if p not in prioridade_counts:
            prioridade_counts[p] = 0
        prioridade_counts[p] += 1

        sint = atendimento.get('sintomas', '') or ''
        sint = sint.strip()
        if sint:
            sintomas_counts[sint] = sintomas_counts.get(sint, 0) + 1

    # Top sintomas (maiores contagens)
    top_sintomas = sorted(sintomas_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    top_sintomas = [{'sintoma': s, 'count': c} for s, c in top_sintomas]

    return jsonify({
        'prioridade_counts': prioridade_counts,
        'top_sintomas': top_sintomas
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)