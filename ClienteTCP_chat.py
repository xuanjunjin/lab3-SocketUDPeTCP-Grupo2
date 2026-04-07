# Camila Huang
# Xuanjun Jin
import socket
import threading

PORTA = 10419 
IP_SERVIDOR = '10.0.11.107'  # IP do servidor

def receber_mensagens(cliente):
    """Função para receber mensagens em thread separada"""
    while True:
        try:
            data = cliente.recv(1024)  # Recebe dados do servidor (máx 1024 bytes)
            if not data:  # Se não recebeu nada, conexão foi fechada
                break
            mensagem = data.decode('utf-8')  # Converte bytes para string
            if mensagem == 'QUIT':  # Se servidor enviou QUIT
                print("\n[Servidor encerrou o chat]")
                return False
            print(f"\n[Servidor]: {mensagem}")  # Mostra mensagem do servidor
            print("Você: ", end='', flush=True)  # Reexibe o prompt para digitar
        except:  # Em caso de erro (ex: conexão perdida)
            break
    return True

def cliente_chat():
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Cria socket TCP
    
    try:
        cliente.connect((IP_SERVIDOR, PORTA))  # Tenta conectar ao servidor
        print(f"Conectado ao servidor {IP_SERVIDOR}:{PORTA}")
        print("Digite 'QUIT' para encerrar o chat\n")
    except:  # Se não conseguir conectar
        print("Erro: Não foi possível conectar ao servidor")
        return
    
    # Thread para receber mensagens em segundo plano
    thread_receber = threading.Thread(target=receber_mensagens, args=(cliente,))
    thread_receber.daemon = True  # Thread fecha quando o programa principal termina
    thread_receber.start()  # Inicia a thread
    
    # Loop principal para enviar mensagens
    while True:
        mensagem = input("Você: ")  # Lê o que o usuário digita
        cliente.send(mensagem.encode('utf-8'))  # Envia mensagem para o servidor
        
        if mensagem == 'QUIT':  # Se usuário digitou QUIT
            print("Encerrando chat...")
            break
    
    cliente.close()  # Fecha a conexão com o servidor

if __name__ == "__main__":  # Executa apenas se for o arquivo principal
    cliente_chat()
