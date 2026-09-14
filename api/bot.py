from http.server import BaseHTTPRequestHandler
import json
import requests
import os

# Token do bot (defina como variável de ambiente na Vercel: TELEGRAM_TOKEN)
TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)
        update = json.loads(body)

        # Extrai a mensagem recebida do Telegram
        message = update.get("message", {})
        chat_id = message.get("chat", {}).get("id")
        text = message.get("text", "")

        if chat_id and text:
            # Responde ecoando a mensagem recebida
            payload = {
                "chat_id": chat_id,
                "text": f"Você disse: {text}"
            }
            requests.post(TELEGRAM_API_URL, json=payload)

        # Sempre responde 200 OK para o Telegram
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"status": "ok"}).encode())

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"Bot is running!")
