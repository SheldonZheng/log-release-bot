from flask import Flask
from flask import render_template, request
import telegram
import logging
from OpenSSL import SSL

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

app = Flask(__name__)

token = ''

bot = telegram.Bot(token='')

bot_name = '@'


@app.route('/<token>',methods=['POST'])
def showInfo(token) :
    print(1)
    if request.method == 'POST':
        update = telegram.Update.de_json(request.get_json(force=True), bot)
        print(update.message.text)
        handle(update.message)
        logging.info("Revice request")
        return "ok"

def handle(message) :
    if None == message :
        return
    text = message.text
    print(type(text))
    if '/echo' in text :
        echo(message)

def echo(meesage) :
    cmd,text = parse_cmd_text(meesage.text)
    if None == text or len(text) == 0 :
        pass
    else :
        chat_id = meesage.chat_id
        bot.sendMessage(chat_id=chat_id,text=text)

def parse_cmd_text(text):
    # Telegram understands UTF-8, so encode text for unicode compatibility
    #text = text.encode('utf-8')
    cmd = None
    if '/' in text:
        try:
            index = text.index(' ')
        except ValueError as e:
            return (text, None)
        cmd = text[:index]
        text = text[index + 1:]
    if cmd != None and '@' in cmd:
        cmd = cmd.replace(bot_name, '')
    return (cmd, text)

if __name__ == '__main__' :
    #context = SSL.Context(SSL.SSLv23_METHOD)
    #context.use_privatekey_file('/etc/letsencrypt/live/evilby.com/privkey.pem')
    #context.use_certificate_file('/etc/letsencrypt/live/evilby.com/fullchain.pem')
    context = None
    app.run(host="0.0.0.0",port='443',ssl_context=context)

