




import telebot
from telebot import types
import sqlite3
import time
import asyncio
from random import randint
#bot = telebot.TeleBot('1433503310:AAGCl7p2pBkmdQd_ivuqnHMrfEoFaJwjmWU')
bot = telebot.AsyncTeleBot('1431129673:AAHxSrKHQX4073FpL-r9kwO0jpBl0UkR-ME')


sec = 0

_connection = None
_connection2 = None

def get_connection():
    global _connection
    _connection = sqlite3.connect('anketa2.db',check_same_thread=False)
    return _connection

def get_connection2():
    global _connection2
    _connection2 = sqlite3.connect("upzazh.db",check_same_thread=False)
    return _connection2

def init_db(force: bool = False):
    conn = get_connection()
    c = conn.cursor()

    if force:
        c.execute('DROP TABLE IF EXISTS user_info')
        
    c.execute('''
            CREATE TABLE IF NOT EXISTS user_info(
                id  INTEGER PRIMARY KEY,
                user_id INTEGER NOT NULL,
                rost INTEGER,
                ves INTEGER,
                age INTEGER
            )
    ''')
    conn.commit()

def init_db_zan(force: bool = False):
    conn = get_connection()
    c = conn.cursor()

    if force:
        c.execute('DROP TABLE IF EXISTS user_info')
        
    c.execute('''
            CREATE TABLE IF NOT EXISTS user_info(
                id  INTEGER PRIMARY KEY,
                name text NOT NULL,
                lv0 text,
                lv1 text,
                lv2 text,
                lv3 text,
                picture text
            )
    ''')
    conn.commit()



def add_info(user_id: int, rost: int, ves: int, age:int):
    conn = get_connection()
    c = conn.cursor()
    ball = 0
    c.execute('INSERT INTO user_info(user_id, rost, ves, age, ball) VALUES(?,?,?,?,?)',(user_id,rost,ves,age,ball))
    conn.commit()
    c.close()

    

def get_info(user_id: int):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM user_info WHERE user_id ='+str(user_id))
    row = c.fetchone()
    rost = row[2]
    ves = row[3]
    age = row[4]
    ball = row[5]
    return rost, ves, age, ball
    conn.commit()
    c.close()

def udate_info(user_id: int, rost: int, ves: int, age:int, ball: int):
    conn = get_connection()
    c = conn.cursor()
    c.execute('UPDATE user_info SET rost = '+str(rost)+', ves = '+str(ves)+', age = '+str(age)+', ball = '+str(ball)+' WHERE user_id = '+str(user_id))
    conn.commit()
    c.close()

rost = 0
ves = 0
age = 0
ind = 0
upr = ['приседания', 'отжимания','прыжки на скакалке','подтягивания','бег']
kat = 0
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.from_user.id, "Привет, я спорт_бот, помогу тебе стать спортивным.").wait()
    bot.send_message(message.from_user.id, "Введи свой рост (Например: 187)").wait()
    bot.register_next_step_handler(message, get_rost)

def get_rost(message):
    global rost
    try:
        rost = int(message.text)
        bot.send_message(message.from_user.id, 'Введи свой вес').wait()
        bot.register_next_step_handler(message, get_ves)
    except:
        bot.send_message(message.from_user.id, 'Введите числом').wait()
        bot.register_next_step_handler(message, get_rost)
    

def get_ves(message):
    global ves
    global ind
    try:
        ves = int(message.text)
        bot.send_message(message.from_user.id, 'Ваш индекс тела:').wait()
        ind = ves/(rost/100*rost/100)
        bot.send_message(message.from_user.id, str(ind)).wait()
        if ind >=25:
            bot.send_message(message.from_user.id, 'Вам стоит сбросить вес').wait()
        if ind < 25 and ind >=17:
            bot.send_message(message.from_user.id, 'У вас нормальный индекс тела').wait()
        if ind <17:
            bot.send_message(message.from_user.id, 'Вам стоит набрать вес').wait()

        bot.send_message(message.from_user.id, 'Введите ваш возраст:').wait()
        bot.register_next_step_handler(message, age)
    except:
        bot.send_message(message.from_user.id, 'Введите числом').wait()
        bot.register_next_step_handler(message, get_ves)
    

def age(message):
    global age 
    global rost
    global ves 
    try:
        age = int(message.text)
        bot.send_message(message.from_user.id, '''Выберите нужное упражнение: 
        /pris - приседания
        /podt - подтягивания
        /beg - бег
        /otzhim - отжимания
        /berpi - берпи
        /vel - велосипед
        /plan - планка
        /beg2 - бег с высоким подъемом колен
        /pres - пресс
        /foot - махи ногами
        /foot2 - выпады
        /windmill - мельница
        /beg2 - бег в упоре лёжа
        /birch - берёзка
        /chair - cтульчик
        /dostig - узнать ваши достижения''')
    except:
        bot.send_message(message.from_user.id, 'Введите числом').wait()
        bot.register_next_step_handler(message, age)
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM user_info WHERE user_id ='+str(message.from_user.id))
    row = c.fetchone()
    conn.commit()
    if row == None:
        add_info(user_id = message.from_user.id, rost=rost, ves=ves, age=age)
    else:
        udate_info(user_id = message.from_user.id, rost=rost, ves=ves, age=age)
    c.close()
    

