#!/usr/bin/env python3
# coding=utf-8
import threading
from telegram.ext import CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from Command import *
from dotenv import load_dotenv
from updater import updater

load_dotenv()

# Main function
def main():
    
	# Commands
	updater.dispatcher.add_handler(CommandHandler('start', Start_Bot))
	updater.dispatcher.add_handler(CommandHandler('help', Start_Bot))
	updater.dispatcher.add_handler(CommandHandler('set', setNotification))
	updater.dispatcher.add_handler(CommandHandler('add', addNotification))
	updater.dispatcher.add_handler(CommandHandler('empty', empty))
	
	updater.dispatcher.add_handler(MessageHandler(Filters.text, when_gettext))
	updater.dispatcher.add_handler(MessageHandler(Filters.document, when_getdocument))

	updater.dispatcher.add_handler(CallbackQueryHandler(callback))


	SendNotification = threading.Thread(target = sendNotification)
	SendNotification.start()
	
	# Bot Start
	print("Bot Server Running...")

	updater.start_polling()
	updater.idle()


# Head of program
if __name__ == '__main__':
    main()
