# Messenger v2

## Description

Messenger v2 is a console-based TCP chat application written in Python using only the standard library.

Unlike the previous version, this messenger supports communication between multiple clients connected to the same local network (LAN). The server relays messages and files between all connected users.

## Features

- Multi-client chat
- Communication between different devices on the same Wi-Fi/LAN
- User nicknames
- File transfer
- System notifications (user connected/disconnected)
- Multi-threaded server
- Custom binary protocol
- No external libraries required

## Technologies

* Python 3
* socket
* threading
* pathlib

## Project structure

```text
Mini-Messenger-v2/
│
├── client.py
├── server.py
├── client_utils.py
├── server_utils.py
├── protocol.py
├── README.md
└── saved/
```

## Protocol

Each packet starts with a 1-byte packet type.

Packet types:

- TEXT
- FILE
- EXIT
- SYSTEM

Text packets:

```text
1 byte   Packet type
8 bytes  Message length
N bytes  UTF-8 message
```

File packets:

```text
1 byte   Packet type
8 bytes  Filename length
N bytes  Filename
8 bytes  File size
N bytes  File data
```

## Running

Start the server:

```bash
python server.py
```

Start one or more clients:

```bash
python client.py
```

Enter a nickname and begin chatting.

### Commands

```text
/send <path_to_file>   #Send a file
/exit or /e            #Leave the chat
```



