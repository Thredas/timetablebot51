from datetime import datetime
from flask import Flask, request, json
import vk

token = '4445b9ec75eca61c00278e8c0ff24a2faacb108eb8551141c71b0aa7fd9385235e6eafcf25e3d0ca77459'
confirmation_token = '209bdff8'

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Как ты забрёл сюда? Это техническая страница для работы TimeTable Bot.'

@app.route('/', methods=['POST'])

def bot():

    data = json.loads(request.data)

    keyboard = {
    "one_time": False,
    "buttons": [
      [{
        "action": {
          "type": "text",
          "payload": "{\"button\": \"1\"}",
          "label": "Расписание"
        },
        "color": "primary"
      }]]}

    keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
    keyboard = str(keyboard.decode('utf-8'))

    hours = int(datetime.strftime(datetime.now(), "%H")) + 3
    minutes = int(datetime.strftime(datetime.now(), "%M"))
    weekDay = str(datetime.today().weekday())

    if 'type' not in data.keys():
        return 'not vk'

    if data['type'] == 'confirmation':
        return confirmation_token

    elif data['type'] == 'message_new':

        session = vk.Session(access_token = token)
        api = vk.API(session, v=5.85)
        user_id = data['object']['from_id']
        peer_id = data['object']['peer_id']
        user_data = data['object']['text']


        #Обработка обращений к боту
        if user_data.startswith("[club172085604|@timetablebot51], "):
            user_message = user_data.replace("[club172085604|@timetablebot51], ", "")
        elif user_data.startswith("[club172085604|@timetablebot51] "):
            user_message = user_data.replace("[club172085604|@timetablebot51] ", "")
        else:
            user_message = user_data


        #Обработка команд и ответ на них
        if user_message == "Начать":
            api.messages.send(access_token = token, user_id = str(user_id), message = 'Привет, я бот, предназначенный для отправки расписания и домашней работы 51-ой группе. Чтобы посмотреть список команд, введите "помощь"', keyboard = keyboard)

        elif user_message.lower() == "расписание":
            api.messages.send(peer_id = str(peer_id), message = raspisanie())

        elif user_message.lower() == "привет":
            api.messages.send(peer_id = str(peer_id), message = "Привет, если ты не знаешь как мной пользоваться введи \"помощь\"")

        elif user_message.lower() == "помощь":
            text = "Список команд:\n расписание,\n домашняя работа "
            api.messages.send(peer_id = str(peer_id), message = text)

        elif user_message.lower() == "рэп для дебилов?":
            api.messages.send(peer_id = str(peer_id), message = 'Даже не обсуждается')

        elif user_message.lower() == "марат лох?":
            api.messages.send(peer_id = str(peer_id), message = 'Да')

        elif user_message.lower() == "время":
            api.messages.send(peer_id = str(peer_id), message = str(hours) + ":" + str(minutes) + " " + weekDay)

        else:
            api.messages.send(peer_id = str(peer_id), message = 'Такой команды нет')

        if str(user_id) == "259297514":
            api.messages.send(peer_id = str(peer_id), message = 'Тупое ониме')

        return 'ok'



