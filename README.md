**Universidade Federal de Pernambuco**  
**Centro de Informática**  
**Disciplina:** CIN0143 - Introdução aos Sistemas Distribuídos e Redes de Computadores  
**Docente:** David J M Cavalcanti  
**Atividade:** APS02 - Sistemas Distribuídos com Socket UDP  

---

## Introdução

Este projeto implementa um **Sistema de Alertas da Defesa Civil** usando **Socket UDP** para comunicação entre clientes, servidor e operador. O sistema permite que clientes se inscrevam em zonas de risco e recebam alertas em tempo real quando a Defesa Civil emite avisos para essas zonas.

### Características Principais

- ✅ Comunicação via **Socket UDP** 
- ✅ Gerenciamento de **3 zonas de risco** (Zona_A, Zona_B, Zona_C)
- ✅ **Inscrição e desinscrição** de clientes em zonas
- ✅ **Broadcast de alertas** para múltiplos clientes
- ✅ **Interface de operador** para simulação da Defesa Civil
- ✅ **Testes automatizados** para validação do sistema

---

## Arquitetura do Sistema

```
                    ┌──────────────────────┐
                    │   SERVIDOR UDP       │
                    │   (localhost:5000)   │
                    └──────────────────────┘
                              │
                ┌─────────────┼─────────────┐
                │             │             │
            ┌───────┐   ┌──────────┐   ┌──────────┐
            │CLIENT1│   │ CLIENT2  │   │ CLIENT3  │
            │Zona_A │   │ Zona_B   │   │ Zona_C   │
            └───────┘   └──────────┘   └──────────┘
                │             │             │
                └─────────────┼─────────────┘
                              ▲
                              │
                    ┌──────────────────────┐
                    │   OPERADOR DEFESA    │
                    │      CIVIL           │
                    │  (Envia Alertas)     │
                    └──────────────────────┘
```

---

## Responsabilidades das Pessoas

| Pessoa | Responsabilidade | Status |
|--------|------------------|--------|
| **Guilherme Barbosa** | Servidor UDP e Gerenciamento de Clientes | ✅ Completo |
| **Gabriel Fonseca** | Gerenciamento de Zonas de Risco | ✅ Completo |
| **Rodrigo de Andrade** | Sistema de Alertas (Push) | ⏳ Em Desenvolvimento |
| **Iranildo Felipe** | Cliente UDP | ✅ Completo |
| **Thiago Bernardo** | Operador, Testes e Documentação | ✅ Completo |

### Detalhes de Cada Responsabilidade

#### Guilherme - Servidor UDP
- Criar servidor UDP escutando em `localhost:5000`
- Receber mensagens dos clientes e operador
- Interpretar comandos (WATCH, UNWATCH, ALERT, FIND)
- Encaminhar requisições para outros módulos

#### Gabriel - Gerenciamento de Zonas
- Manter estrutura de dados das zonas
- Controlar inscrições de clientes
- Manter lista de clientes por zona
- Garantir remoção de clientes desconectados

#### Rodrigo - Sistema de Alertas (Push)
**[FALTANDO - Aguardando implementação]**
- Receber alertas do operador
- Identificar zona afetada
- Distribuir alerta para todos os inscritos
- Garantir envio para múltiplos clientes simultaneamente

#### Iranildo - Cliente UDP
- Permitir inscrição em zonas
- Manter socket UDP ativo
- Receber e exibir alertas
- Interface interativa via terminal

#### Thiago - Operador, Testes e Documentação
- ✅ Criar simulador do operador da Defesa Civil
- ✅ Enviar alertas ao servidor
- ✅ Realizar testes integrados
- ✅ Produzir documentação do projeto

---

## Estrutura de Arquivos

```
APS02-Grupo4-main/
├── README.md                 # Este arquivo
├── operador_teste.py         # Simulador do operador (Pessoa 5)
├── testes.py                 # Testes automatizados (Pessoa 5)
├── server/
│   ├── servidor.py           # Servidor UDP principal (Pessoa 1)
│   ├── protocolo.py          # Protocolo de mensagens
│   ├── zona.py               # Gerenciamento de zonas (Pessoa 2)
│   └── clientes.py           # Registro de clientes
└── client/
    └── cliente.py            # Cliente UDP (Pessoa 4)
```

---

## Protocolo de Comunicação

O sistema utiliza um protocolo baseado em **mensagens delimitadas por pipe (`|`)**:

### Comando: WATCH (Inscrever em Zona)

**Formato:** `WATCH|Zona_X`

**Origem:** Cliente  
**Destino:** Servidor  
**Descrição:** Cliente se inscreve em uma zona para receber alertas

**Exemplo:**
```
Cliente → Servidor: WATCH|Zona_A
Servidor → Cliente: OK|Inscrito em Zona_A
```

---

### Comando: UNWATCH (Desinscrever de Zona)

**Formato:** `UNWATCH|Zona_X`

**Origem:** Cliente  
**Destino:** Servidor  
**Descrição:** Cliente se desinscreve de uma zona

**Exemplo:**
```
Cliente → Servidor: UNWATCH|Zona_B
Servidor → Cliente: OK|Removido de Zona_B
```

---

### Comando: ALERT (Enviar Alerta)

**Formato:** `ALERT|Zona_X|Mensagem`

**Origem:** Operador  
**Destino:** Servidor  
**Descrição:** Operador envia alerta para todos os inscritos em uma zona

**Exemplo:**
```
Operador → Servidor: ALERT|Zona_A|Risco de deslizamento na encosta
Servidor → Clientes: ALERTA DEFESA CIVIL
           Zona: Zona_A
           Mensagem: Risco de deslizamento na encosta
```

---

### Comando: FIND (Verificar Zona)

