from yt_dlp import YoutubeDL
from datetime import datetime


def obter_titulo_video(link):
    try:
        with YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(link, download=False)
            return info.get('title', 'Vídeo Desconhecido')
    except Exception as e:
        return f"Erro ao obter título: {e}"


def baixar_video(link, apenas_audio=False):
    try:
        data_atual = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

        ydl_opts = {
            'format': 'bestaudio/best' if apenas_audio else 'best',
            'outtmpl': f"{data_atual}_%(title)s.%(ext)s",
            'quiet': False,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
            }] if apenas_audio else [],
        }

        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])

        return "\n✅ Download concluído com sucesso!"
    except Exception as e:
        return f"\n❌ Erro ao baixar vídeo: {e}"
