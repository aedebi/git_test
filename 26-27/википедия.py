import requests
from telebot import TeleBot, types
import wikipedia
wikipedia.set_lang("ru")
TOKEN = '8887628327:AAE1neLhfySbGzrOqL4IL1LQXJ9bmEBG3A0'
bot = TeleBot(TOKEN)
def random_duck():
    url = 'https://random-d.uk/api/random'
    res = requests.get(url)
    data =res.json()
    return data['url']


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'привет!') 
@bot.message_handler(commands=['duck'])
def duck(message):
    url = random_duck()
    bot.send_message(message.chat.id, url)



@bot.callback_query_handler(func=lambda call: True)
def answer(call):
    page = wikipedia.page(call.data)
    bot.send_message(call.message.chat.id, text=page.title)
    bot.send_message(call.message.chat.id, text=page.summary)
    bot.send_message(call.message.chat.id, text=page.url)

@bot.message_handler(commands=['wiki'])
def wiki(message):
    text = ' '.join(message.text.split(' ')[1:])
    try:
        results = wikipedia.search(text, results=1)
    except Exception as e:
        bot.send_message(message.chat.id, "Ничего не найдено.")
        return
    markup = types.InlineKeyboardMarkup()
    for res in results:
        markup.add(types.InlineKeyboardButton(res, callback_data=res))
    bot.send_message(
        message.chat.id, text= 'Смотри, что я нашел!', reply_markup=markup)




if __name__ == '__main__':
    bot.polling(none_stop = True)