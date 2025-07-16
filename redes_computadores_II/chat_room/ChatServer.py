import socket
import threading
import time
import os
import base64

MAX_CLIENTS = 10

class ChatServer:
    def __init__(self, host='0.0.0.0', port=12345):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = {}
        self.lock = threading.Lock()
        self.running = True

    def start(self):
        self.server.bind((self.host, self.port))
        self.server.listen(MAX_CLIENTS)
        print(f"Servidor ouvindo em {self.host}:{self.port}")

        threading.Thread(target=self.admin_commands, daemon=True).start()

        while self.running:
            try:
                client_socket, addr = self.server.accept()
                threading.Thread(target=self.handle_client, args=(client_socket,), daemon=True).start()
            except:
                break

    def broadcast(self, message, sender=None):
        with self.lock:
            for username, client in list(self.clients.items()):
                if sender != username:
                    try:
                        client.send(message.encode('utf-8'))
                    except:
                        self.remove_client(username)

    def remove_client(self, username):
        with self.lock:
            if username in self.clients:
                try:
                    self.clients[username].close()
                except:
                    pass
                del self.clients[username]
                self.broadcast(f"[SISTEMA] {username} saiu da sala\n")

    def handle_client(self, client_socket):
        username = None
        try:
            client_socket.send("USERNAME:".encode('utf-8'))
            username = client_socket.recv(1024).decode('utf-8').strip()

            client_socket.send("SENHA:".encode('utf-8'))
            password = client_socket.recv(1024).decode('utf-8').strip()

            with self.lock:
                if len(self.clients) >= MAX_CLIENTS:
                    client_socket.send("Sala cheia. Tente novamente mais tarde.\n".encode('utf-8'))
                    client_socket.close()
                    return
                self.clients[username] = client_socket

            self.broadcast(f"[SISTEMA] {username} entrou na sala\n")
            client_socket.send("Autenticação bem-sucedida! Digite 'exit' para sair\n".encode('utf-8'))

            while self.running:
                message = client_socket.recv(4096).decode('utf-8')
                if not message or message.lower() in ['exit', 'quit']:
                    break
                if message.startswith('/file '):
                    self.handle_file(message, username)
                else:
                    self.broadcast(f"{username}: {message}\n", username)

        except Exception as e:
            print(f"Erro: {e}")
        finally:
            if username:
                self.remove_client(username)
            client_socket.close()

    def handle_file(self, message, sender):
        parts = message.split(' ', 2)
        if len(parts) < 3:
            return
        filename = parts[1]
        file_data = base64.b64decode(parts[2])
        with open(filename, 'wb') as f:
            f.write(file_data)
        self.broadcast(f"[ARQUIVO] {sender} enviou: {filename}\n")

    def admin_commands(self):
        while self.running:
            cmd = input("Comando do servidor (shutdown): ").strip().lower()
            if cmd == 'shutdown':
                self.broadcast("[SISTEMA] O servidor será desligado em 10 segundos!\n")
                time.sleep(10)
                self.shutdown()

    def shutdown(self):
        self.running = False
        with self.lock:
            for client in self.clients.values():
                try:
                    client.close()
                except:
                    pass
        self.server.close()
        print("Servidor desligado")
