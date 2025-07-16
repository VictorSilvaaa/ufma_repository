from ChatServer import ChatServer
from ChatClient import ChatClient

class MainApp:
    def run(self):
        role = input("Iniciar como servidor (s) ou cliente (c)? ").lower()
        
        if role == 's':
            server = ChatServer()
            server.start()
        
        elif role == 'c':
            host = input("Host do servidor: ").strip()
            port = int(input("Porta: ").strip())
            client = ChatClient()
            client.connect(host, port)

if __name__ == "__main__":
    app = MainApp()
    app.run()