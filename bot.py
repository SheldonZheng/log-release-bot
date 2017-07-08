import requests

token = ''

def getToken() :
    with open('token','rt',encoding='utf-8') as f:
        global token
        token = f.read()
        #print(token)

def getUpdates() :
    url = 'https://api.telegram.org/bot%s/getUpdates' % token
    r = requests.get(url)
    return r.text

if __name__ == '__main__' :
    getToken()
    updates = getUpdates()
    print(updates)