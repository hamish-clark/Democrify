<<<<<<< HEAD

import random
from threading import Timer

channels = {}
#loadChanelsFromDatabase(channels)

def getChannelByHostId(id):
    for channel in channels.values():
        if channel.hostId == id:
            return channel

    return None

def getChannels():
    return channels


def loadChannelsFromDatabase(channels):
    """ Requires Implimentation """
    return channels
    
def getChannelNumbers():
    return list(channels.keys())

def getChannel(channelNumber):
    if channelNumber in channels.keys():
        return channels[channelNumber]
    else:
        return None

def createChannel(service):
    channelNumber = None
    while channelNumber in channels.keys() or channelNumber == None:
        channelNumber = random.randint(0, 1000)
    channels[channelNumber] = Channel(channelNumber, service)
    return channelNumber
    
class Channel:
    def __init__(self, channelNumber, service):
        self.channelNumber = channelNumber
        self.service = service
        self.hostId = service.current_user()['id']
        self.songs = []
        self.playing = None
        self.timer = Timer(0, None)

    def skip_song(self):
        self.playNextSong()
        
    def play_song(self, song_uri):
        active_device = self.getActiveDevice()
        if active_device != None:
            self.service.start_playback(active_device, uris=[song_uri])
        else:
            None

    def getDevices(self):
        return self.service.devices()["devices"]

    def getActiveDevice(self):
        devices = self.getDevices()
        for device in devices:
            if device["is_active"] == True:
                return device["id"]

        if len(devices) != 0:
            return devices[0]["id"]
        else:
            return None
    
    def transfer_device(self, device_id):
        self.service.transfer_playback(device_id, force_play=True)

    def get_current_song(self):
        current = self.service.current_playback()
        print(current)
        return current

    def playNextSong(self):
        if len(self.songs) == 0:
            self.playing = None
        else:
            song = self.songs.pop(0)
            self.playing = song 
            self.play_song(song.spotifyUri)

            self.timer.cancel()
            
            self.timer = Timer(song.duration, self.playNextSong)
            self.timer.start()


    def queueSong(self, songName):
        results = self.service.search(songName, type = "track")["tracks"]["items"]
        song = Song(results[0])

        if len(self.songs) == 0 and self.playing == None:
            self.songs.append(song)
            self.playNextSong()
        else:
            self.songs.append(song)

        return True

    def getSize(self):
        return len(self.songs)

    def getSongs(self):
        return self.songs

        
class Song():
    def __init__(self, searchResult):
        self.songName = searchResult["name"]
        self.artistName = searchResult["artists"][0]["name"]
        self.albumName = searchResult["album"]["name"]
        self.duration = searchResult["duration_ms"] / 1000.0
        self.coverImageUrl = searchResult["album"]["images"][1]["url"]
        self.spotifyUri = searchResult["uri"]
=======

import random
from threading import Timer

channels = {}

def playSong(service, device_id, uris):
    service.start_playback(device_id, uris=uris)

def loadChannelsFromDatabase(channels):
    """ Requires Implimentation """
    return channels
    
def getChannelNumbers():
    return list(channels.keys())

def getChannel(channelNumber):
    if channelNumber in channels.keys():
        return channels[channelNumber]
    else:
        return None

def createChannel(service):
    channelNumber = None
    while channelNumber in channels.keys() or channelNumber == None:
        channelNumber = random.randint(0, 1000)
    channels[channelNumber] = Channel(channelNumber, service)
    return channelNumber
    
class Channel:
    def __init__(self, channelNumber, service):
        self.device_id = None
        self.channelNumber = channelNumber
        self.service = service
        self.songs = []
        self.playing = None

    def getActiveDevice(self):
        for device in self.service.devices()["devices"]:
            if device["is_active"] == True:
                return device["id"]
        return None

    def playNextSong(self):
        if len(self.songs) == 0:
            self.playing = None
        else:
            song = self.songs.pop(0)
            self.playing = song
            playSong(self.service, self.getActiveDevice(), [song.spotifyUri])
            print("Song duration!!: ", song.duration)
            t = Timer(song.duration, self.playNextSong)
            t.start()


    def queueSong(self, searchResult):
        if len(self.songs) == 0 and self.playing == None:
            self.songs.append(Song(searchResult))
            self.playNextSong()
        else:
            self.songs.append(Song(searchResult))

    def getSize(self):
        return len(self.songs)

    def getSongs(self):
        return self.songs

        
class Song():
    def __init__(self, searchResult):
        self.songName = searchResult["name"]
        self.artistName = searchResult["artists"][0]["name"]
        self.albumName = searchResult["album"]["name"]
        self.duration = searchResult["duration_ms"] / 1000.0
        self.coverImageUrl = searchResult["album"]["images"][1]["url"]
        self.spotifyUri = searchResult["uri"]
>>>>>>> d879de03cfa1f199f3015592751264f91f1daaae
