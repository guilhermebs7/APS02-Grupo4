import socket
import threading
from datetime import datetime

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
server_addr = ('localhost', 5000)

status = ""
zone = ""
alerts = []
unregister = False
screen_state = ""

def get_status():
    msg = "FIND"
    sock.sendto(msg.encode(), server_addr)
    response, addr = sock.recvfrom(1024)
    rsp = response.decode()

    global status
    global zone

    if rsp == "NONE":
        status = "UNREGISTERED"
        zone = ""
    else:
        status = "REGISTERED"
        zone = rsp.split("_")[1]

def header():
    print("------------------------------------------------------------------------------------------------")
    print("------------------------------ Sistema de Alertas da Defesa Civil ------------------------------")
    print("------------------------------------------------------------------------------------------------\n")

def unregistered_opts():
    print("Cliente não está inscrito em nenhuma zona. Deseja inscrever-se?\n")
    print("1 - Sim")
    print("2 - Listar zonas")
    print("3 - Não (sair)")

def registered_opts():
    print("Cliente inscrito no sistema de alertas.")
    print(f"Zona atual: {zone}\n")
    print("1 - Ver histórico de alertas para a minha zona")
    print("2 - Cancelar inscrição na zona atual")
    print("3 - Sair")

def get_screen_state():
    match (screen_state):
        case "UNREG_INIT":
            unregistered_opts()
            print("-> ")
        case "REG_INIT":
            registered_opts()
            print("-> ")
        case "UNREG_REG":
            print("> Inscrever\n")
            print("Digite a sua zona: ", end="")
        case "REG_HIST":
            print(f"> Alertas para Zona {zone} ({len(alerts)} alertas):\n")
            for alt in alerts:
                print(alt + "\n")
            print("Aperte ENTER para voltar")
        case "UNREG_LIST":
            print("> Lista de zonas disponíveis\n")
            print("A\nB\nC\n")
            print("Digite enter para voltar ")
        case "REG_UNSB":
            print("> Cancelar inscrição\n")
            print(f"Tem certeza de que deseja cancelar sua inscrição na zona {zone} (S / N)? ")
        case "UNREG_EXIT":
            print("Você não está inscrito em nenhuma zona e a defesa civil não poderá lhe enviar alertas. Tem certeza? (s / n): ")
            

def check_alerts():
    while True:
        try:
            msg, addr = sock.recvfrom(1024)
            alert = msg.decode()
            if alert.startswith("ALERTA DEFESA CIVIL"):
                now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                print("\033c", end="")
                header()
                print(f"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! {now.split(" ")[0]} !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")
                print(alert + "\n")
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")
                alerts.append({
                    "message": alert,
                    "timestamp": now
                    })
                get_screen_state()
                continue
            elif unregister == True and alert.split("|")[0] == "OK":
                alerts.clear()
                break
            else:
                continue
        except Exception as e:
            print(str(e))
            exit(1)
            
get_status()

while True:
    header()
    if status == "UNREGISTERED":
        screen_state = "UNREG_INIT"
        unregistered_opts()
    else:
        screen_state = "REG_INIT"
        registered_opts()
    
    resposta = input("-> ")
    if resposta != "3":
        print("\033c", end="") #pra limpar o terminal
    
    match (resposta):
        case "1":
            header()
            if status == "UNREGISTERED":
                screen_state = "UNREG_REG"
                print("> Inscrever\n")
                zona = input("Digite a sua zona: ")
                msg = f"WATCH|Zona_{zona.upper()}"
                sock.sendto(msg.encode(), server_addr)
                print("\033c", end="")
                print("Mensagem enviada.")
                get_status()
                alert_thread = threading.Thread(target=check_alerts, daemon=True)
                alert_thread.start()
            else:
                screen_state = "REG_HIST"
                print(f"> Alertas para Zona {zone} ({len(alerts)} alertas):\n")
                for alt in alerts:
                    msg_line = next((line for line in alt["message"].splitlines() if line.startswith("Mensagem:")), None)
                    print(f"[{alt["timestamp"]}]")
                    print(msg_line + "\n")
                input("Aperte ENTER para voltar")
                print("\033c", end="")


        case "2":
            if status == "UNREGISTERED":
                screen_state = "UNREG_LIST"
                header()
                print("> Lista de zonas disponíveis\n")
                print("A\nB\nC\n")
                input("Digite enter para voltar ")
                print("\033c", end="")
            else:
                screen_state = "REG_UNSB"
                unregister = True
                header()
                print("> Cancelar inscrição\n")
                resposta = input(f"Tem certeza de que deseja cancelar sua inscrição na zona {zone} (S / N)? ")
                if resposta.upper() == "S":
                    msg = f"UNWATCH|Zona_{zone}"
                    sock.sendto(msg.encode(), server_addr)
                    print("\033c", end="")
                    print("Inscrição cancelada")
                    get_status()
                else:
                    continue
                unregister = False

        case "3":
            if status == "UNREGISTERED":
                screen_state = "UNREG_EXIT"
                confirm = input("Você não está inscrito em nenhuma zona e a defesa civil não poderá lhe enviar alertas. Tem certeza? (s / n): ")
                if(confirm == "s" or confirm == "S"):
                    exit(0)
                else:
                    print("\033c", end="")
                    continue
            else:
                exit(0)

        case _:
            break
