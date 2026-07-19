import pathlib, protocol, os

os.system("")


def send_text(sock, message,):
    message = message.encode("utf-8")
    size_of_message = len(message)
    sock.sendall(size_of_message.to_bytes(8, "big"))
    sock.sendall(message)
    

    print("\033[A\033[K", end="", flush=True)
    


def receive_text(sock):
    len_nick = int.from_bytes(sock.recv(8), 'big')
    nick = sock.recv(len_nick).decode()
    len_message = int.from_bytes(sock.recv(8), "big")
    message_bytes = bytearray()
    while len(message_bytes) < len_message:
        remaining = len_message - len(message_bytes)
        chunk_t = min(4096, remaining)

        chunk = sock.recv(chunk_t)
        message_bytes.extend(chunk)
    message = message_bytes.decode()
    print("\r\033[K", end="", flush=True)
    print(f"[{nick}]: {message}")
    print(">> ", end="", flush=True)


def send_file(sock, path):
    path = pathlib.Path(path)
    nameu = path.name.encode("utf-8")
    sock.sendall(len(nameu).to_bytes(8, byteorder="big"))
    sock.sendall(nameu)
    file_size = path.stat().st_size
    sock.sendall(file_size.to_bytes(8, byteorder="big"))
    with open(path, "rb") as file:
        while True:
            chunk = file.read(4096)
            if not chunk:
                break
            sock.sendall(chunk)


def receive_file(sock):
    len_nick = int.from_bytes(sock.recv(8), 'big')
    nick = sock.recv(len_nick).decode()
    size_name_bytes = sock.recv(8)
    int_size_name = int.from_bytes(size_name_bytes, "big")
    name = sock.recv(int_size_name).decode("utf-8")
    size_bytes = sock.recv(8)
    file_size = int.from_bytes(size_bytes, byteorder="big")
    save_path = pathlib.Path("saved")
    save_path.mkdir(exist_ok=True)
    with open(save_path / f"{name}", "wb") as file:
        recev = 0
        while recev < file_size:
            remaining = file_size - recev
            chunk_to_read = min(4096, remaining)
            chunk = sock.recv(chunk_to_read)
            file.write(chunk)
            recev += len(chunk)
            
    print("\r\033[K", end="", flush=True)
    print(f'Получен файл от [{nick}]: {name}, {file_size} Байт')
    print('>> ', end='', flush = True)

def receive_exit(sock):
    sock.close()


def send_loop(sock, nick):
    try:
        while True:
            print(">> ", end="", flush=True)
            message = input("")
            if message.startswith("/send "):
                sock.sendall(protocol.FILE.to_bytes(1, "big"))
                send_file(sock, message[6:])
            elif message == "/send":
                print("использование: /send путь_к_файлу")
            elif message in {"/exit", "/e"}:
                sock.sendall(protocol.EXIT.to_bytes(1, "big"))
                print(f"Вы покинул чат.")
                break
            elif not message.strip():
                continue
            else:
                sock.sendall(protocol.TEXT.to_bytes(1, "big"))
                send_text(sock, message)
                print(f"[{nick}]: {message}")
    except OSError:
        print("Собеседник покинул чат.")
        return 

def receive_system(sock):
    size = int.from_bytes(sock.recv(8), 'big')
    
    data = bytearray()
    while len(data) < size:
        data.extend(sock.recv(min(4096, size - len(data))))

    print("\r\033[K", end="")
    print(f"** {data.decode()} **")
    print(">> ", end="", flush=True)

def receive_loop(sock):
    while True:
        data = sock.recv(1)
        if not data:
            break

        first_byte = int.from_bytes(data, "big")

        if first_byte == protocol.FILE:
            receive_file(sock,)

        elif first_byte == protocol.TEXT:
            receive_text(sock,)

        elif first_byte == protocol.EXIT:
            receive_exit(sock)
            break
        
        elif first_byte == protocol.SYSTEM:
            receive_system(sock)