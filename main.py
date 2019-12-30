from flask import Flask, request, abort
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (FollowEvent, MessageEvent, TextMessage, TextSendMessage,)
import os

import urllib.request, urllib.error                         # urlアクセス
import requests                                             # urlアクセス
from bs4 import BeautifulSoup                               # web scraping用
from selenium import webdriver                              # 動的ページに対するscraping用
from selenium.webdriver.chrome.options import Options       # webdriverの設定用
import time                                                 # scrapingの時間制御用

app = Flask(__name__)

# 環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]
# 各クライアントライブラリのインスタンス作成
line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)


# 著名検証とhandleに定義されている関数呼び出し
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


# 友達追加時、最初のメッセージ
@handler.add(FollowEvent)
def handle_follow(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='駅の何番出口にどんなお店があるかをお知らせするアプリです\n\n〇使い方\n駅名のみ入力してください\n（例：渋谷駅）\n※「駅」までご入力下さい')
    )


# メッセージ
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # 駅情報格納用
    stationInfo = {}    # {'駅名-路線':'ページurl'}

    # 入力テキストチェック
    result = list(event.message.text)
    # 入力値OKの場合
    if result[-1] == '駅' and result.count('駅') == 1:
        driver.get(f"https://transit.goo.ne.jp/station/train/confirm.php?st_name={event.message.text}&input=検索")        # 駅名検索ページアクセス
        html = driver.page_source.encode('utf-8')       # HTMLを文字コードをUTF-8に変換してから取得します。
        soup = BeautifulSoup(html, "html.parser")       # htmlをBeautifulSoupで扱う

        # 駅名-路線名と駅ページのurlをリストstationInfoへ格納
        stationName_tag = soup.select('ul.stationname > li > a')
        for sn_tag in stationName_tag:
            stationName = sn_tag.string
            stationInfo[stationName] = sn_tag.get('href')

        # 出口案内情報を取得
        for stationName in stationInfo:
            # 変数初期化
            text = ""
            reUrl = ""
            reUrlCnt = 0
            feedpageFlag = False
            feedpageNum = 0
            feedCnt = 0

            # urlの作り直し
            exitUrl = stationInfo[stationName].split('/')
            for exitUrlOne in exitUrl:
                if reUrlCnt == 4:
                    reUrlCnt += 1
                    continue
                else:
                    reUrlCnt += 1
                    reUrl = reUrl + exitUrlOne + '/'
            driver.get(f"https://transit.goo.ne.jp{reUrl}exit.html")        # 出口案内ページアクセス
            html = driver.page_source.encode('utf-8')       # HTMLを文字コードをUTF-8に変換してから取得します。
            soup = BeautifulSoup(html, "html.parser")       # htmlをBeautifulSoupで扱う

            # 複数ページにまたがるかどうか本処理前にチェック
            feedpage = soup.find(class_='feedpage')
            if feedpage == None:
                feedpageFlag = False
            else:
                feedpage = feedpage.find_all('a')
                feedpageNum = len(feedpage) - 2     #feedpageの数（1ページ目と次への項目を除く）
                feedpageFlag = True

            # 1ページ目は必ず実行 複数ページにまたがる場合は繰り返し
            while True:
                # 変数初期化
                exitCnt = 0

                # 出口と施設をリストexitInfoへ格納
                exit_tag = soup.find_all(id='facility')
                facility_tag = soup.find_all(class_='exit')
                for et in exit_tag:
                    exitName = et.string
                    facility_total = facility_tag[exitCnt].find_all('li')
                    text = text + exitName + '\n----\n'
                    for facility_one in facility_total:
                        facility = facility_one.string
                        text = text + facility + '\n'
                    text = text + '----\n'
                    exitCnt += 1
                if feedpageFlag == False:
                    break
                else:
                    if feedCnt >= feedpageNum:
                        break
                    else:
                        driver.get(f"https://transit.goo.ne.jp{reUrl}{2+feedCnt}/exit.html")        # 出口案内ページアクセス
                        html = driver.page_source.encode('utf-8')       # HTMLを文字コードをUTF-8に変換してから取得します。
                        soup = BeautifulSoup(html, "html.parser")       # htmlをBeautifulSoupで扱う
                        feedCnt += 1
            break

        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=text))

    # 入力値NGの場合
    else:
        line_bot_api.reply_message(event.reply_token,
            TextSendMessage(text="駅名を確認してください（名前の最後に「駅」がついているか等）\n例:渋谷駅")
        )

if __name__ == "__main__":
    # スクレイピング準備
    options = Options()             # ブラウザオプション格納
    options.set_headless(True)      # Headlessモードを有効にする（コメントアウトするとブラウザが実際に立ち上がる）
    driver = webdriver.Chrome(chrome_options=options, executable_path='/app/.chromedriver/bin/chromedriver')        # ブラウザを起動

    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
