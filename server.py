import socket, threading, server_utils

HOST, PORT = '0.0.0.0', 65432
clients = {}
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.bind((HOST,PORT))
    sock.listen()

    while True:
        conn, addr = sock.accept()
        nickname_len = int.from_bytes(conn.recv(8), 'big')
        
        nickname_str = conn.recv(nickname_len).decode()
        
        clients.setdefault(conn, nickname_str) 
        server_utils.broadcast_sytem(clients, f'{nickname_str} подключился', conn)
        threading.Thread(target=server_utils.handle_client, args = (conn, clients), daemon = True).start()
        