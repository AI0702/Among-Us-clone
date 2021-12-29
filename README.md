# Among Us (clone)
An unofficial clone of the popular multiplayer game 'Among Us', recreated in Python using various supported libraries. Support for upto 5 (or more?) players via LAN. Assets ripped from the from the game.

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

#### Singleplayer
* To start the game `python main.py`
* Choose 'Freeplay' from the menu to start playing

#### Local Multiplayer
* To start the game server for multiplayer support `python server.py`
* To start the game client `python main.py`
* Choose 'Local' from the menu
* Enter IP Address of the server (displayed in the server console). If the server is running on the same machine as the game, use the address `127.0.0.1`.
* Upto 5 (or more?) game clients can cannect to the server by entering the server address, if they are connected to the same network. Though, the server might crash if too many players are connected.

#### Voice Chat Support (experimental)
* To start the voice chat server `python server_voice.py`
* To start the voice chat client `python voice.py`
* Enter IP Address and Port of the voice chat server (displayed in the server console). 

### Controls

#### Menu
* `Up` `Down` `Left` `Right` `W` `S` `A` `D` Navigate Menu
* `Enter` Select
* `Esc` Back

#### Game
* `Up` `Down` `Left` `Right` `W` `S` `A` `D` Move
* `Space` Interact, Perform Actions, Vent
* `Left Click` View Tasks, Complete Tasks, Vote. 
  * Click on the 'Tasks' button on the top-left to view the list of tasks. 
  * When a task window is displayed, click on appropriate hotspots to complete the task. 
  * During voting, click on the checkbox next to a player to vote.
* `Tab` View Map
* `Alt` Change Vent. 
  * Stand next to a vent and interact with it to move inside. Once inside, move from vent to vent using the `Alt` button. 
* `Enter` Kill
* `Ctrl` Sabotage Lights
  * To fix the lights, go the the Electrical room, stand close to the glowing-elctric-symbol circuit-box on the north wall of the room, and press `Ctrl`
* `Shift` Sabotage Reactor
  * To fix the reactor, go the the Reactor room, stand close to the glowing-hand-symbol hand-scanner on the north wall of the room, and press `Shift`

## Screenshots

![ui_1_menu](https://user-images.githubusercontent.com/69671663/147409060-7f0d63b1-3f32-4c25-bbf1-433c613f820b.png)

![ui_2_colour](https://user-images.githubusercontent.com/69671663/147409062-a5858620-f5a1-4141-bd2f-4ef0bfd7ca3e.png)

![ui_3_help](https://user-images.githubusercontent.com/69671663/147409063-c97fe81c-c8ec-456e-b598-63321b00c2b6.png)

![ui_9_name](https://user-images.githubusercontent.com/69671663/147409064-90f23e65-a9cd-47aa-8d05-1a1a7fe7bd31.png)

![ui_10_ip](https://user-images.githubusercontent.com/69671663/147409066-eb2f1487-d109-4fbe-a703-b269ada864ba.png)

![ui_11_game](https://user-images.githubusercontent.com/69671663/147409067-52eab964-79db-453c-88d8-d8cb55c40306.png)

![ui_13_tasks](https://user-images.githubusercontent.com/69671663/147409069-507db846-f623-451b-bb34-0165fc4c8b63.png)

![ui_14_tasks](https://user-images.githubusercontent.com/69671663/147409073-f1c74836-9e87-4abc-a0cb-a02a1e451eed.png)

![ui_15_tasks](https://user-images.githubusercontent.com/69671663/147409078-d338251c-0a6e-4187-9757-331f5435d9e5.png)

![ui_16_tasks](https://user-images.githubusercontent.com/69671663/147409083-b4ed9d5a-07f0-4f97-900a-98337391bd28.png)

![ui_17_tasks](https://user-images.githubusercontent.com/69671663/147409084-2fc34ff2-2d02-4a80-aeef-fabdea828ce4.png)

![ui_18_taks](https://user-images.githubusercontent.com/69671663/147409086-8e0bb48e-a4d3-4756-88d3-05e95fe443ab.png)

![ui_19_taks](https://user-images.githubusercontent.com/69671663/147409087-f4d685f4-83e0-4c69-b26b-4696a69390d3.png)

![ui_20_task](https://user-images.githubusercontent.com/69671663/147409088-e6dbed19-5d80-4f8c-8327-2e7c3d21cad2.png)

![ui_21_bots](https://user-images.githubusercontent.com/69671663/147409091-82231587-803b-498a-ba04-97984b867ad4.png)

![ui_22_map](https://user-images.githubusercontent.com/69671663/147409095-f29d80c9-f2d1-420c-a8eb-d261691096e8.png)

![ui_23_sabotage](https://user-images.githubusercontent.com/69671663/147409097-0c3416c7-0773-4c75-bdc4-afbcf52827c4.png)

![ui_24_sabotage](https://user-images.githubusercontent.com/69671663/147409100-bf6266cc-2d39-42a9-8f4f-400ca2000071.png)

![ui_25_kill](https://user-images.githubusercontent.com/69671663/147409102-336f8dd1-c0b0-4f16-9ac0-4cb4dfb2a7f7.png)

![ui_26_emergency](https://user-images.githubusercontent.com/69671663/147409104-6560334d-7baf-4948-8458-800992b71c78.png)

![ui_27_report](https://user-images.githubusercontent.com/69671663/147409107-22a499ec-1ece-4925-b52c-1ff548e491f3.png)

![ui_28_vote](https://user-images.githubusercontent.com/69671663/147409108-33d52556-f70c-4253-bdb2-e469e8ef6730.png)

![ui_29_eject](https://user-images.githubusercontent.com/69671663/147409109-cda58d4f-a7d7-4764-9b26-594ae78ab82a.png)

![ui_31_kill](https://user-images.githubusercontent.com/69671663/147409055-8d9fd203-b79e-4848-9631-252d6a62b22c.png)

![ui_32_admin_map](https://user-images.githubusercontent.com/69671663/147409056-156ad9f1-4377-40f1-b88b-b976031edf2b.png)

![ui_33_victory](https://user-images.githubusercontent.com/69671663/147409057-e88c21ec-672b-4a40-b29d-83b23fc855bd.png)

![ui_34_defeat](https://user-images.githubusercontent.com/69671663/147409058-2d27a26f-f21e-4323-95c1-6972cbb6a541.png)

![ui_35_server](https://user-images.githubusercontent.com/69671663/147409059-2ce0dda8-87a3-4189-ba29-1ec39249814e.png)


# Credits
* [Innersloth](https://www.innersloth.com) for their game 'Among Us' and its assets. 
* [kidscancode](https://github.com/kidscancode) for their [tutorial](https://www.youtube.com/watch?v=3UxnelT9aCo&list=PLsk-HSGFjnaGQq7ybM8Lgkh5EMxUWPm2i), and [sample projects](https://github.com/kidscancode/pygame_tutorials) used as the base for the game. 
* [Albert-91](https://github.com/Albert-91) for their [project](https://github.com/Albert-91/zombie-in-clab), used as a reference.
* [PlainSight](https://github.com/PlainSight) for their [project](https://github.com/PlainSight/pygameblog), used as the base for multiplayer functionality.
* [TomPrograms](https://github.com/TomPrograms) for their [project](https://github.com/TomPrograms/Python-Voice-Chat), used as the base for voice chat functionality.