def uprazh(name2):
    conn = get_connection2()
    c = conn.cursor() 
    c.execute('SELECT * FROM user_info')
    while True:
        row = c.fetchone()
        if row[1] == name2:
            break
    inform = row[2]
    lv0 = row[3]
    lv1 = row[4]
    lv2 = row[5]
    lv3 = row[6]
    picture = row[7]
    c.close()
    return inform,lv0, lv1, lv2, lv3, picture
    
def timerr(message):
    global sec 
    h = ["https://ds02.infourok.ru/uploads/ex/01ac/0003beb3-7ab8b022/img22.jpg","https://sun9-16.userapi.com/INVy-wcp5PfJkQdkBngxnDvFncBv_rqk5pqlYA/1WNNxeBLtZE.jpg",
    "https://ne-kurim.ru/forum/attachments/molodec-jpg.1125450/", "https://sun9-46.userapi.com/Qz-dJPzKVUC7BbbqW4qm9rqB6N_JtHHnoD--vA/2WfAEIxEw-c.jpg",
    "https://cloud.prezentacii.org/18/10/93138/images/screen23.jpg","https://fs01.infourok.ru/images/doc/86/103722/img25.jpg",
    "https://sun9-55.userapi.com/K833PBZR_zeeQXNsfo2YsZ90LgKGhr4UCZvYWA/fDAum9wqSnA.jpg", "https://w7.pngwing.com/pngs/681/659/png-transparent-smiley-font-great-job-text-smiley-emoticon-thumbnail.png",
    "https://sun9-43.userapi.com/SM9XZoFYPs5NgbHIYpX6MDqqtwmQ377cj-umjw/mQWumGh9l-8.jpg"
    ]
    if message.text.lower() == 'да' or message.text.lower() == 'ок' or message.text.lower() == 'yes':
        count = sec
        bot.send_message(message.from_user.id,'Таймер запущен на '+ str(count)+ ' секунд').wait()
        while count > 0:
            time.sleep(1)
            count -= 1
        bot.send_message(message.from_user.id,'Время вышло') .wait()
        bot.send_message(message.from_user.id,'/list') .wait()
        a = randint(0,8)
        bot.send_photo(message.chat.id,h[a],"").wait() 
        rost,ves,age, ball = get_info(message.from_user.id)
        ball+=1
        udate_info(message.from_user.id, rost, ves, age, ball)
    else:
        bot.send_message(message.from_user.id,'Как-нибудь в другой раз!').wait()
        bot.send_message(message.from_user.id,'/list') .wait()

def zapUpr(message,name):
    tim = 0
    tim2 = 0
    flag = ""
    h = ['0','1','2','3','4','5','6','7','8','9']
    s = 0
    rost,ves,age, ball = get_info(message.from_user.id)
    inform, lv0, lv1, lv2, lv3, picture = uprazh(name)
    bot.send_message(message.from_user.id, inform).wait()
    bot.send_photo(message.chat.id,picture,name).wait()
    if (ves/((rost/100)*(rost/100))) > 30:
        bot.send_message(message.from_user.id, 'Упражнение не рекомендуется').wait()
    else:
        if age < 13:
            bot.send_message(message.from_user.id, lv0).wait()
            flag = lv0
        if age >= 13 and age < 18:
            bot.send_message(message.from_user.id, lv1).wait()
            flag = lv1
        if age >= 18 and age < 45:
            bot.send_message(message.from_user.id, lv2).wait()
            flag = lv2
        if age >= 45:
            bot.send_message(message.from_user.id, lv3).wait()
            flag = lv3
        tim1 = flag.find('Таймер')
        tim2 = flag[tim1:len(flag)]
        for i in range(len(tim2)):
            if tim2[i] in h:
                s = s*10 + int(tim2[i])
        return s

@bot.message_handler(commands=['dostig'])
def dos(message):
    rost,ves,age, ball = get_info(message.from_user.id)
    bot.send_message(message.from_user.id,'У вас всего '+str(ball)+' баллов.').wait()
    if ball <=5 :
        bot.send_message(message.from_user.id,'Нужно еще постараться!').wait()
    if ball > 5 and ball <= 10:
        bot.send_message(message.from_user.id,'Ваше достижение - начинающий спортсмен').wait()
    if ball > 10 and ball <= 15:
        bot.send_message(message.from_user.id,'Ваше достижение - спортсмен любитель').wait()
    if ball > 15:
        bot.send_message(message.from_user.id,'Ваше достижение - профессиональный спортсмен!!').wait()


