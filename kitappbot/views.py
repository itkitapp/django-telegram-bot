
from django.http import JsonResponse
from django.conf import settings
from kitappbot.models import TelegramReceivedMessage, TelegramCallbackQuery
import importlib
import json

def webHook(request):
    print(request.body.decode("utf-8"))
    try:
        j = json.loads(request.body.decode("utf-8"))
    except:
        return JsonResponse({'success':False,'message':'request body is not json format'})
    if 'message' in j and 'text' in j['message']:
        trm = TelegramReceivedMessage(
            json = request.body.decode("utf-8")
        )
        trm.save()
        trm.text = j['message']['text']
        trm.sender = j['message']['from']['id']
        if 'is_bot' in j['message']['from']:
            trm.is_bot = j['message']['from']['is_bot']
        if 'first_name' in j['message']['from']:
            trm.first_name = j['message']['from']['first_name']
        if 'last_name' in j['message']['from']:
            trm.last_name = j['message']['from']['last_name']
        if 'username' in j['message']['from']:
            trm.username = j['message']['from']['username']
        trm.save()
        function_string = settings.KITAPPBOT_TELEGRAM_RECEIVINGMETHOD
        mod_name, func_name = function_string.rsplit('.',1)
        mod = importlib.import_module(mod_name)
        func = getattr(mod, func_name)
        func(trm)
        return JsonResponse({'success':True})
    elif 'callback_query' in j:
        callback = TelegramCallbackQuery(
            json = request.body.decode("utf-8")
        )
        callback.save()
        callback.data = j['callback_query']['data']
        callback.sender = j['callback_query']['from']['id']
        if 'is_bot' in j['callback_query']['from']:
            callback.is_bot = j['callback_query']['from']['is_bot']
        if 'first_name' in j['callback_query']['from']:
            callback.first_name = j['callback_query']['from']['first_name']
        if 'last_name' in j['callback_query']['from']:
            callback.last_name = j['callback_query']['from']['last_name']
        if 'username' in j['callback_query']['from']:
            callback.username = j['callback_query']['from']['username']
        callback.save()
        function_string = settings.KITAPPBOT_TELEGRAM_CALLBACKMETHOD
        mod_name, func_name = function_string.rsplit('.',1)
        mod = importlib.import_module(mod_name)
        func = getattr(mod, func_name)
        func(callback)
        return JsonResponse({'success':True})
    return JsonResponse({'success':True})
