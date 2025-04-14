from telegram import (
    Update, InlineKeyboardMarkup, InlineKeyboardButton, InputFile
)
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler,
    ContextTypes
)
from app.services.downloader import baixar_video, obter_titulo_video
import tempfile
import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎉 *Bem-vindo ao Mammoth Down!*\n\n"
        "⚠️ *Essa é uma versão de testes!* Ainda tem muita coisa pra ser implementada, mas você já pode brincar com o que está disponível.\n\n"
        "📥 Use:\n"
        "`/d <link>` para baixar vídeo ou playlist.\n\n"
        "📌 *Exemplo:*\n"
        "`/d https://youtube.com/watch?v=...`\n\n"
        "🎬 *Vídeo* e *Áudios:*.\n\n"
        "🎧 * Já testado com sucesso em:\n"
        "- YouTube\n"
        "- Instagram\n"
        "- Facebook\n"
        "- Pinterest\n"
        "- (e outras… 👀)\n\n"
        "💡 *Tem uma ideia, sugestão ou bug pra reportar?* Me chama aqui: @LogosTechn. Estou coletando feedback pra deixar o Mammoth ainda mais brabo 🐘💪\n\n"
        "_Valeu por testar!_ 🚀",
        parse_mode="Markdown"
    )


async def download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❗ Envie um link. Ex: `/d https://youtube.com/...`", parse_mode="Markdown")
        return

    url = context.args[0]
    is_playlist = 'playlist' in url.lower() or 'list=' in url.lower()

    # Aviso prévio caso seja uma playlist
    if is_playlist:
        await update.message.reply_text("📂 Playlist detectada! Isso pode levar um tempinho para processar as informações... Segura aí! ⏳")

    await update.message.reply_text("🔎 Buscando informações...")

    titulo = obter_titulo_video(url)
    if "Erro" in titulo:
        await update.message.reply_text(f"❌ {titulo}")
        return

    context.user_data["url"] = url
    context.user_data["is_playlist"] = is_playlist
    context.user_data["titulo"] = titulo

    tipo = "playlist" if is_playlist else "vídeo/música"

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("📹 Baixar vídeo", callback_data="baixar_video")],
        [InlineKeyboardButton("🎵 Apenas áudio (MP3)",
                              callback_data="baixar_audio")],
        [InlineKeyboardButton("❌ Cancelar", callback_data="cancelar_download")]
    ])

    await update.message.reply_text(
        f"🎬 Detectado:\n*{titulo}*\nTipo: *{tipo}*\n\nEscolha como deseja baixar:",
        parse_mode="Markdown",
        reply_markup=keyboard
    )

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data
    if data == "cancelar_download":
        await query.edit_message_text("❌ Download cancelado.")
        return

    apenas_audio = data == "baixar_audio"
    url = context.user_data.get("url")
    is_playlist = context.user_data.get("is_playlist")
    titulo = context.user_data.get("titulo")

    await query.edit_message_text(f"⏬ Baixando {'áudio' if apenas_audio else 'vídeo'}: *{titulo}*", parse_mode="Markdown")

    try:
        with tempfile.TemporaryDirectory() as tmp_dir:
            # função de progresso que envia updates pro usuário
            async def progresso(i, total, nome):
                await query.message.reply_text(
                    f"📥 Baixando item {i} de {total}:\n*{nome}*", parse_mode="Markdown"
                )

            # wrapper pro asyncio poder rodar callback síncrono
            def on_progress(i, total, nome):
                context.application.create_task(progresso(i, total, nome))

            resultado = baixar_video(
                url,
                apenas_audio=apenas_audio,
                destino=tmp_dir,
                is_playlist=is_playlist,
                on_progress=on_progress
            )

            arquivos = os.listdir(tmp_dir)

            if not arquivos:
                await query.message.reply_text("⚠️ Nenhum arquivo foi baixado.")
                return

            for nome in arquivos:
                caminho = os.path.join(tmp_dir, nome)
                tamanho = os.path.getsize(caminho)

                if tamanho > 49 * 1024 * 1024:
                    await query.message.reply_text(f"⚠️ '{nome}' excede 50MB e não pode ser enviado via Telegram.")
                    continue

                with open(caminho, "rb") as f:
                    await query.message.reply_document(
                        document=InputFile(f, filename=nome),
                        caption=f"✅ *{nome}* enviado com sucesso!",
                        parse_mode="Markdown"
                    )

            await query.message.reply_text("✅ Todos os arquivos foram enviados com sucesso!")

    except Exception as e:
        await query.message.reply_text(f"❌ Erro no download:\n`{str(e)}`", parse_mode="Markdown")


def iniciar_bot():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("d", download))
    app.add_handler(CallbackQueryHandler(handle_callback))
    print("🤖 Bot do Mammoth Down está rodando!")
    app.run_polling()


if __name__ == "__main__":
    iniciar_bot()