**Formato:** `FIND`

**Origem:** Cliente  
**Destino:** Servidor  
**Descrição:** Cliente verifica em qual zona está inscrito

**Exemplo:**
```
Cliente → Servidor: FIND
Servidor → Cliente: Zona_A
           (ou NONE se não inscrito)
```

---

### Comando: ERRO (Mensagem de Erro)

**Formato:** `ERRO|Descrição`

**Origem:** Servidor  
**Destino:** Cliente  
**Descrição:** Servidor responde com erro se mensagem for inválida

**Exemplo:**
```
Servidor → Cliente: ERRO|Mensagem inválida
```

---

## Como Executar

### Pré-requisitos

- Python 3.7+
- Sistema operacional: Windows, Linux ou macOS
- Terminal/Console

### Passo 1: Iniciar o Servidor

Abra um terminal e execute:

```bash
cd server
python servidor.py
```

**Saída Esperada:**
```
==================================================
Servidor UDP iniciado na porta 5000
==================================================
```

---

### Passo 2: Iniciar o Cliente (em outro terminal)

```bash
cd client
python cliente.py
```

**Interface do Cliente:**
```
------------------------------------------------------------------------------------------------
------------------------------ Sistema de Alertas da Defesa Civil ------------------------------
------------------------------------------------------------------------------------------------

Cliente não está inscrito em nenhuma zona. Deseja inscrever-se?

1 - Sim
2 - Listar zonas
3 - Não (sair)
-> 
```

---

### Passo 3: Iniciar o Operador (em outro terminal)

```bash
python operador_teste.py
```

**Interface do Operador:**
```
================================================================================
 SISTEMA DE ALERTAS DA DEFESA CIVIL - OPERADOR
================================================================================

1 - Enviar Alerta
2 - Ver Histórico de Alertas
3 - Listar Zonas Disponíveis
4 - Enviar Alerta Rápido (Predefinido)
5 - Sair

Digite sua opção (1-5): 
```

---

## Testes Integrados

### Executando os Testes

Para executar os testes automatizados:

```bash
python testes.py
```

### Testes Disponíveis

O arquivo `testes.py` contém **7 testes automatizados**:

| # | Teste | Descrição |
|---|-------|-----------|
| 1 | Conexão Básica | Verifica se servidor responde |
| 2 | Inscrição em Zona | Testa comando WATCH |
| 3 | Verificar Zona | Testa comando FIND |
| 4 | Mudar de Zona | Testa troca de zona |
| 5 | Desinscrição | Testa comando UNWATCH |
| 6 | Envio de Alerta | Testa broadcast de alertas |
| 7 | Mensagem Inválida | Testa rejeição de erros |




## 📝 Exemplos de Uso

### Exemplo 1: Fluxo Básico (Cliente Inscrito e Recebendo Alerta)

**Terminal 1 - Servidor:**
```bash
$ python server/servidor.py
==================================================
Servidor UDP iniciado na porta 5000
==================================================

[RECEBIDO] ('127.0.0.1', 54321) -> WATCH|Zona_A
[INFO] ('127.0.0.1', 54321) inscrito em Zona_A

[RECEBIDO] ('127.0.0.1', 54322) -> ALERT|Zona_A|Risco de deslizamento
[ALERTA] Enviando alerta para Zona_A
[ENVIADO] -> ('127.0.0.1', 54321)
```

**Terminal 2 - Cliente:**
```bash
$ python client/cliente.py
# [Cliente escolhe opção 1, inscreve em Zona_A]
# [Cliente recebe ALERTA DEFESA CIVIL com a mensagem]
```

**Terminal 3 - Operador:**
```bash
$ python operador_teste.py
[INFO] Operador conectado ao servidor em localhost:5000

Digite sua opção (1-5): 1
> Inscrever

Digite a sua zona: A
Informe a mensagem do alerta: Risco de deslizamento

[✓] Alerta enviado com sucesso para Zona_A
```

---

### Exemplo 2: Múltiplos Clientes em Diferentes Zonas

**Cenário:**
- Cliente 1 inscrito em Zona_A
- Cliente 2 inscrito em Zona_B
- Operador envia alerta para Zona_A

**Resultado:**
- ✅ Cliente 1 recebe alerta
- ❌ Cliente 2 NÃO recebe alerta (não inscrito em Zona_A)

---

### Exemplo 3: Troca de Zona

**Sequência:**
1. Cliente inscreve em Zona_A
2. Cliente vê `FIND` → resposta: `Zona_A`
3. Cliente inscreve em Zona_B
4. Cliente vê `FIND` → resposta: `Zona_B` (automaticamente removido de Zona_A)

---

## Detalhes de Implementação

### Zonas Disponíveis

O sistema suporta 3 zonas de risco:

| Zona | Descrição | Exemplo de Alerta |
|------|-----------|-------------------|
| **Zona_A** | Setor Norte (Encostas e Morros) | Risco de deslizamento na encosta |
| **Zona_B** | Setor Central (Comercial e Residencial) | Alagamento em rua principal |
| **Zona_C** | Setor Sul (Industrial e Portuário) | Vazamento químico industrial |



## Fluxograma de Estados (Cliente)

```
┌─────────────────┐
│   DESCONECTADO  │
└────────┬────────┘
         │ WATCH|Zona_X
         ▼
┌──────────────────┐       ┌──────────────────┐
│ INSCRITO EM ZONA │◄──────┤ AGUARDANDO ALERTA│
└────────┬─────────┘       └──────────────────┘
         │                         ▲
         │ UNWATCH|Zona_X          │
         │                    Alerta recebido
         ▼                         │
┌─────────────────┐
│   DESCONECTADO  │
└─────────────────┘
```

---
