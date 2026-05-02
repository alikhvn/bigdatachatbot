import asyncio
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from app.main import main

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

def run_server():
    port = 10000  
    server = HTTPServer(("", port), Handler)
    server.serve_forever()

def run_async():
    asyncio.run(main())

if __name__ == "__main__":
    threading.Thread(target=run_server).start()

    run_async()