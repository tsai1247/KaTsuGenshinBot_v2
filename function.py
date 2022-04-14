import time
from typing import Any, List
from telegram import ForceReply, InlineKeyboardButton, InlineKeyboardMarkup, Update
from updater import updater

def getUserID(update: Update): 
    if update.message == None: return None
    return update.message.from_user.id

def getRoomID(update: Update): 
    if update.message == None: return None
    return update.message.chat_id

class Message:
    def Delete(roomID: int, message_id: int):
        return updater.bot.delete_message(roomID, message_id)

    class Reply:
        def Text(update: Update, message: str, forceReply: bool = False):
            return update.message.reply_text(message, reply_markup = ForceReply(selective=forceReply))

        def Photo(update: Update, photoLink: str, forceReply: bool = False, title: str = ''):
            return update.message.reply_photo(photoLink, caption=title, reply_markup = ForceReply(selective=forceReply))

    class Send:
        def Text(roomID: int, message: str, forceReply: bool = False):
            return updater.bot.send_message(roomID, message, reply_markup = ForceReply(selective=forceReply))

        def Photo(roomID: int, photoLink: str, forceReply: bool = False, title: str = ''):
            return updater.bot.send_photo(roomID, photoLink, caption=title, reply_markup = ForceReply(selective=forceReply))

        def Button(roomID: int, message: str, buttons: List[List[InlineKeyboardButton]]):
            return updater.bot.send_message(roomID, message, reply_markup = InlineKeyboardMarkup(buttons))

class Cache:
    def __init__(self) -> None:
        self.cache = {}

    def initCache(self, roomID: int) -> None:
        if roomID not in self.cache.keys():
            self.cache[roomID] = {'CreateTime': time.time(), 'LastUpdateTime': time.time()}
        return None

    def set(self, roomID: int, key: str, value: Any) -> bool:
        try:
            self.initCache(roomID)
            self.cache[roomID][key] = value
            self.cache[roomID]['LastUpdateTime'] = time.time()
            return True
        except:
            return False

    def get(self, roomID: int, key: str) -> Any:
        try:
            return self.cache[roomID][key]
        except :
            return None