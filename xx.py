import os
import telebot
import pytube

# Replace YOUR_BOT_TOKEN with your actual bot token
bot = telebot.TeleBot('5631323333:AAFAkRg1Eo36KbUcILoHTYIUyH9LoS6R8yU')

# Handler for the /start command
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Welcome to the YouTube Downloader Bot!')

# Handler for the /download command
@bot.message_handler(commands=['download'])
def download(message):
    chat_id = message.chat.id
    msg = bot.reply_to(message, "Please send me the YouTube link:")
    bot.register_next_step_handler(msg, process_url_step)

def process_url_step(message):
    chat_id = message.chat.id
    url = message.text

    try:
        # Get video streams
        video = pytube.YouTube(url)
        video_streams = video.streams.filter(progressive=True, file_extension='mp4')

        # Get video streams for SD and HD quality
        video_stream_sd = video_streams.get_by_resolution('360p')
        video_stream_hd = video_streams.get_by_resolution('720p')

        # Download video streams
        video_stream_sd.download()
        video_stream_hd.download()

        # Get filenames
        video_filename_sd = video_stream_sd.default_filename
        video_filename_hd = video_stream_hd.default_filename

        # Download audio stream
        audio_stream = video_streams.get_audio_only()
        audio_stream.download()
        audio_filename = audio_stream.default_filename

        # Send buttons
        buttons = telebot.types.InlineKeyboardMarkup()
        buttons.add(telebot.types.InlineKeyboardButton(text="SD", callback_data=f"video {video_filename_sd}"), 
                    telebot.types.InlineKeyboardButton(text="HD", callback_data=f"video {video_filename_hd}"),
                    telebot.types.InlineKeyboardButton(text="Audio", callback_data=f"audio {audio_filename}"))
        bot.send_message(chat_id, "Choose what to send:", reply_markup=buttons)

    except Exception as e:
        bot.send_message(chat_id, 'An error occurred while downloading the video. Please try again later.')
        print(e)

# Handler for the callback queries
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    query_data = call.data.split()
    file_type = query_data[0]
    file_name = query_data[1]

    # Send file
    if file_type == "video":
        file = open(file_name, 'rb')
        bot.send_video(chat_id, file, reply_to_message_id=message_id)
        file.close()
    elif file_type == "audio":
        file = open(file_name, 'rb')
        bot.send_audio(chat_id, file, reply_to_message_id=message_id)
        file.close()

    # Remove downloaded files
    os.remove(file_name)

bot.polling()
