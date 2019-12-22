from flask import Flask, request, abort
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (MessageEvent, TextMessage, TextSendMessage,)
import os

app = Flask(__name__)

#環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

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


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print("test4********")
    print(event.reply_token)
    print("test8********")
    print(event.message.text)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
#    app.run()
    print("test5********")
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
