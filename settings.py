import pygame

# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SKYBLUE = (135, 206, 235)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
Orange = (255, 165, 0)
Brown = (106, 55, 5)
Transparent_Black = (0, 0, 0, 1)
MENU_FONT_COLOR = (255, 255, 255)

# game settings
WIDTH = 1280   # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 640  # 16 * 48 or 32 * 24 or 64 * 12
FPS = 60
TITLE = "Multi Player Game"
BGCOLOR = Brown
NO_OF_MISSIONS = 8
NO_OF_BOTS = 9
TILESIZE = 32
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE
FONT = 'Assets/Fonts/Rubik-ExtraBold.TTF'


# Menu setting
INTRO_SPRITE_WIDTH = 40
INTRO_SPRITE_HEIGHT = 40
INTRO_SPRITE_POS_X = 0.37
OPTIONS_SPRITE_WIDTH = 45
OPTIONS_SPRITE_HEIGHT = 45
OPTIONS_SPRITE_POS_X = 0.3


# Player settings
PLAYER_SPEED = 400

# Walls setting
WALL_IMG = 'wall.png'

# Sprite Layers
WALL_LAYER = 1
PLAYER_LAYER = 2
BOT_LAYER = 1
EFFECTS_LAYER = 3
ITEM_LAYER = 1

# Sound Effects
#BG_MUSIC1 = 'Background/background.wav'
#BG_MUSIC2 = 'Background/espionage.ogg'
BG_MUSIC3 = 'Ambience/AMB_Main.wav'

CAFETERIA_AMBIENT_DETECT_RADIUS = 750
MEDBAY_AMBIENT_DETECT_RADIUS = 450
SECURITY_ROOM_AMBIENT_DETECT_RADIUS = 350
REACTOR_ROOM_AMBIENT_DETECT_RADIUS = 450
ENGINE_ROOM_AMBIENT_DETECT_RADIUS = 400
ELECTRICAL_ROOM_AMBIENT_DETECT_RADIUS = 570
STORAGE_ROOM_AMBIENT_DETECT_RADIUS = 580
ADMIN_ROOM_AMBIENT_DETECT_RADIUS = 400
COMMUNICATION_ROOM_AMBIENT_DETECT_RADIUS = 370
OXYGEN_ROOM_AMBIENT_DETECT_RADIUS = 250
COCKPIT_ROOM_AMBIENT_DETECT_RADIUS = 300
WEAPON_ROOM_AMBIENT_DETECT_RADIUS = 400

stepping_rate = 230  # the time interval between each footstep sound played in milisecs
FOOTSTEP_SOUNDS = ['Footsteps/Footstep01.wav',
                   'Footsteps/Footstep02.wav',
                   'Footsteps/Footstep03.wav',
                   'Footsteps/Footstep04.wav',
                   'Footsteps/Footstep05.wav',
                   'Footsteps/Footstep06.wav',
                   'Footsteps/Footstep07.wav',
                   'Footsteps/Footstep08.wav'
                   ]

EFFECT_SOUNDS = {'main_menu_music': 'Background/main_menu_music.mp3',
                 'start_game': 'General/roundstart.wav',
                 'emergency_alarm': 'General/alarm_emergencymeeting.wav',
                 'dead_body_found': 'General/report_Bodyfound.wav',
                 'crises_alarm': 'General/crises.wav',
                 'invisible': 'General/swap.wav',
                 'vent': 'General/vent.wav',
                 'victory_crew': 'General/victory_crew.wav',
                 'victory_imposter': 'General/victory_impostor.wav',
                 'game_left': 'General/victory_disconnect.wav',
                 'fill_gas_can': 'General/gas_can_fill.wav',
                 'pick_gas_can': 'General/pick_up_gas_can.wav',
                 'menu_sel': 'UI/select.wav',
                 'go_back': 'UI/back2.wav',
                 'selected': 'UI/selected2.wav',
                 'pause': 'UI/pause.wav',
                 'backspace': 'UI/backspace.wav',
                 'keypress': 'UI/keypress.wav',
                 'map_click': 'UI/map_btn_click.wav',
                 'map_click2': 'UI/pause.wav',
                 'task_completed': 'General/task_complete.wav',
                 'imposter_kill_sound': 'Kill/imposter_kill.wav',
                 'imposter_kill_cooldown_sound': 'Kill/imposter_kill_cooldown.wav',
                 'imposter_kill_victim_sound': 'Kill/imposter_kill_victim.wav',
                 'vote_sound': 'UI/votescreen_locking.wav',
                 'fix_electric_wires_BG': 'Tasks Backgrounds/AMB_Electrical.wav',
                 'fixed_electric_wires_BG': 'Tasks Backgrounds/AMB_ElectricRoom.wav',
                 'stabilize_nav_BG': 'Tasks Backgrounds/AMB_Admin.wav',
                 'emtpy_garbage_BG': 'Tasks Backgrounds/AMB_DecontaminationHall.wav',
                 'reboot_wifi_BG': 'Tasks Backgrounds/AMB_Laboratory.wav',
                 'rebooted_wifi_BG': 'Tasks Backgrounds/AMB_comms #16940.wav',
                 }

