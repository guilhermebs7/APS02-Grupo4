"""Módulo de broadcast/push em UDP para alertas da Defesa Civil.

Este arquivo é carregado diretamente pelos testes e por isso não depende de
importação por pacote.
"""

from __future__ import annotations

from collections.abc import Iterable

ALERTA_PREFIXO = "ALERTA DEFESA CIVIL"


def normalizar_zona(zona: str) -> str:
	"""Normaliza a identificação da zona para o formato esperado pelo projeto."""

	zona_limpa = zona.strip()
	if not zona_limpa:
		raise ValueError("zona não pode estar vazia")

	if zona_limpa.lower().startswith("zona_"):
		sufixo = zona_limpa.split("_", 1)[1].strip()
		return f"Zona_{sufixo.upper()}"

	return f"Zona_{zona_limpa.upper()}"


def criar_mensagem_alerta(zona: str, mensagem: str) -> str:
	"""Monta a mensagem em formato de broadcast enviada aos clientes."""

	zona_formatada = normalizar_zona(zona)
	mensagem_limpa = mensagem.strip()

	if not mensagem_limpa:
		raise ValueError("mensagem não pode estar vazia")

	return (
		f"{ALERTA_PREFIXO}\n"
		f"Zona: {zona_formatada}\n"
		f"Mensagem: {mensagem_limpa}"
	)


def _destinos_unicos(destinos: Iterable[tuple[str, int]]) -> list[tuple[str, int]]:
	vistos = set()
	destinos_unicos = []

	for destino in destinos:
		if destino not in vistos:
			vistos.add(destino)
			destinos_unicos.append(destino)

	return destinos_unicos


def distribuir_alerta(sock, zona: str, mensagem: str, inscritos: Iterable[tuple[str, int]]):
	"""Envia o alerta via UDP para todos os inscritos únicos da zona.

	Retorna a quantidade de destinos que receberam a mensagem.
	"""

	alerta = criar_mensagem_alerta(zona, mensagem)
	destinos = _destinos_unicos(inscritos)

	for destino in destinos:
		sock.sendto(alerta.encode(), destino)

	return len(destinos)


def interpretar_alerta_operador(mensagem: str) -> tuple[str, str]:
	"""Interpreta mensagens no formato ALERT|zona|conteudo."""

	partes = mensagem.strip().split("|")

	if len(partes) < 3 or partes[0] != "ALERT":
		raise ValueError("mensagem de alerta inválida")

	zona = normalizar_zona(partes[1])
	conteudo = "|".join(partes[2:]).strip()

	if not conteudo:
		raise ValueError("mensagem de alerta vazia")

	return zona, conteudo


def processar_alerta_operador(sock, mensagem: str, inscritos: Iterable[tuple[str, int]]):
	"""Converte o alerta bruto do operador em broadcast UDP para a zona alvo.

	Esta função concentra a integração esperada pelo servidor: recebe a mensagem
	raw no formato `ALERT|zona|conteudo`, interpreta a zona afetada e distribui
	o alerta para todos os clientes inscritos.
	"""

	zona, conteudo = interpretar_alerta_operador(mensagem)
	return distribuir_alerta(sock, zona, conteudo, inscritos)
