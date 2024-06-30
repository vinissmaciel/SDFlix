import Pyro5.api
import webbrowser

def main():
    central_server = Pyro5.api.Proxy("PYRONAME:central.server")
    
    video_list = central_server.get_video_list()
    print("\nFilmes disponíveis:")
    for video in video_list:
        print("-", video)

    video_name = input("\nDigite o nome do filme que deseja assistir (com a extensão): ")

    server_name = central_server.get_server_for_video(video_name)
    if server_name:
        media_server = Pyro5.api.Proxy(f"PYRONAME:media.server.{server_name}")
        video_url = media_server.stream_video(video_name)
        if video_url:
            print(f"Transmitindo video de: {video_url}")
            webbrowser.open(video_url)
        else:
            print("Vídeo não encontrado no servidor de mídia.")
    else:
        print("Vídeo não encontrado.")

if __name__ == "__main__":
    main()
