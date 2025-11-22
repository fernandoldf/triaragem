class Node:
    """Nó da lista duplamente encadeada"""
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None

class DoublyLinkedList:
    """Lista Duplamente Encadeada (DLL) - Classe pai"""
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0
    
    def add_first(self, data):
        """Adiciona elemento no início"""
        new_node = Node(data)
        if not self.head:
            self.head = self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
        self.size += 1
        return new_node
    
    def add_last(self, data):
        """Adiciona elemento no final"""
        new_node = Node(data)
        if not self.tail:
            self.head = self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
        self.size += 1
        return new_node
    
    def remove_first(self):
        """Remove e retorna primeiro elemento"""
        if not self.head:
            return None
        data = self.head.data
        if self.head == self.tail:
            self.head = self.tail = None
        else:
            self.head = self.head.next
            self.head.prev = None
        self.size -= 1
        return data
    
    def remove_last(self):
        """Remove e retorna último elemento"""
        if not self.tail:
            return None
        data = self.tail.data
        if self.head == self.tail:
            self.head = self.tail = None
        else:
            self.tail = self.tail.prev
            self.tail.next = None
        self.size -= 1
        return data
    
    def remove_middle(self, target_data):
        """Remove elemento específico do meio"""
        current = self.head
        while current:
            if current.data == target_data or (isinstance(target_data, dict) and 
                                               isinstance(current.data, dict) and 
                                               current.data.get('cpf') == target_data.get('cpf')):
                if current == self.head:
                    return self.remove_first()
                if current == self.tail:
                    return self.remove_last()
                
                current.prev.next = current.next
                current.next.prev = current.prev
                self.size -= 1
                return current.data
            current = current.next
        return None

    def remove_by_cpf(self, cpf):
        """Remove elemento cujo dicionário tem chave 'cpf' igual a `cpf`.
        Retorna o dado removido ou None se não encontrado.
        """
        current = self.head
        while current:
            data = current.data
            if isinstance(data, dict) and data.get('cpf') == cpf:
                # remove node
                if current == self.head:
                    return self.remove_first()
                if current == self.tail:
                    return self.remove_last()

                current.prev.next = current.next
                current.next.prev = current.prev
                self.size -= 1
                return data
            current = current.next
        return None
    
    def to_list(self):
        """Converte DLL para lista Python"""
        result = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return result
    
    def is_empty(self):
        """Verifica se está vazia"""
        return self.size == 0


class Stack(DoublyLinkedList):
    """Pilha (LIFO) - herda de DLL"""
    
    def push(self, data):
        """Empilha elemento"""
        return self.add_last(data)
    
    def pop(self):
        """Desempilha elemento"""
        return self.remove_last()
    
    def peek(self):
        """Retorna topo sem remover"""
        return self.tail
    
    def get_history(self):
        """Retorna histórico em ordem reversa (mais recente primeiro)"""
        return list(reversed(self.to_list()))


class PriorityQueue(DoublyLinkedList):
    """Fila de Prioridades - herda de DLL"""

    PRIORITY_VALUES = {
        'emergência': 3,
        'urgente': 2,
        'normal': 1
    }
    
    def enqueue(self, data):
        """Adiciona elemento respeitando prioridade"""
        if not isinstance(data, dict) or 'prioridade' not in data:
            raise ValueError("Dados devem conter campo 'prioridade'")
        
        new_priority = self.PRIORITY_VALUES.get(data['prioridade'], 1)
        
        # Fila vazia ou novo elemento tem menor/igual prioridade que o último
        if self.is_empty():
            return self.add_last(data)
        
        tail_priority = self.PRIORITY_VALUES.get(self.tail.data['prioridade'], 1)
        if tail_priority >= new_priority:
            return self.add_last(data)
        
        # Nova maior prioridade - adiciona no início
        head_priority = self.PRIORITY_VALUES.get(self.head.data['prioridade'], 1)
        if head_priority < new_priority:
            return self.add_first(data)
        
        # Inserir no meio - encontrar posição correta
        current = self.head
        while current:
            current_priority = self.PRIORITY_VALUES.get(current.data['prioridade'], 1)
            if current_priority < new_priority:
                new_node = Node(data)
                new_node.next = current
                new_node.prev = current.prev
                if current.prev:
                    current.prev.next = new_node
                current.prev = new_node
                self.size += 1
                return new_node
            current = current.next
        
        return self.add_last(data)
    
    def dequeue(self):
        """Remove elemento de maior prioridade (primeiro da fila)"""
        return self.remove_first()
    
    def front(self):
        """Retorna primeiro da fila sem remover"""
        return self.head.data if self.head else None
