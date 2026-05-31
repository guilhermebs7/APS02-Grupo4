import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_addr = ('localhost', 5000)

while True:
    alert = input("Mensagem de alerta: ")
    zona = input("Zona do alerta: ")

    msg = f"ALERT|Zona_{zona}|{alert}"

    sock.sendto(msg.encode(), server_addr)
    print("Mensagem enviada")
