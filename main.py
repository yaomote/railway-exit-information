from flask import Flask, request, abort
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (FollowEvent, MessageEvent, TextMessage, TextSendMessage,)
import os

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
    print("test1********")
    print(signature)

    # get request body as text
    body = request.get_data(as_text=True)
    print("test6********")
    print(request)
    print("test7********")
    print(body)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
        print("test2********")
    except InvalidSignatureError:
        abort(400)
        print("test3********")

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
    if event.message.text == "渋谷駅"
        print("**********成功***********")
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="成功"))
    else:
        print("**********失敗***********")
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="失敗"))


if __name__ == "__main__":
#    app.run()
    print("test5********")
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
