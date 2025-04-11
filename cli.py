from rich import print
from rich.prompt import Prompt, Confirm
from rich.console import Console
from datetime import datetime
from app.services.downloader import obter_titulo_video, baixar_video
from app.utils.paths import obter_diretorio_download
import os

console = Console()

ASCII_ART = r'''
[bold blue]
███╗   ███╗ █████╗ ███╗   ███╗ ██████╗  ██████╗ ████████╗██╗  ██╗
████╗ ████║██╔══██╗████╗ ████║██╔═══██╗██╔═══██╗╚══██╔══╝██║  ██║
██╔████╔██║███████║██╔████╔██║██║   ██║██║   ██║   ██║   ███████║
██║╚██╔╝██║██╔══██║██║╚██╔╝██║██║   ██║██║   ██║   ██║   ██╔══██║
██║ ╚═╝ ██║██║  ██║██║ ╚═╝ ██║╚██████╔╝╚██████╔╝   ██║   ██║  ██║
╚═╝     ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝ ╚═════╝  ╚═════╝    ╚═╝   ╚═╝  ╚═╝
                                                                 
           ░█▀▄░█▀█░█░█░█▀█░█░░░█▀█░█▀█░█▀▄                      
           ░█░█░█░█░█▄█░█░█░█░░░█░█░█▀█░█░█                      
           ░▀▀░░▀▀▀░▀░▀░▀░▀░▀▀▀░▀▀▀░▀░▀░▀▀░                      
[/bold blue]'''


def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(ASCII_ART)
    print("[bold green]Bem-vindo ao Mammoth Down![/bold green]")

    while True:
        url = Prompt.ask(
            "\n[bold yellow]Cole o link do vídeo ou playlist[/bold yellow]")

        if not url.strip():
            print("[red]❌ Nenhum link fornecido.[/red]")
            continue

        print("[cyan]🔎 Obtendo informações do vídeo...[/cyan]")
        titulo = obter_titulo_video(url)
        print(f"[green]🎬 Vídeo detectado:[/green] [bold]{titulo}[/bold]")

        confirmar = Confirm.ask("Deseja iniciar o download?")
        if not confirmar:
            print("[cyan]🔁 Download cancelado pelo usuário.[/cyan]")
            continue

        apenas_audio = Confirm.ask("Deseja baixar apenas o áudio (MP3)?")

        destino = Prompt.ask(
            "Deseja salvar em qual pasta? (Deixe vazio para usar a pasta de Downloads)",
            default=""
        )

        if not destino.strip():
            destino = obter_diretorio_download()

        is_playlist = 'playlist' in url.lower() or 'list=' in url.lower()

        try:
            resultado = baixar_video(
                url, apenas_audio=apenas_audio, destino=destino, is_playlist=is_playlist)
            os.system('cls' if os.name == 'nt' else 'clear')
            print(ASCII_ART)
            print(f"[bold green]{resultado}[/bold green]")
        except Exception as e:
            print(f"[red]❌ Erro ao baixar: {e}[/red]")

        novamente = Confirm.ask("Deseja baixar outro vídeo?")
        if not novamente:
            print("[bold magenta]\n👋 Até a próxima com o Mammoth Down![/bold magenta]")
            break


if __name__ == '__main__':
    main()