ELECTRIC_SHOCK_SOUNDS = ['Electric Shock/AMB_Electricshock1.wav',
                         'Electric Shock/AMB_Electricshock2.wav',
                         'Electric Shock/AMB_Electricshock3.wav',
                         'Electric Shock/AMB_Electricshock4.wav'
                         ]

COMMS_RADIO_SOUNDS = ['Comms Radio/AMB_comms #16940.wav',
                      'Comms Radio/AMB_Comms.wav',
                      'Comms Radio/AMB_CommsRoom.wav',
                      ]

AMBIENT_SOUNDS = {'admin_room': 'Ambience/AMB_Admin.wav',
                  'cafeteria': 'Ambience/AMB_Cafeteria.wav',
                  'cockpit': 'Ambience/AMB_Cockpit.wav',
                  'comms1': 'Ambience/AMB_comms #16940.wav',
                  'comms2': 'Ambience/AMB_Comms.wav',
                  'comms3': 'Ambience/AMB_CommsRoom.wav',
                  'electrical1': 'Ambience/AMB_Electrical.wav',
                  'medbay_room': 'Ambience/AMB_MedbayRoom.wav',
                  'electrical_room': 'Ambience/AMB_ElectricRoom.wav',
                  'u_engine_room': 'Ambience/AMB_EngineRoom.wav',
                  'l_engine_room': 'Ambience/AMB_EngineRoom.wav',
                  'reactor_room': 'Ambience/AMB_ReactorRoom.wav',
                  'security_room': 'Ambience/AMB_SecurityRoom.wav',
                  'storage_room': 'Ambience/AMB_Storage.wav',
                  'oxygen_room': 'Ambience/AMB_Oxygen.wav',
                  'launchpad': 'Ambience/AMB_Launchpad.wav',
                  'main': 'Ambience/AMB_Main.wav',
                  'weapons': 'Ambience/AMB_Weapons.wav',
                  }

# Visual Effects
LIGHT_MASK = 'light_350_med.png'
LIGHT_MASK_REACTOR = 'light_350_med_reactor.png'
NIGHT_COLOR = (20, 20, 20)
NIGHT_COLOR_REACTOR = (200, 20, 20)
LIGHT_RADIUS = (500, 500)
LIGHT_RADIUS_REACTOR = (500, 500)

# Bots Position
BOT_POS = [(5401, 1530), (3686, 1857), (3733, 2626), (2325, 1814),
           (1718, 1282), (1288, 2418), (1249, 506), (2513, 1286)
           ]


# Mini Map
MAP_BUTTON = "UI/map_button.png"

# ITEMS-------------------

ITEM_IMAGES = {'health': 'health_pack.png',
               'weapon': 'shotgun.png',
               'vent': 'ventilation.png',
               'emerg_btn': 'emergency_icon_inv.png',
               'destroy_asteroids': 'destroy_asteroids.png',
               'nav': 'nav.png',
               'nav_highlight': 'nav_highlight.png'

               }

