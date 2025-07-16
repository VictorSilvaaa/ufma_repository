import socket
import threading
import os
import base64
import time

class ChatClient:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.running = False
        self.on_message = None          # callback para mensagens texto normais (string)
        self.on_file_received = None    # callback para arquivo recebido (filename, caminho completo salvo)

    def connect(self, host, port, username, senha):
        print("⏳ Conectando ao servidor...")
        time.sleep(0.5)  # pequeno delay visual

        self.client.connect((host, port))
        self.running = True

        print("🔐 Autenticando...")
        time.sleep(0.3)

        self.client.recv(1024)
        self.client.send(username.encode('utf-8'))
        self.client.recv(1024)
        self.client.send(senha.encode('utf-8'))

        print("✅ Conectado com sucesso!")
        threading.Thread(target=self.receive_messages, daemon=True).start()

    def receive_messages(self):
        while self.running:
            try:
                message = self.client.recv(4096).decode('utf-8')
                if not message:
                    break

                # Detecta mensagem especial de arquivo no formato "/file filename base64data"
                if message.startswith("/file "):
                    parts = message.split(' ', 2)
                    if len(parts) == 3:
                        filename = parts[1]
                        b64data = parts[2]

                        # Cria pasta downloads se não existir
                        os.makedirs("downloads", exist_ok=True)
                        filepath = os.path.join("downloads", filename)

                        # Salva arquivo decodificado
                        with open(filepath, "wb") as f:
                            f.write(base64.b64decode(b64data))

                        # Chama callback para GUI carregar a imagem
                        if self.on_file_received:
                            self.on_file_received(filename, filepath)
                    else:
                        # Mensagem mal formatada
                        if self.on_message:
                            self.on_message("[SISTEMA] Arquivo recebido com formato inválido.")
                else:
                    if self.on_message:
                        self.on_message(message)

            except Exception:
                self.running = False
                break

    def send_message(self, message):
        if self.running:
            try:
                self.client.send(message.encode('utf-8'))
            except:
                self.running = False

    def send_file(self, filename):
        # A pasta base onde estão as imagens que deseja enviar
        base_dir = os.path.join(os.getcwd(), 'imagens')
        filepath = os.path.join(base_dir, filename)

        if os.path.exists(filepath):
            with open(filepath, 'rb') as f:
                file_data = base64.b64encode(f.read()).decode('utf-8')

            # Envia comando especial com nome e dados do arquivo
            self.send_message(f"/file {filename} {file_data}")
        else:
            if self.on_message:
                self.on_message(f"[SISTEMA] Arquivo não encontrado: {filepath}")

    def close(self):
        self.running = False
        self.client.close()