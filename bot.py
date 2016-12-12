from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from datetime import datetime
from functools import reduce
import logging

competitors = {}
scores = {}
arrivals = {}
arrivalsYesterday = {}
lastDate = datetime.now()

# Telegram bot token: 301838740:AAEBm36YW8ebArED6GScm4Hj1SRwtqwzDDM

updater = Updater(token='301838740:AAEBm36YW8ebArED6GScm4Hj1SRwtqwzDDM')
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def unknown(bot, update):
    global commands
    message = "Sorry, I didn't understand that command. Available commands are:\n"
    for command in commands:
        message += "/"+command+"\n"
    bot.sendMessage(chat_id=update.message.chat_id, text=message)

def repo(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="My source code is located at https://github.com/SidneyBovet/WakeUpBot")

def test(bot, update):
    chat_id = update.message.chat_id
    message_id = update.message.message_id
    from_user = update.message.from_user
    date = update.message.date
    bot.sendMessage(chat_id=chat_id, text="chat_id="+str(chat_id)+" message_id="+str(message_id)+" from_user="+str(from_user)+" date="+str(date))

def checkNewDay(date):
    global arrivals, arrivalsYesterday

    if date.date() > lastDate.date():
        bestPlayerID = findBestPlayerID()
        scores[bestPlayerID] =+ 1
        arrivalsYesterday = arrivals.deepcopy()
        arrivals = None;

def arrived(bot, update):
    global competitors, arrivals, arrivalsYesterday, lastDate
    user_id = update.message.from_user['id']
    date = update.message.date

    checkNewDay(date)

    if not user_id in competitors:
        registerNewUser(bot, update)

    if user_id in arrivalsYesterday:
        if arrivalsYesterday[user_id] < date:
            bot.sendMessage(chat_id=update.message.chat_id, text="You did better than yesterday, gg!")

    if not user_id in arrivals:
        lastDate = date
        arrivals[user_id] = date
    else:
        bot.sendMessage(chat_id=update.message.chat_id, text="You already participated today.")

def registerNewUser(bot, update):
    user_id = update.message.from_user['id']
    competitors[user_id] = update.message.from_user['first_name']
    scores[user_id] = 0
    bot.sendMessage(chat_id=update.message.chat_id, text="Welcome in the competition, " + str(update.message.from_user['first_name']))

def bestPlayer(bot, update):
    date = update.message.date
    checkNewDay(date)

    if arrivals == None or not arrivals: # if None or empty
        bot.sendMessage(chat_id=update.message.chat_id, text="No one yet arrived at work today.")
    else:
        bestKey = findBestPlayerID()
        bot.sendMessage(chat_id=update.message.chat_id, text="Today's best is " + str(competitors[bestKey]))

def findBestPlayerID():
    global arrivals
    return reduce(lambda bestKey,key: key if arrivals[key] < arrivals[bestKey] else bestKey, arrivals)

def displayScores(bot, update):
    global scores, competitors
    message = "Scores: (last updated yesterday)\n"
    for playerID in competitors:
        message += "- " + competitors[playerID] + ": " + str(scores[playerID])
    bot.sendMessage(chat_id=update.message.chat_id, text=message)

# Add all commands to the dispatcher
commands = {'start':registerNewUser, 'test':test, 'git':repo, 'arrived':arrived, 'best':bestPlayer, 'scoreboard':displayScores}
for command in commands:
    dispatcher.add_handler(CommandHandler(command, commands[command]))
unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)

updater.start_polling()
