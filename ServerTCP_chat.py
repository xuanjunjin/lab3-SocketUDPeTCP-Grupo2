import socket
import threading

PORTA = 10419
IP = '10.0.11.107'  

def receber_mensagens(conn):
    """Função para receber mensagens em thread separada"""
    while True:
        try:
            data = conn.recv(1024)
            if not data:
                break
            mensagem = data.decode('utf-8')
            if mensagem == 'QUIT':
                print("\n[Cliente encerrou o chat]")
                return False
            print(f"\n[Cliente]: {mensagem}")
            print("Você: ", end='', flush=True)
        except:
            break
    return True

def servidor_chat():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((IP, PORTA))
    servidor.listen(1)
    
    print(f"Servidor aguardando conexão na porta {PORTA}...")
    conn, addr = servidor.accept()
    print(f"Conectado a: {addr}")
    print("Digite 'QUIT' para encerrar o chat\n")
    
    # Thread para receber mensagens
    thread_receber = threading.Thread(target=receber_mensagens, args=(conn,))
    thread_receber.daemon = True
    thread_receber.start()
    
    # Loop para enviar mensagens
    while True:
        mensagem = input("Você: ")
        conn.send(mensagem.encode('utf-8'))
        
        if mensagem == 'QUIT':
            print("Encerrando chat...")
            break
    
    conn.close()
    servidor.close()

if __name__ == "__main__":
    servidor_chat()