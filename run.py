import aiogram
from aiogram import Bot, Dispatcher
import asyncio
from config import TOKEN
from app.handlers import router
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- HTTP сервер для Render (health check) ---
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Bot is alive')
    
    def log_message(self, format, *args):
        # Отключаем логи HTTP сервера, чтобы не засорять вывод
        pass

def run_http_server():
    server = HTTPServer(('0.0.0.0', 10000), HealthCheckHandler)
    server.serve_forever()

# Запускаем HTTP сервер в отдельном потоке
http_thread = threading.Thread(target=run_http_server, daemon=True)
http_thread.start()
print("✅ HTTP health check server started on port 10000")
# --------------------------------------------

async def main():
    dp.include_router(router)
    print("🤖 Бот запущен и готов к работе!")
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt as e:
        print(f"Exit bot {e}")
