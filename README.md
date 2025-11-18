# 🏥 Sistema de Triagem Hospitalar

Um sistema web de gerenciamento de filas de atendimento hospitalar com priorização automática de pacientes baseada em critérios de urgência.

## 📋 Sobre o Projeto

Este é um projeto acadêmico desenvolvido para a disciplina de **Estrutura de Dados** que implementa um sistema de triagem hospitalar utilizando estruturas de dados avançadas como:

- **Lista Duplamente Encadeada (DLL)** - Estrutura base para todas as operações
- **Fila de Prioridades** - Ordenação automática de pacientes por urgência
- **Pilha (Stack)** - Registro do histórico de atendimentos

O sistema permite:
- ✅ Cadastro de pacientes com priorização automática
- ✅ Visualização em tempo real da fila de espera
- ✅ Atendimento com histórico rastreável
- ✅ Possibilidade de retornar ao paciente anterior
- ✅ Interface intuitiva e responsiva

## 🚀 Funcionalidades

### 1. **Painel de Atendimento**
- Exibição do paciente em atendimento com destaque visual por prioridade
- Visualização completa da fila de espera
- Botões para chamar próximo paciente e voltar ao anterior
- Contador de pacientes na fila e atendimentos realizados

### 2. **Cadastro de Pacientes**
- Formulário com validação de campos obrigatórios
- Seleção de prioridade (Normal, Urgente, Emergência)
- Armazenamento automático de data/hora do cadastro
- Priorização automática na fila respeitando critérios de urgência

### 3. **Histórico de Atendimentos**
- Registro de todos os atendimentos realizados
- Exibição em ordem cronológica (mais recente primeiro)
- Informações completas do paciente e horário de atendimento

### 4. **Gerenciamento de Dados**
- Opção de zerar todos os dados para recomeçar
- Persistência em sessão durante a navegação

## 🛠️ Tecnologias Utilizadas

### Backend
- **Python 3.x** - Linguagem principal
- **Flask** - Framework web
- **Estruturas de Dados customizadas** em Python puro

### Frontend
- **HTML5** - Estrutura
- **CSS3** - Estilização responsiva
- **JavaScript Vanilla** - Interatividade
- **Jinja2** - Templates dinâmicos

## 📁 Estrutura do Projeto

```
triaragem/
├── app.py                          # Aplicação Flask principal
├── estrutura_dados.py              # Implementação de estruturas de dados
├── requirements.txt                # Dependências do projeto
├── README.md                       # Este arquivo
└── templates/
    ├── base.html                   # Template base com menu
    ├── index.html                  # Painel de atendimento
    ├── cadastro.html               # Formulário de cadastro
    └── historico.html              # Histórico de atendimentos
```

## 🏗️ Arquitetura de Dados

### Classe `Node`
Representa um nó individual na estrutura de dados.

```python
class Node:
    def __init__(self, data):
        self.data = data
        self.prev = None      # Referência ao nó anterior
        self.next = None      # Referência ao próximo nó
```

### Classe `DoublyLinkedList` (DLL)
Implementa uma lista duplamente encadeada com operações básicas:
- `add_first(data)` - Adiciona no início
- `add_last(data)` - Adiciona no final
- `remove_first()` - Remove do início
- `remove_last()` - Remove do final
- `remove_middle(target_data)` - Remove do meio
- `to_list()` - Converte para lista Python
- `is_empty()` - Verifica se está vazia

### Classe `Stack` (Pilha)
Herda de DLL implementando LIFO (Last In, First Out):
- `push(data)` - Empilha
- `pop()` - Desempilha
- `peek()` - Retorna topo sem remover
- `get_history()` - Retorna histórico em ordem reversa

### Classe `PriorityQueue` (Fila de Prioridades)
Herda de DLL com ordenação automática por prioridade:

**Níveis de Prioridade:**
| Nível | Valor | Descrição |
|-------|-------|-----------|
| Emergência | 3 | Risco de morte iminente |
| Urgente | 2 | Necessário atendimento rápido |
| Normal | 1 | Atendimento regular |

