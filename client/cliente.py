import socket

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

server_addr = ('localhost', 5000)

def header():
    print("------------ Sistema de Alertas da Defesa Civil ------------")
    print("\n")

while True:
    header()
    print("Cliente não está inscrito em nenhuma zona. Deseja inscrever-se?")
    print("1 - Sim")
    print("2 - Listar zonas")
    print("3 - Não (sair)")

    resposta = input("-> ")
    
    match (resposta):
        case "1":
            print("> Inscrever")
            print("\n")
            zona = input("Digite a sua zona: ")
            msg = f"WATCH|ZONA_{zona.upper}"
            sock.sendto(msg.encode(), server_addr)
            print("Mensagem enviada.")

        case "2":
            print("> Lista de zonas disponíveis")
            print("\n")
            print("A\nB\nC\n")

        case "3":
            confirm = input("Você não está inscrito em nenhuma zona e a defesa civil não poderá lhe enviar alertas. Tem certeza? (s / n): ")
            if(confirm == "s" or confirm == "S"):
                exit(0)
            else:
                continue

        case _:
            break
