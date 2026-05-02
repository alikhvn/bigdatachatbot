import asyncio
import threading
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from app.main import main

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

def start_http():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), Handler)
    print(f"Server running on port {port}")
    server.serve_forever()

def start_async():
    asyncio.run(main())

if __name__ == "__main__":
    # HTTP сервер в отдельном потоке
    threading.Thread(target=start_http).start()

    # твоя логика
    start_async()
