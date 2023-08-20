import telebot
import sqlite3

bot = telebot.TeleBot('6406476329:AAHWoWf_LWWZ1nWkyN8471h4NhcxIzvJjyI')

@bot.message_handler(commands=['start'])
def start(message):
    #создание бд
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()

    #создание таблицы в бд
    cursor.execute("CREATE TABLE IF NOT EXISTS login_id( id INTEGER );")
    connect.commit()

    #Перед вводом данных в таблицу, осуществляем проверку на наличие id
    people_id = message.chat.id
    cursor.execute(f"SELECT id FROM login_id WHERE id={people_id}")
    data = cursor.fetchone()
    if data is None:
        #Добавляем записи в таблицу
        user_id = [message.chat.id]
        cursor.execute("INSERT INTO login_id VALUES(?);", user_id)
        connect.commit()
    else:
        bot.send_message(message.chat.id, 'Такой пользователь уже существует')

@bot.message_handler(commands=['delete'])
def delete(message):
    # подключение к бд
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()

    people_id = message.chat.id
    cursor.execute(f"DELETE FROM login_id WHERE id={people_id}")
    connect.commit()

bot.polling()