#Импортироваине библиотек
from datetime import datetime
import sqlite3
from flask import Flask, request, json
import vk

#Переменные с клчом доступа сообщества и кодом подтверждения
token = '4445b9ec75eca61c00278e8c0ff24a2faacb108eb8551141c71b0aa7fd9385235e6eafcf25e3d0ca77459'
confirmation_token = '209bdff8'

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Как ты забрёл сюда? Это техническая страница для работы TimeTable Bot.'

@app.route('/', methods=['POST'])

def bot(): #Главная функция

    data = json.loads(request.data) #Получаем данные JSON

    #Кнопка
    keyboard = {
    "one_time": False,
    "buttons": [
      [{
        "action": {
          "type": "text",
          "payload": "{\"button\": \"1\"}",
          "label": "Пары сегодня"
        },
        "color": "default"
      }, {
        "action": {
          "type": "text",
          "payload": "{\"button\": \"1\"}",
          "label": "Пары завтра"
        },
        "color": "default"
      }],
      [{
        "action": {
          "type": "text",
          "payload": "{\"button\": \"1\"}",
          "label": "Следующая пара"
        },
        "color": "positive"
      }]
      ]}

    #Перевод клавиатуры в строку, как просит VK API
    keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
    keyboard = str(keyboard.decode('utf-8'))

    #Переменные с часами, минутами и днем недели
    hour = int(datetime.strftime(datetime.now(), "%H")) + 3 #Время +3 часа, т.к. на сервере часовой пояс UTC
    minutes = int(datetime.strftime(datetime.now(), "%M"))
    weekday = str(datetime.today().weekday())

    if 'type' not in data.keys(): #Если запрос не от ВК, то скрипт не выполняется
        return 'not vk'

    if data['type'] == 'confirmation': #Если запрос на подтверждение сервера, то возращаем код подтверждения
        return confirmation_token

    elif data['type'] == 'message_new': #Если приходит новое сообщение

        session = vk.Session(access_token = token)
        api = vk.API(session, v=5.85)
        user_id = data['object']['from_id'] #Получение UserId из JSON
        peer_id = data['object']['peer_id'] #Получение PeerID, чтобы бот знал, откуда пришло сообщение
        user_data = data['object']['text'] #Получение текста, отправленного пользователем


        #Обработка обращений к боту
        if user_data.startswith("[club172085604|@ttbot51], "): #Если строка начинается с @idбота, то @idбота убирается из строки
            user_message = user_data.replace("[club172085604|@ttbot51], ", "")
        elif user_data.startswith("[club172085604|@ttbot51] "):
            user_message = user_data.replace("[club172085604|@ttbot51] ", "")
        else:
            user_message = user_data


        #Обработка команд и ответ на них
        if user_message.lower() == "начать":
            api.messages.send(user_id = str(user_id), message = 'Привет, я бот, предназначенный для отправки расписания и домашней работы 51-ой группе. Чтобы посмотреть список команд, введите "помощь"', keyboard = keyboard)

        elif "пары сегодня" in user_message.lower():
            api.messages.send(peer_id = str(peer_id), message = timetable(False))

        elif "следующая пара" in user_message.lower():
            api.messages.send(peer_id = str(peer_id), message = next_class())

        elif "пары завтра" in user_message.lower():
            api.messages.send(peer_id = str(peer_id), message = timetable(True))

        elif "т1000" in user_message.lower()  :
            api.messages.send(peer_id = str(peer_id), message = "А кодом Марата можно подтереть жопу")

        elif user_message.lower() == "помощь":
            text = "Список команд:\n пары сегодня,\n пары завтра, \n следующая пара "
            api.messages.send(peer_id = str(peer_id), message = text)

        elif "рэп" in user_message.lower() :
            api.messages.send(peer_id = str(peer_id), message = 'Рэп для дебилов')

        elif "марат" in user_message.lower():
            api.messages.send(peer_id = str(peer_id), message = 'Марат - тупой говнокодер, все это знают.')

        elif user_message.lower() == "время":
            api.messages.send(peer_id = str(peer_id), message = str(hour) + ":" + str(minutes) + " " + weekday)

        return 'ok' #Выполненная функция должна возвращать ok, как требует VK API



def timetable(isTomorrow):

    if datetime.now().isocalendar()[1] % 2 == 1:
        isHighWeek = 1
    else:
        isHighWeek = 0

    if isTomorrow:
        weekDay = datetime.today().weekday() + 2
        text = "Расписание на завтра: \n\n" + "*****************************" + "\n\n"
    else:
        weekDay = datetime.today().weekday() + 1
        text = "Расписание на сегодня: \n\n" + "*****************************" + "\n\n"

    conn = sqlite3.connect('TimeTableData.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM timeTable')
    row = cursor.fetchone()

    while weekDay != row[8]:
        row = cursor.fetchone()

    while weekDay == row[8]:
        if row[3] == isHighWeek:
            if row[6] == 1:
                classType = "Практика "
            else:
                classType = "Лекция "

            shedule = str(row[2]) + ", " + classType + "\n" + str(row[1]) + "\n" + "Аудитория - " + str(row[5]) + ", " + str(row[4]) + "\n" + "Препод - " + str(row[7]) + "\n\n" + "*****************************" + "\n\n"
            text = text + shedule
            row = cursor.fetchone()
        else:
            row = cursor.fetchone()

    cursor.close()
    conn.close()

    return text

def next_class():

    hour = (int(datetime.strftime(datetime.now(), "%H")) + 3) * 60
    minutes = int(datetime.strftime(datetime.now(), "%M"))
    weekDay = datetime.today().weekday() + 1
    nowTime = hour + minutes
    text = "Сегодня пар больше нет"

    conn = sqlite3.connect('TimeTableData.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM timeTable')
    row = cursor.fetchone()

    if datetime.now().isocalendar()[1] % 2 == 1:
        isHighWeek = 0
    else:
        isHighWeek = 1

    while weekDay != row[8]:
        row = cursor.fetchone()

    while weekDay == row[8]:
        if row[3] == isHighWeek:

            if row[6] == 1:
                classType = "Практика "
            else:
                classType = "Лекция "

            shedule = str(row[2]) + ", " + classType + "\n" + str(row[1]) + "\n" + "Аудитория - " + str(row[5]) + ", " + str(row[4]) + "\n" + "Препод - " + str(row[7]) + "\n\n"

            classTime = int(row[1][0] + row[1][1]) * 60 + int(row[1][3] + row[1][4])

            if nowTime <= classTime:
                text = shedule
                break
            else:
                row = cursor.fetchone()

        else:
            row = cursor.fetchone()

    return text