CLEAR_ASTEROIDS_IMAGES = ['Assets/Images/Tasks/Clear Asteroids/asteroid1.png',
                          'Assets/Images/Tasks/Clear Asteroids/asteroid2.png',
                          'Assets/Images/Tasks/Clear Asteroids/asteroid3.png',
                          'Assets/Images/Tasks/Clear Asteroids/asteroid4.png'

                          ]


# Tasks Setting
DETECT_RADIUS = 250
DETECT_RADIUS_SABOTAGE_FIX = 50
STABILIZE_NAV_RADIUS = 140
EMPTY_GARBAGE_RADIUS = 70
REBOOT_WIFI_RADIUS = 50
FIX_ELECTRICITY_WIRES_RADIUS = 50
VIEW_ADMIN_MAP_CONTROL_RADIUS = 85
VIEW_SECURITY_MONITOR_RADIUS = 170
DIVERT_POWER_TOP_REACTOR_RADIUS = 50
ALIGN_ENGINE_OUTPUT = 50
PICK_STORAGE_GAS_CAN_RADIUS = 50
FUEL_ENGINE = 50

# Pygame Mouse Button Codes
LEFT_MOUSE_BUTTON = 1
MIDDLE_MOUSE_BUTTON = 2
RIGHT_MOUSE_BUTTON = 3


# PLAYER SPRITES MOVEMENTS ----------------------------
# Red Player Movements
# Player left movement
red_player_imgs_left = []
# loops 1 to N-1
for i in range(1, 18):
    red_player_imgs_left.append(pygame.image.load('Assets/Images/Player/Red/red_left_walk/'+'step'+str(i)+'.png'))
# loops 1 to N-1
for i in range(0, 17):
    red_player_imgs_left[i] = pygame.transform.smoothscale(red_player_imgs_left[i], (64, 86))

# Player right movement
red_player_imgs_right = []
# loops 1 to 17
for i in range(1, 18):
    red_player_imgs_right.append(pygame.image.load('Assets/Images/Player/Red/red_right_walk/'+'step'+str(i)+'.png'))
# loops 1 to 16
for i in range(0, 17):
    red_player_imgs_right[i] = pygame.transform.smoothscale(red_player_imgs_right[i], (64, 86))


# Player down movement
red_player_imgs_down = []
for i in range(1, 19):
    red_player_imgs_down.append(pygame.image.load('Assets/Images/Player/Red/red_down_walk/'+'step'+str(i)+'.png'))
# loops 1 to 16
for i in range(0, 18):
    red_player_imgs_down[i] = pygame.transform.smoothscale(red_player_imgs_down[i], (64, 86))

# Player Up movement
red_player_imgs_up = []
# loops 1 to 16
for i in range(1, 18):
    red_player_imgs_up.append(pygame.image.load('Assets/Images/Player/Red/red_up_walk/'+'step'+str(i)+'.png'))
# loops 1 to 16
for i in range(0, 17):
    red_player_imgs_up[i] = pygame.transform.smoothscale(red_player_imgs_up[i], (64, 86))

red_player_imgs_dead = pygame.image.load('Assets/Images/Player/Dead/Deadred.png')

red_player_imgs_ghost_left = pygame.image.load('Assets/Images/Player/Red/red_ghost/step1_left.png')
red_player_imgs_ghost_left = pygame.transform.smoothscale(red_player_imgs_ghost_left, (64, 86))

red_player_imgs_ghost_right = pygame.image.load('Assets/Images/Player/Red/red_ghost/step1_right.png')
red_player_imgs_ghost_right = pygame.transform.smoothscale(red_player_imgs_ghost_right, (64, 86))

red_player_emergency_meeting = pygame.image.load('Assets/Images/Alerts/emergency_meeting_red.png')
red_player_emergency_meeting_report = pygame.image.load('Assets/Images/Alerts/report_dead_body_red.png')

# Blue Player Movements-----------------
# Player left movement
blue_player_imgs_left = []
# loops 1 to N-1
for i in range(1, 18):
    blue_player_imgs_left.append(pygame.image.load('Assets/Images/Player/Blue/blue_left_walk/'+'step'+str(i)+'.png'))
# loops 1 to N-1
for i in range(0, 17):
    blue_player_imgs_left[i] = pygame.transform.smoothscale(blue_player_imgs_left[i], (64, 86))


