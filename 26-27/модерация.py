from telebot import TeleBot, types
from random import choice, randint
from time import time

with open('bad_words.txt', 'r', encoding='utf-8') as f:
    data = [word.strip().lower() for word in f.readlines()]

TOKEN = '8887628327:AAE1neLhfySbGzrOqL4IL1LQXJ9bmEBG3A0'
bot = TeleBot(TOKEN)
def is_group(message):
    return message.chat.type in ('group', 'supergroup')

sun_check = 0

@bot.message_handler(commands=["check"])
def default_test(message):
    global sum_check
    keyboard = types.InlineKeyboardMarkup()
    numbers = ["один", "два" ,"три", "четыре", "пять", "шесть", "семь", "восемь", "девять", "десять"]
    keys = []
    for indx, number in enumerate(numbers):
        keys.append(types.InlineKeyboardButton(
            text=number, callback_data=indx+1))
    keyboard.row(*keys)
    n1 = randint(1,5)
    n2 = randint(1,5)
    sum_check = n1 + n2
    bot.send_message(
        message.chat.id, f"Решите пример: {n1} + {n2} = ?", reply_markup=keyboard)
    @bot.callback_query_handler(func=lambda call: call.data)
    def callback_inlite(call):
        global sum_check
        if int(call.data) == sum_check:
            bot.edit_message_text(chat_id=call.message.chat.id,
                                message_id=call.message.message_id,
                                text='Проверка пройдена')

        if int(call.data) != sum_check:
            bot.ban_chat_member(
                    call.message.chat.id,
                    call.from_user.id)


@bot.message_handler(func=lambda message: message.entities is not None and is_group(message))
def delete_links(message):
    for entity in message.entities:
        if entity.type in ["url", "text_link"]:
            bot.delete_message(message.chat.id, message.message_id)

@bot.message_handler(func=lambda message: has_bad_words(message.text.lower()) and is_group(message))

def has_bad_words(text):
    message_words = text.split(' ')
    for word in message_words:
        if word in data:
            return True
    return False



            


def bad_badwords(message):
    bot.restrict_chat_member(
        message.chat.id,
        message.from_user.id,
        until_date = time()+1200)
    bot.send_message(message.chat.id, text = 'Тебе бан на 20 минут',
                     reply_to_message_id=message.message_id)



    
if __name__ == '__main__':
    bot.polling(none_stop = True)