# Democirify 

## About

Democrify is a web application that gives Spotify premium users the ability to host public channels.

Anyone with a device and internet connection can connect to these channels via the browser and queue a song.


## Setup/Requirements

Democrify was created usng Python Version 3.6

Democrify requires the following Python modules to run and can be installed with the following from the command line/terminal:

python -m pip install Flask  
python -m pip install qrcode  
python -m pip install Spotipy 

Democrify is required to be spotify authorised by supplying credentials to the spotifyAuth.txt file.
They can be retrieved by registering the application at https://beta.developer.spotify.com/

Once the application has been registered and all the dependant libraries are installed, it can simply be run by launching main.py

The service can be accessed via  localhost:5000 or via the local ip address on port 5000.

