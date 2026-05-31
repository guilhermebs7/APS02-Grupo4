# APS02 – Sistema Distribuído de Alertas da Defesa Civil utilizando Socket UDP

## Universidade Federal de Pernambuco

**Centro de Informática (CIn)**
**Disciplina:** CIN0143 - Introdução aos Sistemas Distribuídos e Redes de Computadores
**Docente:** Prof. David J. M. Cavalcanti

---

# Equipe 4

| Integrante         | Responsabilidade                         |
| ------------------ | ---------------------------------------- |
| Guilherme Barbosa  | Servidor UDP e Gerenciamento de Clientes |
| Gabriel Fonseca    | Gerenciamento de Zonas de Risco          |
| Rodrigo de Andrade | Sistema de Alertas (Push)                |
| Iranildo Felipe    | Cliente UDP                              |
| Thiago Bernardo    | Operador, Testes e Documentação          |

---

# 1. Introdução

Os sistemas distribuídos permitem que múltiplos dispositivos cooperem através de uma rede para executar tarefas de forma integrada. Uma das aplicações mais relevantes desse paradigma é a disseminação rápida de informações críticas para diversos usuários simultaneamente.

Neste projeto foi desenvolvido um **Sistema de Alertas da Defesa Civil** utilizando comunicação baseada em **Socket UDP**, permitindo que usuários se inscrevam em zonas de risco específicas e recebam alertas emitidos por um operador responsável.

A solução segue o modelo **Cliente-Servidor**, em que um servidor central gerencia inscrições de clientes, organiza as zonas de risco e distribui mensagens de alerta para os usuários cadastrados.

---

# 2. Objetivos

O objetivo deste projeto é implementar uma aplicação distribuída capaz de:

* Utilizar comunicação baseada em UDP;
* Permitir inscrição e remoção de clientes em zonas de risco;
* Gerenciar múltiplos clientes simultaneamente;
* Distribuir alertas em tempo real;
* Simular a atuação de um operador da Defesa Civil;
* Aplicar conceitos fundamentais de Sistemas Distribuídos.

---

# 3. Fundamentação Teórica

## 3.1 User Datagram Protocol (UDP)

O UDP (User Datagram Protocol) é um protocolo da camada de transporte que permite a troca de mensagens entre aplicações sem a necessidade de estabelecer uma conexão prévia.

Diferentemente do TCP, o UDP possui menor sobrecarga de comunicação, oferecendo maior velocidade na transmissão dos dados. Por esse motivo, é amplamente utilizado em aplicações que exigem rapidez na entrega das mensagens, como sistemas de monitoramento, streaming e alertas emergenciais.

Neste projeto, o UDP foi escolhido por sua simplicidade e eficiência na distribuição de alertas em tempo real.

---

## 3.2 Arquitetura Cliente-Servidor

O sistema adota uma arquitetura Cliente-Servidor.

O servidor central é responsável por:

* Receber mensagens dos clientes;
* Gerenciar inscrições em zonas de risco;
* Manter o cadastro dos clientes;
* Distribuir alertas emitidos pelo operador.

Os clientes atuam como receptores das informações, enquanto o operador representa a entidade responsável pela emissão dos alertas.

---

# 4. Arquitetura da Solução

A arquitetura do sistema é composta por três elementos principais:

1. Servidor UDP;
2. Clientes UDP;
3. Operador da Defesa Civil.

Fluxo geral de funcionamento:

1. O cliente se inscreve em uma zona de risco.
2. O servidor registra a inscrição.
3. O operador envia um alerta para uma determinada zona.
4. O servidor identifica os clientes inscritos.
5. O alerta é distribuído para todos os destinatários daquela zona.

Este comportamento implementa uma versão simplificada do padrão **Publish/Subscribe**, em que os clientes recebem apenas os eventos relacionados à zona de interesse.

---

# 5. Estrutura de Dados

As zonas de risco são armazenadas através de estruturas de dados que associam cada região aos respectivos clientes inscritos.

Exemplo conceitual:

```
zonas = {
    "Zona_A": [cliente1, cliente2],
    "Zona_B": [cliente3],
    "Zona_C": []
}
```

Cada cliente é identificado pelo endereço IP e pela porta UDP utilizada durante a comunicação.

---

# 6. Protocolo de Comunicação

A comunicação entre os componentes utiliza mensagens textuais delimitadas pelo caractere `|`.

## Inscrição em Zona

