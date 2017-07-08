import requests
import json

token = ''

def getToken() :
    with open('token','rt',encoding='utf-8') as f:
        global token
        token = f.read()
        #print(token)

def getUpdates(offset) :
    url = 'https://api.telegram.org/bot%s/getUpdates' % token
    param = {
        'offset' : offset
    }
    r = requests.post(url,param)
    return r.text

if __name__ == '__main__' :
    getToken()

    #updater = Updater(token=token)
    #dispatcher = updater.dispatcher

    #updatesStr = getUpdates(351162951)
    #updates = json.loads(updatesStr)

    #print(updates)