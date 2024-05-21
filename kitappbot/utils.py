
from django.conf import settings
from kitappbot.models import TelegramSendedMessage, TelegramGroup
import requests
import json

def createToGroupMessage(to:TelegramGroup, message, connectionId, messageType):
    tsm = TelegramSendedMessage(text = message, receiver = to.chatId, connectionId = connectionId, messageType = messageType, status = 1)
    tsm.save()
    return tsm

def createMessage(to, message, connectionId, messageType):
    tsm = TelegramSendedMessage(text = message, receiver = to, connectionId = connectionId, messageType = messageType, status = 1)
    tsm.save()
    return tsm

def sendAllNewMessages():
    tsms = TelegramSendedMessage.objects.filter(status = 1)
    for tsm in tsms:
        sendMessage(tsm)

def customMethod(method:str, data:dict, telegram_key:str = None):
    if telegram_key is None:
        telegram_key = settings.KITAPPBOT_TELEGRAM_KEY
    telegram_url = f"https://api.telegram.org/bot{telegram_key}/{method}"
    r = requests.post(telegram_url, data=data)
    j = json.loads(r.text)
    return j

def sendPhoto(receiver: str, caption: str, photoFile: str, reply_markup={}, telegram_key:str = None):
    if telegram_key is None:
        telegram_key = settings.KITAPPBOT_TELEGRAM_KEY
    telegram_url = f"https://api.telegram.org/bot{telegram_key}/sendPhoto"
    data = {
        "chat_id": receiver,
        "caption": caption,
        "photo": photoFile,
        "reply_markup": json.dumps(reply_markup),
    }
    r = requests.post(telegram_url, data=data)
    j = json.loads(r.text)
    return j

def sendMessage(tsm: TelegramSendedMessage, reply_markup = {}, telegram_key:str = None):
    if telegram_key is None:
        telegram_key = settings.KITAPPBOT_TELEGRAM_KEY
    telegram_url = f"https://api.telegram.org/bot{telegram_key}/sendMessage"
    data = {
        "chat_id": tsm.receiver,
        "text": tsm.text,
        "reply_markup": json.dumps(reply_markup),
    }
    tsm.status = 2
    tsm.save()
    r = requests.post(telegram_url, data=data)
    tsm.telegramResponse = r.text
    j = json.loads(tsm.telegramResponse)
    if 'ok' in j and j['ok']:
        tsm.status = 3
    else:
        tsm.status = 5
    tsm.save()
    return tsm

def createAndSendMessageWithConnectionId(to, message, connectionId, messageType):
    tsm = TelegramSendedMessage(text = message, receiver = to, connectionId = connectionId, messageType = messageType, status = 1)
    tsm.save()
    sendMessage(tsm)

def createAndSendMessage(to, message):
    return createAndSendMessageWithConnectionId(to, message, '', '')