**Métodos:**
- `enqueue(data)` - Adiciona respeitando prioridade
- `dequeue()` - Remove de maior prioridade
- `front()` - Retorna primeiro sem remover

## 🎨 Prioridades Visuais

Cada nível de prioridade possui cores e estilos únicos:

- 🔴 **Emergência** - Vermelho (#ef4444)
- 🟠 **Urgente** - Laranja (#f59e0b)
- 🟢 **Normal** - Verde (#10b981)

## 💻 Como Executar

### Pré-requisitos
- Python 3.8+
- pip (gerenciador de pacotes Python)

### Instalação

1. **Clone ou extraia o projeto:**
```bash
cd triaragem
```

2. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

3. **Execute a aplicação:**
```bash
python app.py
```

4. **Acesse no navegador:**
```
http://localhost:5000
```

## 📝 Uso do Sistema

### 1. Adicionar Paciente
1. Clique em "Adicionar Paciente" no menu lateral
2. Preencha os dados obrigatórios (nome, CPF, idade, contato)
3. Selecione a prioridade apropriada
4. Clique em "Adicionar à Fila"

### 2. Atender Paciente
1. Na tela de atendimento, clique em "Chamar Próximo"
2. O paciente de maior prioridade será exibido
3. Após o atendimento, chame o próximo

### 3. Voltar Paciente
- Se necessário voltar ao paciente anterior, clique em "Voltar Anterior"
- O paciente voltará à fila respeitando sua prioridade

### 4. Consultar Histórico
1. Clique em "Histórico" no menu lateral
2. Visualize todos os atendimentos realizados

## 🔄 Fluxo de Atendimento

```
┌─────────────────────┐
│ Cadastro Paciente   │
│ (Define Prioridade) │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Fila de Prioridades │
│ (Ordena pacientes)  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Chamar Próximo      │
│ (Maior prioridade)  │
└──────────┬──────────┘
           │
           ├─► Em Atendimento ─┬─► Próximo
           │                   └─► Voltar Anterior
           │
           ▼
┌─────────────────────┐
│ Histórico Stack     │
│ (LIFO)              │
└─────────────────────┘
```

## 📊 Exemplo de Dados

**Paciente:**
```python
{
    'nome': 'João Silva',
    'cpf': '123.456.789-00',
    'idade': 45,
    'contato': '(11) 98765-4321',
    'prioridade': 'urgente',
    'sintomas': 'Dor no peito',
    'hora_cadastro': '14:30:45',
    'data_cadastro': '18/11/2025'
}
```

## 🐛 Troubleshooting

### Aplicação não inicia
- Verifique se Python está instalado: `python --version`
- Reinstale as dependências: `pip install -r requirements.txt --force-reinstall`

### Porta 5000 já está em uso
- Modifique a porta em `app.py`:
```python
if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Use outra porta
```

### Dados não persistem
- Os dados são armazenados em sessão durante a execução
- Para persistência permanente, implemente um banco de dados

## 🚀 Melhorias Futuras

- [ ] Integração com banco de dados (SQLite, PostgreSQL)
- [ ] Autenticação de usuários
- [ ] Relatórios e estatísticas
- [ ] Sistema de alertas e notificações
- [ ] API REST completa
- [ ] Dashboard com gráficos em tempo real
- [ ] Integração com painéis eletrônicos

## 📚 Conceitos Aprendidos

- ✓ Estruturas de dados lineares (Listas, Pilhas, Filas)
- ✓ Listas duplamente encadeadas
- ✓ Algoritmos de busca e inserção ordenada
- ✓ Fila com prioridades
- ✓ Desenvolvimento web com Flask
- ✓ Manipulação de sessões
- ✓ Interface responsiva com HTML/CSS

## 👨‍💻 Autor

**Fernando Lorentz Domingues Flores**  
Projeto desenvolvido para a disciplina de Estrutura de Dados

## 📄 Licença

Este projeto é fornecido como material educacional.

## 📞 Suporte

Para dúvidas ou problemas, consulte:
- Documentação do Flask: https://flask.palletsprojects.com/
- Python Documentation: https://docs.python.org/3/

---

**Versão:** 1.0.0  
**Última atualização:** Novembro 2025
