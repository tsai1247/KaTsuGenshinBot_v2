from os import getenv
import sqlite3
import time
from typing import Any
from function import *
from telegram import InlineKeyboardButton

from interact_with_imgur import uploadAndGetPhoto

cache = Cache()

def Start_Bot(update, bot):
    Message.Send.Text(getRoomID(update), 'just use /set to turn on/off nitifications. ')
    return

def sendNotification():
    success = False
    for i in range(10):
        try:
            Message.Send.Text(int(getenv('DEVELOP')), 'start Notification')
            success = True
            break
        except Exception as err:
            print(err)
            time.sleep(2)
    if not success: return



    while True:
        try:
            curTime = time.time()

            conn = sqlite3.connect('data.db')
            c = conn.cursor()
            cursor = c.execute(f'SELECT ID, text, file from notification where time < {curTime} and sent is NULL')
            init = False
            data = cursor.fetchall()
            for row in data:
                ID = row[0]
                text = row[1]
                file = row[2]

                if not init:
                    cursor = c.execute(f'SELECT roomID from rooms where isEnabled = 1')
                    roomIDList = []
                    for row in cursor:
                        roomIDList.append(row[0])

                for roomID in roomIDList:
                    if file == '' and text == '':
                        break
                    if file == '':
                        Message.Send.Text(roomID, text)
                    else:
                        Message.Send.Photo(roomID, file, title = text)

                c.execute(f"UPDATE notification set sent = 1 where ID={ID}")
                conn.commit()
            conn.close()
            time.sleep(600)
        except Exception as err:
            print('err:', err)
            break
    try:
        Message.Send.Text(int(getenv('DEVELOP')), 'end Notification')
    except:
        pass

def setNotification(update, bot):
    roomID = getRoomID(update)
    if cache.get(roomID, 'setNotificationMessage') != None:
        Message.Delete(roomID, cache.get(roomID, 'setNotificationMessage').message_id)

    buttons = [
        [InlineKeyboardButton('True', callback_data=f"True {roomID}"), InlineKeyboardButton('False', callback_data=f"False {roomID}")]
    ]

    curStatus = cache.get(roomID, 'isNotificationEnabled') == "1"
    if not curStatus:
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        cursor = c.execute(f'SELECT isEnabled from rooms where roomID = {roomID}')
        data = cursor.fetchall()
        if len(data) == 0:
            c.execute(f"INSERT INTO rooms \
                VALUES ({roomID}, {False})")
            conn.commit()
        else:
            curStatus = data[0][0]

        conn.close()

    message= Message.Send.Button(roomID, f'Set notifications\n current: {curStatus}', buttons)
    cache.set(roomID, 'setNotificationMessage', message)
    cache.set(roomID, 'isNotificationEnabled', curStatus)

def callback(update, bot):
    isEnabled, roomID = update.callback_query.data.split()
    isEnabled = isEnabled == 'True'
    roomID = int(roomID)
    
    if isEnabled != cache.get(roomID, 'isNotificationEnabled'):
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        
        cursor = c.execute(f'SELECT isEnabled from rooms where roomID = {roomID}')
        data = cursor.fetchall()
        if len(data) == 0:
            c.execute(f"INSERT INTO rooms \
                VALUES ({roomID}, {isEnabled})")
        else:
            c.execute(f"UPDATE rooms set isEnabled = {isEnabled} where roomID={roomID}")
        conn.commit()
        conn.close()
        cache.set(roomID, 'isNotificationEnabled', isEnabled)
    if cache.get(roomID, 'setNotificationMessage') != None:
        Message.Delete(roomID, cache.get(roomID, 'setNotificationMessage').message_id)
    
    buttons = [
        [InlineKeyboardButton('True', callback_data=f"True {roomID}"), InlineKeyboardButton('False', callback_data=f"False {roomID}")]
    ]

    message= Message.Send.Button(roomID, f'Set notifications\n current: {isEnabled}', buttons)
    cache.set(roomID, 'setNotificationMessage', message)
    cache.set(roomID, 'isNotificationEnabled', isEnabled)

def addNotification(update, bot):
    if int(getenv('DEVELOP')) != getRoomID(update): return
    roomID = getRoomID(update)
    Message.Reply.Text(update, 'Enter text or /empty')
    cache.set(roomID, 'status', 'text')
        
    return

def empty(update, bot):
    if int(getenv('DEVELOP')) != getRoomID(update): return
    when_gettext(update, bot)
        
def instant(update, bot):
    if int(getenv('DEVELOP')) != getRoomID(update): return
    when_gettext(update, bot)
        
def when_gettext(update: Update, bot):
    if int(getenv('DEVELOP')) != getRoomID(update): return
    
    msgText = update.message.text

    roomID = getRoomID(update)

    if cache.get(roomID, 'status') == 'text':
        cache.set(roomID, 'status', 'file')
        cache.set(roomID, 'text', msgText)
        Message.Reply.Text(update, 'Send a file or /empty')
    elif cache.get(roomID, 'status') == 'file' and msgText == '/empty':
        cache.set(roomID, 'status', 'time')
        cache.set(roomID, 'file', msgText)
        Message.Reply.Text(update, 'Set the time ( /instant support only)')
    
    elif cache.get(roomID, 'status') == 'time':
        cache.set(roomID, 'status', None)
        cache.set(roomID, 'time', msgText)
        Message.Reply.Text(update, 'Done.')
        saveNotification(cache.get(roomID, 'text'), cache.get(roomID, 'file'), cache.get(roomID, 'time'))

def saveNotification(text: str, file: str, startTime: str):
    if text == '/empty':
        text = ''
    if file == '/empty':
        file = ''
    if startTime == '/instant':
        startTime = time.time()

    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute(f"INSERT INTO Notification (text,file,time) \
      VALUES ('{text}', '{file}', {startTime} )")
    conn.commit()
    conn.close()

    pass

def when_getdocument(update: Update, bot):
    if int(getenv('DEVELOP')) != getRoomID(update): return
    roomID = getRoomID(update)

    if cache.get(roomID, 'status') == 'file':
        cache.set(roomID, 'status', 'time')
        Message.Reply.Text(update, 'Uploading...')
        cache.set(roomID, 'file', uploadAndGetPhoto(update.message.document.file_id))
        Message.Reply.Text(update, 'Set the time() or /instant')
    
    return

