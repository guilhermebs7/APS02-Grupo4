# Protocolo de Alertas

Este módulo documenta o formato de comunicação usado pelo sistema de alertas em UDP.

## Mensagem do operador para o servidor

O operador envia um datagrama UDP ao servidor com o comando abaixo.

Formato:

```text
ALERT|zona_A|Risco de deslizamento
```

Campos:

1. `ALERT`: comando que identifica a operação de broadcast.
2. `zona_A`: zona afetada. O módulo aceita `zona_A`, `Zona_A`, `A`, `B` e `C`, normalizando para `Zona_A`, `Zona_B` e `Zona_C`.
3. `Risco de deslizamento`: conteúdo livre da mensagem.

## Mensagem enviada aos clientes

O servidor replica o alerta como datagrama UDP para todos os clientes inscritos.

O payload segue este formato:

```text
ALERTA DEFESA CIVIL
Zona: Zona_A
Mensagem: Risco de deslizamento
```

## Regras do broadcast

- O envio é feito em memória, usando a lista de inscritos da zona.
- Destinos repetidos são removidos antes do `sendto`.
- A mesma mensagem é replicada instantaneamente para todos os clientes registrados na zona.