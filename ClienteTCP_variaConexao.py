import socket
import threading
import sys

IP_SERVIDOR = '10.0.11.107'  # Ou IP do servidor na rede
PORTA = 10419

def receber_mensagens(cliente):
    """Thread separada APENAS para RECEBER mensagens do servidor"""
    while True:
        try:
            msg = cliente.recv(1024).decode('utf-8')
            if not msg:
                break
            # Exibe a mensagem recebida (já vem formatada do servidor)
            print(f"\n{msg}")
            print("Você: ", end='', flush=True)
        except:
            print("\n[ERRO] Conexão perdida com o servidor!")
            break

def cliente():
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        cliente.connect((IP_SERVIDOR, PORTA))
        print(f"Conectado ao servidor {IP_SERVIDOR}:{PORTA}")
    except:
        print("Erro: Não foi possível conectar ao servidor")
        return
    
    # 1. Primeiro, recebe a solicitação de apelido (BLOQUEANTE)
    msg_inicial = cliente.recv(1024).decode('utf-8')
    
    if msg_inicial.startswith("APELIDO:"):
        # 2. Pede o apelido para o usuário
        apelido = input("Digite seu apelido: ")
        # 3. Envia o apelido para o servidor
        cliente.send(apelido.encode('utf-8'))
    
    # 4. Inicia a thread para receber mensagens (a partir de agora, assíncrono)
    thread_receber = threading.Thread(target=receber_mensagens, args=(cliente,))
    thread_receber.daemon = True
    thread_receber.start()
    
    # 5. Loop principal para enviar mensagens
    print("\nConectado ao chat! Digite 'sair' para encerrar\n")
    
    while True:
        try:
            msg = input("Você: ")
            if msg.lower() == 'sair':
                cliente.send(msg.encode('utf-8'))
                break
            cliente.send(msg.encode('utf-8'))
        except KeyboardInterrupt:
            break
        except:
            print("Erro ao enviar mensagem")
            break
    
    cliente.close()
    print("Desconectado do servidor.")

if __name__ == "__main__":
    cliente()