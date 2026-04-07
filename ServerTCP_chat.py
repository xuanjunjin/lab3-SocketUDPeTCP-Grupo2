import socket
import threading

PORTA = 10419
IP = '10.0.11.107'  # IP onde o servidor vai rodar

def receber_mensagens(conn):
    """Função para receber mensagens em thread separada"""
    while True:
        try:
            data = conn.recv(1024)  # Recebe dados do cliente (máx 1024 bytes)
            if not data:  # Se não recebeu nada, cliente desconectou
                break
            mensagem = data.decode('utf-8')  # Converte bytes para string
            if mensagem == 'QUIT':  # Se cliente enviou QUIT
                print("\n[Cliente encerrou o chat]")
                return False
            print(f"\n[Cliente]: {mensagem}")  # Mostra mensagem do cliente
            print("Você: ", end='', flush=True)  # Reexibe o prompt para digitar
        except:  # Em caso de erro (ex: conexão perdida)
            break
    return True

def servidor_chat():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Cria socket TCP
    servidor.bind((IP, PORTA))  # Associa o socket ao IP e porta
    servidor.listen(1)  # Aguarda conexão (máximo 1 cliente na fila)
    
    print(f"Servidor aguardando conexão na porta {PORTA}...")
    conn, addr = servidor.accept()  # Aceita a conexão do cliente
    print(f"Conectado a: {addr}")
    print("Digite 'QUIT' para encerrar o chat\n")
    
    # Thread para receber mensagens em segundo plano
    thread_receber = threading.Thread(target=receber_mensagens, args=(conn,))
    thread_receber.daemon = True  # Thread fecha quando o programa principal termina
    thread_receber.start()  # Inicia a thread
    
    # Loop principal para enviar mensagens
    while True:
        mensagem = input("Você: ")  # Lê o que o servidor digita
        conn.send(mensagem.encode('utf-8'))  # Envia mensagem para o cliente
        
        if mensagem == 'QUIT':  # Se servidor digitou QUIT
            print("Encerrando chat...")
            break
    
    conn.close()  # Fecha conexão com o cliente
    servidor.close()  # Fecha o socket do servidor

if __name__ == "__main__":  # Executa apenas se for o arquivo principal
    servidor_chat()
