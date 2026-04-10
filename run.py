import asyncio
import os
from aiogram import Bot, Dispatcher
from config import TOKEN
from app.handlers import router
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

bot = Bot(token=TOKEN)
dp = Dispatcher()

# HTTP сервер для Render
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Bot is alive')
    def log_message(self, format, *args):
        pass

def run_http_server():
    port = int(os.environ.get('PORT', 10000))
    server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
    server.serve_forever()

# Запускаем HTTP сервер в фоне
threading.Thread(target=run_http_server, daemon=True).start()

async def main():
    dp.include_router(router)
    print("🤖 Бот запущен!")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
