# Camila Huang
# Xuanjun Jin
import socket
import threading

PORTA = 10419
IP = '10.0.11.107'

clientes = []  # Lista de (conexao, apelido) - guarda todos os clientes conectados
lock = threading.Lock()  # Lock para evitar conflitos ao acessar a lista de clientes

def broadcast(mensagem, remetente=None):
    """Envia mensagem para todos os clientes, exceto o remetente"""
    with lock:  # Garante que ninguém mexe na lista enquanto enviamos
        for conn, apelido in clientes:  # Percorre todos os clientes
            if conn != remetente:  # Não envia para quem enviou a mensagem
                try:
                    conn.send(mensagem.encode('utf-8'))  # Envia a mensagem
                except:
                    pass  # Se falhar, ignora (cliente pode ter desconectado)

def tratar_cliente(conn, addr):
    """Thread para cada cliente - gerencia um cliente específico"""
    try:
        # 1. Primeiro, pede o apelido AO CLIENTE
        conn.send("APELIDO:".encode('utf-8'))  # Solicita o apelido
        
        # 2. Aguarda a resposta do apelido (bloqueante)
        apelido = conn.recv(1024).decode('utf-8').strip()  # Recebe o apelido escolhido
        
        # 3. Adiciona à lista de clientes
        with lock:  # Usa lock para evitar problemas com múltiplas threads
            clientes.append((conn, apelido))  # Guarda conexão e apelido
        
        # 4. Avisa todos que o cliente entrou
        broadcast(f"[{apelido} entrou no chat]", conn)  # Mensagem para todos
        print(f"{apelido} conectou de {addr} - Total: {len(clientes)}")  # Log no servidor
        
        # 5. Envia mensagem de boas-vindas APENAS para o cliente que entrou
        conn.send(f"Bem-vindo ao chat, {apelido}! Digite 'sair' para encerrar.\n".encode('utf-8'))
        
        # 6. Loop de recebimento de mensagens
        while True:
            msg = conn.recv(1024).decode('utf-8').strip()  # Recebe mensagem do cliente
            if not msg:  # Se não recebeu nada, cliente desconectou
                break
            if msg.lower() == 'sair':  # Comando de saída
                break
            print(f"{apelido}: {msg}")  # Mostra no console do servidor
            broadcast(f"{apelido}: {msg}", conn)  # Envia para todos (exceto remetente)
    
    except Exception as e:  # Captura qualquer erro
        print(f"Erro com cliente {addr}: {e}")
    
    finally:  # Sempre executa, mesmo com erro
        # Remove cliente da lista
        with lock:
            if (conn, apelido) in clientes:  # Verifica se ainda está na lista
                clientes.remove((conn, apelido))  # Remove o cliente
        conn.close()  # Fecha a conexão
        broadcast(f"[{apelido} saiu do chat]")  # Avisa todos que saiu
        print(f"{apelido} desconectou - Total: {len(clientes)}")  # Log no servidor

def servidor():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Cria socket TCP
    servidor.bind((IP, PORTA))  # Associa ao IP e porta
    servidor.listen(5)  # Aceita até 5 conexões na fila
    print(f"=== CHAT MULTIPLAYER ===")
    print(f"Servidor rodando em {IP}:{PORTA}")
    print(f"Aguardando conexões...\n")
    
    while True:  # Loop infinito aceitando novos clientes
        conn, addr = servidor.accept()  # Aceita nova conexão
        thread = threading.Thread(target=tratar_cliente, args=(conn, addr))  # Cria thread para o cliente
        thread.daemon = True  # Thread fecha quando servidor fechar
        thread.start()  # Inicia a thread

if __name__ == "__main__":
    servidor()  # Inicia o servidor
