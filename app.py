
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *

from SiteSet import token, secret
from flask import Flask, request, abort
from message import *
import tempfile
import os
import datetime
import time

app = Flask(__name__)
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')

line_bot_api = token
handler = secret

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    if '確診訊息' in msg:
        try:
            message = scr_cov19_web()
            line_bot_api.reply_message(event.reply_token, message)
        except Exception:
            message = TextSendMessage(text='系統更新中，造成不便請見諒！')
            line_bot_api.reply_message(event.reply_token, message)
    else:
        message = TextSendMessage(text="感謝您傳訊息給我！但很抱歉我無法回覆您")
        line_bot_api.reply_message(event.reply_token, message)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
