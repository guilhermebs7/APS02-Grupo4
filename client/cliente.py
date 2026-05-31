import socket
import threading
from datetime import datetime
import os

os.system('color') #pro windows

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
server_addr = ('localhost', 5000)

RED     = "\033[1;31m"
GREEN   = "\033[1;32m"    
YELLOW  = "\033[1;33m"
BLUE    = "\033[1;34m"
MAGENTA = "\033[1;35m"
ORANGE = "\033[1;38;5;208m"
RESET   = "\033[0m"

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
    print(f"{ORANGE}------------------------------------------------------------------------------------------------")
    print(f"------------------------------ Sistema de Alertas da Defesa Civil ------------------------------")
    print(f"------------------------------------------------------------------------------------------------{RESET}\n")

def unregistered_opts():
    print(f"{BLUE}Cliente não está inscrito em nenhuma zona. Deseja inscrever-se?\n")
    print("1 - Sim")
    print("2 - Listar zonas")
    print(f"3 - Não (sair){RESET}")

def registered_opts():
    print(f"{GREEN}Cliente inscrito no sistema de alertas.")
    print(f"Zona atual: {zone}{RESET}\n")
    print(f"{BLUE}1 - Ver histórico de alertas para a minha zona")
    print("2 - Cancelar inscrição na zona atual")
    print(f"3 - Sair{RESET}")

def get_screen_state():
    match (screen_state):
        case "UNREG_INIT":
            unregistered_opts()
            print("-> ")
        case "REG_INIT":
            registered_opts()
            print("-> ")
        case "UNREG_REG":
            print(f"{MAGENTA}> Inscrever{RESET}\n")
            print("Digite a sua zona: ", end="")
        case "REG_HIST":
            print(f"{MAGENTA}> Alertas para Zona {zone} ({len(alerts)} alertas):{RESET}\n")
            for alt in alerts:
                print(alt + "\n")
            print("Aperte ENTER para voltar")
        case "UNREG_LIST":
            print(f"{MAGENTA}> Lista de zonas disponíveis{RESET}\n")
            print("A\nB\nC\n")
            print("Digite enter para voltar ")
        case "REG_UNSB":
            print(f"{MAGENTA}> Cancelar inscrição{RESET}\n")
            print(f"Tem certeza de que deseja cancelar sua inscrição na zona {zone} (S / N)? ")
        case "UNREG_EXIT":
            print("Você não está inscrito em nenhuma zona e a defesa civil não poderá lhe enviar alertas. Tem certeza? (s / n): ")
        case _:
            print(f"{ORANGE}Ouvindo alertas em tempo real{RESET}")
            

def check_alerts():
    while True:
        try:
            msg, addr = sock.recvfrom(1024)
            alert = msg.decode()
            if alert.startswith("ALERTA DEFESA CIVIL"):
                now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                print("\033c", end="")
                header()
                print(f"{RED}!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! {now.split(" ")[0]} !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!{RESET}\n")
                print(f"{ORANGE}" + alert + f"{RESET}\n")
                print(f"{RED}!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!{RESET}\n")
                os.system('paplay /usr/share/sounds/freedesktop/stereo/suspend-error.oga')
                #os.system() #pra windows
                #os.system() #pra mac
                #os.system() #outras distros linux ???
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
                print(f"{MAGENTA}> Inscrever{RESET}\n")
                zona = input("Digite a sua zona: ")
                msg = f"WATCH|Zona_{zona.upper()}"
                sock.sendto(msg.encode(), server_addr)
                print("\033c", end="")
                print(f"{GREEN}Mensagem enviada.{RESET}")
                get_status()
                alert_thread = threading.Thread(target=check_alerts)
                alert_thread.start()
            else:
                screen_state = "REG_HIST"
                print(f"{MAGENTA}> Alertas para Zona {zone} ({len(alerts)} alertas):{RESET}\n")
                for alt in alerts:
                    msg_line = next((line for line in alt["message"].splitlines() if line.startswith("Mensagem:")), None)
                    print(f"{YELLOW}[{alt["timestamp"]}]{RESET}")
                    print(msg_line + "\n")
                input("Aperte ENTER para voltar")
                print("\033c", end="")


        case "2":
            if status == "UNREGISTERED":
                screen_state = "UNREG_LIST"
                header()
                print(f"{MAGENTA}> Lista de zonas disponíveis{RESET}\n")
                print("A\nB\nC\n")
                input("Digite enter para voltar ")
                print("\033c", end="")
            else:
                screen_state = "REG_UNSB"
                unregister = True
                header()
                print(f"{MAGENTA}> Cancelar inscrição{RESET}\n")
                resposta = input(f"{RED}Tem certeza de que deseja cancelar sua inscrição na zona {zone} (S / N)?{RESET} ")
                if resposta.upper() == "S":
                    msg = f"UNWATCH|Zona_{zone}"
                    sock.sendto(msg.encode(), server_addr)
                    print("\033c", end="")
                    print(f"{RED}Inscrição cancelada{RESET}")
                    get_status()
                else:
                    continue
                unregister = False

        case "3":
            if status == "UNREGISTERED":
                screen_state = "UNREG_EXIT"
                confirm = input("Você não está inscrito em nenhuma zona e a defesa civil não poderá lhe enviar alertas. Tem certeza? (s / n): ")
                if(confirm == "s" or confirm == "S"):
                    screen_state = ""
                    exit(0)
                else:
                    print("\033c", end="")
                    continue
            else:
                screen_state = ""
                print("\033c", end="")
                exit(0)

        case _:
            break
