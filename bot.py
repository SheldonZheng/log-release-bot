import requests

token = ''

def getUpdates() :
    url = 'https://api.telegram.org/bot%s/getUpdates' % token
    r = requests.get(url)
    return r.text

if __name__ == '__main__' :
    updates = getUpdates()
    print(updates)