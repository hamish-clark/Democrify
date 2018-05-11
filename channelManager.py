
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
