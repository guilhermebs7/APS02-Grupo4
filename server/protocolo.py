def interpretar_mensagem(msg):
    partes = msg.strip().split("|")

    comando = partes[0]

    if comando == "WATCH" and len(partes) == 2:
        return {
            "tipo": "WATCH",
            "zona": partes[1]
        }

    elif comando == "UNWATCH" and len(partes) == 2:
        return {
            "tipo": "UNWATCH",
            "zona": partes[1]
        }

    elif comando == "ALERT" and len(partes) >= 3:
        return {
            "tipo": "ALERT",
            "zona": partes[1],
            "mensagem": "|".join(partes[2:])
        }
    elif comando == "FIND":
        return {
            "tipo": "FIND"
        }

    return None