import sqlite3
from random import shuffle


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
        sql = f"UPDATE players SET role = '{role}' WHERE player_id = {row[0]}"
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
    for row in data:
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


def clear(dead=False):
    con = sqlite3.connect("db.db")
    cur = con.cursor()
    sql = f"UPDATE players SET citizen_vote = 0, mafia_vote = 0, voted = 0"
    if dead:
        sql += ', dead = 0'
    cur.execute(sql)
    con.commit()
    con.close()