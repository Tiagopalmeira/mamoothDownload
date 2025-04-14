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


def baixar_video(url, apenas_audio=False, destino=".", is_playlist=False, on_progress=None):
    try:
        if is_playlist:
            with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                info = ydl.extract_info(url, download=False)
                entries = info.get('entries', [])
                total = len(entries)

                for i, entry in enumerate(entries, start=1):
                    video_url = entry['webpage_url']
                    titulo = entry.get('title', f"Vídeo {i}")

                    if on_progress:
                        on_progress(i, total, titulo)

                    # Baixa item individual
                    baixar_video(
                        video_url,
                        apenas_audio=apenas_audio,
                        destino=destino,
                        is_playlist=False  # baixar item por item
                    )

        else:
            ydl_opts = {
                "outtmpl": os.path.join(destino, "%(title).40s.%(ext)s"),
                "quiet": True,
                "noplaylist": not is_playlist,
                "merge_output_format": "mp4",
                "postprocessors": [],
            }

            if apenas_audio:
                ydl_opts["format"] = "bestaudio/best"
                ydl_opts["postprocessors"].append({
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                })
            else:
                ydl_opts["format"] = "bestvideo+bestaudio/best"

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
