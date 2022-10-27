
from app import *
from cgitb import text
from re import L
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *
import requests
from bs4 import BeautifulSoup

def scr_cov19_web():
    target_url = 'https://covid-19.nchc.org.tw'
    rs = requests.session()
    res = rs.get(target_url, verify=False)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')
    update=soup.find('p', class_='btn-xl-font').find_all('span')

    # 更新日期
    d = update[2].text.strip() + "-" * 5
    count=soup.find_all('div', class_='col-lg-3 col-sm-6 col-6 text-center my-5')

    today_add = count[1].h1.text + "(" + count[1].p.span.text + ")"  # 新增確診
    today_dead = count[2].p.span.text  # 新增死亡
    all_count = count[0].h1.text  # 累積確診數
    all_dead = count[2].h1.text  # 累積死亡

    send = '\nCOVID-19 台灣即時資訊-\n'+d+'\n\n今日新增確診：'+today_add+'\n今日新增死亡：'+today_dead\
        +'\n累積確診人數：'+all_count+'\n累積死亡人數：'+all_dead+'\n\n資料來源：全球疫情地圖'
    
    message = TextSendMessage(text=send)
    line_bot_api.broadcast(message)

scr_cov19_web()