# Player right movement
blue_player_imgs_right = []
# loops 1 to 17
for i in range(1, 18):
    blue_player_imgs_right.append(pygame.image.load('Assets/Images/Player/Blue/blue_right_walk/'+'step'+str(i)+'.png'))
# loops 1 to 16
for i in range(0, 17):
    blue_player_imgs_right[i] = pygame.transform.smoothscale(blue_player_imgs_right[i], (64, 86))


# Player down movement
blue_player_imgs_down = []
for i in range(1, 19):
    blue_player_imgs_down.append(pygame.image.load('Assets/Images/Player/Blue/blue_down_walk/'+'step'+str(i)+'.png'))
# loops 1 to 16
for i in range(0, 18):
    blue_player_imgs_down[i] = pygame.transform.smoothscale(blue_player_imgs_down[i], (64, 86))

# Player Up movement
blue_player_imgs_up = []
# loops 1 to 16
for i in range(1, 18):
    blue_player_imgs_up.append(pygame.image.load('Assets/Images/Player/Blue/blue_up_walk/'+'step'+str(i)+'.png'))
# loops 1 to 16
for i in range(0, 17):
    blue_player_imgs_up[i] = pygame.transform.smoothscale(blue_player_imgs_up[i], (64, 86))

blue_player_imgs_dead = pygame.image.load('Assets/Images/Player/Dead/Deadblue.png')

blue_player_imgs_ghost_left = pygame.image.load('Assets/Images/Player/Blue/blue_ghost/step1_left.png')
blue_player_imgs_ghost_left = pygame.transform.smoothscale(blue_player_imgs_ghost_left, (64, 86))

blue_player_imgs_ghost_right = pygame.image.load('Assets/Images/Player/Blue/blue_ghost/step1_right.png')
blue_player_imgs_ghost_right = pygame.transform.smoothscale(blue_player_imgs_ghost_right, (64, 86))

blue_player_emergency_meeting = pygame.image.load('Assets/Images/Alerts/emergency_meeting_blue.png')
blue_player_emergency_meeting_report = pygame.image.load('Assets/Images/Alerts/report_dead_body_blue.png')

# Green Player Movements-----------------
# Player left movement
green_player_imgs_left = []
# loops 1 to N-1
for i in range(1, 18):
    green_player_imgs_left.append(pygame.image.load('Assets/Images/Player/Green/green_left_walk/'+'step'+str(i)+'.png'))
# loops 1 to N-1
for i in range(0, 17):
    green_player_imgs_left[i] = pygame.transform.smoothscale(green_player_imgs_left[i], (64, 86))


# Player right movement
green_player_imgs_right = []
# loops 1 to 17
for i in range(1, 18):
    green_player_imgs_right.append(pygame.image.load('Assets/Images/Player/Green/green_right_walk/'+'step'+str(i)+'.png'))
# loops 1 to 16
for i in range(0, 17):
    green_player_imgs_right[i] = pygame.transform.smoothscale(green_player_imgs_right[i], (64, 86))


# Player down movement
green_player_imgs_down = []
for i in range(1, 19):
    green_player_imgs_down.append(pygame.image.load('Assets/Images/Player/Green/green_down_walk/'+'step'+str(i)+'.png'))
# loops 1 to 16
for i in range(0, 18):
    green_player_imgs_down[i] = pygame.transform.smoothscale(green_player_imgs_down[i], (64, 86))

# Player Up movement
green_player_imgs_up = []
# loops 1 to 16
for i in range(1, 18):
    green_player_imgs_up.append(pygame.image.load('Assets/Images/Player/Green/green_up_walk/'+'step'+str(i)+'.png'))
# loops 1 to 16
for i in range(0, 17):
    green_player_imgs_up[i] = pygame.transform.smoothscale(green_player_imgs_up[i], (64, 86))

green_player_imgs_dead = pygame.image.load('Assets/Images/Player/Dead/Deadgreen.png')

green_player_imgs_ghost_left = pygame.image.load('Assets/Images/Player/Green/green_ghost/step1_left.png')
green_player_imgs_ghost_left = pygame.transform.smoothscale(green_player_imgs_ghost_left, (64, 86))

