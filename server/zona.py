class ControleZonas:
    def __init__(self):
        self.zonas = {
            'Zona_A': set(),
            'Zona_B': set(),
            'Zona_C': set()
            }
        self.clientes = {}

    def inscrever(self, zona, endereco):
        if zona not in self.zonas:
            print(f"Zona não encontrada.")
            return False
        
        zona_atual = self.clientes.get(endereco)

        if zona_atual is not None:
            if zona_atual == zona:
                print(f"Endereço {endereco} já inscrito na zona {zona}!")
                return False
            self.zonas[zona_atual].discard(endereco)

        
        try:
            self.zonas[zona].add(endereco)
            self.clientes[endereco] = zona
        except Exception as e:
            print(f"Erro na inscrição de {endereco}: {e}")
            return False
        else:
            return True

    def desinscrever(self, zona, endereco):
        if zona not in self.zonas:
            print("Zona não encontrada.")
            return False
        
        try:
            if endereco not in self.zonas[zona]:
                print(f"Endereço {endereco} não está inscrito na zona {zona}.")
                return False
            
            self.zonas[zona].remove(endereco)
            self.clientes.pop(endereco, None)
        except Exception as e:
            print(f"Erro no cancelamento de {endereco}: {e}")
            return False
        else:
            return True
        
    def remover_desconectado(self, endereco):
        zona = self.clientes.get(endereco)

        if zona is None:
            return False
        
        try:
            self.zonas[zona].discard(endereco)
            del self.clientes[endereco]
        except Exception as e:
            print(f"Erro ao remover {endereco}: {e}")
            return False
        else:
            return True

    
    def listar_zona(self, zona):
        if zona not in self.zonas:
            return []
        return sorted(self.zonas[zona])
    
    def listar_associacoes(self):
        return dict(self.clientes)