import socket

from protocolo import interpretar_mensagem
from clientes import (
    adicionar_cliente,
    remover_cliente,
    listar_clientes
)

from zona import ControleZonas

HOST = "0.0.0.0"
PORTA = 5000

# cria o socket UDP
servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# associa IP e porta
servidor.bind((HOST, PORTA))

print("=" * 50)
print(f"Servidor UDP iniciado na porta {PORTA}")
print("=" * 50)


controlador = ControleZonas()

while True:
    try:
        
        dados, endereco = servidor.recvfrom(1024)

        mensagem = dados.decode()

        print(f"\n[RECEBIDO] {endereco} -> {mensagem}")

       
        adicionar_cliente(endereco)

       
        protocolo = interpretar_mensagem(mensagem)

        if protocolo is None:
            resposta = "ERRO|Mensagem inválida"

            servidor.sendto(
                resposta.encode(),
                endereco
            )

            continue

        tipo = protocolo["tipo"]

      
        if tipo == "WATCH":

            zona = protocolo["zona"]

            sucesso = controlador.inscrever(
                zona,
                endereco
            )

            if sucesso:
                resposta = f"OK|Inscrito em {zona}"

                print(f"[INFO] {endereco} inscrito em {zona}")

            else:
                resposta = f"ERRO|Falha ao inscrever em {zona}"

            servidor.sendto(
                resposta.encode(),
                endereco
            )

        elif tipo == "UNWATCH":

            zona = protocolo["zona"]

            sucesso = controlador.desinscrever(
                zona,
                endereco
            )

            if sucesso:
                resposta = f"OK|Removido de {zona}"

                print(f"[INFO] {endereco} removido de {zona}")

            else:
                resposta = f"ERRO|Falha ao remover de {zona}"

            servidor.sendto(
                resposta.encode(),
                endereco
            )

        elif tipo == "ALERT":

            zona = protocolo["zona"]

            mensagem_alerta = protocolo["mensagem"]

            inscritos = controlador.listar_zona(zona)

            print(f"[ALERTA] Enviando alerta para {zona}")

            for cliente in inscritos:

                alerta = (
                    f"ALERTA DEFESA CIVIL\n"
                    f"Zona: {zona}\n"
                    f"Mensagem: {mensagem_alerta}"
                )

                servidor.sendto(
                    alerta.encode(),
                    cliente
                )

                print(f"[ENVIADO] -> {cliente}")

        elif tipo == "FIND":
            try:
                zona_cliente = controlador.clientes[endereco]
                msg = zona_cliente
                servidor.sendto(msg.encode(), endereco)
            except:
                msg = "NONE"
                servidor.sendto(msg.encode(), endereco)
            print("Mensagem enviada")
                

    except KeyboardInterrupt:
        print("\nServidor encerrado.")
        break

    except Exception as e:
        print(f"[ERRO] {e}")