green_player_imgs_ghost_right = pygame.image.load('Assets/Images/Player/Green/green_ghost/step1_right.png')
green_player_imgs_ghost_right = pygame.transform.smoothscale(green_player_imgs_ghost_right, (64, 86))

green_player_emergency_meeting = pygame.image.load('Assets/Images/Alerts/emergency_meeting_green.png')
green_player_emergency_meeting_report = pygame.image.load('Assets/Images/Alerts/report_dead_body_green.png')

# Orange Player Movements-----------------
# Player left movement
orange_player_imgs_left = []
# loops 1 to N-1
for i in range(1, 18):
    orange_player_imgs_left.append(pygame.image.load('Assets/Images/Player/Orange/orange_left_walk/'+'step'+str(i)+'.png'))
# loops 1 to N-1
for i in range(0, 17):
    orange_player_imgs_left[i] = pygame.transform.smoothscale(orange_player_imgs_left[i], (64, 86))


# Player right movement
orange_player_imgs_right = []
# loops 1 to 17
for i in range(1, 18):
    orange_player_imgs_right.append(pygame.image.load('Assets/Images/Player/Orange/orange_right_walk/'+'step'+str(i)+'.png'))
# loops 1 to 16
for i in range(0, 17):
    orange_player_imgs_right[i] = pygame.transform.smoothscale(orange_player_imgs_right[i], (64, 86))


# Player down movement
orange_player_imgs_down = []
for i in range(1, 19):
    orange_player_imgs_down.append(pygame.image.load('Assets/Images/Player/Orange/orange_down_walk/'+'step'+str(i)+'.png'))
# loops 1 to 16
for i in range(0, 18):
    orange_player_imgs_down[i] = pygame.transform.smoothscale(orange_player_imgs_down[i], (64, 86))

# Player Up movement
orange_player_imgs_up = []
# loops 1 to 16
for i in range(1, 18):
    orange_player_imgs_up.append(pygame.image.load('Assets/Images/Player/Orange/orange_up_walk/'+'step'+str(i)+'.png'))
# loops 1 to 16
for i in range(0, 17):
    orange_player_imgs_up[i] = pygame.transform.smoothscale(orange_player_imgs_up[i], (64, 86))

orange_player_imgs_dead = pygame.image.load('Assets/Images/Player/Dead/Deadorange.png')

orange_player_imgs_ghost_left = pygame.image.load('Assets/Images/Player/Orange/orange_ghost/step1_left.png')
orange_player_imgs_ghost_left = pygame.transform.smoothscale(orange_player_imgs_ghost_left, (64, 86))

orange_player_imgs_ghost_right = pygame.image.load('Assets/Images/Player/Orange/orange_ghost/step1_right.png')
orange_player_imgs_ghost_right = pygame.transform.smoothscale(orange_player_imgs_ghost_right, (64, 86))

orange_player_emergency_meeting = pygame.image.load('Assets/Images/Alerts/emergency_meeting_orange.png')
orange_player_emergency_meeting_report = pygame.image.load('Assets/Images/Alerts/report_dead_body_orange.png')

# Yellow Player Movements-----------------
# Player left movement
yellow_player_imgs_left = []
# loops 1 to N-1
for i in range(1, 18):
    yellow_player_imgs_left.append(pygame.image.load('Assets/Images/Player/Yellow/yellow_left_walk/'+'step'+str(i)+'.png'))
# loops 1 to N-1
for i in range(0, 17):
    yellow_player_imgs_left[i] = pygame.transform.smoothscale(yellow_player_imgs_left[i], (64, 86))


# Player right movement
yellow_player_imgs_right = []
# loops 1 to 17
for i in range(1, 18):
    yellow_player_imgs_right.append(pygame.image.load('Assets/Images/Player/Yellow/yellow_right_walk/'+'step'+str(i)+'.png'))
# loops 1 to 16
for i in range(0, 17):
    yellow_player_imgs_right[i] = pygame.transform.smoothscale(yellow_player_imgs_right[i], (64, 86))


