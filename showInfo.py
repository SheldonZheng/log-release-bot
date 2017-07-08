from flask import Flask
from flask import render_template, request
from OpenSSL import SSL

app = Flask(__name__)

@app.route('/<token>',methods=['POST'])
def showInfo(token) :
    print(1)
    if request.method == 'POST':
        json = request.get_json(force=True)
        print(json)
        return "ok"

if __name__ == '__main__' :
    #context = SSL.Context(SSL.SSLv23_METHOD)
    #context.use_privatekey_file('/etc/letsencrypt/live/evilby.com/privkey.pem')
    #context.use_certificate_file('/etc/letsencrypt/live/evilby.com/fullchain.pem')
    context = ('/etc/letsencrypt/live/evilby.com/fullchain.pem','/etc/letsencrypt/live/evilby.com/privkey.pem')
    app.run(host="0.0.0.0",port='443',ssl_context=context)
