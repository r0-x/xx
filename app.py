import telegram
import os
import subprocess
import re

# Define your bot token and chat ID
bot_token = "5631323333:AAFAkRg1Eo36KbUcILoHTYIUyH9LoS6R8yU"
chat_id = "1150883146"

# Initialize the Telegram bot using your bot token
bot = telegram.Bot(token=bot_token)

# Define the handler function for the /start command
def start_command(update, context):
    # Send a welcome message to the user
    bot.send_message(chat_id=update.message.chat_id, text="Hello! I'm a YouTube downloader bot. Just send me a YouTube video link and I'll download it for you.")

# Define the handler function for the YouTube video link message
def youtube_command(update, context):
    # Get the YouTube video link from the user message
    video_link = update.message.text
    # Download the YouTube video using youtube-dl command-line tool
    download_command = f"youtube-dl -f 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best' --output '%(title)s.%(ext)s' {video_link}"
    output = subprocess.Popen(download_command, shell=True, stdout=subprocess.PIPE).stdout.read().decode()
    # Get the downloaded video file name from the output
    filename = re.findall(r'(?<=\[download\]).+?(?=\n)', output)[-1]
    # Send the downloaded video file to the user
    with open(filename, 'rb') as video:
        bot.send_video(chat_id=update.message.chat_id, video=video, supports_streaming=True)
    # Delete the downloaded video file from the server
    os.remove(filename)

# Define the handler function for the unknown command
def unknown_command(update, context):
    # Send an error message to the user
    bot.send_message(chat_id=update.message.chat_id, text="Sorry, I don't understand that command. Please send a YouTube video link.")

# Create the bot's command handlers
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram.ext import Updater
updater = Updater(token=bot_token, use_context=True)
dispatcher = updater.dispatcher
start_handler = CommandHandler('start', start_command)
youtube_handler = MessageHandler(Filters.regex(r'^https?:\/\/(www\.)?youtube\.com\/'), youtube_command)
unknown_handler = MessageHandler(Filters.command, unknown_command)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(youtube_handler)
dispatcher.add_handler(unknown_handler)

# Start the bot
updater.start_polling()
updater.idle()
