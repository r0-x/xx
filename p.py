import requests 
import telebot
import os
import telebot

# Replace YOUR_BOT_TOKEN with your actual bot token
bot = telebot.TeleBot('5631323333:AAGdnFxvw36F5aNYJqYl-a3P-MUHszWwB60')

token = "5631323333:AAGdnFxvw36F5aNYJqYl-a3P-MUHszWwB60"
bot = telebot.TeleBot(token)
@bot.message_handler(commands =["start","starts"])
def info(message) :
	ch =	"iiwiw"
	id = message.chat.id
	if  int((id)):
		url =f"https://api.telegram.org/bot{token}/getChatMember?chat_id=@iiwiw&user_id={id}"
		x = requests.get(url).text
		if x.count("left") or x.count("Bad Request: user not found"):
			print("not join")
			bot.send_message(message.chat.id,text="** اشترك اولا @iiwiw ** ",parse_mode ="markdown")
		else:
			bot.reply_to(message, 'Welcome to the Trending Photo Bot! \n اهلاَ بكَ في بوت اشهر الصور في العالم الانَ . \n ارسل /photo لمراجعه الصور. ')

UNSPLASH_API_URL = 'https://api.unsplash.com/photos/random'

@bot.message_handler(commands=['photo'])
def photo(message):
    chat_id = message.chat.id
    UNSPLASH_ACCESS_KEY = "zP1GZJlDL5OcFp12ictHLqfRiAsMYsbgHf32Y1GdsIc"
    # Fetch photo from Unsplash API
    headers = {'Authorization': f'Client-ID {UNSPLASH_ACCESS_KEY}'}
    response = requests.get(UNSPLASH_API_URL, headers=headers)
    if response.status_code == 200:
        photo_data = response.json()
        photo_url = photo_data['urls']['regular']
        photo_author = photo_data['user']['name']
        photo_description = photo_data['description'] or 'No description'

        # Send photo
        bot.send_photo(chat_id, photo_url, caption=f'Photo by {photo_author}\n{photo_description}')
    else:
        bot.send_message(chat_id, 'An error occurred while fetching the photo. Please try again later.')
			
bot.polling()
