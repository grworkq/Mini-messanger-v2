import socket, threading, client_utils

HOST, PORT = '192.168.0.41', 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((HOST,PORT))
    
    nickname_str = (input('Введите никнейм: '))
    nickname = nickname_str.encode('utf-8')
    sock.sendall(len(nickname).to_bytes(8, 'big'))
    sock.sendall(nickname)
    print('Вы подключились.')
    
    thr1 = threading.Thread(target = client_utils.send_loop, args = (sock, nickname_str))
    thr2 = threading.Thread(target = client_utils.receive_loop, args = (sock, ))
    
    thr1.start()
    thr2.start()
    
    thr1.join()
    thr2.join()
    
    