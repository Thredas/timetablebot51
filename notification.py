# This Python file uses the following encoding: utf-8
from datetime import datetime
import sqlite3
import vk

token = '4445b9ec75eca61c00278e8c0ff24a2faacb108eb8551141c71b0aa7fd9385235e6eafcf25e3d0ca77459'
t = True
session = vk.Session(access_token = token)
api = vk.API(session, v=5.85)

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

api.messages.send(peer_id = str(201225663), message = next_class())
