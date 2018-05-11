
import sqlite3
import random

connection = sqlite3.connect("queueDatabase.db")

conn = connection.cursor()

class Channel:
    def __init__(self, channelNumber, token, service):
        self.channelNumber = int(channelNumber)
        self.token = token
        self.service = service
        self.songs = []
        self.playing = None
        self.device_id = None

    def requestSong(self, searchString):
        results = self.service.search(searchString, type = "track")["tracks"]["items"]
        song = Song(results[0])
        self.queueSong(song)

    def getDevices(self):
        return self.service.devices()

    def prepareActiveDevice(self):
        device = spotify.get_active_device(self.service)
        if device == None:
            print("Error")
        self.device_id = device["id"]

    def playNextSong(self):
        if len(self.songs) == 0:
            self.playing = None
        else:
            song = self.songs.pop(0)
            self.playing = song
            self.prepareActiveDevice()
            playSong(service, self.device_id, [song.spotifyUri])
            print("Song duration!!: ", song.duration)
            t = Timer(song.duration, self.playNextSong)
            t.start()
            
    def queueSong(self, song):
        if len(self.songs) == 0 and self.playing == None:
            self.songs.append(song)
            self.playNextSong()
        else:
            self.songs.append(song)
            
    def getSize(self):
        return len(self.songs)

    def getSongs(self):
        return self.songs



def createDatabase(conn):   
    conn.execute('''CREATE TABLE channels
                 (channelNumber real, channelHostId real, channelName text)''')
    connection.comit()
    connection.close()

def createChannel():
    newChannelNumber = None
    existingChannelNumbers = getChannelNumbers()
    while newChannelNumber in existingChannelNumbers or newChannelNumber == None:
        newChannelNumber = random.randint(0, 1000)
    
    conn.execute("INSERT INTO channels VALUES ({0}, 224, 'Channel Name')".format(newChannelNumber))
    print("Created Channel #" + str(newChannelNumber))

def getChannelNumbers():
    return [channelData[0] for channelData in conn.execute('SELECT * FROM channels ORDER BY channelNumber')]

def printChannels():
    for row in conn.execute('SELECT * FROM channels ORDER BY channelNumber'):
        print(row)


def loadChannels():
    return {}




createChannel()
createChannel()
createChannel()

printChannels()

print(getChannelNumbers())
