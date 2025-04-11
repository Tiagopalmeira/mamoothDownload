import os
import sys
from datetime import datetime
from app.services.downloader import baixar_video, obter_titulo_video


def exibir_menu():
    print("\n🎬 Bem-vindo ao Video Downloader CLI")
    print("====================================")
    link = input("🔗 Cole o link do vídeo: ").strip()
    if not link:
        print("❌ Link inválido.")
        sys.exit()

    titulo = obter_titulo_video(link)
    print(f"\n🎥 Título do vídeo detectado: {titulo}")

    opcao_audio = input(
        "🎵 Deseja baixar apenas o áudio (MP3)? (s/n): ").lower()
    apenas_audio = opcao_audio == 's'

    confirmar = input(
        f"✅ Confirmar download de: \"{titulo}\"? (s/n): ").lower()
    if confirmar != 's':
        print("🚫 Download cancelado.")
        sys.exit()

    print("⬇️ Iniciando download...\n")
    resultado = baixar_video(link, apenas_audio)
    print(resultado)


if __name__ == "__main__":
    exibir_menu()
