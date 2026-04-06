# lab3-SocketUDPeTCP-Grupo2

**Disciplina:** Redes de Computadores  
**Integrantes:** Camila Huang / Xuanjun Jin  
**Turma:** 5N

---

## 📋 Índice

- [Sobre o Projeto](#sobre-o-projeto)
- [Parte 2 - Chat Simples](#parte-2---chat-simples)
- [Parte 3 - Chat Multiplayer com Threads](#parte-3---chat-multiplayer-com-threads)
- [Como Executar](#como-executar)
- [Vídeos Demonstrativos](#vídeos-demonstrativos)

---

## Sobre o Projeto

Este projeto foi desenvolvido como parte da disciplina de Redes de Computadores, com o objetivo de explorar e implementar comunicação via sockets em Python, utilizando os protocolos **TCP** e **UDP**.

O trabalho está dividido em três partes:

1. **Questão teórica** sobre comportamento de sockets TCP vs UDP
2. **Chat simples** (um cliente, um servidor) com comando `QUIT`
3. **Chat multiplayer** com suporte a múltiplas conexões simultâneas usando **threads**

---

## Parte 2 - Chat Simples

### Descrição

Chat básico onde um servidor e um cliente trocam mensagens em tempo real. O chat é encerrado quando qualquer uma das partes digita o comando `QUIT`.

### Características

- Protocolo **TCP** (garante entrega e ordem das mensagens)
- Porta definida pelos **primeiros 5 números do TIA** (exemplo: 10419)
- Comunicação bidirecional (ambos enviam e recebem)
- Encerramento elegante com comando `QUIT`

### Como testar

1. **Inicie o servidor:**
   ```bash
   python ServerTCP_chat.py

2. **Em outro terminal, inicie o cliente:**

    ```bash
    python ClienteTCP_chat.py

3. **Digite mensagens** de ambos os lados

4. **Para encerrar**, digite QUIT em qualquer um dos dois

## Parte 3 - Chat Multiplayer com Threads

### Descrição

Um chat em grupo onde **múltiplos clientes** podem se conectar simultaneamente ao servidor e trocar mensagens entre si. Cada cliente é tratado em uma **thread separada**, permitindo que o servidor atenda várias conexões ao mesmo tempo.

### Funcionalidades

| Funcionalidade | Descrição |
|----------------|-----------|
| **Múltiplas conexões** | Suporta vários clientes simultâneos |
| **Threads** | Cada cliente roda em uma thread independente |
| **Broadcast** | Mensagens são enviadas para todos os clientes conectados |
| **Notificações** | Entrada e saída de usuários são anunciadas ao grupo |
| **Apelidos** | Cada cliente escolhe um nome ao entrar |
| **Comando sair** | Cliente digita `sair` para desconectar |

### Como testar

1. **Inicie o servidor:**
   ```bash
   python Server_variaConexao.py


2. **Em terminais separados, inicie os clientes:**
```bash
python Cliente_variaConexao.py
```

* Digite um apelido quando solicitado
* Envie mensagens - todos os clientes conectados receberão
* Para sair, digite `sair`

### Exemplo de execução

**Terminal 1 (Servidor):**
```text
Servidor rodando em 127.0.0.1:5000
Ana conectou de ('127.0.0.1', 54321) - Total: 1
Bruno conectou de ('127.0.0.1', 54322) - Total: 2
Carlos conectou de ('127.0.0.1', 54323) - Total: 3
Bruno: Olá pessoal!
Carlos desconectou - Total: 2
```

**Terminal 2 (Cliente Ana):**
```text
Digite seu apelido: Ana
[Bruno entrou no chat]
[Carlos entrou no chat]
Bruno: Olá pessoal!
Você: Oi Bruno!
[Carlos saiu do chat]
```

---

## Como Executar

* No servidor: Descubra o IP local
  * Windows: `ipconfig`
  * Linux/Mac: `ifconfig` ou `ip addr`
* No servidor: Configure `IP = 'IP_SERVIDOR'` (escuta em todas as interfaces)
* Nos clientes: Configure `IP_SERVIDOR = 'IP_DO_SERVIDOR'`
* Certifique-se que a porta está liberada no firewall

---

## Vídeos Demonstrativos

| Vídeo | Conteúdo | Link |
|-------|----------|------|
| Vídeo 1 | Questões 1 e 2 + demonstração do chat simples | Assistir no YouTube |
| Vídeo 2 | Questão 3 - Chat multiplayer com threads | Assistir no YouTube |