@bot.message_handler(commands=['list'])
def start1(message): 
    bot.send_message(message.from_user.id, '''Выберите нужное упражнение: 
    /list - вывести список упражнений
    /pris - приседания
    /podt - подтягивания
    /beg - бег
    /otzhim - отжимания
    /berpi - берпи
    /vel - велосипед
    /plan - планка
    /beg2 - бег с высоким подъемом колен
    /pres - пресс
    /foot - махи ногами
    /foot2 - выпады
    /windmill - мельница
    /beg2 - бег в упоре лёжа
    /birch - берёзка
    /chair - cтульчик
    /dostig - узнать ваши достижения''')

@bot.message_handler(commands=['pris'])
def start3(message):
    global sec 
    name = 'Приседания'
    s = zapUpr(message,name)
    bot.send_message(message.from_user.id,'Запустить таймер?').wait()
    sec = s
    bot.register_next_step_handler(message, timerr)


@bot.message_handler(commands=['otzhim'])
def start4(message):
    global sec
    name = 'Отжимания'
    s = zapUpr(message,name)
    bot.send_message(message.from_user.id,'Запустить таймер?').wait()
    sec = s
    rost,ves,age, ball = get_info(message.from_user.id)
    ball+=1
    udate_info(message.from_user.id, rost, ves, age, ball)
    bot.register_next_step_handler(message, timerr)
   
@bot.message_handler(commands=['beg'])
def start2(message): 
    global sec
    name = 'Бег'
    s = zapUpr(message,name)
    bot.send_message(message.from_user.id,'Запустить таймер?').wait()
    sec = s
    bot.register_next_step_handler(message, timerr)

@bot.message_handler(commands=['berpi'])
def start5(message): 
    global sec
    name = 'Берпи'
    s = zapUpr(message,name)
    bot.send_message(message.from_user.id,'Запустить таймер?').wait()
    sec = s
    bot.register_next_step_handler(message, timerr)

@bot.message_handler(commands=['podt'])
def start6(message): 
    global sec
    name = 'Подтягивания'
    s = zapUpr(message,name)
    bot.send_message(message.from_user.id,'Запустить таймер?').wait()
    sec = s
    bot.register_next_step_handler(message, timerr)

@bot.message_handler(commands=['vel'])
def start7(message): 
    global sec
    name = 'Велосипед'
    s = zapUpr(message,name)
    bot.send_message(message.from_user.id,'Запустить таймер?').wait()
    sec = s
    bot.register_next_step_handler(message, timerr)

@bot.message_handler(commands=['plan'])
def start8(message):
    global sec 
    name = 'Планка'
    s = zapUpr(message,name)
    bot.send_message(message.from_user.id,'Запустить таймер?').wait()
    sec = s
    bot.register_next_step_handler(message, timerr)

@bot.message_handler(commands=['beg2'])
def start9(message):
    global sec 
    name = 'Бег с высоким подъемом колен'
    s = zapUpr(message,name)
    bot.send_message(message.from_user.id,'Запустить таймер?').wait()
    sec = s
    bot.register_next_step_handler(message, timerr)

@bot.message_handler(commands=['pres'])
def start10(message):
    global sec 
    name = 'Пресс'
    s = zapUpr(message,name)
    bot.send_message(message.from_user.id,'Запустить таймер?').wait()
    sec = s
    bot.register_next_step_handler(message, timerr)


@bot.message_handler(commands=['foot'])
def start11(message): 
    global sec
    name = 'Махи ногами'
    s = zapUpr(message,name)
    bot.send_message(message.from_user.id,'Запустить таймер?').wait()
    sec = s
    bot.register_next_step_handler(message, timerr)

@bot.message_handler(commands=['foot2'])
def start12(message):
    global sec 
    name = 'Выпады'
    s = zapUpr(message,name)
    bot.send_message(message.from_user.id,'Запустить таймер?').wait()
    sec = s
    bot.register_next_step_handler(message, timerr)

@bot.message_handler(commands=['windmill'])
def start13(message):
    global sec 
    name = 'Мельница'
    s = zapUpr(message,name)
    bot.send_message(message.from_user.id,'Запустить таймер?').wait()
    sec = s
    bot.register_next_step_handler(message, timerr)

@bot.message_handler(commands=['beg2'])
def start14(message): 
    global sec
    name = 'Бег в упоре лёжа'
    s = zapUpr(message,name)
    bot.send_message(message.from_user.id,'Запустить таймер?').wait()
    sec = s
    bot.register_next_step_handler(message, timerr)

@bot.message_handler(commands=['birch'])
def start14(message): 
    global sec
    name = 'Берёзка'
    s = zapUpr(message,name)
    bot.send_message(message.from_user.id,'Запустить таймер?').wait()
    sec = s
    bot.register_next_step_handler(message, timerr)

@bot.message_handler(commands=['chair'])
def start14(message): 
    global sec
    name = 'Стульчик'
    s = zapUpr(message,name)
    bot.send_message(message.from_user.id,'Запустить таймер?').wait()
    sec = s
    bot.register_next_step_handler(message, timerr)

bot.polling()

