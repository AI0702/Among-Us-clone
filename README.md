# Among_Us_clone
An unofficial clone of the popular multiplayer game 'Among Us', developed in Python using various supported libraries, as a final year project. Assets ripped from the from the game. Support for upto 5 (or more?) players via LAN.

## Requirements
* python 3.X 
* pygame 
* pytmx
* pickle
* select
* socket
* asyncore
* threading
* pyaudio (optional, for voice chat)

## How to run

####Singleplayer
* To start the game `python main.py`
* Choose 'Freeplay' from the menu to start playing

####Local Multiplayer
* To start the game server for multiplayer support `python server.py`
* To start the game client `python main.py`
* Choose 'Local' from the menu to start playing
* Enter IP Address of the server (displayed in the server console). If the server is running on the same machine as the game, use the address `127.0.0.1`.
* Upto 5 (or more?) game clients can cannect to the server by entering the server address, if they are connected to the same network. Though, the server might crash if too many players are connected.

####Voice Chat Support (experimental)
* To start the voice chat server `python server_voice.py`
* To start the voice chat client `python voice.py`
* Enter IP Address and Port of the voice chat server (displayed in the server console).



