import socket
import threading

PORTA = 10419 
IP_SERVIDOR = '10.0.11.107'  # IP do servidor

def receber_mensagens(cliente):
    """Função para receber mensagens em thread separada"""
    while True:
        try:
            data = cliente.recv(1024)
            if not data:
                break
            mensagem = data.decode('utf-8')
            if mensagem == 'QUIT':
                print("\n[Servidor encerrou o chat]")
                return False
            print(f"\n[Servidor]: {mensagem}")
            print("Você: ", end='', flush=True)
        except:
            break
    return True

def cliente_chat():
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        cliente.connect((IP_SERVIDOR, PORTA))
        print(f"Conectado ao servidor {IP_SERVIDOR}:{PORTA}")
        print("Digite 'QUIT' para encerrar o chat\n")
    except:
        print("Erro: Não foi possível conectar ao servidor")
        return
    
    # Thread para receber mensagens
    thread_receber = threading.Thread(target=receber_mensagens, args=(cliente,))
    thread_receber.daemon = True
    thread_receber.start()
    
    # Loop para enviar mensagens
    while True:
        mensagem = input("Você: ")
        cliente.send(mensagem.encode('utf-8'))
        
        if mensagem == 'QUIT':
            print("Encerrando chat...")
            break
    
    cliente.close()

if __name__ == "__main__":
    cliente_chat()