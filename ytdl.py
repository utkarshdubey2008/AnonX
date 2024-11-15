import os
import yt_dlp
import telebot

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
TELEGRAM_BOT_TOKEN = '8037777628:AAHzJTKjDiHJJjlpBNrb-cWxUrTXdDt_-lY'
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# Define a function to start the bot
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Welcome! Send me a YouTube video link to download.")

# Define a function to handle incoming messages
@bot.message_handler(func=lambda message: True)
def download_video(message):
    video_url = message.text
    download_message = bot.send_message(message.chat.id, "Downloading... 0%")

    # Set up yt-dlp options with a progress hook
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

            # Send the downloaded video with a caption
            if os.path.exists(file_name):
                with open(file_name, 'rb') as video:
                    bot.send_video(message.chat.id, video, caption="Downloaded By @TheAlphabotz")
                os.remove(file_name)  # Remove file after sending
            else:
                bot.reply_to(message, "Failed to download video.")
    except Exception as e:
        bot.reply_to(message, f"An error occurred: {str(e)}")
    finally:
        bot.delete_message(download_message.chat.id, download_message.message_id)

# Store the last known percentage to avoid unnecessary edits
last_percent = -1

def progress_hook(d, message):
    global last_percent  # Use a global variable to keep track of last percent
    if d['status'] == 'downloading':
        # Calculate percentage downloaded
        if 'downloaded_bytes' in d and 'total_bytes' in d:
            percent = d['downloaded_bytes'] / d['total_bytes'] * 100
            
            # Update message only if the percent is 0% or changes by 30%
            if percent == 0 or (percent // 30) != (last_percent // 30):
                bot.edit_message_text(f"Downloading... {percent:.2f}%", chat_id=message.chat.id, message_id=message.message_id)
                last_percent = percent  # Update the last percent

if __name__ == '__main__':
    # Create downloads folder if it doesn't exist
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
    
    # Start the bot
    bot.polling(none_stop=True)