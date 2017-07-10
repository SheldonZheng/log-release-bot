from flask import Flask
from flask import render_template, request
import telegram
import logging
from sqlalchemy import Column, String, create_engine,Integer,Boolean,DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from OpenSSL import SSL

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

app = Flask(__name__)

token = ''

bot = telegram.Bot(token='')

bot_name = '@'


Base = declarative_base()

class LogRelease(Base) :
    __tablename__ = 'log_release'

    id = Column(Integer,primary_key=True)
    project_name = Column(String(100),index=True)
    tag_name = Column(String(100),index=True)
    result = Column(String(100))
    operator = Column(String(100))
    status = Column(Boolean)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

engine = create_engine('mysql+mysqlconnector://')

DBSession = sessionmaker(bind=engine)

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
    elif '/new' in text :
        newLogRelease(message)
    elif '/report' in text :
        reportResult(message)
    elif '/queryByOperator' in text :
        queryByOperator(message)

def echo(meesage) :
    cmd,text = parse_cmd_text(meesage.text)
    if None == text or len(text) == 0 :
        pass
    else :
        chat_id = meesage.chat_id
        bot.sendMessage(chat_id=chat_id,text=text)


def newLogRelease(meesage) :
    cmd,text = parse_cmd_text(meesage.text)
    if None == text or len(text) == 0 :
        pass
    else :
        textSplited = text.split('/')

        session = DBSession()

        new_log = LogRelease(project_name = textSplited[0],tag_name=textSplited[1],operator=textSplited[2],result='UNCOMMIT',status = True)
        session.add(new_log)
        session.commit()
        session.close()
        chat_id = meesage.chat_id
        bot.sendMessage(chat_id=chat_id,text='创建新的上线记录成功')

def reportResult(meesage) :
    cmd,text = parse_cmd_text(meesage.text)
    if None == text or len(text) == 0 :
        pass
    else :
        textSplited = text.split('/')
        session = DBSession()
        logrelease = session.query(LogRelease).filter(LogRelease.project_name==textSplited[0],LogRelease.tag_name==textSplited[1]).first();
        if logrelease == None :
            chat_id = meesage.chat_id
            bot.sendMessage(chat_id=chat_id,text='未查询到对应的上线记录')
        logrelease.result = textSplited[2]
        session.add(logrelease)
        session.commit()
        session.close()
        chat_id = meesage.chat_id
        bot.sendMessage(chat_id=chat_id, text='汇报上线记录状态成功')

def queryByOperator(meesage) :
    cmd,text = parse_cmd_text(meesage.text)
    if None == text or len(text) == 0:
        pass
    else:
        session = DBSession()
        logreleases = session.query(LogRelease).filter(LogRelease.operator==text).all()
        result = ''
        for logrelease in logreleases :
            result = result + logrelease.project_name + '/' + logrelease.tag_name + '/' + logrelease.result + '\n'
        chat_id = meesage.chat_id
        bot.sendMessage(chat_id=chat_id, text=result)


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

