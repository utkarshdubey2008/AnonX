import os
import yt_dlp
import telebot


TELEGRAM_BOT_TOKEN = '🖕'
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Welcome! Send me a YouTube video link to download.```Bot by @thealphabotz```")


@bot.message_handler(func=lambda message: True)
def download_video(message):
    video_url = message.text
    download_message = bot.send_message(message.chat.id, "Downloading... 0️⃣")

    
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'progress_hooks': [lambda d: progress_hook(d, download_message)],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=True)
            video_title = info_dict.get('title', None)
            file_name = f'downloads/{video_title}.mp4'

            
            if os.path.exists(file_name):
                with open(file_name, 'rb') as video:
                    bot.send_video(message.chat.id, video, caption="Bot By @TheAlphabotz")
                os.remove(file_name)  
            else:
                bot.reply_to(message, "Failed to download video.👄")
    except Exception as e:
        bot.reply_to(message, f"An error occurred: {str(e)}")
    finally:
        bot.delete_message(download_message.chat.id, download_message.message_id)


last_percent = -1

def progress_hook(d, message):
    global last_percent  
    if d['status'] == 'downloading':
        
        if 'downloaded_bytes' in d and 'total_bytes' in d:
            percent = d['downloaded_bytes'] / d['total_bytes'] * 100
            
            
            if percent == 0 or (percent // 30) != (last_percent // 30):
                bot.edit_message_text(f"Downloading... {percent:.2f}%", chat_id=message.chat.id, message_id=message.message_id)
                last_percent = percent  

if __name__ == '__main__':
    
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
    
    
    bot.polling(none_stop=True)
