from telebot import TeleBot
from telebot.types import Message, ReplyKeyboardRemove
from dotenv import load_dotenv
import os
import yt_dlp
from database import save_user_data, get_user, save_history, get_history
from reply import send_contact
import re
import time

load_dotenv()
bot = TeleBot(os.getenv("TOKEN"))

@bot.message_handler(commands=['start', 'help', 'about', 'history'])
def handle_commands(message: Message):
    chat_id = message.chat.id

    if message.text == '/start':
        user = get_user(chat_id)
        print(user)
        if user:
            bot.send_message(chat_id, "👋 Привет! Отправь мне ссылку на YouTube-видео, и я пришлю тебе аудио 🎵")
        else:
            bot.send_message(chat_id, "📲 Поделитесь контактом для регистрации", reply_markup=send_contact())

    elif message.text == '/help':
        bot.send_message(chat_id, "❓ Просто отправь мне ссылку на YouTube, и я верну тебе аудио. /history — покажет историю ссылок, разработчик @Jafroo")

    elif message.text == '/about':
        bot.send_message(chat_id, "🎧 Бот, который скачивает аудио с YouTube.")

    elif message.text == '/history':
        history = get_history(chat_id)
        if history:
            result = "\n\n".join(link[0] for link in history)
            bot.send_message(chat_id, f"🕓 Последние ссылки:\n{result}")
        else:
            bot.send_message(chat_id, "📭 История пуста.")

@bot.message_handler(content_types=['contact'])
def register_contact(message: Message):
    chat_id = message.chat.id
    full_name = message.from_user.full_name
    phone = message.contact.phone_number

    if not get_user(chat_id):
        save_user_data(chat_id, full_name, phone)
        bot.send_message(chat_id, "✅ Регистрация прошла успешно!", reply_markup=ReplyKeyboardRemove())

    bot.send_message(chat_id, "Теперь отправьте ссылку на видео 🎬")

def clean_filename(title):
    return re.sub(r'[<>:"/\\|?*]', '', title)



@bot.message_handler(func=lambda message: message.text.startswith('http'))
def download_audio(message: Message):
    chat_id = message.chat.id
    url = message.text.strip()

    loading_message = bot.send_message(chat_id, "⏬ Загружаю аудио, подождите...")

    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'media/%(id)s.%(ext)s',  # сохраняется как media/ID.webm, потом сразу заменяется на ID.mp3
            'quiet': True,
            'postprocessors': [
                {
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '128',
                }
            ],
            'noplaylist': True,
            'http_chunk_size': 1048576,
            'retries': 10,
            'socket_timeout': 30,
            'keepvideo': False,
            'final_ext': 'mp3'
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info.get('title', 'Без названия')
            video_id = info.get('id')
            safe_title = clean_filename(title)
            final_path = f'media/{video_id}.mp3'


        # ⏳ Ожидание до 10 секунд, пока mp3 появится
        for _ in range(10):
            if os.path.exists(final_path):
                break
            time.sleep(1)
        else:
            bot.send_message(chat_id, "❌ MP3 файл не был создан даже после ожидания.")
            bot.delete_message(chat_id, loading_message.message_id)
            return

        author = info.get('uploader', 'Неизвестный автор')
        upload_date = info.get('upload_date', 'Неизвестная дата')
        if upload_date:
            upload_date = f'{upload_date[:4]}-{upload_date[4:6]}-{upload_date[6:]}'
        view_count = info.get("view_count") or 0
        like_count = info.get("like_count") or 0

        caption = (
            f'🎵 <b>{title}</b>\n'
            f'👤 {author}\n'
            f'📅 {upload_date}\n'
            f'👁️ {view_count:,}\n'
            f'👍 {like_count:,}'
        )

        if os.path.getsize(final_path) > 50 * 1024 * 1024:
            bot.send_message(chat_id, "❌ Файл слишком большой для отправки через Telegram (больше 50MB).")
            os.remove(final_path)
            bot.delete_message(chat_id, loading_message.message_id)
            return
        else:
            with open(final_path, 'rb') as audio:
                bot.send_audio(chat_id, audio, parse_mode='HTML', caption=caption, timeout=960, title=title)

        os.remove(final_path)
        save_history(chat_id, url)
        bot.delete_message(chat_id, loading_message.message_id)

    except Exception as e:
        print("Ошибка:", e)
        bot.send_message(chat_id, "❌ Ошибка при загрузке аудио. Убедитесь, что это правильная ссылка на YouTube.")
        bot.delete_message(chat_id, loading_message.message_id)

bot.infinity_polling()
