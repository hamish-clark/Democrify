from flask import Flask
from flask import render_template
from flask import redirect
from flask import url_for
from flask import request
from flask import session

import channelManager
import spotifyManager
import qrGenerator
import random

import socket

authorisationObjects = {}

app = Flask(__name__)

@app.route('/')
def index():
    url_for('static', filename='layout.css')
    url_for('static', filename='searchIcon.png')
    return render_template("index.html")

@app.route('/login')
def login():
    loginUrl, autho = spotifyManager.createLoginUrl()
    authoKey = ''.join([str(random.randint(0,9)) for _ in range(10)])
    
    session["authoKey"] = authoKey
    authorisationObjects[authoKey] = autho
    
    return redirect(loginUrl )

@app.route('/processLogin.html/')
def processLogin():
    verifyUrl = "http://localhost:5000/processLogin.html/?code=" + request.args.get("code")
    token = spotifyManager.get_token(authorisationObjects[session["authoKey"]], verifyUrl)
    if token: #Sucessful Login
        service = spotifyManager.get_spotify_service(token)
        channelNumber = channelManager.createChannel(service)
        hostIp = socket.gethostbyname(socket.gethostname())
        print(hostIp)
        qrGenerator.generate(channelNumber, "http://" + hostIp + ":5000/channel/" + str(channelNumber))
        return redirect('/channel/' + str(channelNumber))
    else: # Unsucsesful Login
        return render_templace("loginFailed.html")


@app.route('/createChannel')
def createChannel():
    return redirect('/login')


@app.route('/channel/<int:channelNumber>')
def channel(channelNumber):
    url_for('static', filename='layout.css')
    url_for('static', filename='qrCodes')

    channel = channelManager.getChannel(channelNumber)
    if channel:
        return render_template('channel.html', channel=channel)
    else:
        return render_template('pergitory.html',)


@app.route('/channel/<int:channelNumber>/requestSong/<string:id>')
def requestSong(channelNumber, id):
    channel = channelManager.getChannel(channelNumber)
    service = channel.service
    if service != None:
        results = service.search(id, type = "track")["tracks"]["items"]
        channel.queueSong(results[0])
        return redirect("/channel/" + str(channel.channelNumber))
    else:
        return redirect("/")



if __name__ == "__main__":
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    app.run("0.0.0.0", debug = True)
