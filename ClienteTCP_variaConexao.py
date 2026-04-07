# Camila Huang 
# Xuanjun Jin
import socket
import threading
import sys

IP_SERVIDOR = '10.0.11.107'  # Ou IP do servidor na rede
PORTA = 10419

def receber_mensagens(cliente):
    """Thread separada APENAS para RECEBER mensagens do servidor"""
    while True:
        try:
            msg = cliente.recv(1024).decode('utf-8')  # Recebe mensagem do servidor
            if not msg:  # Se não recebeu nada, conexão foi fechada
                break
            # Exibe a mensagem recebida (já vem formatada do servidor)
            print(f"\n{msg}")  # Mostra a mensagem (ex: "João: Olá pessoal")
            print("Você: ", end='', flush=True)  # Reexibe o prompt para digitar
        except:
            print("\n[ERRO] Conexão perdida com o servidor!")
            break

def cliente():
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Cria socket TCP
    
    try:
        cliente.connect((IP_SERVIDOR, PORTA))  # Tenta conectar ao servidor
        print(f"Conectado ao servidor {IP_SERVIDOR}:{PORTA}")
    except:
        print("Erro: Não foi possível conectar ao servidor")
        return
    
    # 1. Primeiro, recebe a solicitação de apelido (BLOQUEANTE)
    msg_inicial = cliente.recv(1024).decode('utf-8')  # Aguarda mensagem do servidor
    
    if msg_inicial.startswith("APELIDO:"):  # Verifica se é pedido de apelido
        # 2. Pede o apelido para o usuário
        apelido = input("Digite seu apelido: ")
        # 3. Envia o apelido para o servidor
        cliente.send(apelido.encode('utf-8'))
    
    # 4. Inicia a thread para receber mensagens (a partir de agora, assíncrono)
    thread_receber = threading.Thread(target=receber_mensagens, args=(cliente,))
    thread_receber.daemon = True  # Thread fecha quando o programa principal termina
    thread_receber.start()  # Inicia a thread de recebimento
    
    # 5. Loop principal para enviar mensagens
    print("\nConectado ao chat! Digite 'sair' para encerrar\n")
    
    while True:
        try:
            msg = input("Você: ")  # Lê o que o usuário digita
            if msg.lower() == 'sair':  # Se digitou 'sair' (case insensitive)
                cliente.send(msg.encode('utf-8'))  # Envia comando de saída
                break  # Sai do loop
            cliente.send(msg.encode('utf-8'))  # Envia mensagem normal
        except KeyboardInterrupt:  # Ctrl+C pressionado
            break
        except:  # Outros erros
            print("Erro ao enviar mensagem")
            break
    
    cliente.close()  # Fecha a conexão com o servidor
    print("Desconectado do servidor.")

if __name__ == "__main__":
    cliente()
