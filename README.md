# 🦣 Mammoth Down

**Mammoth Down** é um downloader de vídeos poderoso, simples e estiloso feito em Python, com uma interface de terminal interativa utilizando o `rich`. Baixe vídeos ou playlists do YouTube com facilidade, seja em formato de vídeo ou apenas o áudio (MP3).

---

## 🚀 Funcionalidades

- Suporte a vídeos individuais e playlists.
- Escolha entre baixar vídeo ou apenas o áudio.
- Salve os downloads em um diretório personalizado.
- Interface interativa com arte ASCII e terminal colorido.
- Compatível com ambientes Linux, Windows e Termux.

---

## 📦 Requisitos

- Python 3.8+.
- `ffmpeg` instalado (necessário para conversão de áudio).
- Conexão com a internet. 😄

---

## 📥 Instalação

### 1. Clone o repositório do GitHub:

```bash
git clone https://github.com/seu-usuario/mammothDownload.git
cd mammothDownload
```

### 2. Instale as dependências:

```bash
pip install -r requirements.txt
```

### 3. Dica para Termux:

Se estiver no Termux, instale também o `ffmpeg` com:

```bash
pkg install ffmpeg
```

---

## ⚙️ Variáveis de ambiente (opcional)

Caso deseje definir um diretório padrão para os downloads, você pode configurar a variável de ambiente:

```bash
export MAMMOTH_DOWN_DIR="/caminho/para/salvar/downloads"
```

No Termux, para tornar isso permanente, adicione ao final do arquivo `~/.bashrc` ou `~/.zshrc`.

---

## 🧠 Como usar

Execute no terminal:

```bash
python cli.py
```

Depois, siga as instruções no terminal:

1. Cole o link do vídeo ou playlist.
2. Escolha se deseja baixar apenas o áudio.
3. Defina (ou não) o diretório de destino.

O **Mammoth Down** fará o resto! 😎

---

## 💡 Exemplo de uso

```plaintext
🎬 Vídeo detectado: Chill Lofi Hip Hop Mix
Deseja iniciar o download? [Y/n]: y
Deseja baixar apenas o áudio (MP3)? [Y/n]: y
Deseja salvar em qual diretório? (Deixe vazio para usar a pasta atual): /sdcard/Downloads
Download concluído com sucesso! 🎉
```

---

## 🛠️ To-Do Futuro

- Suporte a legendas.
- Interface web opcional.
- Integração com bot do Telegram.
- Histórico de downloads (se o usuário mudar de ideia 😜).

---

## 🧊 Licença

Este projeto é open-source. Use, modifique e compartilhe à vontade. Só não venda! 😉

---

## 📬 Contato

Quer contribuir ou dar ideias? Abra uma issue ou entre em contato!

---

🐘 ASCII Art by me
