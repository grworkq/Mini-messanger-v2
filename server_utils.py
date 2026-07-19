import protocol

def relay_text(sock, clients):
    message_len = int.from_bytes(sock.recv(8), byteorder='big')
    message_for_users = bytearray()
    while len(message_for_users) < message_len:
        remaining = message_len - len(message_for_users)
        chunk = sock.recv(min(4096, remaining))
        
        if not chunk:
            raise ConnectionError('Клиент отключился')
        
        message_for_users.extend(chunk)
    
   
    for client in clients:
        if client != sock:
            client.sendall(protocol.TEXT.to_bytes(1))
            nickname = clients[sock].encode('utf-8')
            client.sendall(len(nickname).to_bytes(8, 'big'))
            client.sendall(nickname)
            client.sendall(message_len.to_bytes(8, byteorder='big'))
            client.sendall(message_for_users)
        
    
    

def relay_file(sock,clients):
    filename_len = int.from_bytes(sock.recv(8), byteorder='big')
    filename_str = sock.recv(filename_len).decode()
    file_size = int.from_bytes(sock.recv(8), byteorder='big')
    for client in clients:
            if client != sock:
                client.sendall(protocol.FILE.to_bytes(1, "big"))
                nickname = clients[sock].encode('utf-8')
                client.sendall(len(nickname).to_bytes(8))
                client.sendall(nickname)
                client.sendall(filename_len.to_bytes(8, "big"))
                client.sendall(filename_str.encode('utf-8'))
                client.sendall(file_size.to_bytes(8, "big"))
    recev = 0
    while recev < file_size:
        remaining = file_size - recev
        chunk = sock.recv(min(4096, remaining))
        if not chunk:
            raise ConnectionError('Клиент отключился')
        
        for client in clients:
            if client != sock:
                client.sendall(chunk)
        
        recev += len(chunk)
            

def relay_exit(sock, clients):
    if sock in clients:
        broadcast_sytem(clients, f'{clients[sock]} покинул чат.', exclude=sock)
        del clients[sock]
    sock.close()
    
def broadcast_sytem(clients, message, exclude=None):
    message = message.encode('utf-8')
    
    for client in clients:
        if client == exclude:
            continue
        
        client.sendall(protocol.SYSTEM.to_bytes(1, 'big'))
        client.sendall(len(message).to_bytes(8, 'big'))
        client.sendall(message)

def relay_loop(sock, clients):
    while True:
        data = sock.recv(1)
        if not data:
            break
        
        packet_type = int.from_bytes(data, 'big')
        
        if packet_type == protocol.FILE:
            relay_file(sock, clients)
        
        elif packet_type == protocol.TEXT:
            relay_text(sock, clients)
        
        elif packet_type == protocol.EXIT:
            relay_exit(sock, clients)
            break
        
def handle_client(conn, clients):
    try:
        relay_loop(conn, clients)
    finally:
        if conn in clients:
            del clients[conn]
        conn.close()
        
    