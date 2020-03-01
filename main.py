from flask import Flask
from flask import render_template
from flask import redirect
from flask import url_for
from flask import request
from flask import session
<<<<<<< HEAD
from flask import jsonify
=======
>>>>>>> d879de03cfa1f199f3015592751264f91f1daaae

import channelManager
import spotifyManager
import qrGenerator
import random
<<<<<<< HEAD
import os
=======
>>>>>>> d879de03cfa1f199f3015592751264f91f1daaae

import socket

authorisationObjects = {}

app = Flask(__name__)
<<<<<<< HEAD
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

PROJECT_DIR = '/home/mishmouse224/democrify'
=======
>>>>>>> d879de03cfa1f199f3015592751264f91f1daaae

@app.route('/')
def index():
    url_for('static', filename='layout.css')
    url_for('static', filename='searchIcon.png')
<<<<<<< HEAD
    return render_template("index.html", channels = channelManager.getChannels())
=======
    return render_template("index.html")
>>>>>>> d879de03cfa1f199f3015592751264f91f1daaae

@app.route('/login')
def login():
    loginUrl, autho = spotifyManager.createLoginUrl()
    authoKey = ''.join([str(random.randint(0,9)) for _ in range(10)])
<<<<<<< HEAD

    session["authoKey"] = authoKey
    authorisationObjects[authoKey] = autho

    return redirect(loginUrl)

@app.route('/processLogin/')
def processLogin():
    verifyUrl = spotifyManager.get_redirect_uri() + "?code=" + request.args.get("code")

    print("VERIFY URL:", verifyUrl)

    autho = authorisationObjects[session["authoKey"]]

    token = spotifyManager.get_token(autho, verifyUrl)

    if token: #Sucessful Login
        service = spotifyManager.get_spotify_service(token)
        userId = service.current_user()['id']
        channel = channelManager.getChannelByHostId(userId)
        if channel == None:
            channelNumber = channelManager.createChannel(service)
            hostIp = socket.gethostbyname(socket.gethostname())
            print(hostIp)
            qrGenerator.generate(channelNumber, "http://" + hostIp + ":5000/channel/" + str(channelNumber))
            return redirect('/channel/' + str(channelNumber))
        else: #User already has channel
            return redirect('/channel/' + str(channel.channelNumber))

    else: # Unsucsesful Login
        return render_templace("loginFailed.html")

=======
    
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


>>>>>>> d879de03cfa1f199f3015592751264f91f1daaae
@app.route('/createChannel')
def createChannel():
    return redirect('/login')

<<<<<<< HEAD
=======

>>>>>>> d879de03cfa1f199f3015592751264f91f1daaae
@app.route('/channel/<int:channelNumber>')
def channel(channelNumber):
    url_for('static', filename='layout.css')
    url_for('static', filename='qrCodes')

    channel = channelManager.getChannel(channelNumber)
    if channel:
        return render_template('channel.html', channel=channel)
    else:
        return render_template('pergitory.html',)

<<<<<<< HEAD
#/channel/801/requestSong/
@app.route('/channel/<int:channelNumber>/requestSong/<string:songName>')
def requestSong(channelNumber, songName):
    channel = channelManager.getChannel(channelNumber)
    result = channel.queueSong(songName)
    return redirect("/channel/" + str(channelNumber))


@app.route('/channel/<int:channelNumber>/playSong/<string:song_uri>')
def playSong(channelNumber, song_uri):
    channel = channelManager.getChannel(channelNumber)
    result = channel.play_song(song_uri)
    return redirect("/channel/" + str(channelNumber))

#/channel/801/requestSong/
@app.route('/channel/<int:channelNumber>/current_song')
def current_song(channelNumber):
    channel = channelManager.getChannel(channelNumber)
    return jsonify(channel.get_current_song())

#/channel/801/requestSong/
@app.route('/channel/<int:channelNumber>/transfer_device/<string:device_id>')
def transfer_device(channelNumber, device_id):
    channel = channelManager.getChannel(channelNumber)
    channel.transfer_device(device_id)
    return redirect("/channel/" + str(channelNumber))

#/channel/801/skip/
@app.route('/channel/<int:channelNumber>/skip')
def skip(channelNumber):
    channel = channelManager.getChannel(channelNumber)
    channel.skip_song()
    return redirect("/channel/" + str(channelNumber))


if __name__ == "__main__":
    app.run("0.0.0.0", debug = False)
=======

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
>>>>>>> d879de03cfa1f199f3015592751264f91f1daaae
