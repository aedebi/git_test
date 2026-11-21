from telebot import TeleBot
from random import choice
import json

TOKEN = '8887628327:AAE1neLhfySbGzrOqL4IL1LQXJ9bmEBG3A0'
bot = TeleBot(TOKEN)

with open('cities.txt', 'r', encoding='utf-8') as f:
    cities = []
    for line in f.readlines():
        cities.append(line.strip().lower())

with open('cities.txt', 'r', encoding='utf-8') as f:
    cities = [word.strip().lower() for word in f.readlines()]
game = False
used_cities = []
points = 0
leaderboard = {}
letter = ''    
def select_letter(text):
    i = 1
    while text[-1*i] in ('ъ', 'ы', 'ь', 'ё'):
        i += 1
    return text[-1*i]

@bot.message_handler(commands=['goroda'])
def goroda(message):
    global game
    global letter
    game = True
    city = choice(cities)
    letter = select_letter(city)
    bot.send_message(message.chat.id, city)


@bot.message_handler()
def game(message):
    global used_words, letter, game, points
    from telebot import TeleBot



def goroda(message):
    city = choice(cities)
    letter = select_letter(city)
    bot.send_message(message.chat.id, city)

@bot.message_handler()
def game(message):
    global used_words, letter, game, points
    if game:
        if message.text.lower() in used_words:
            print(letter)
            bot.send_message(message.chat.id, 'Город назывался!')
            return
        if message.text.lower()[0] != letter:
            bot.send_message(message.chat.id, 'Не та буква!')
            return
        if message.text.lower() in cities:
            if message.from_user.first_name in leaderboard:
                leaderboard[message.from_user.first_name] += 1
            else:
                leaderboard[message.from_user.first_name] = 1
            letter = select_letter(message.text.lower())
            used_words.append(message.text.lower())
            for city in cities:
                if city[0] == letter and city not in used_words:
                    letter = select_letter(city)
                    bot.send_message(message.chat.id, city)
                    used_words.append(city)
                    return
            bot.send_message(message.chat.id, 'Я проиграл')
            game = False
            return
        bot.send_message(message.chat.id, 'Такого города не существует!')
        if message.text.lower() in cities:
            select_letter(message.text.lower())



            if message.from_user.first_name in leaderboard:
                leaderboard[message.from_user.first_name] += 1
            else:
                leaderboard[message.from_user.first_name] = 1
    

@bot.message_handler(commands=['save'])
def save(message):
    with open ('scores.json', 'w', encoding='utf-8') as f:
        json.dump(leaderboard,f)
    bot.send_message(message.chat.id, 'Прогресс сохранен!')


    





    
if __name__ == '__main__':
    bot.polling(none_stop = True)


