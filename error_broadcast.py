
from main import *
from cgitb import text
from re import L
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *

# 大聲公
def error_broadcast():
    send = '公告！由於全球疫情地圖網站更新維護中，小助手功能暫時無法使用，若造成不便請見諒～小助手敬上😥'
    message = TextSendMessage(text=send)
    line_bot_api.broadcast(message)

error_broadcast()