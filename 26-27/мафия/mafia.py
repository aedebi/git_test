import sqlite3
from telebot import TeleBot
from random import choice, shuffle
import json
import db

con = sqlite3.connect("db.db")
cur = con.cursor()

TOKEN = '8887628327:AAE1neLhfySbGzrOqL4IL1LQXJ9bmEBG3A0'
bot = TeleBot(TOKEN)
game = False
night = False

def get_mafia_username():
    con = sqlite3.connect("db.db")
    cur = con.cursor()
    sql = f"SELECT username from players where role = 'mafia' "
    cur.execute(sql)
    data = cur.fetchall()
    names = ' '
    for row in data:
        name = row[0]
        names += name + '\n'
    con.close()
    return names

def get_players_roles():
    con = sqlite3.connect("db.db")
    cur = con.cursor()
    sql = f"SELECT player_id, role FROM players "
    cur.execute(sql)
    data = cur.fetchall()
    con.close()
    return data

def vote(type, username, player_id):
    con = sqlite3.connect("db.db")
    cur = con.cursor()
    sql = f"SELECT usernamee FROM players WHERE player_id ={player_id} AND dead = 0 AND voted = 0"
    cur.execute(sql)
    can_vote = cur.fetchall()
    cur.execute(f"UPDATE players SET (type) = (type) + 1 WHERE usernames = (username)")
    
    if can_vote:
        sql = '''UPDATE players
        SET voted = 1
        WHERE player_id = {player_id}
        '''
        cur.execute(sql)
        con.close()


def mafia_kill():
    con = sqlite3.connect("db.db")
    cur = con.cursor()
    cur.execute = (f"SELECT MAX(mafia_vote) FROM  players")
    max_votes = cur.fetchone()[0]
    cur.execute(f"SELECT COUNT (*) FROM players WHERE dead = 0 AND role = 'mafia'")
    mafia_alive = cur.fetchone()[0]
    username_killed = 'никого'
    if max_votes == mafia_alive:
        cur.execute(f"SELECT username FROM players WHERE mafia_vote = {max_votes}")
        username_killed = cur.fetchone()[0]
        cur.execute(f"UPDATE players SET dead = 1 WHERE username = '{username_killed}")
        con.commit()
    con.close()
    return username_killed


def citizens_kill():
    con = sqlite3.connect("db.db")
    cur = con.cursor()
    cur.execute = (f"SELECT MAX(citizen_vote) FROM  players")
    max_votes = cur.fetchone()[0]
    cur.execute(f"SELECT COUNT (*) FROM players WHERE citizen_vote = {max_votes}")
    max_votes_count = cur.fetchone()[0]
    username_killed = 'никого'
    if max_votes_count == 1:
        cur.execute(f"SELECT username FROM players WHERE citizen_vote = {max_votes}")
        username_killed = cur.fetchone()[0]
        cur.execute(f"UPDATE players SET dead = 1 WHERE username = '{username_killed}")
        con.commit()
    con.close()
    return username_killed
    


@bot.message_handler(func=lambda m: m.text.lower() == '/start' and m.chat.type == 'private')
def send_text(message):
    bot.send_message(message.chat.id, f'{message.from_user.first_name} играет')
    bot.send_message(message.from_user.id, 'Вы добавлены в игру')
    db.insert_player(message.from_user.id, username=message.from_user.username)

@bot.message_handler(commands=['start_game'])
def game_start(message):
    global game
    players = db.get_players_amount()
    if players >= 5 and not game:
        db.set_roles(players)
        players_roles = db.get_players_roles()
        mafia_usernames = db.get_mafia_usernames()
        for player_id, role in players_roles:
            bot.send_message(player_id, text=role)
            if role == 'mafia':
                bot.send_message(player_id, 
                                 text=f'Все члены мафии:\n{", ".join(mafia_usernames)}')
        game = True
        bot.send_message(message.chat.id, text='Игра началась!')
        return

    bot.send_message(message.chat.id, text='недостаточно людей!')


def get_all_alive():
    con = sqlite3.connect("db.db")
    cur = con.cursor()
    sql = f"SELECT username FROM players WHERE 'dead' = 0"
    cur.execute(sql)
    data = cur.fetchall()
    con.close()
    data = [row[0] for row in data]
    return data

def set_roles(players):
    game_roles = ['citizen']*players
    mafias = int(players*0.3)
    for i in range(mafias):
        game_roles[i] = 'mafia'
        shuffle(game_roles)
    con = sqlite3.connect("db.db")
    cur = con.cursor()
    sql = f"SELECT player_id FROM players"
    cur.execute(sql)
    data = cur.fetchall()
    data = [row[0] for row in data]

    for role, player_id in zip(game_roles, data):
        sql = f"UPDATE players SET role = '{role}' WHERE player_id = {player_id}"
        cur.execute(sql)
    con.commit()
    con.close()



def insert_player(player_id, username):
    con = sqlite3.connect("db.db")
    cur = con.cursor()
    sql = f"INSERT INTO players (player_id, username) VALUES ('{player_id}', '{username}')"
    cur.execute(sql)
    con.commit()
    con.close()

def players_amount():
    con = sqlite3.connect("db.db")
    cur = con.cursor()
    sql = f"SELECT * FROM PLAYERS"
    cur.execute(sql)
    res = cur.fetchall()
    con.close()
    return len(res)


def get_mafia_usernames():
    con = sqlite3.connect("db.db")
    cur = con.cursor()
    sql = f"SELECT usernames FROM PLAYERS WHERE role = 'mafia'"
    cur.execute(sql)
    res = cur.fetchall()
    names = ' '
    for row in res:
        name = row[0]
        names += name + '\n'
    con.close()
    return names
 
@bot.message_handler(commands=["kick"])
def kick(message):
    username = ' '.join(message.text.split(' ')[1:])
    usernames = db.get_all_alive()
    if not night:
        if not username in usernames:
            bot.send_message(message.chat.id, 'Такого имени нет')
            return
        voted = db.vote("citizen_vote", username, message.from_user.id)
        if voted:
            bot.send_message(message.chat.id, 'Ваш голос учтен')
            return
        bot.send_message(message.chat.id, 'У вас больше нет права голосовать')
        return
    bot.send_message(
        message.chat.id, 'Сейчас ночь вы не можете никого выгнать')


def clear(dead=False):
    con = sqlite3.connect("db.db")
    cur = con.cursor()
    sql = f"UPDATE players SET citizen_vote = 0, mafia_vote = 0, voted = 0"
    if dead:
        sql += ', dead = 0'
    cur.execute(sql)
    con.commit()
    con.close()



