import socket
import threading

PORTA = 10419
IP = '10.0.11.107'

clientes = []  # Lista de (conexao, apelido)
lock = threading.Lock()

def broadcast(mensagem, remetente=None):
    """Envia mensagem para todos os clientes, exceto o remetente"""
    with lock:
        for conn, apelido in clientes:
            if conn != remetente:
                try:
                    conn.send(mensagem.encode('utf-8'))
                except:
                    pass

def tratar_cliente(conn, addr):
    """Thread para cada cliente"""
    try:
        # 1. Primeiro, pede o apelido AO CLIENTE
        conn.send("APELIDO:".encode('utf-8'))
        
        # 2. Aguarda a resposta do apelido (bloqueante)
        apelido = conn.recv(1024).decode('utf-8').strip()
        
        # 3. Adiciona à lista de clientes
        with lock:
            clientes.append((conn, apelido))
        
        # 4. Avisa todos que o cliente entrou
        broadcast(f"[{apelido} entrou no chat]", conn)
        print(f"{apelido} conectou de {addr} - Total: {len(clientes)}")
        
        # 5. Envia mensagem de boas-vindas APENAS para o cliente que entrou
        conn.send(f"Bem-vindo ao chat, {apelido}! Digite 'sair' para encerrar.\n".encode('utf-8'))
        
        # 6. Loop de recebimento de mensagens
        while True:
            msg = conn.recv(1024).decode('utf-8').strip()
            if not msg:
                break
            if msg.lower() == 'sair':
                break
            print(f"{apelido}: {msg}")
            broadcast(f"{apelido}: {msg}", conn)
    
    except Exception as e:
        print(f"Erro com cliente {addr}: {e}")
    
    finally:
        # Remove cliente da lista
        with lock:
            if (conn, apelido) in clientes:
                clientes.remove((conn, apelido))
        conn.close()
        broadcast(f"[{apelido} saiu do chat]")
        print(f"{apelido} desconectou - Total: {len(clientes)}")

def servidor():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((IP, PORTA))
    servidor.listen(5)
    print(f"=== CHAT MULTIPLAYER ===")
    print(f"Servidor rodando em {IP}:{PORTA}")
    print(f"Aguardando conexões...\n")
    
    while True:
        conn, addr = servidor.accept()
        thread = threading.Thread(target=tratar_cliente, args=(conn, addr))
        thread.daemon = True
        thread.start()

if __name__ == "__main__":
    servidor()