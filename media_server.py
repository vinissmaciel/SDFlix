import os
import http.server
import socketserver
import socket
import threading
import Pyro5.api

def list_files(directory):
    try:
        return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    except FileNotFoundError:
        print(f"O diretório {directory} não existe.")
        return []
    except PermissionError:
        print(f"Permissão negada para o diretório {directory}.")
        return []

@Pyro5.api.expose
class MediaServer:
    def __init__(self, server_name, http_port, video_dir):
        self.server_name = server_name
        self.http_port = http_port
        self.video_dir = video_dir
        self.video_list = list_files(video_dir)

    def stream_video(self, video_name):
        if video_name in self.video_list:
            video_url = f"http://{socket.gethostbyname(socket.gethostname())}:{self.http_port}/{video_name}"
            return video_url
        return None

def run_http_server(directory, port):
    os.chdir(directory)
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"Servindo HTTP na porta {port}")
        httpd.serve_forever()

def main():
    server_name = "MediaServer1"
    video_dir = "./videos"
    http_port = 8000

    media_server = MediaServer(server_name, http_port, video_dir)
    
    # Start HTTP server in a new thread
    threading.Thread(target=run_http_server, args=(video_dir, http_port), daemon=True).start()

    # Pyro server setup
    daemon = Pyro5.server.Daemon()
    uri = daemon.register(media_server)
    ns = Pyro5.api.locate_ns()
    ns.register(f"media.server.{server_name}", uri)

    central_server = Pyro5.api.Proxy("PYRONAME:central.server")
    central_server.register_server(server_name, media_server.video_list)

    print(f"{server_name} está pronto.")
    daemon.requestLoop()

if __name__ == "__main__":
    main()
