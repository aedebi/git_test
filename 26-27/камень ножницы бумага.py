from telebot import TeleBot
from random import choice

TOKEN = '8887628327:AAE1neLhfySbGzrOqL4IL1LQXJ9bmEBG3A0'
bot = TeleBot(TOKEN)
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'привет!') 
game_choise =["камень", "ножницы", "бумага"]
@bot.message_handler(func=lambda x: x.text.lower() in game_choise)
def game(message):
    global user_points
    global comp_points
    user_choice = message.text.lower
    bot_choice=choice(game_choise)
    bot.send_message(message.chat.id, bot_choice)
    if user_choice == "камень" and bot_choice == "ножницы":
        msg = 'Победа!'
        user_points += 1
    elif user_choice == "бумага" and bot_choice == "камень":
        msg = 'Победа!'
        user_points += 1
    elif user_choice == "ножницы" and bot_choice == "бумага":
        msg = 'Победа!'
        user_points += 1
    else:
        msg = "Ты проиграл"
        comp_points += 1
    bot.send_message(message.chat.id, msg)
@bot.message_handler(commands=['points'])
def points(message):
    bot.send_message(message.chat.id, f"бот: {comp_points} игрок: {user_points}")
@bot.message_handler(commands=['reset'])
def reset(message):
    comp_points = 0
    user_points = 0
    bot.send_message(message.chat.id, f"бот: {comp_points} игрок: {user_points}")

'''
class Game:
    comp = 0
    user = 0

    def update(self, user_winner):
        if user_winner:
            self.user += 1
            return 'победил'
        self.comp += 1
        return 'проиграл'
    
    def reset(self):
        self.comp = 0
        self.user = 0
'''

if __name__ == '__main__':
    bot.polling(none_stop = True)