```
WATCH|Zona_A
```

Solicita a inscrição do cliente em uma zona de risco.

---

## Cancelamento de Inscrição

```
UNWATCH|Zona_A
```

Remove o cliente da zona especificada.

---

## Consulta de Zona

```
FIND
```

Retorna a zona atualmente associada ao cliente.

---

## Envio de Alerta

```
ALERT|Zona_A|Risco de deslizamento
```

Solicita o envio de um alerta para todos os clientes inscritos na zona especificada.

---

# 7. Implementação

O projeto foi desenvolvido utilizando a linguagem Python e a biblioteca Socket para comunicação em rede.

A implementação foi dividida em módulos independentes:

* Servidor UDP;
* Gerenciamento de Clientes;
* Gerenciamento de Zonas;
* Sistema de Alertas;
* Cliente UDP;
* Operador da Defesa Civil.

Essa modularização facilita a manutenção, os testes e futuras evoluções do sistema.

---

# 8. Estrutura do Projeto

```
APS02-Grupo4/

├── README.md
├── operador_teste.py
├── testes.py
│
├── server/
│   ├── servidor.py
│   ├── protocolo.py
│   ├── clientes.py
│   └── zona.py
│
└── client/
    └── cliente.py
```

---

# 9. Execução

## Iniciar o Servidor

```
cd server
python servidor.py
```

---

## Iniciar o Cliente

```
cd client
python cliente.py
```

---

## Iniciar o Operador

```
python operador_teste.py
```

---

# 10. Casos de Uso

## Inscrição em uma Zona

O cliente seleciona uma zona de risco para receber alertas.

Exemplo:

```
WATCH|Zona_A
```

---

## Consulta da Zona Atual

O cliente pode consultar sua inscrição atual.

Exemplo:

```
FIND
```

---

## Emissão de Alerta

O operador envia um alerta para determinada região.

Exemplo:

```
ALERT|Zona_A|Risco de deslizamento na encosta
```

Todos os clientes inscritos em `Zona_A` recebem a notificação.

---

# 11. Testes Realizados

Foram executados testes para validação das funcionalidades do sistema.

| Teste             | Objetivo                           | Resultado |
| ----------------- | ---------------------------------- | --------- |
| Conexão Básica    | Verificar comunicação com servidor | Aprovado  |
| Inscrição em Zona | Validar comando WATCH              | Aprovado  |
| Consulta de Zona  | Validar comando FIND               | Aprovado  |
| Mudança de Zona   | Validar atualização de inscrição   | Aprovado  |
| Desinscrição      | Validar comando UNWATCH            | Aprovado  |
| Envio de Alerta   | Validar distribuição de mensagens  | Aprovado  |
| Mensagem Inválida | Validar tratamento de erros        | Aprovado  |

---

# 12. Conceitos de Sistemas Distribuídos Aplicados

Durante o desenvolvimento foram aplicados diversos conceitos abordados na disciplina:

* Comunicação por troca de mensagens;
* Comunicação cliente-servidor;
* Protocolos de aplicação;
* Endereçamento por IP e porta;
* Comunicação assíncrona;
* Distribuição de eventos;
* Publish/Subscribe;
* Gerenciamento de múltiplos participantes.

---

# 13. Contribuições dos Integrantes

### Guilherme Barbosa

* Implementação do servidor UDP;
* Gerenciamento de clientes;
* Integração dos módulos.

### Gabriel Fonseca

* Implementação das estruturas de zonas;
* Controle de inscrições e cancelamentos.

### Rodrigo de Andrade

* Sistema de distribuição de alertas;
* Broadcast para múltiplos clientes.

### Iranildo Felipe

* Desenvolvimento do cliente UDP;
* Interface de interação via terminal.

### Thiago Bernardo

* Simulador do operador da Defesa Civil;
* Testes integrados;
* Documentação do projeto.

---

# 14. Conclusão

O sistema desenvolvido permitiu aplicar, na prática, conceitos fundamentais de Sistemas Distribuídos por meio da implementação de um Sistema de Alertas da Defesa Civil baseado em UDP.

A solução implementada possibilita o gerenciamento de clientes distribuídos, a organização de usuários em zonas de risco e a distribuição eficiente de alertas em tempo real.

Os resultados obtidos demonstram o correto funcionamento da arquitetura proposta e evidenciam a aplicabilidade dos conceitos estudados ao longo da disciplina.
