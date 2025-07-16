from chat_server import ChatServer
from chat_client import ChatClient
from chat_gui import ChatGUI
import warnings
import sys

# Oculta warnings do tipo RuntimeWarning
warnings.filterwarnings("ignore", category=RuntimeWarning)

try:
    sys.stdout.write("Iniciar como servidor (s), cliente (c) ou cliente GUI (g)? ")
    sys.stdout.flush()
    role = input().strip().lower()
except KeyboardInterrupt:
    print("\nEncerrado pelo usuário.")
    sys.exit(0)

if role == 's':
    server = ChatServer()
    server.start()

elif role == 'c':
    host = input("Host do servidor: ").strip()
    port = int(input("Porta: ").strip())
    client = ChatClient()
    username = input("Usuário: ")
    senha = input("Senha: ")
    client.connect(host, port, username, senha)
    try:
        while True:
            msg = input()
            if msg.lower() in ['exit', 'quit']:
                client.send_message(msg)
                break
            client.send_message(msg)
    except KeyboardInterrupt:
        print("\nConexão encerrada.")
        client.close()

elif role == 'g':
    app = ChatGUI()
    app.run()

else:
    print("Opção inválida. Use 's' para servidor, 'c' para cliente, ou 'g' para cliente com interface.")