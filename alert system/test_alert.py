import importlib.util
from pathlib import Path
import unittest


def carregar_modulo_alerta():
    caminho = Path(__file__).resolve().with_name("alert.py")
    spec = importlib.util.spec_from_file_location("alert_system_alert", caminho)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


class SocketFake:
    def __init__(self):
        self.envios = []

    def sendto(self, dados, destino):
        self.envios.append((dados, destino))


class TestBroadcastAlertas(unittest.TestCase):
    def setUp(self):
        self.alerta = carregar_modulo_alerta()

    def test_distribuir_alerta_envia_para_todos_sem_repetir_destino(self):
        sock = SocketFake()
        inscritos = [
            ("127.0.0.1", 10001),
            ("127.0.0.1", 10002),
            ("127.0.0.1", 10001),
        ]

        total = self.alerta.distribuir_alerta(
            sock,
            "zona_a",
            "Risco de deslizamento",
            inscritos,
        )

        self.assertEqual(total, 2)
        self.assertEqual(len(sock.envios), 2)
        self.assertEqual(sock.envios[0][1], ("127.0.0.1", 10001))
        self.assertEqual(sock.envios[1][1], ("127.0.0.1", 10002))

    def test_interpretar_alerta_operador_normaliza_zona(self):
        zona, mensagem = self.alerta.interpretar_alerta_operador(
            "ALERT|zona_a|Chuva intensa"
        )

        self.assertEqual(zona, "Zona_A")
        self.assertEqual(mensagem, "Chuva intensa")


if __name__ == "__main__":
    unittest.main()