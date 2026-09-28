# YouTube Music Downloader Bot 🎵

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![Telegram](https://img.shields.io/badge/Telegram-Bot-26A5E4?logo=telegram&logoColor=white)
![yt-dlp](https://img.shields.io/badge/yt--dlp-audio-red)
![License](https://img.shields.io/badge/license-MIT-green)

A Telegram bot that turns a YouTube link into an MP3. Send it a link and get the audio back with the title, channel, upload date, views and likes.

## Features

- 🎧 Send a YouTube link → receive an MP3 (128 kbps)
- 📝 Rich caption: title, author, upload date, views, likes
- 🕓 `/history` shows your last 5 links
- 📲 One-tap registration by sharing a contact
- 🚫 Skips files over Telegram's 50 MB limit

## Commands

| Command | Description |
|---|---|
| `/start` | Register / greeting |
| `/help` | How to use the bot |
| `/about` | About the bot |
| `/history` | Your last 5 downloaded links |

## Tech stack

Python · [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI) · [yt-dlp](https://github.com/yt-dlp/yt-dlp) · FFmpeg · SQLite

## Getting started

**Requirements:** Python 3.10+ and [FFmpeg](https://ffmpeg.org/download.html) on your `PATH`.

```bash
git clone https://github.com/jafarallaberdiyev/YoutubeMusicDownloader_bot.git
cd YoutubeMusicDownloader_bot

python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS / Linux

pip install -r requirements.txt
cp .env.example .env           # put your bot token from @BotFather in .env
python main.py
```

The SQLite database (`audiodown.db`) is created automatically on first run and is git-ignored, since it stores users' contact details.

## Project structure

```
main.py        # bot handlers and download logic
database.py    # SQLite storage for users and history
reply.py       # reply keyboards
```

## License

[MIT](LICENSE)