def raspisanie():

    hours = int(datetime.strftime(datetime.now(), "%H")) + 3
    weekDay = int(datetime.today().weekday())

    times = ["8:00", "9:30", "9:40", "11:10", "11:50", "13:20", "13:30", "15:00", "15:10", "16:40"]
    classes = ["ТСИ", "Математика", "Физ-ра", "Основы программирования", "Английский", "Архитектура комп. систем", "IT", "Операционнные системы"]
    classRooms = ["109, УЛК5", "412, УЛК2", "308, УБК", "320, УЛК2", "322, УБК", "320, УБК", "418, УЛК2", "302, УЛК2", "308, УЛК2"]
    teachers = ["Альбина Рашидовна", "Анна Николаевна", "", "Екатерина Валерьевна", "Марьям Рифовна", "Айгуль Фларитовна", "Айрат Анварович", "Ольга Николаевна"]

    isHighWeek = True

    if isHighWeek == False:

        if weekDay == 0:
            if hours <= 11: #ТСИ
                zanyatie = classes[0]
                time = times[4] + " - " + times[5]
                classRoom = classRooms[0]
                teacher = teachers[0]

            elif hours >= 11 and hours <= 13: #ТСИ
                zanyatie = classes[0]
                time = times[6] + " - " + times[7]
                classRoom = classRooms[1]
                teacher = teachers[0]

            elif hours >= 13 and hours <= 15: #ТСИ
                zanyatie = classes[0]
                time = times[8] + " - " + times[9]
                classRoom = classRooms[1]
                teacher = teachers[0]

            else:
                return "На сегодня пар больше нет"

        elif weekDay == 1:
            if hours <= 13: #Матан
                zanyatie = classes[1]
                time = times[6] + " - " + times[7]
                classRoom = classRooms[2]
                teacher = teachers[1]

            elif hours >= 13 and hours <= 15: #Матан
                zanyatie = classes[1]
                time = times[8] + " - " + times[9]
                classRoom = classRooms[3]
                teacher = teachers[1]

            else:
                return "На сегодня пар больше нет"

        elif weekDay == 2:
            if hours <= 8: #Физра
                zanyatie = classes[2]
                time = times[0] + " - " + times[1]
                classRoom = "Спорткомплекс"
                teacher = teachers[2]

            elif hours >= 8 and hours <= 9: #Инглиш
                zanyatie = classes[4]
                time = times[2] + " - " + times[3]
                classRoom = classRooms[5]
                teacher = teachers[4]

            elif hours >= 9 and hours <= 11: #ОП
                zanyatie = classes[3]
                time = times[4] + " - " + times[5]
                classRoom = classRooms[1]
                teacher = teachers[3]

            elif hours >= 11 and hours <= 13: #ОП
                zanyatie = classes[3]
                time = times[6] + " - " + times[7]
                classRoom = classRooms[4]
                teacher = teachers[3]

            else:
                return "На сегодня пар больше нет"

        elif weekDay == 3:
            if hours <= 8: #Архитектура КС
                zanyatie = classes[5]
                time = times[0] + " - " + times[1]
                classRoom = classRooms[1]
                teacher = teachers[5]

            else:
                return "На сегодня пар больше нет"

        elif weekDay == 4:
            if hours <= 8: #IT
                zanyatie = classes[6]
                time = times[0] + " - " + times[1]
                classRoom = classRooms[6]
                teacher = teachers[6]

            elif hours >= 8 and hours <= 9: #IT
                zanyatie = classes[6]
                time = times[2] + " - " + times[3]
                classRoom = classRooms[7]
                teacher = teachers[6]

            elif hours >= 9 and hours <= 11: #Матан
                zanyatie = classes[1]
                time = times[4] + " - " + times[5]
                classRoom = classRooms[2]
                teacher = teachers[1]

            elif hours >= 11 and hours <= 13: #Матан
                zanyatie = classes[1]
                time = times[6] + " - " + times[7]
                classRoom = classRooms[3]
                teacher = teachers[1]
            else:
                return "На сегодня пар больше нет"

        elif weekDay == 5:
            if hours <= 8: #ОС
                zanyatie = classes[7]
                time = times[0] + " - " + times[1]
                classRoom = classRooms[8]
                teacher = teachers[7]

            elif hours >= 8 and hours <= 9: #ОС
                zanyatie = classes[7]
                time = times[2] + " - " + times[3]
                classRoom = classRooms[2]
                teacher = teachers[7]

            elif hours >= 9 and hours <= 11: #ОС
                zanyatie = classes[7]
                time = times[4] + " - " + times[5]
                classRoom = classRooms[2]
                teacher = teachers[7]

            elif hours >= 11 and hours <= 13: #Архитектура КС
                zanyatie = classes[5]
                time = times[6] + " - " + times[7]
                classRoom = classRooms[1]
                teacher = teachers[5]
            else:
                return "На сегодня пар больше нет"

        elif weekDay == 6:
            isHighWeek = True
            return "На сегодня пар больше нет"
    else:

        if weekDay == 0:
            if hours <= 13: #ТСИ
                zanyatie = classes[0]
                time = times[6] + " - " + times[7]
                classRoom = classRooms[4]
                teacher = teachers[0]

            elif hours >= 13 and hours <= 15: #ТСИ
                zanyatie = classes[0]
                time = times[8] + " - " + times[9]
                classRoom = classRooms[1]
                teacher = teachers[0]

            else:
                return "На сегодня пар больше нет"

        elif weekDay == 1:
            if hours <= 13: #ОП
                zanyatie = classes[3]
                time = times[6] + " - " + times[7]
                classRoom = classRooms[2]
                teacher = teachers[3]

            else:
                return "На сегодня пар больше нет"

        elif weekDay == 2:
            if hours <= 8: #Физра
                zanyatie = classes[2]
                time = times[0] + " - " + times[1]
                classRoom = "Спорткомплекс"
                teacher = teachers[2]

            elif hours >= 8 and hours <= 9: #Инглиш
                zanyatie = classes[4]
                time = times[2] + " - " + times[3]
                classRoom = classRooms[5]
                teacher = teachers[4]

            elif hours >= 9 and  hours <= 11: #ОП
                zanyatie = classes[3]
                time = times[4] + " - " + times[5]
                classRoom = classRooms[1]
                teacher = teachers[3]

            elif hours >= 11 and hours <= 13: #ОП
                zanyatie = classes[3]
                time = times[6] + " - " + times[7]
                classRoom = classRooms[4]
                teacher = teachers[3]

            else:
                return "На сегодня пар больше нет"

        elif weekDay == 3:
            if hours <= 8: #Архитектура КС
                zanyatie = classes[5]
                time = times[0] + " - " + times[1]
                classRoom = classRooms[8]
                teacher = teachers[5]

            elif hours >= 8 and hours <= 9: #Архитектура КС
                zanyatie = classes[5]
                time = times[2] + " - " + times[3]
                classRoom = classRooms[0]
                teacher = teachers[5]

            elif hours >= 9 and hours <= 11: #Архитектура КС
                zanyatie = classes[5]
                time = times[4] + " - " + times[5]
                classRoom = classRooms[1]
                teacher = teachers[5]

            else:
                return "На сегодня пар больше нет"

        elif weekDay == 4:
            if hours <= 8: #IT
                zanyatie = classes[6]
                time = times[0] + " - " + times[1]
                classRoom = classRooms[6]
                teacher = teachers[6]

            elif hours >= 8 and hours <= 9: #IT
                zanyatie = classes[6]
                time = times[2] + " - " + times[3]
                classRoom = classRooms[7]
                teacher = teachers[6]

            elif hours >= 9 and hours <= 11: #Матан
                zanyatie = classes[1]
                time = times[4] + " - " + times[5]
                classRoom = classRooms[2]
                teacher = teachers[1]

            elif hours >= 11 and hours <= 13: #Матан
                zanyatie = classes[1]
                time = times[6] + " - " + times[7]
                classRoom = classRooms[3]
                teacher = teachers[1]
            else:
                return "На сегодня пар больше нет"

        elif weekDay == 5:
            if hours <= 8: #ОС
                zanyatie = classes[7]
                time = times[0] + " - " + times[1]
                classRoom = classRooms[8]
                teacher = teachers[7]

            elif hours >= 8 and hours <= 9: #ОС
                zanyatie = classes[7]
                time = times[2] + " - " + times[3]
                classRoom = classRooms[2]
                teacher = teachers[7]

            elif hours >= 9 and hours <= 11: #ОС
                zanyatie = classes[7]
                time = times[4] + " - " + times[5]
                classRoom = classRooms[2]
                teacher = teachers[7]

            elif hours >= 11 and hours <= 13: #ОС
                zanyatie = classes[7]
                time = times[6] + " - " + times[7]
                classRoom = classRooms[2]
                teacher = teachers[7]
            else:
                return "На сегодня пар больше нет"

        elif weekDay == 6:
            isHighWeek = False
            return "На сегодня пар больше нет"

    text = "Следующая пара - " + zanyatie + "\n" + time + "\n" + "Аудитория - " + classRoom + "\n" + "Препод - " + teacher
    return text