# Player down movement
yellow_player_imgs_down = []
for i in range(1, 19):
    yellow_player_imgs_down.append(pygame.image.load('Assets/Images/Player/Yellow/yellow_down_walk/'+'step'+str(i)+'.png'))
# loops 1 to 16
for i in range(0, 18):
    yellow_player_imgs_down[i] = pygame.transform.smoothscale(yellow_player_imgs_down[i], (64, 86))

# Player Up movement
yellow_player_imgs_up = []
# loops 1 to 16
for i in range(1, 18):
    yellow_player_imgs_up.append(pygame.image.load('Assets/Images/Player/Yellow/yellow_up_walk/'+'step'+str(i)+'.png'))
# loops 1 to 16
for i in range(0, 17):
    yellow_player_imgs_up[i] = pygame.transform.smoothscale(yellow_player_imgs_up[i], (64, 86))
    
yellow_player_imgs_dead = pygame.image.load('Assets/Images/Player/Dead/Deadyellow.png')

yellow_player_imgs_ghost_left = pygame.image.load('Assets/Images/Player/Yellow/yellow_ghost/step1_left.png')
yellow_player_imgs_ghost_left = pygame.transform.smoothscale(yellow_player_imgs_ghost_left, (64, 86))

yellow_player_imgs_ghost_right = pygame.image.load('Assets/Images/Player/Yellow/yellow_ghost/step1_right.png')
yellow_player_imgs_ghost_right = pygame.transform.smoothscale(yellow_player_imgs_ghost_right, (64, 86))

yellow_player_emergency_meeting = pygame.image.load('Assets/Images/Alerts/emergency_meeting_yellow.png')
yellow_player_emergency_meeting_report = pygame.image.load('Assets/Images/Alerts/report_dead_body_yellow.png')


# Black Player Movements-----------------
# Player left movement
black_player_imgs_left = []
black_player_imgs_left.append(pygame.image.load('Assets/Images/Player/Black/black_left_walk/step1.png'))
black_player_imgs_left[0] = pygame.transform.smoothscale(black_player_imgs_left[0], (64, 86))


# Player right movement
black_player_imgs_right = []
black_player_imgs_right.append(pygame.image.load('Assets/Images/Player/Black/black_right_walk/step1.png'))
black_player_imgs_right[0] = pygame.transform.smoothscale(black_player_imgs_right[0], (64, 86))

# Player down movement
black_player_imgs_down = []
black_player_imgs_down.append(pygame.image.load('Assets/Images/Player/Black/black_down_walk/step1.png'))
black_player_imgs_down[0] = pygame.transform.smoothscale(black_player_imgs_down[0], (64, 86))

# Player Up movement
black_player_imgs_up = []
black_player_imgs_up.append(pygame.image.load('Assets/Images/Player/Black/black_up_walk/step1.png'))
black_player_imgs_up[0] = pygame.transform.smoothscale(black_player_imgs_up[0], (64, 86))
    
black_player_imgs_dead = pygame.image.load('Assets/Images/Player/Dead/Deadblack.png')


# Brown Player Movements-----------------
# Player left movement
brown_player_imgs_left = []
brown_player_imgs_left.append(pygame.image.load('Assets/Images/Player/Brown/brown_left_walk/step1.png'))
brown_player_imgs_left[0] = pygame.transform.smoothscale(brown_player_imgs_left[0], (64, 86))


# Player right movement
brown_player_imgs_right = []
brown_player_imgs_right.append(pygame.image.load('Assets/Images/Player/Brown/brown_right_walk/step1.png'))
brown_player_imgs_right[0] = pygame.transform.smoothscale(brown_player_imgs_right[0], (64, 86))

# Player down movement
brown_player_imgs_down = []
brown_player_imgs_down.append(pygame.image.load('Assets/Images/Player/Brown/brown_down_walk/step1.png'))
brown_player_imgs_down[0] = pygame.transform.smoothscale(brown_player_imgs_down[0], (64, 86))

# Player Up movement
brown_player_imgs_up = []
brown_player_imgs_up.append(pygame.image.load('Assets/Images/Player/Brown/brown_up_walk/step1.png'))
brown_player_imgs_up[0] = pygame.transform.smoothscale(brown_player_imgs_up[0], (64, 86))
    
