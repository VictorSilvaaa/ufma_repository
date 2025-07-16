import socket
import threading
import time
import os
import base64

MAX_CLIENTS = 10

class ChatClient:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.running = True

    def connect(self, host, port):
        self.client.connect((host, port))

        # Recebe e mostra o prompt de USERNAME
        prompt = self.client.recv(1024).decode('utf-8')
        print(prompt, end='')
        username = input().strip()
        self.client.send(username.encode('utf-8'))

        # Recebe e mostra o prompt de SENHA
        prompt = self.client.recv(1024).decode('utf-8')
        print(prompt, end='')
        senha = input().strip()
        self.client.send(senha.encode('utf-8'))

        # Agora inicia a thread para receber mensagens
        threading.Thread(target=self.receive_messages, daemon=True).start()

        # E começa a enviar mensagens
        self.send_messages()

    def receive_messages(self):
        while self.running:
            try:
                message = self.client.recv(4096).decode('utf-8')
                if message:
                    print(message, end='')
                else:
                    break
            except:
                break
        self.running = False

    def send_messages(self):
        try:
            while self.running:
                message = input()
                if message.lower() in ['exit', 'quit']:
                    self.client.send(message.encode('utf-8'))
                    self.running = False
                elif message.startswith('/file '):
                    self.send_file(message)
                else:
                    self.client.send(message.encode('utf-8'))
        finally:
            self.client.close()

    def send_file(self, command):
        try:
            parts = command.split(' ', 1)
            if len(parts) < 2:
                print("Uso: /file <caminho-do-arquivo>")
                return
            filepath = parts[1]
            if os.path.exists(filepath):
                with open(filepath, 'rb') as f:
                    file_data = base64.b64encode(f.read()).decode('utf-8')
                filename = os.path.basename(filepath)
                self.client.send(f"/file {filename} {file_data}".encode('utf-8'))
            else:
                print("Arquivo não encontrado!")
        except Exception as e:
            print(f"Erro ao enviar arquivo: {e}")
