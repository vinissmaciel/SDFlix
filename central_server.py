import Pyro5.api

@Pyro5.api.expose
class CentralServer:
    def __init__(self):
        self.servers = {}
        self.videos = {}

    def register_server(self, server_name, video_list):
        self.servers[server_name] = video_list
        for video in video_list:
            self.videos[video] = server_name

    def get_video_list(self):
        return list(self.videos.keys())

    def get_server_for_video(self, video_name):
        return self.videos.get(video_name, None)

def main():
    central_server = CentralServer()
    daemon = Pyro5.server.Daemon()
    uri = daemon.register(central_server)
    ns = Pyro5.api.locate_ns()
    ns.register("central.server", uri)

    print("Servidor Central está pronto.")
    daemon.requestLoop()

if __name__ == "__main__":
    main()
