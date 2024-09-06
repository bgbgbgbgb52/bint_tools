# This Python file uses the following encoding: utf-8
from telebot import TeleBot
import threading
import datetime
import pytz
import random
import os

bot = TeleBot("7267179561:AAFGHbX65uzhd3d0aHoSAqMrxmOrMqHKcx0")


@bot.message_handler(func=lambda m: True)
def echo_all(message):
	# Assuming 'message.date' is a Unix timestamp
	messageTime = message.date

	# Convert the timestamp to a datetime object in UTC
	messageTime = datetime.datetime.utcfromtimestamp(messageTime)

	# Define the Cairo time zone
	cairo_tz = pytz.timezone('Africa/Cairo')

	# Convert the UTC time to Cairo time
	messageTime = messageTime.replace(tzinfo=pytz.utc).astimezone(cairo_tz)

	# Format the datetime object to a string in the 'YYYY-MM-DD HH:MM:SS' format
	messageTime = messageTime.strftime('%Y-%m-%d %H:%M:%S')

	# Store the formatted date and time as a string
	TimeStamp = str(messageTime)
	bot.send_message(chat_id=566211382,
	                 text=f"User ID :{message.from_user.id}\nFull Name : {message.from_user.first_name} {message.from_user.last_name}\n"
	                      f"User Name: {message.from_user.username}\nChat ID : {message.chat.id}\nMessage ID : {message.message_id}\n"
	                      f"Message Content: {message.text}\n"
	                      f"Time : {TimeStamp}")
	message_text = str(message.text)
	message_content = message_text.split(' ')
	message_text = message_content[0]
	try:
		int(message_text[0])
		int(message_text.replace('x','').replace('X',''))
	except ValueError:
		bot.reply_to(message,"you sent invalid bin")
		return  # Stop execution after sending the reply
	if len(message_text) >= 16:
		bot.reply_to(message, "bin must be less than 16 digit")
		return  # Stop execution after sending the reply
	bin = message_text
	if len(message_content) == 1:
		card_amount = 1
	else:
		try:
			card_amount = int(message_content[1])
		except ValueError:
			bot.reply_to(message, "you sent invalid card amount")
			return  # Stop execution after sending the reply
	cards = []
	for i in range(card_amount):
		# Replace each 'x' with a random digit
		card = ''.join([str(random.randint(0, 9)) if char == 'x' else char for char in bin])

		# If the number needs to be exactly 16 digits, add additional random digits at the end
		while len(card) < 16:
			card += str(random.randint(0, 9))
		# Generate a random month (1-12)
		random_month = random.randint(1, 12)

		# Generate a random year (you can define the range, for example, between 2000 and 2030)
		random_year = random.randint(2025, 2030)

		# Format the month and year as MM/YY
		random_date = f"{random_month:02d}/{str(random_year)[-2:]}"  # :02d ensures two digits for month
		random_csv = random.randint(100, 999)
		card = f"{card} {random_date} {random_csv}\n"
		cards.append(card)
	with open(f'{message.chat.id}.txt','w',encoding='utf-8') as f:
		f.writelines(cards)
	with open(f'{message.chat.id}.txt', 'rb') as file:
		bot.send_document(message.chat.id, file)
	os.remove(f'{message.chat.id}.txt')






# bot_thread = threading.Thread(target=bot.infinity_polling)
# bot_thread.start()
bot.polling()