brown_player_imgs_dead = pygame.image.load('Assets/Images/Player/Dead/Deadbrown.png')


# Pink Player Movements-----------------
# Player left movement
pink_player_imgs_left = []
pink_player_imgs_left.append(pygame.image.load('Assets/Images/Player/Pink/pink_left_walk/step1.png'))
pink_player_imgs_left[0] = pygame.transform.smoothscale(pink_player_imgs_left[0], (64, 86))


# Player right movement
pink_player_imgs_right = []
pink_player_imgs_right.append(pygame.image.load('Assets/Images/Player/Pink/pink_right_walk/step1.png'))
pink_player_imgs_right[0] = pygame.transform.smoothscale(pink_player_imgs_right[0], (64, 86))

# Player down movement
pink_player_imgs_down = []
pink_player_imgs_down.append(pygame.image.load('Assets/Images/Player/Pink/pink_down_walk/step1.png'))
pink_player_imgs_down[0] = pygame.transform.smoothscale(pink_player_imgs_down[0], (64, 86))

# Player Up movement
pink_player_imgs_up = []
pink_player_imgs_up.append(pygame.image.load('Assets/Images/Player/Pink/pink_up_walk/step1.png'))
pink_player_imgs_up[0] = pygame.transform.smoothscale(pink_player_imgs_up[0], (64, 86))
    
pink_player_imgs_dead = pygame.image.load('Assets/Images/Player/Dead/Deadpink.png')


# Purple Player Movements-----------------
# Player left movement
purple_player_imgs_left = []
purple_player_imgs_left.append(pygame.image.load('Assets/Images/Player/Purple/Purple_left_walk/step1.png'))
purple_player_imgs_left[0] = pygame.transform.smoothscale(purple_player_imgs_left[0], (64, 86))


# Player right movement
purple_player_imgs_right = []
purple_player_imgs_right.append(pygame.image.load('Assets/Images/Player/Purple/Purple_right_walk/step1.png'))
purple_player_imgs_right[0] = pygame.transform.smoothscale(purple_player_imgs_right[0], (64, 86))

# Player down movement
purple_player_imgs_down = []
purple_player_imgs_down.append(pygame.image.load('Assets/Images/Player/Purple/Purple_down_walk/step1.png'))
purple_player_imgs_down[0] = pygame.transform.smoothscale(purple_player_imgs_down[0], (64, 86))

# Player Up movement
purple_player_imgs_up = []
purple_player_imgs_up.append(pygame.image.load('Assets/Images/Player/Purple/Purple_up_walk/step1.png'))
purple_player_imgs_up[0] = pygame.transform.smoothscale(purple_player_imgs_up[0], (64, 86))
    
purple_player_imgs_dead = pygame.image.load('Assets/Images/Player/Dead/DeadPurple.png')


# White Player Movements-----------------
# Player left movement
white_player_imgs_left = []
white_player_imgs_left.append(pygame.image.load('Assets/Images/Player/White/White_left_walk/step1.png'))
white_player_imgs_left[0] = pygame.transform.smoothscale(white_player_imgs_left[0], (64, 86))


# Player right movement
white_player_imgs_right = []
white_player_imgs_right.append(pygame.image.load('Assets/Images/Player/White/White_right_walk/step1.png'))
white_player_imgs_right[0] = pygame.transform.smoothscale(white_player_imgs_right[0], (64, 86))

# Player down movement
white_player_imgs_down = []
white_player_imgs_down.append(pygame.image.load('Assets/Images/Player/White/White_down_walk/step1.png'))
white_player_imgs_down[0] = pygame.transform.smoothscale(white_player_imgs_down[0], (64, 86))

# Player Up movement
white_player_imgs_up = []
white_player_imgs_up.append(pygame.image.load('Assets/Images/Player/White/White_up_walk/step1.png'))
white_player_imgs_up[0] = pygame.transform.smoothscale(white_player_imgs_up[0], (64, 86))
    
white_player_imgs_dead = pygame.image.load('Assets/Images/Player/Dead/DeadWhite.png')