clientes_conectados = set()

def adicionar_cliente(endereco):
    clientes_conectados.add(endereco)

def remover_cliente(endereco):
    clientes_conectados.discard(endereco)

def listar_clientes():
    return list(clientes_conectados)