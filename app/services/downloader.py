import yt_dlp
import os
from datetime import datetime


def obter_titulo_video(url):
    try:
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(url, download=False)
            return info.get('title', 'Título não encontrado')
    except Exception as e:
        return f"Erro ao obter título: {str(e)}"


def baixar_video(url, apenas_audio=False, destino=".", is_playlist=False):
    try:
        # Se for uma playlist, criar subpasta com o nome da playlist
        if is_playlist:
            with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                info = ydl.extract_info(url, download=False)
                playlist_title = info.get('title', 'playlist')
                destino = os.path.join(destino, playlist_title)
                os.makedirs(destino, exist_ok=True)

        # Configurações do yt_dlp
        ydl_opts = {
            "outtmpl": os.path.join(destino, "%(title).40s.%(ext)s"),
            "quiet": True,
            "noplaylist": not is_playlist,
            "merge_output_format": "mp4",
            "postprocessors": [],
        }

        # Ajustar para apenas áudio se solicitado
        if apenas_audio:
            ydl_opts["format"] = "bestaudio/best"
            ydl_opts["postprocessors"].append({
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            })
        else:
            ydl_opts["format"] = "bestvideo+bestaudio/best"

        # Download
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        # Atualiza a data de modificação dos arquivos baixados
        for root, dirs, files in os.walk(destino):
            for file in files:
                file_path = os.path.join(root, file)
                now = datetime.now().timestamp()
                os.utime(file_path, (now, now))

        return "Download concluído com sucesso! 🎉"

    except Exception as e:
        return f"❌ Erro ao baixar vídeo: {str(e)}"
