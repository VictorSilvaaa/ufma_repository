import threading
import os
import pygame
import pyperclip 
from chat_client import ChatClient

# Constantes
WIDTH, HEIGHT = 600, 500
FPS = 30
INPUT_HEIGHT = 30
MARGIN = 10
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (230, 230, 230)
BLUE = (100, 149, 237)
pygame.init()

class ChatGUI:
    def __init__(self):
        self.pygame = pygame
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Chat Cliente Pygame")

        self.clock = pygame.time.Clock()
        self.FONT = pygame.font.SysFont("arial", 20)

        self.client = ChatClient()
        self.client.on_message = self.on_message_received
        self.client.on_file_received = self.on_file_received

        self.messages = []
        self.input_text = ""
        self.connected = False
        self.username = ""

        self.login_active = True
        self.host = "127.0.0.1"
        self.port = 12345
        self.password = ""

        self.login_fields = {
            "host": self.host,
            "port": str(self.port),
            "username": "",
            "password": "",
        }
        self.login_field_names = list(self.login_fields.keys())
        self.active_input = 0

        self.image_previews = {}

    def on_message_received(self, message):
        self.messages.append(message)
        if len(self.messages) > 100:
            self.messages.pop(0)

    def on_file_received(self, filename, filepath):
        try:
            image = pygame.image.load(filepath)
            image = pygame.transform.scale(image, (100, 100))
            self.image_previews[filename] = image
            self.messages.append(f"[SISTEMA] Arquivo recebido: {filename} (salvo em {filepath})")
        except:
            self.messages.append(f"[SISTEMA] Erro ao carregar imagem: {filename}")
        if len(self.messages) > 100:
            self.messages.pop(0)

    def draw_login_screen(self):
        self.screen.fill(WHITE)
        y = 50
        for idx, key in enumerate(self.login_field_names):
            label = self.FONT.render(key.capitalize() + ":", True, BLACK)
            self.screen.blit(label, (50, y))

            rect = pygame.Rect(150, y - 5, 300, INPUT_HEIGHT)
            color = BLUE if idx == self.active_input else GRAY
            pygame.draw.rect(self.screen, color, rect, 2)

            txt = self.login_fields[key]
            if key == "password":
                txt = "*" * len(txt)
            txt_surface = self.FONT.render(txt, True, BLACK)
            self.screen.blit(txt_surface, (rect.x + 5, rect.y + 5))
            y += 50

        button_rect = pygame.Rect(250, y, 100, 40)
        pygame.draw.rect(self.screen, BLUE, button_rect)
        btn_text = self.FONT.render("Conectar", True, WHITE)
        self.screen.blit(btn_text, (button_rect.x + 10, button_rect.y + 8))

        return button_rect

    def draw_chat_screen(self):
        self.screen.fill(WHITE)

        msg_rect = pygame.Rect(MARGIN, MARGIN, WIDTH - 2 * MARGIN, HEIGHT - 100)
        pygame.draw.rect(self.screen, GRAY, msg_rect)

        y = msg_rect.bottom - 25
        for msg in reversed(self.messages):
            import re
            match = re.match(r"\[SISTEMA\] (?:Arquivo recebido|Enviando arquivo): ([^\s]+)", msg)
            if match:
                filename = match.group(1)
                if filename in self.image_previews:
                    img = self.image_previews[filename]
                    img_rect = img.get_rect()
                    img_rect.x = msg_rect.x + 5
                    img_rect.y = y - img_rect.height
                    self.screen.blit(img, img_rect)
                    y = img_rect.y - 5
                    name_surface = self.FONT.render(filename, True, BLACK)
                    self.screen.blit(name_surface, (img_rect.x, y))
                    y -= 25
                    if y < msg_rect.y:
                        break
                    continue

            msg = msg.strip()
            if msg.startswith(f"{self.username}:"):
                color = (0, 100, 255)
                align_right = True
            elif msg.startswith("[SISTEMA]"):
                color = (150, 0, 0)
                align_right = False
            else:
                color = BLACK
                align_right = False

            msg_surface = self.FONT.render(msg, True, color)
            msg_width = msg_surface.get_width()
            x = msg_rect.right - msg_width - 10 if align_right else msg_rect.x + 5
            self.screen.blit(msg_surface, (x, y))
            y -= 25
            if y < msg_rect.y:
                break

        input_rect = pygame.Rect(MARGIN, HEIGHT - 80, WIDTH - 120, INPUT_HEIGHT)
        pygame.draw.rect(self.screen, WHITE, input_rect)
        pygame.draw.rect(self.screen, BLACK, input_rect, 2)

        input_surface = self.FONT.render(self.input_text, True, BLACK)
        self.screen.blit(input_surface, (input_rect.x + 5, input_rect.y + 5))

        send_rect = pygame.Rect(WIDTH - 100, HEIGHT - 80, 90, INPUT_HEIGHT)
        pygame.draw.rect(self.screen, BLUE, send_rect)
        send_text = self.FONT.render("Enviar", True, WHITE)
        self.screen.blit(send_text, (send_rect.x + 15, send_rect.y + 5))

        return input_rect, send_rect

    def handle_login_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                self.active_input = (self.active_input + 1) % len(self.login_fields)
            elif event.key == pygame.K_BACKSPACE:
                field_key = self.login_field_names[self.active_input]
                self.login_fields[field_key] = self.login_fields[field_key][:-1]
            elif event.key == pygame.K_RETURN:
                self.try_connect()
            else:
                field_key = self.login_field_names[self.active_input]
                self.login_fields[field_key] += event.unicode

        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            button_rect = self.draw_login_screen()
            if button_rect.collidepoint(x, y):
                self.try_connect()

    def try_connect(self):
        host = self.login_fields["host"]
        username = self.login_fields["username"]
        try:
            port = int(self.login_fields["port"])
        except:
            self.messages.append("[Erro] Porta inválida")
            return
        password = self.login_fields["password"]

        if not host or not username or not password:
            self.messages.append("[Erro] Preencha todos os campos")
            return

        try:
            self.client.connect(host, port, username, password)
            self.username = username
            self.connected = True
            self.login_active = False
        except Exception as e:
            self.messages.append(f"[Erro] {e}")

    def handle_chat_events(self, event, input_rect, send_rect):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.input_text = self.input_text[:-1]
            elif event.key == pygame.K_RETURN:
                self.send_message()
            elif event.key == pygame.K_v and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                pasted = pyperclip.paste()
                self.input_text += pasted
            else:
                self.input_text += event.unicode

        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if send_rect.collidepoint(x, y):
                self.send_message()

    def send_message(self):
        msg = self.input_text.strip()
        if msg:
            if msg.startswith("/sendfile "):
                filepath = msg[len("/sendfile "):].strip()
                base_dir = os.path.join(os.getcwd(), 'imagens')
                full_path = os.path.join(base_dir, filepath)
                try:
                    image = pygame.image.load(full_path)
                    image = pygame.transform.scale(image, (100, 100))
                    self.image_previews[filepath] = image
                    self.messages.append(f"[SISTEMA] Enviando arquivo: {filepath}")
                    if len(self.messages) > 100:
                        self.messages.pop(0)
                except Exception as e:
                    self.messages.append(f"[SISTEMA] Erro ao carregar imagem para envio: {filepath}")
                self.client.send_file(filepath)
                self.input_text = ""
            else:
                full_msg = f"{self.username}: {msg}"
                self.messages.append(full_msg)
                self.client.send_message(msg)
                self.input_text = ""

            if msg.lower() in ['exit', 'quit']:
                self.pygame.quit()
                exit()

    def run(self):
        running = True
        while running:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if self.login_active:
                    self.handle_login_events(event)
                else:
                    input_rect, send_rect = self.draw_chat_screen()
                    self.handle_chat_events(event, input_rect, send_rect)

            if self.login_active:
                self.draw_login_screen()
            else:
                self.draw_chat_screen()

            pygame.display.flip()

        pygame.quit()