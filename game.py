import random
from time import sleep
import pygame as pg
import sys
import math
from os import path
import pygame.font
import tasks
from settings import *
from sprites import *
from tilemap import *
from pygame import mixer
from menu import Menu
from board import Board
from gamefunctions import GameFunctions
from tasks import *
import time, datetime
import time
from pygame.locals import *
import pickle
import select
import socket

BUFFERSIZE = 8192


class Game:
    def __init__(self):
        pg.init()
        # pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.board = Board(WIDTH, HEIGHT, self)
        self.tasks = Task(self)
        #self.mini_game = MiniGame(self)
        self.gamefuctions = GameFunctions(self)
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        # pg.key.set_repeat(100, 100)
        self.missions_done = 0  # Access this variable, increment everytime a mission is completed
        # root directory is game_folder
        self.game_folder = path.dirname(__file__)
        # 2nd parameter is folder location
        self.img_folder = path.join(self.game_folder, 'Assets/Images')
        self.walls_img_folder = path.join(self.game_folder, 'Assets/Images/Walls')
        self.player_img_folder = path.join(self.game_folder, 'Assets/Images/Player')
        self.Environment_folder = path.join(self.game_folder, 'Assets/Images/Environment')
        self.map_folder = path.join(self.game_folder, 'Assets/Maps')
        self.items_img_folder = path.join(self.game_folder, 'Assets/Images/Items')
        self.Menu_folder = path.join(self.game_folder, 'Assets/Images/Menu')
        self.sound_folder = path.join(self.game_folder, 'Assets/Sounds')
        self.font_folder = path.join(self.game_folder, 'Assets/Fonts')
        self.playing = False
        self.sound_playing = False
        self.game_left = False
        self.screen.get_height()
        self.invisible_play_count = 0
        self.night = False
        self.night_sync = 0
        self.emergency = False
        self.emergency_sync = 0
        self.night_reactor = False
        self.night_reactor_sync = 0
        self.paused = False
        self.score_list = []
        self.voters = []
        self.menu = Menu(self)

        # These two variables used in progress bar's formula
        # for imposter in multiplayer mode
        self.bot_killed = 0
        self.bot_count = 9
        self.bot_count_show_status = True
        # ------------------------------

        # These two variables used in progress bar's formula
        # for imposter in multiplayer mode
        self.server_player_killed = 0
        self.server_players_connected = 0
        self.server_player_alive = 0
        # ------------------------------



        self.sabotage_timer_visible_status = False
        self.kill_timer_visible_status = False
        self.reactor_timer_cooldown_visible_status = False
        self.reactor_timer_visible_client_status = False
        self.meeting_timer_visible_status = False
        self.meeting_timer_cooldown_visible_status = False

        self.gamemode = None
        self.sabotagecritical = False
        self.serveraddress = ""
        self.player_highest_id = 0
        self.emergency_img_sync = None
        self.emergency_img_sync_report = None
        self.eject = False
        self.eject_sync = 0
        self.eject_img = None
        self.eject_colour = None
        self.eject_pos = 0
        self.timer = pygame.time.get_ticks()
        self.timer_start = pygame.time.get_ticks()

        self.player_pos = [(3288, 873), (3046, 791), (3046, 651), (3563, 653), (3563, 762), (2968, 530), (3566, 553)]
        # Vent Locations
        self.vent = [(3898, 791), (5309, 1144), (5309, 1525), (4513, 1525), (4531, 2459), (3694, 1942), (2220, 1711),
                     (1580, 2407), (1887, 1578), (931, 1626), (802, 1151), (1586, 460), (2121, 1249), (4447, 363)]
        # Botc olours
        self.bot_colours = ["Black", "Blue", "Brown", "Green", "Orange", "Pink", "Purple", "Red", "White", "Yellow"]

        # Mini Map-----
        # 57292 = width of main map image, 3168 = height of main map image
        self.mini_map = pg.Surface([5792 / 15, 3168 / 15], pg.SRCALPHA, 32).convert_alpha()
        self.mini_map = pg.transform.scale(self.mini_map, (int(3 * (5792 / 15)), int(3 * (3168 / 15)))).convert_alpha()
        self.mini_map_img = pg.image.load(path.join(self.map_folder, 'mini_map.png')).convert_alpha()
        # 57292 = width of main map image, 3168 = height of main map image
        self.mini_map_img = pg.transform.smoothscale(self.mini_map_img,
                                                     (int(3 * (5792 / 15)), int(3 * (3168 / 15)))).convert_alpha()
        # Admin Room Mini Map
        self.admin_mini_map = pg.Surface([5792 / 15, 3168 / 15], pg.SRCALPHA, 32).convert_alpha()
        self.admin_mini_map = pg.transform.scale(self.admin_mini_map,
                                                 (int(3 * (5792 / 15)), int(3 * (3168 / 15)))).convert_alpha()
        self.admin_mini_map_img = pg.image.load(path.join(self.map_folder, 'mini_map3.png')).convert_alpha()
        # 57292 = width of main map image, 3168 = height of main map image
        self.admin_mini_map_img = pg.transform.smoothscale(self.admin_mini_map_img,
                                                           (int(3 * (5792 / 15)), int(3 * (3168 / 15)))).convert_alpha()

        # UI ELEMENTS----------------------------
        # Mini Map Button
        self.mini_map_button_img = pg.image.load(path.join(self.img_folder, MAP_BUTTON))
        # self.mini_map_button_img = pg.transform.scale(self.mini_map_button_img, (56, 56))
        self.mini_map_button_status = False

        # Tasks checks
        self.isdoingTask = False
        # Task Button
        self.task_button_click_status = False
        self.task_button_show_status = False
        self.pause_quit_button_status = False
        self.emerg_meeting_button_status = False
        self.emerg_meeting_report_status = False
        self.skip_meeting_button_status = False
        self.imposter_among_us_status = True
        self.kill_victim_anim = False
        self.kill_victim_anim_index = -1
        self.emergency_meeting_index = 0
        self.emerg_vote_red_checkbox_tick_status = False
        self.emerg_vote_blue_checkbox_tick_status = False
        self.emerg_vote_green_checkbox_tick_status = False
        self.emerg_vote_orange_checkbox_tick_status = False
        self.emerg_vote_yellow_checkbox_tick_status = False
        # Navigation_task checks
        self.stabilize_steering_button_status = False
        self.stabilize_steering_window_status = False
        self.target_center_bt_status = False
        self.stabilize_target_btn1_status = False
        self.stabilize_close_btn_status = False
        self.stablize_sound_play_count = 1
        self.stabilize_task_play_count = 1
        self.target_center_sel_count = 1
        # Empty_Garbage_task checks
        self.empty_garbage_window_status = False
        self.garbage_liver_Up_status = False
        self.garbage_liver_Down_status = False
        self.empty_garbage_img_status = False
        self.empty_garbage_close_btn_status = False
        self.garbage_liver_Up_sel_count = 1
        self.empty_garbage_sound_play_count = 1
        self.empty_garbage_task_play_count = 1
        # Reboot_Wifi_task checks
        self.reboot_wifi_window_status = False
        self.reboot_wifi_liver_up_status = False
        self.reboot_wifi_liver_down_status = False
        self.reboot_wifi_close_btn_status = False
        self.rebooted_wifi_window_status = False
        self.reboot_wifi_liver_sel_count = 1
        self.reboot_wifi_sound_play_count = 1
        self.reboot_wifi_task_play_count = 1
        # Fix_Electricity_Wires_task checks
        self.electricity_wire_window_status = False
        self.electricity_wire_close_btn_status = False
        self.electricity_wire_btns_visible = False
        self.electricity_wire_red_btn_status = False
        self.electricity_wire_blue_btn_status = False
        self.electricity_wire_yellow_btn_status = False
        self.electricity_wire_pink_btn_status = False
        self.electricity_wires_fixed_count = 0
        self.electricity_wire_sound_play_count = 1
        self.electricity_wire_task_play_count = 1
        self.electricity_wires_red_sel_count = 1
        self.electricity_wires_blue_sel_count = 1
        self.electricity_wires_yellow_sel_count = 1
        self.electricity_wires_pink_sel_count = 1
        # Divert Power to Reactor
        self.divert_power_to_reactor_window_status = False
        self.divert_power_to_reactor_livers_btn_status = False
        self.divert_power_to_reactor_liversUP_status = False
        self.divert_power_to_reactor_close_btn_status = False
        self.divert_power_to_reactor_livers_btn_sel_count = 1
        self.divert_power_to_reactor_liversUP_sel_count = 1
        self.divert_power_to_reactor_task_play_count = 1
        self.divert_power_to_reactor_sound_play_count = 1
        # Align Engine Output
        self.align_engine_output_window_status = False
        self.align_engine_output_window2_status = False
        self.align_engine_output_window3_status = False
        self.align_engine_output_window4_status = False
        self.align_engine_liver_status = False
        self.align_engine_liver_pos_btn1_status = False
        self.align_engine_liver_pos_btn2_status = False
        self.align_engine_output_close_btn_status = False
        self.align_engine_liver_pos_btn1_sel_count = 1
        self.align_engine_liver_pos_btn2_sel_count = 1
        self.align_engine_output_task_play_count = 1
        self.align_engine_output_sound_play_count = 1
        # Fuel Engine
        self.fuel_engine_window_status = False
        self.fuel_engine_fill_btn_status = False
        self.fuel_engine_close_btn_status = False
        self.is_gas_can_picked = False
        self.gas_can_not_picked_text_visible_status = False
        self.gas_can_picking_count = 1
        self.gas_can_picking_sound_play_count = 1
        self.fuel_engine_task_play_count = 1
        self.fuel_engine_fill_btn_sel_count = 1
        self.fuel_engine_sound_play_count = 1
        self.fuel_engine_sound_play_count2 = 1
        self.fuel_level = 310

        # Clear asteroid task
        self.clear_asteroid_task_available = False
        self.clear_asteroid_task_window_status = False
        self.clear_asteroid_task_play_count = 1
        self.clear_asteroid_sound_play_count = 1


        # View Admin and Security Room Monitor Task
        self.view_admin_security_monitor_window_status = False
        self.view_admin_security_monitor_close_btn_status = False
        self.view_admin_security_monitor_sound_play_count = 1
        # Open Cafeteria Computer
        self.open_cafe_comp_window_status = False
        self.open_cafe_comp_check_btn_status = False
        self.open_cafe_comp_check_pic_status = True
        self.open_cafe_comp_close_btn_status = False
        self.open_cafe_comp_imposter_select_status = False
        self.open_cafe_comp_sound_play_count = 1
        # Kill timer Icon status
        self.kill_timer_icon_status = True
        self.kill_timer_icon_dim_status = True
        # Sabotage timer Icon status
        self.sabotage_timer_icon_status = False
        self.sabotage_timer_icon_dim_status = True
        # Emergency timer Icon status
        self.emergency_timer_icon_status = False
        self.emergency_timer_icon_dim_status = True
        # Light Bulb timer Icon status
        self.light_bulb_timer_icon_status = True
        self.light_bulb_timer_icon_dim_status = True
        self.load_data()

    # THIS METHOD LOADS EVERYTHING FROM PROJECT DIRECTORIES
    # load map directory - map.txt and create map
    def load_data(self):
        # root directory is game_folder
        # game_folder = path.dirname(__file__)
        # 2nd parameter is folder location

        # Load tiled map from specified directory
        self.map = TiledMap(path.join(self.map_folder, 'map.tmx'))
        self.map_img = self.map.make_map()
        # make make outer rectangle that will display on screen
        self.map_rect = self.map_img.get_rect()

        # Load Dim screen
        # Dimmed Screen used for Pause Menu/ Emergency meeting/ Dead body reporting
        # can be used with any flash animation or text blitting
        self.dim_screen = pg.Surface(self.screen.get_size()).convert_alpha()
        self.dim_screen.fill((0, 0, 0, 180))


        """ CUSTOM EVENTS FOR DIFFERENT TIMERS - OPEN HERE"""

        # Kill Timer Custom User Event - USED IN BOTH FREEPLAY & MULTIPLAYER
        # initialze the time interval of killing a bot to 15
        self.time_left_to_kill = 15
        # Creating a user event that we will use for time interval
        self.kill_timer_event = pygame.USEREVENT + 1
        # Setting up the user event to respond every 1 second
        pygame.time.set_timer(self.kill_timer_event, 1000)
        # Condition to toggle show or hide kill_a_bot time interval
        self.kill_timer_visible_status = True

        # Reactor Sabotage Cool down Timer Custom User Event - USED IN BOTH FREEPLAY & MULTIPLAYER
        # it starts as soon as game is started, hides when imposter press K_Shift
        # and again reappears when players turn the reactor ON
        self.time_left_to_boom_cooldown = 15
        self.reactor_timer_cooldown_event = pygame.USEREVENT + 2
        # timer starts decrement as soon as game starts
        pygame.time.set_timer(self.reactor_timer_cooldown_event, 1000)
        self.reactor_timer_cooldown_visible_status = True

        # Reactor Timer Custom User Event - USED IN BOTH FREEPLAY & MULTIPLAYER
        # For each Client (Crewmate and Imposter)
        # it starts when imposter press K_Shift and hides when crewmate turns on
        # the reactor
        self.time_left_to_boom_client = 20
        self.reactor_timer_event_client = pygame.USEREVENT + 3
        self.reactor_timer_visible_client_status = False

        # Emergency Timer Custom User Event - USED IN BOTH FREEPLAY & MULTIPLAYER
        # it starts when crew mate or imposter press K_space on emergency_button
        # in cafeteria
        self.time_left_to_end_meeting = 30
        self.meeting_timer_event = pygame.USEREVENT + 4
        self.meeting_timer_visible_status = False

        # Emergency Icon Timer Custom User Event - USED IN BOTH FREEPLAY & MULTIPLAYER
        # it starts was soon as game starts and decrements time_left_to_end_meeting_cooldown
        self.time_left_to_end_meeting_cooldown = 15
        self.meeting_timer_cooldown_event = pygame.USEREVENT + 5
        pygame.time.set_timer(self.meeting_timer_cooldown_event, 1000)
        self.meeting_timer_cooldown_visible_status = True

        # light on/off Timer Custom User Event - USED IN BOTH FREEPLAY & MULTIPLAYER
        # initialze the time interval of turning light on/off
        self.time_left_to_light = 15
        self.light_timer_event = pygame.USEREVENT + 6
        pygame.time.set_timer(self.light_timer_event, 1000)
        self.light_timer_visible_status = True

        """ CUSTOM EVENTS FOR DIFFERENT TIMERS - CLOSE HERE"""



        """ TASK & ITEM IMAGES & PLAYER PROPERTIES LOADING - CLOSE HERE"""
        # Some task and Items Images and player properties
        self.kill_icon = pg.image.load("Assets/Images/UI/kill_icon.png").convert_alpha()
        self.kill_icon_dim = pg.image.load("Assets/Images/UI/kill_icon_dim.png").convert_alpha()
        self.sabotage_icon = pg.image.load("Assets/Images/UI/sabotage_icon.png").convert_alpha()
        self.sabotage_icon_dim = pg.image.load("Assets/Images/UI/sabotage_icon_dim.png").convert_alpha()
        self.emergency_icon = pg.image.load("Assets/Images/UI/emergency_icon.png").convert_alpha()
        self.emergency_icon = pg.transform.smoothscale(self.emergency_icon, (95, 81)).convert_alpha()
        self.emergency_icon_dim = pg.image.load("Assets/Images/UI/emergency_icon_dim.png").convert_alpha()
        self.emergency_icon_dim = pg.transform.smoothscale(self.emergency_icon_dim, (95, 81)).convert_alpha()
        self.light_bulb_icon = pg.image.load("Assets/Images/UI/light_bulb_icon.png").convert_alpha()
        self.light_bulb_icon = pg.transform.smoothscale(self.light_bulb_icon, (75, 90)).convert_alpha()
        self.light_bulb_icon_dim = pg.image.load("Assets/Images/UI/light_bulb_icon_dim.png").convert_alpha()
        self.light_bulb_icon_dim = pg.transform.smoothscale(self.light_bulb_icon_dim, (75, 90)).convert_alpha()

        self.invsible_player_image = pg.image.load("Assets\Images\Player\invisble3.png").convert_alpha()
        self.invsible_player_image = pygame.transform.scale(self.invsible_player_image, (64, 86)).convert_alpha()
        self.imposter_among_us_img = pygame.image.load('Assets\Images\Menu\imposteramongus.png').convert_alpha()
        self.kill_victim_anim_img = []
        for i in range(1, 19):
            self.kill_victim_anim_img.append(pygame.image.load('Assets/Images/Alerts/' + 'kill' + str(i) + '.png').convert_alpha())
        self.cafe_comp_img = pygame.image.load(
            'Assets\Images\Tasks\Become Imposter\cafe_computer_base.png').convert_alpha()
        self.cafe_comp_check_img = pygame.image.load('Assets\Images\Tasks\Become Imposter\check.png').convert_alpha()
        self.chat_img = pygame.image.load('Assets\Images\Meeting\chat.png').convert_alpha()
        self.vote_img = pygame.image.load('Assets\Images\Meeting\e_vote_base.png').convert_alpha()
        self.vote_tick_img = pygame.image.load('Assets\Images\Meeting\select_vote.png').convert_alpha()
        self.chat_img_dead = pygame.image.load('Assets\Images\Meeting\chat_dead.png').convert_alpha()
        self.vote_img_dead = pygame.image.load('Assets\Images\Meeting\e_vote_base_dead.png').convert_alpha()
        self.eject_screen_img = pygame.image.load('Assets\Images\Alerts\eject.png').convert_alpha()
        self.navigation_screen_img = pygame.image.load(
            'Assets\Images\Tasks\Stabilize Steering\stabilizer_base.png').convert_alpha()
        self.full_garbage_screen_img = pygame.image.load(
            'Assets\Images\Tasks\Empty Garbage\garbage_base_full.png').convert_alpha()
        self.empty_garbage_screen_img = pygame.image.load(
            'Assets\Images\Tasks\Empty Garbage\garbage_base_empty.png').convert_alpha()
        self.reboot_wifi_screen_img = pygame.image.load(
            'Assets\Images\Tasks\Reboot Wifi\panel_wifi_bg.png').convert_alpha()
        self.wifi_on_img = pygame.image.load('Assets\Images\Tasks\Reboot Wifi\wifi_on.png').convert_alpha()
        self.wifi_liver_down_img = pygame.image.load(
            'Assets\Images\Tasks\Reboot Wifi\panel_wifi-lever.png').convert_alpha()
        self.electricity_wire_img = pygame.image.load(
            'Assets\Images\Tasks\Fix Wiring\electricity_wire_base1.png').convert_alpha()
        self.electricity_wire_red_img = pygame.image.load('Assets/Images/Tasks/Fix Wiring/red_wire.png').convert_alpha()
        self.electricity_wire_blue_img = pygame.image.load(
            'Assets/Images/Tasks/Fix Wiring/blue_wire.png').convert_alpha()
        self.electricity_wire_yellow_img = pygame.image.load(
            'Assets/Images/Tasks/Fix Wiring/yellow_wire.png').convert_alpha()
        self.electricity_wire_pink_img = pygame.image.load(
            'Assets/Images/Tasks/Fix Wiring/pink_wire.png').convert_alpha()
        self.divert_power_to_reactor_window_img = pygame.image.load(
            'Assets/Images/Tasks/Divert Power/electricity_Divert_Base.png').convert_alpha()
        self.divert_power_to_reactor_liverUp_window_img = pygame.image.load(
            'Assets/Images/Tasks/Divert Power/electricity_divert_btn.png').convert_alpha()
        self.power_diverted_to_reactor_window_img = pygame.image.load(
            'Assets/Images/Tasks/Divert Power/electricity_Divert_Base2.png').convert_alpha()
        self.align_engine_output_window_img = pygame.image.load(
            'Assets/Images/Tasks/Align Engine Output/engineAlign_base.png').convert_alpha()
        self.align_engine_output_window2_img = pygame.image.load(
            'Assets/Images/Tasks/Align Engine Output/engineAlign_base2.png').convert_alpha()
        self.align_engine_output_window3_img = pygame.image.load(
            'Assets/Images/Tasks/Align Engine Output/engineAlign_base3.png').convert_alpha()
        self.align_engine_output_window4_img = pygame.image.load(
            'Assets/Images/Tasks/Align Engine Output/engineAlign_base4.png').convert_alpha()
        self.align_engine_liver_img = pygame.image.load(
            'Assets/Images/Tasks/Align Engine Output/engine_liver.png').convert_alpha()
        self.gas_can_img = pygame.image.load(
            'Assets/Images/Tasks/Fuel Engines/gas_can.png').convert_alpha()
        self.fuel_engine_window_img = pygame.image.load(
            'Assets/Images/Tasks/Fuel Engines/fuel_engines_base.png').convert_alpha()
        self.fuel_engine_filled_black_bg = pg.Surface((340, 495))
        self.fuel_engine_filled_black_bg.fill((0, 0, 0))
        """ TASK & ITEM IMAGES & PLAYER PROPERTIES LOADING - CLOSE HERE"""




        """ DIFFERENT BUTTONS FOR DIFFERENT TASKS - OPEN HERE"""

        self.emerg_red_checkbox = Button(self, None, None, 35, 35, WIDTH / 2 - 95, 223, "chkbox_red_btn",
                                         Transparent_Black, Transparent_Black, "Assets/Images/Meeting/checkbox.png", 35,
                                         35, 255)
        self.emerg_orange_checkbox = Button(self, None, None, 35, 35, WIDTH / 1.5 - 30, 223, "chkbox_orange_btn",
                                            Transparent_Black, Transparent_Black, "Assets/Images/Meeting/checkbox.png",
                                            35, 35, 255)
        self.emerg_green_checkbox = Button(self, None, None, 35, 35, WIDTH / 2 - 95, 276, "chkbox_green_btn",
                                           Transparent_Black, Transparent_Black, "Assets/Images/Meeting/checkbox.png",
                                           35, 35, 255)
        self.emerg_yellow_checkbox = Button(self, None, None, 35, 35, WIDTH / 1.5 - 30, 276, "chkbox_yellow_btn",
                                            Transparent_Black, Transparent_Black, "Assets/Images/Meeting/checkbox.png",
                                            35, 35, 255)
        self.emerg_blue_checkbox = Button(self, None, None, 35, 35, WIDTH / 2 - 95, 329, "chkbox_blue_btn",
                                          Transparent_Black, Transparent_Black, "Assets/Images/Meeting/checkbox.png",
                                          35, 35, 255)
        self.open_cafe_comp_check_btn = Button(self, None, None, 189, 191, WIDTH / 3 + 110, 200, "cafe_comp_check_btn",
                                               Transparent_Black,
                                               Transparent_Black,
                                               "Assets/Images/Tasks/Become Imposter/cafe_computer_check.png", 189, 191,
                                               255)

        self.open_cafe_comp_close_btn = Button(self, None, None, 65, 65, WIDTH / 1.5 + 80, 40, "cafe_comp_close_btn",
                                               Transparent_Black,
                                               Transparent_Black,
                                               "Assets/Images/Tasks/Become Imposter/close.png", 65, 65,
                                               255)
        self.garbage_liver_Up = Button(self, None, None, 64, 64, WIDTH / 1.5 - 80, HEIGHT / 2 - 80, "grbg_up_btn",
                                       Transparent_Black,
                                       Transparent_Black,
                                       "Assets/Images/Tasks/Empty Garbage/liver_up.png", 64, 64,
                                       255)
        self.garbage_liver_Down = Button(self, None, None, 64, 64, WIDTH / 1.5 - 80, HEIGHT / 2 - 50,
                                         "grbg_down_btn", Transparent_Black,
                                         Transparent_Black,
                                         "Assets/Images/Tasks/Empty Garbage/liver_down.png", 64, 64,
                                         255)
        self.empty_garbage_close_btn = Button(self, None, None, 65, 65, WIDTH / 1.5 + 80, 40, "grbg_close_btn",
                                              Transparent_Black, Transparent_Black,
                                              "Assets/Images/Tasks/Empty Garbage/close.png", 65, 65,
                                              255)
        self.reboot_wifi_liver = Button(self, None, None, 63, 45, WIDTH / 2 + 61, 187, "rbt_wifi_liver_btn",
                                        Transparent_Black, Transparent_Black,
                                        "Assets/Images/Tasks/Reboot Wifi/panel_wifi-lever.png", 63, 45, 255)
        self.reboot_wifi_close_btn = Button(self, None, None, 65, 65, WIDTH / 1.5 + 80, 40, "rbt_wifi_liver_btn",
                                            Transparent_Black, Transparent_Black,
                                            "Assets/Images/Tasks/Reboot Wifi/close.png", 65, 65, 255)
        self.electricity_wire_close_btn = Button(self, None, None, 65, 65, WIDTH / 1.5 + 80, 40,
                                                 "elec_wire_close_btn",
                                                 Transparent_Black, Transparent_Black,
                                                 "Assets/Images/Tasks/Fix Wiring/close.png", 65, 65,
                                                 255)
        self.electricity_wire_red_btn = Button(self, None, None, 91, 26, WIDTH / 1.5 - 63, 185, "elec_wire_red_btn",
                                               Transparent_Black, Transparent_Black,
                                               "Assets/Images/Tasks/Fix Wiring/electricity_wire_btn.png", 91, 26,
                                               255)
        self.electricity_wire_blue_btn = Button(self, None, None, 91, 26, WIDTH / 1.5 - 63, 290,
                                                "elec_wire_blue_btn",
                                                Transparent_Black, Transparent_Black,
                                                "Assets/Images/Tasks/Fix Wiring/electricity_wire_btn.png", 91, 26,
                                                255)
        self.electricity_wire_yellow_btn = Button(self, None, None, 91, 26, WIDTH / 1.5 - 63, 400,
                                                  "elec_wire_yellow_btn",
                                                  Transparent_Black, Transparent_Black,
                                                  "Assets/Images/Tasks/Fix Wiring/electricity_wire_btn.png", 91, 26,
                                                  255)
        self.electricity_wire_pink_btn = Button(self, None, None, 91, 26, WIDTH / 1.5 - 63, 505,
                                                "elec_wire_pink_btn",
                                                Transparent_Black, Transparent_Black,
                                                "Assets/Images/Tasks/Fix Wiring/electricity_wire_btn.png", 91, 26,
                                                255)
        self.divert_power_to_reactor_livers_btn = Button(self, None, None, 423, 36, WIDTH / 3 - 7, 500,
                                                         "dvrt_pwr_lvrs_btn",
                                                         Transparent_Black, Transparent_Black,
                                                         "Assets/Images/Tasks/Divert Power/electricity_divert_btn.png",
                                                         423, 36,
                                                         255)
        self.divert_power_to_reactor_close_btn = Button(self, None, None, 65, 65, WIDTH / 1.5 + 80, 40,
                                                        "dvrt_pwr_close_btn",
                                                        Transparent_Black, Transparent_Black,
                                                        "Assets/Images/Tasks/Divert Power/close.png", 65, 65,
                                                        255)
        self.view_security_monitor_close_btn = Button(self, None, None, 65, 65, WIDTH / 1.5 + 140, 30,
                                                      "elec_wire_close_btn",
                                                      Transparent_Black, Transparent_Black,
                                                      "Assets/Images/UI/close.png", 65, 65,
                                                      255)
        self.align_engine_liver_pos_btn1 = Button(self, None, None, 9, 8, WIDTH / 2 + 156, 213, "liver_pos1_btn",
                                                  Transparent_Black,
                                                  Transparent_Black,
                                                  "Assets/Images/Tasks/Align Engine Output/alignment_position.png",
                                                  9, 8, 255)
        self.align_engine_liver_pos_btn2 = Button(self, None, None, 9, 8, WIDTH / 2 + 144, 302, "liver_pos1_btn",
                                                  Transparent_Black,
                                                  Transparent_Black,
                                                  "Assets/Images/Tasks/Align Engine Output/alignment_position.png",
                                                  9, 8, 255)
        self.align_engine_output_close_btn = Button(self, None, None, 65, 65, WIDTH / 1.5 + 80, 40,
                                                    "alg_engn_op_close_btn",
                                                    Transparent_Black,
                                                    Transparent_Black,
                                                    "Assets/Images/Tasks/Align Engine Output/close.png", 65, 65,
                                                    255)
        self.fuel_engine_fill_btn = Button(self, None, None, 76, 77, WIDTH / 1.5 - 45, 467,
                                           "alg_engn_op_close_btn",
                                           Transparent_Black,
                                           Transparent_Black,
                                           "Assets/Images/Tasks/Fuel Engines/engineFuel_Button.png", 76, 77,
                                           255)
        self.fuel_engine_close_btn = Button(self, None, None, 65, 65, WIDTH / 1.5 - 10, 70,
                                                    "alg_engn_op_close_btn",
                                                    Transparent_Black,
                                                    Transparent_Black,
                                                    "Assets/Images/Tasks/Fuel Engines/close.png", 65, 65,
                                                    255)
        self.fuel_engine_close_btn2 = Button(self, None, None, 65, 65, WIDTH / 1.5 - 10, 70,
                                                    "alg_engn_op_close_btn",
                                                    Transparent_Black,
                                                    Transparent_Black,
                                                    "Assets/Images/Tasks/Fuel Engines/close.png", 65, 65,
                                                    255)


        """ DIFFERENT BUTTONS FOR DIFFERENT TASKS - CLOSE HERE"""

        # Load Fonts
        self.font = FONT

        # Light Effects__________________________
        self.fog = pg.Surface((WIDTH, HEIGHT))
        self.fog.fill(NIGHT_COLOR)
        self.light_mask = pg.image.load(path.join(self.Environment_folder, LIGHT_MASK)).convert_alpha()
        self.light_mask = pg.transform.scale(self.light_mask, LIGHT_RADIUS)  # LIGHT_RADIUS = (500, 500)
        self.fog_reactor = pg.Surface((WIDTH, HEIGHT))
        self.fog_reactor.fill(NIGHT_COLOR_REACTOR)
        self.light_mask_reactor = pg.image.load(path.join(self.Environment_folder, LIGHT_MASK_REACTOR)).convert_alpha()
        self.light_mask_reactor = pg.transform.scale(self.light_mask_reactor,
                                                     LIGHT_RADIUS_REACTOR).convert_alpha()  # LIGHT_RADIUS = (500, 500)

        # Make rectangle so that we can easily placed them anywhere on screen
        # We only make rectangle of the image that we load into light_mask
        # Round circle of light when light is off
        self.light_rect = self.light_mask.get_rect()
        # Round circle of light when light is red
        self.light_rect_reactor = self.light_mask_reactor.get_rect()
        # special flags = pygame flags to draw pixels on other pixels
        self.screen.blit(self.fog, (0, 0), special_flags=pg.BLEND_MULT)
        self.screen.blit(self.fog_reactor, (0, 0), special_flags=pg.BLEND_MULT)

        # ITEMS LOADING___________________________
        self.item_images = {}
        for item in ITEM_IMAGES:
            self.item_images[item] = pg.image.load(path.join(self.items_img_folder, ITEM_IMAGES[item])).convert_alpha()
            # scale up all item's images that store in dictionary
            self.item_images[item] = pg.transform.scale(self.item_images[item], (48, 48))
            if item == 'vent':
                self.item_images[item] = pg.transform.scale(self.item_images[item], (64, 48))
            if item == 'emerg_btn':
                self.item_images[item] = pg.transform.scale(self.item_images[item], (250, 250))

        # CLEAR ASTEROID TASK LOADING -----------------------------------------
        # Asteroid images loading
        self.asteroid_images = []
        for image in CLEAR_ASTEROIDS_IMAGES:
            self.asteroid_images.append(pg.image.load(image).convert_alpha())

        self.screen_width = 700
        self.screen_height = 600

        # Player image
        self.starship_image = pg.image.load("Assets/Images/Tasks/Clear Asteroids/starship.png").convert_alpha()
        self.starship_image = pg.transform.smoothscale(self.starship_image, (96, 96)).convert_alpha()
        self.starship_image2 = pg.image.load("Assets/Images/Tasks/Clear Asteroids/starship2.png").convert_alpha()
        self.starship_image2 = pg.transform.smoothscale(self.starship_image2, (96, 96)).convert_alpha()
        self.starship_image3 = pg.image.load("Assets/Images/Tasks/Clear Asteroids/starship3.png").convert_alpha()
        self.starship_image3 = pg.transform.smoothscale(self.starship_image3, (96, 96)).convert_alpha()
        self.starship_image_alignment = "middle"
        self.starship_posX = 370
        self.starship_posY = 550
        self.starship_posX_change = 0
        self.starship_posY_change = 0

        # Enemy image
        self.asteroid_image = []
        self.asteroid_posX = []
        self.asteroid_posY = []
        self.asteroid_posX_change = 0.5
        self.asteroid_posY_change = 1
        self.num_of_asteroids = 10
        self.total_num_of_asteroids = 30
        self.increment_in_missions = 1
        self.asteroid_kill_count = 0
        self.asteroid_mov = "right"

        # randomly select asteroid image from self.asteroid_images array
        for i in range(self.num_of_asteroids):
            self.asteroid_image.append(random.choice(self.asteroid_images).convert_alpha())
            self.asteroid_posX.append(random.randint(50, 1200))
            self.asteroid_posY.append(random.randint(-200, -100))

        # Bullet
        # ready - you cant see the bullet on the screen
        # fire - the bullet moves towards enemy
        self.bullet_image = pg.image.load("Assets/Images/Tasks/Clear Asteroids/laser.png").convert_alpha()
        self.bulletX = 0
        self.bulletY = 550
        # self.bulletX_change = 20
        self.bulletY_change = 30
        self.bullet_state = "ready"

        # Background image
        self.clear_asteroid_background = pg.image.load("Assets/Images/Tasks/Clear Asteroids/space3.png").convert_alpha()

        self.bgX = 0
        self.bgY = 0

        # Background music
        self.asteroid_bg = mixer.Sound("Assets/Sounds/Clear Asteroids/AMB_Space.wav")
        # Bullet Sound
        self.bullet_sound = mixer.Sound("Assets/Sounds/Clear Asteroids/fire3.mp3")
        # Collision Sound
        self.collision_sound = mixer.Sound("Assets/Sounds/Clear Asteroids/explosion2.mp3")

        # Score Board
        self.score_box_img = pg.image.load("Assets/Images/Tasks/Clear Asteroids/score_box.png").convert_alpha()
        self.score_box_img = pg.transform.smoothscale(self.score_box_img, (250, 60)).convert_alpha()
        self.score_value = 30
        self.font = pg.font.Font("Assets/fonts/Hunger Games.ttf", 24)

        # Game Over Text
        self.game_over_font = pg.font.Font("Assets/fonts/Hunger Games.ttf", 64)
        # CLEAR ASTEROID TASK LOADING -------------------------------------------


        # SOUND LOADING __________________________
        pg.mixer.music.load(path.join(self.sound_folder, BG_MUSIC3))

        self.effect_sounds = {}
        # Load each sound from sound directory into EFFECTS_SOUNDS array
        for type in EFFECT_SOUNDS:
            self.effect_sounds[type] = pg.mixer.Sound(path.join(self.sound_folder, EFFECT_SOUNDS[type]))
        self.foot_sounds = {}
        self.foot_sounds['footsteps'] = []
        for i in FOOTSTEP_SOUNDS:
            self.foot_sounds['footsteps'].append(pg.mixer.Sound(path.join(self.sound_folder, i)))
        self.electric_shock_sounds = {}
        self.electric_shock_sounds['electric_shock'] = []
        for i in ELECTRIC_SHOCK_SOUNDS:
            self.electric_shock_sounds['electric_shock'].append(pg.mixer.Sound(path.join(self.sound_folder, i)))
        self.comms_radio_sounds = {}
        self.comms_radio_sounds['comms_radio'] = []
        for i in COMMS_RADIO_SOUNDS:
            self.comms_radio_sounds['comms_radio'].append(pg.mixer.Sound(path.join(self.sound_folder, i)))
        self.ambient_sounds = {}
        # Load each sound from sound directory into AMBIENT_SOUNDS array
        for type in AMBIENT_SOUNDS:
            self.ambient_sounds[type] = pg.mixer.Sound(path.join(self.sound_folder, AMBIENT_SOUNDS[type]))

    # THIS METHOD CREATES ALL OBJECTS, INSTANCES & VARIABLES
    # create sprites/ objects/ walls/ camera = all sprites
    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.LayeredUpdates()
        # self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.items = pg.sprite.Group()
        self.bots = pg.sprite.Group()
        self.players_server = pg.sprite.Group()

        # mini map player position indicator
        self.player_map_square = pg.Surface([3 * 5, 3 * 5], pg.SRCALPHA, 32)


        bot_colours_temp = self.bot_colours
        bot_colours_temp_current = None

        for tile_object in self.map.tmxdata.objects:
            obj_center = vec(tile_object.x + tile_object.width / 2, tile_object.y + tile_object.height / 2)
            # if tile_object.name == 'player':
            # Spawn obstacles
            if tile_object.name == 'walls':
                Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
                # Spawn tables
            if tile_object.name == 'tables':
                Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            if tile_object.name == 'props':
                Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            if tile_object.name == 'generator':
                Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            if tile_object.name == 'medbay_comp':
                Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            if tile_object.name == 'engines':
                Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            if tile_object.name == 'reactor':
                Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            if tile_object.name == 'security_room_comp':
                Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            if tile_object.name == 'admin_btn1':
                Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            if tile_object.name == 'admin_btn2':
                Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)

            if tile_object.name == 'bot1':
                bot_colours_temp_current = random.choice(bot_colours_temp)
                self.bot1 = Bot(self, tile_object.x, tile_object.y, "Left", "bot1", bot_colours_temp_current)
                bot_colours_temp.remove(bot_colours_temp_current)
            if tile_object.name == 'bot2':
                bot_colours_temp_current = random.choice(bot_colours_temp)
                self.bot2 = Bot(self, tile_object.x, tile_object.y, "Right", "bot2", bot_colours_temp_current)
                bot_colours_temp.remove(bot_colours_temp_current)
            if tile_object.name == 'bot3':
                bot_colours_temp_current = random.choice(bot_colours_temp)
                self.bot3 = Bot(self, tile_object.x, tile_object.y, "Down", "bot3", bot_colours_temp_current)
                bot_colours_temp.remove(bot_colours_temp_current)
            if tile_object.name == 'bot4':
                bot_colours_temp_current = random.choice(bot_colours_temp)
                self.bot4 = Bot(self, tile_object.x, tile_object.y, "Down", "bot4", bot_colours_temp_current)
                bot_colours_temp.remove(bot_colours_temp_current)
            if tile_object.name == 'bot5':
                bot_colours_temp_current = random.choice(bot_colours_temp)
                self.bot5 = Bot(self, tile_object.x, tile_object.y, "Right", "bot5", bot_colours_temp_current)
                bot_colours_temp.remove(bot_colours_temp_current)
            if tile_object.name == 'bot6':
                bot_colours_temp_current = random.choice(bot_colours_temp)
                self.bot6 = Bot(self, tile_object.x, tile_object.y, "Right", "bot6", bot_colours_temp_current)
                bot_colours_temp.remove(bot_colours_temp_current)
            if tile_object.name == 'bot7':
                bot_colours_temp_current = random.choice(bot_colours_temp)
                self.bot7 = Bot(self, tile_object.x, tile_object.y, "Up", "bot7", bot_colours_temp_current)
                bot_colours_temp.remove(bot_colours_temp_current)
            if tile_object.name == 'bot8':
                bot_colours_temp_current = random.choice(bot_colours_temp)
                self.bot8 = Bot(self, tile_object.x, tile_object.y, "Down", "bot8", bot_colours_temp_current)
                bot_colours_temp.remove(bot_colours_temp_current)
            if tile_object.name == 'bot9':
                bot_colours_temp_current = random.choice(bot_colours_temp)
                self.bot9 = Bot(self, tile_object.x, tile_object.y, "Right", "bot9", bot_colours_temp_current)
                bot_colours_temp.remove(bot_colours_temp_current)
            if tile_object.name == 'bot10':
                bot_colours_temp_current = random.choice(bot_colours_temp)
                self.bot10 = Bot(self, tile_object.x, tile_object.y, "Up", "bot10", bot_colours_temp_current)
                bot_colours_temp.remove(bot_colours_temp_current)

            # if tile object - heath exists in our dictionary
            # " health " is a key in dictionary " ITEM_IMAGES " which points to " health_pack.png "
            if tile_object.name in ['vent']:
                # Spawn item if tile is vent
                Item(self, obj_center, tile_object.name)
            if tile_object.name in ['emerg_btn']:
                # Spawn item if tile is emergency button
                Item(self, obj_center, tile_object.name)

        # Spawn camera / Create camera instance
        self.camera = Camera(self.map.width, self.map.height)
        self.draw_debug = False
        self.effect_sounds['start_game'].play()

    # CLEAR ASTEROIDS FUNCTIONS
    def show_score(self, x, y):
        self.screen.blit(self.score_box_img, (x, y))
        GAME_FONT = pg.font.Font(FONT, 20)
        self.score = GAME_FONT.render("Asteroids Left: " + str(self.score_value), True, BLACK)
        self.screen.blit(self.score, (x+30, y+10))

    def display_starship(self, x, y, alignment):
        if alignment == "middle":
            self.screen.blit(self.starship_image, (self.starship_posX, self.starship_posY))
        if alignment == "left":
            self.screen.blit(self.starship_image3, (self.starship_posX, self.starship_posY))
        if alignment == "right":
            self.screen.blit(self.starship_image2, (self.starship_posX, self.starship_posY))
    def display_clear_asteroids_window(self):
        self.screen.blit(self.clear_asteroid_background, (0, 0))

    def display_asteroid(self,x, y, i):
        self.screen.blit(self.asteroid_image[i], (x, y))

    def fire_bullet(self, x, y):
        self.bullet_state = "fire"
        self.screen.blit(self.bullet_image, (x+15,y+10))

    def isCollision(self, asteroid_posX, asteroid_posY, bulletX, bulletY, i):
        # this is the distance formula
        asteroid_radius = self.asteroid_image[i].get_rect().center[0]
        bullet_radius = self.bullet_image.get_rect().center[0]
        colliding_perimeter = asteroid_radius + bullet_radius

        # Distance formula
        # 50 is added in order to perfect the horizontal collision
        # 27 for vertical collision with asteroid
        # asteroid and bullet
        distance = math.sqrt((math.pow(asteroid_posX - bulletX + 50, 2)) + (math.pow(asteroid_posY - bulletY + 27, 2)))
        # this distance is the distance from asteroid center i.e 75 pixels
        # if bullet is in between this distance then consider it a hit and
        # destroy the asteroid
        if distance <= colliding_perimeter and self.bullet_state == "fire":
            self.asteroid_kill_count += 1
            return True
        else:
            return False

    # THIS METHOD DRAWS EMERGENCY FLASH MESSAGE ON SCREEN
    """ VOTE """
    def display_meeting_alert(self):
        self.screen.blit(eval(self.emergency_img_sync), (0, 0))

    # More Task displays
    def display_open_cafe_comp_window(self):
        self.screen.blit(self.cafe_comp_img, (WIDTH / 3 - 50, 70))

    def display_open_cafe_comp_check_window(self):
        self.screen.blit(self.cafe_comp_check_img, (WIDTH / 3 + 110, 200))

    def display_stablize_navigation_window(self):
        self.screen.blit(self.navigation_screen_img, (WIDTH / 3 - 50, 70))

    def display_full_garbage_window(self):
        self.screen.blit(self.full_garbage_screen_img, (WIDTH / 3 - 50, 70))

    def display_empty_garbage_window(self):
        self.screen.blit(self.empty_garbage_screen_img, (WIDTH / 3 - 50, 70))

    def display_reboot_wifi_window(self):
        self.screen.blit(self.reboot_wifi_screen_img, (WIDTH / 3, -100))

    def display_rebooted_wifi_window(self):
        self.screen.blit(self.wifi_on_img, (WIDTH / 3 + 56, 181))

    def display_reboot_wifi_liver_down(self):
        self.screen.blit(self.wifi_liver_down_img, (WIDTH / 2 + 61, 520))

    def display_electricity_wire_window(self):
        self.screen.blit(self.electricity_wire_img, (WIDTH / 3 - 45, 70))

    def display_electricity_red(self):
        self.screen.blit(self.electricity_wire_red_img, (WIDTH / 3 - 45, 140))

    def display_electricity_blue(self):
        self.screen.blit(self.electricity_wire_blue_img, (WIDTH / 3 - 45, 242))

    def display_electricity_yellow(self):
        self.screen.blit(self.electricity_wire_yellow_img, (WIDTH / 3 - 44, 348))

    def display_electricity_pink(self):
        self.screen.blit(self.electricity_wire_pink_img, (WIDTH / 3 - 43, 452))

    def display_divert_power_to_reactor_window(self):
        self.screen.blit(self.divert_power_to_reactor_window_img, (WIDTH / 3 - 45, 70))

    def display_divert_power_to_reactor_liverUp_window(self):
        self.screen.blit(self.divert_power_to_reactor_liverUp_window_img, (WIDTH / 3 - 7, 380))

    def display_power_diverted_to_reactor_window(self):
        self.screen.blit(self.power_diverted_to_reactor_window_img, (WIDTH / 3 - 5, 108))

    def display_meeting_alert_report(self):
        self.screen.blit(eval(self.emergency_img_sync_report), (0, 0))

    def display_align_engine_output_window(self):
        self.screen.blit(self.align_engine_output_window_img, (WIDTH / 3 - 45, 70))
    def display_align_engine_output_window2(self):
        self.screen.blit(self.align_engine_output_window2_img, (WIDTH / 3 +36, 127))
    def display_align_engine_output_window3(self):
        self.screen.blit(self.align_engine_output_window3_img, (WIDTH / 3 - 5, 210))
    def display_align_engine_output_window4(self):
        self.screen.blit(self.align_engine_output_window4_img, (WIDTH / 3 - 10, 228))
    def display_align_engine_liver(self, pos_x, pos_y):
        self.screen.blit(self.align_engine_liver_img, (pos_x, pos_y))

    def display_gas_can_picked(self):
        self.screen.blit(self.gas_can_img, (WIDTH - 640, HEIGHT-110))
    def display_fuel_engine_window(self):
        self.screen.blit(self.fuel_engine_window_img, (WIDTH / 3 - 45, 70))

    # UI BUTTON IMAGES
    def display_light_bulb_icon(self):
        self.screen.blit(self.light_bulb_icon, (WIDTH-160, HEIGHT-117))
    def display_light_bulb_icon_dim(self):
        self.screen.blit(self.light_bulb_icon_dim, (WIDTH - 160, HEIGHT - 117))
    def display_sabotage_icon(self):
        self.screen.blit(self.sabotage_icon, (WIDTH-280, HEIGHT-110))
    def display_sabotage_icon_dim(self):
        self.screen.blit(self.sabotage_icon_dim, (WIDTH-280, HEIGHT-110))
    def display_kill_icon(self):
        self.screen.blit(self.kill_icon, (WIDTH-400, HEIGHT-110))
    def display_kill_icon_dim(self):
        self.screen.blit(self.kill_icon_dim, (WIDTH-400, HEIGHT-110))
    def display_emergency_icon(self):
        self.screen.blit(self.emergency_icon, (WIDTH-540, HEIGHT-109))
    def display_emergency_icon_dim(self):
        self.screen.blit(self.emergency_icon_dim, (WIDTH-540, HEIGHT-109))

    # CHAT
    def display_chat(self):
        if self.player.alive_status:
            self.screen.blit(self.chat_img, (WIDTH / 3, HEIGHT / 7))
        else:
            self.screen.blit(self.chat_img_dead, (WIDTH / 3, HEIGHT / 7))

    def display_vote(self):
        if self.player.alive_status == True:
            self.screen.blit(self.vote_img, (WIDTH / 4 - 25, HEIGHT / 6))
            self.emerg_red_checkbox.draw_Image(self.screen)
            self.emerg_orange_checkbox.draw_Image(self.screen)
            self.emerg_green_checkbox.draw_Image(self.screen)
            self.emerg_yellow_checkbox.draw_Image(self.screen)
            self.emerg_blue_checkbox.draw_Image(self.screen)
            if self.emerg_vote_red_checkbox_tick_status:
                self.display_vote_tick(WIDTH / 2 - 94, 223)
            if self.emerg_vote_orange_checkbox_tick_status:
                self.display_vote_tick(WIDTH / 1.5 - 29, 223)
            if self.emerg_vote_green_checkbox_tick_status:
                self.display_vote_tick(WIDTH / 2 - 94, 276)
            if self.emerg_vote_yellow_checkbox_tick_status:
                self.display_vote_tick(WIDTH / 1.5 - 29, 276)
            if self.emerg_vote_blue_checkbox_tick_status:
                self.display_vote_tick(WIDTH / 2 - 94, 329)
        else:
            self.screen.blit(self.vote_img_dead, (WIDTH / 4 - 25, HEIGHT / 6))

    def display_vote_tick(self, x, y):
        self.screen.blit(self.vote_tick_img, (x, y))

    def display_deadbody_alert(self):
        pass

    def display_kill_victim_anim(self):
        self.screen.blit(self.kill_victim_anim_img[self.kill_victim_anim_index], (0, 0))

    def display_eject_alert(self, x):
        self.screen.blit(self.eject_screen_img, (0, 0))
        self.board.draw_ejected_text(self.eject_colour)
        self.screen.blit(eval(self.eject_img), (x, HEIGHT / 3))

    def draw_health(self):
        self.name_block = pg.Surface((20, 7))
        width = int(self.player.rect.width)
        self.health_bar = pg.Rect(0, 0, width, 7)
        font = pg.font.Font(FONT, 14)
        textsurface = font.render("tango", False, BLACK)
        # rect = text.get_rect()
        pg.draw.rect(self.player.image, WHITE, self.health_bar)
        # pg.draw.rect(text, WHITE, rect)
        # self.screen.blit(textsurface, (self.player.pos.x + 10, self.player.pos.y -10))


    def draw_text(self, text, font_name, size, color, x, y, align="topleft"):
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(**{align: (x, y)})
        self.map_img.blit(text_surface, text_rect)

    def display_imposter_among_us(self):
        self.imposter_among_us_img = pg.transform.smoothscale(self.imposter_among_us_img, (WIDTH, HEIGHT))
        self.screen.blit(self.imposter_among_us_img, (0, 0))

    # THIS METHOD RUNS THE GAME AND ITS MAIN FUNCTIONS IN LOOP

    def runfreeplay(self):
        # Game main loop - set self.playing = False to end the game
        # bg music
        mixer.music.play(-1)
        mixer.music.set_volume(0.7)

        self.player = Player(self, random.choice(self.player_pos), 0, True, self.player_colour)

        self.playing = True
        self.player.imposter = True

        for b in self.bots:
            if b.bot_colour == self.player_colour:
                b.kill()
                break

        self.imposter_among_us_status = False

        self.timer_start = pygame.time.get_ticks()
        self.killcooldown_start = pygame.time.get_ticks()
        self.sabotagecooldown_start = pygame.time.get_ticks()
        self.sabotagecriticaltimer_start = pygame.time.get_ticks()
        self.ventcooldown_start = pygame.time.get_ticks()
        self.meetingcooldown_start = pygame.time.get_ticks()
        self.start_ticks = pg.time.get_ticks()
        self.time_left = 20

        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            if self.paused == False:
                self.update()
            self.draw()

            self.killcooldown = pygame.time.get_ticks()
            self.sabotagecooldown = pygame.time.get_ticks()
            self.sabotagecriticaltimer = pygame.time.get_ticks()
            self.ventcooldown = pygame.time.get_ticks()
            self.meetingcooldown = pygame.time.get_ticks()
            self.timer = pygame.time.get_ticks()
            self.seconds = (pg.time.get_ticks() - self.start_ticks) / 1000
            self.sabotage_timer_visible_status = True

            # If missions are completed then win or loss display
            # For crew mate
            if self.missions_done == 8:
                pg.mixer.music.stop()  # turn off background music
                pg.mixer.Channel(0).stop()
                for m in self.foot_sounds['footsteps']:
                    m.stop()
                for m in self.effect_sounds.values():
                    m.stop()
                for m in self.electric_shock_sounds['electric_shock']:
                    m.stop()
                for m in self.comms_radio_sounds['comms_radio']:
                    m.stop()
                for m in self.ambient_sounds.values():
                    m.stop()
                self.effect_sounds["victory_crew"].play()
                self.menu.game_over(self.score_list, '')
                return
            # For imposter
            # if imposter kills all the bots or reactor meltdown sabotage timer equals to 0 then imposter wins
            elif self.bot_count == 0 or (self.sabotagecritical == True and (self.sabotagecriticaltimer - self.sabotagecriticaltimer_start) > 20000):
                pg.mixer.music.stop()  # turn off background music
                pg.mixer.Channel(0).stop()
                for m in self.foot_sounds['footsteps']:
                    m.stop()
                for m in self.effect_sounds.values():
                    m.stop()
                for m in self.electric_shock_sounds['electric_shock']:
                    m.stop()
                for m in self.comms_radio_sounds['comms_radio']:
                    m.stop()
                for m in self.ambient_sounds.values():
                    m.stop()
                self.effect_sounds["victory_imposter"].play()
                self.menu.game_over_imposter(self.score_list, '')
                return
            elif self.game_left:
                pg.mixer.music.stop()  # turn off background music
                pg.mixer.Channel(0).stop()
                for m in self.foot_sounds['footsteps']:
                    m.stop()
                for m in self.effect_sounds.values():
                    m.stop()
                for m in self.electric_shock_sounds['electric_shock']:
                    m.stop()
                for m in self.comms_radio_sounds['comms_radio']:
                    m.stop()
                for m in self.ambient_sounds.values():
                    m.stop()
                self.effect_sounds["game_left"].play()
                return

    def runmultiplayer(self):
        # Game main loop - set self.playing = False to end the game
        # bg music
        global ge
        mixer.music.play(-1)
        mixer.music.set_volume(0.7)

        # remove bots
        for b in self.bots:
            b.kill()
        self.bot_count = 0

        self.killcooldown_start = pygame.time.get_ticks()
        self.sabotagecooldown_start = pygame.time.get_ticks()
        self.sabotagecriticaltimer_start = pygame.time.get_ticks()
        self.ventcooldown_start = pygame.time.get_ticks()
        self.meetingcooldown_start = pygame.time.get_ticks()
        self.timer_start = pygame.time.get_ticks()


        # socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.serveraddress.strip(), 4321))

        # temp var to store dynamically generated id
        player_id = 0

        # dictionary that stores all connected players as objects, including local player. uses player id as key
        self.player = Player(self, random.choice(self.player_pos), 0, True, self.player_colour)
        self.Players = {}


        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            if self.paused == False:
                self.update()
            self.draw()

            self.killcooldown = pygame.time.get_ticks()
            self.sabotagecooldown = pygame.time.get_ticks()
            self.sabotagecriticaltimer = pygame.time.get_ticks()
            self.ventcooldown = pygame.time.get_ticks()
            self.meetingcooldown = pygame.time.get_ticks()
            self.timer = pygame.time.get_ticks()

            if (self.timer - self.timer_start) > 3000:
                self.imposter_among_us_status = False

            # update player tasks count for server
            self.player.tasks_completed = self.missions_done

            # server shit
            ins, outs, ex = select.select([s], [], [], 0)
            for inm in ins:
                # receiving data from server and storing in gameEvent
                # gameEvent = pickle.loads(inm.recv(BUFFERSIZE))
                try:
                    gameEvent = pickle.loads(inm.recv(BUFFERSIZE))
                except Exception:
                    print("yes exception")

                # if event is such that it contains below string
                if gameEvent[0] == 'id update':
                    # generate player id
                    player_id = gameEvent[1]
                    print(player_id)
                # if event is such that it contains below string
                if gameEvent[0] == 'player locations':
                    # remove the string
                    gameEvent.pop(0)
                    # iterating gameEvent
                    for p in gameEvent:
                        # case1, when local player is connected and needs to be appended to the dictionary
                        # check if player is not already in the dictionary, and if the player id created dynamically 
                        # previously in gameEvent 'id update' matches with the id received right now
                        # we don't want to add any random player as local player
                        if p[0] not in self.Players.keys() and p[0] == player_id:
                            # update previously created player object id with the id created dynamically by the server
                            self.player.player_id = p[0]
                            # updating local player selected colour on the server
                            self.Players[p[0]] = self.player
                            # just to check if previously created id and newly assigned id match up
                            print(self.Players[p[0]].player_id)
                        # case2, when a new server side player wants to join, and we want to store a copy of the object locally
                        # check if player is not already in the list
                        if p[0] not in self.Players.keys():
                            # jugaad to fix colour inconsistency
                            if p[10] != None:
                                # create new player object
                                self.Players[p[0]] = Player(self, (p[1], p[2]), p[0], False, p[10])
                                self.server_players_connected += 1
                                self.server_player_alive += 1

                        # case3, when player is already in the list and data needs to be received locally from the server
                        # check if player is already in the list and that player is not local player, since we do not want to receive
                        # data for our local player, only send it
                        elif p[0] in self.Players.keys() and p[0] != self.player.player_id:
                            # update shit
                            self.Players[p[0]].pos = vec(p[1], p[2])
                            self.Players[p[0]].alive_status = p[3]
                            self.Players[p[0]].sync_img = p[4]
                            self.Players[p[0]].sync_img_index = p[5]
                            self.Players[p[0]].image = eval(p[4] + p[5])
                            self.Players[p[0]].left_img_index = p[6]
                            self.Players[p[0]].right_img_index = p[7]
                            self.Players[p[0]].up_img_index = p[8]
                            self.Players[p[0]].down_img_index = p[9]
                            self.Players[p[0]].tasks_completed = p[11]
                            self.Players[p[0]].imposter = p[15]
                            self.Players[p[0]].voted = p[17]
                            self.Players[p[0]].got_votes = p[18]
                            self.Players[p[0]].emergency_meeting_img_sync = p[19]
                            self.Players[p[0]].emergency_meeting_img_sync_report = p[20]
                            self.Players[p[0]].victim_id_report = p[21]
                            self.Players[p[0]].got_reported = p[22]

                            if self.player.player_id == p[14] and self.player.alive_status == True:
                                self.player.alive_status = False
                                self.player.image = self.player.image_dead
                                self.player.sync_img = "self.Players[p[0]].image_dead"
                                self.player.sync_img_index = ""
                                self.player.pos_corpse.x = self.player.pos.x
                                self.player.pos_corpse.y = self.player.pos.y
                                self.kill_victim_anim = True
                                #self.isdoingTask = False
                                

                            # If Dead body of Ghost - victim is reported
                            if self.player.player_id == p[21] and self.player.alive_status == False and self.player.got_reported == False:
                                self.player.got_reported = True
                                self.emerg_meeting_report_status = 1
                                self.emergency = True
                                self.effect_sounds['dead_body_found'].play()
                                self.emergency_sync += 1
                                self.emergency_img_sync_report = self.player.emergency_meeting_img_sync_report
                                self.isdoingTask = False

                                # If some player from server reports dead body, meeting timer of
                                # 30 seconds will be displayed and decremented on voting screen but it does not
                                # decrements on ghost voting screen, the trick is to decrement meeting_timer_event
                                # when someone report dead body
                                self.time_left_to_end_meeting = 30
                                pg.time.set_timer(self.meeting_timer_event, 1000)
                                self.timer_start = pygame.time.get_ticks()

                            if self.player.victim_id != 0 and self.player.victim_id == p[0] and p[3] == False:
                                self.player.victim_id = 0

                            if self.player.victim_id_report != 0 and self.player.victim_id_report == p[0] and p[
                                22] == True:
                                self.player.victim_id_report = 0

                            # Night - Turn On/Off the lights
                            if self.night_sync < p[12]:
                                self.night_sync = p[12]
                                if self.night_sync % 2 != 0:
                                    self.night = True
                                elif self.night_sync % 2 == 0:
                                    self.night = False

                                    # if some other player from server turn on the light
                                    # then reset the light timer to 15 and again decrement
                                    # light_timer_event
                                    self.time_left_to_light = 15
                                    pygame.time.set_timer(self.light_timer_event, 1000)
                                    self.light_bulb_timer_icon_status = True

                                    # if some other player from server turn on the light
                                    # then reset the ractor cooldown timer and decrement
                                    # reactor_timer_cooldown_event
                                    self.time_left_to_boom_cooldown = 15
                                    pg.time.set_timer(self.reactor_timer_cooldown_event, 1000)

                                    self.sabotagecooldown_start = self.sabotagecooldown

                            # To Trigger Reactor meltdown Sabotage - Multiplayer Mode
                            # If reactor medltdown on and sync with other server players
                            # then show meltdown timer
                            if self.night_reactor_sync < p[13]:
                                self.night_reactor_sync = p[13]
                                if self.night_reactor_sync % 2 != 0:
                                    self.night_reactor = True
                                    self.sabotagecritical = True
                                    self.reactor_timer_visible_client_status = True
                                    pg.time.set_timer(self.reactor_timer_event_client, 1000)
                                    self.sabotagecriticaltimer_start = pygame.time.get_ticks()

                                # If crew mates turn on reactor then show reactor sabotage cooldown
                                # timer + sabotage_icon on imposter window
                                elif self.night_reactor_sync % 2 == 0:
                                    self.time_left_to_boom_cooldown = 15
                                    pg.time.set_timer(self.reactor_timer_cooldown_event, 1000)
                                    self.night_reactor = False

                                    #if player turn on the reactor then also reset the light timer
                                    # and decrement light_timer_event
                                    self.time_left_to_light = 15
                                    pygame.time.set_timer(self.light_timer_event, 1000)
                                    self.light_bulb_timer_icon_status = True

                                    self.sabotagecooldown_start = self.sabotagecooldown
                                    self.sabotagecritical = False
                                    pygame.mixer.Channel(0).stop()

                            # Emergency Meeting called from server player
                            # connected to the server
                            if self.emergency_sync < p[16] and p[19] != None:
                                self.emergency_sync = p[16]
                                self.emerg_meeting_button_status = 1
                                self.emergency = True
                                self.effect_sounds['emergency_alarm'].play()
                                self.emergency_img_sync = p[19]
                                self.isdoingTask = False

                                # If some player from server starts meeting then show
                                # meeting timer of 30 seconds on each client connected
                                # on server and decrement meeting_timer_event
                                self.time_left_to_end_meeting = 30
                                pg.time.set_timer(self.meeting_timer_event, 1000)

                                # If some player from server starts meeting then hide
                                # meeting highlighted icon and meeting cooldown timer of 15 sec
                                # and when meeting is over decrement meeting_timer_cooldown_event
                                # for other client connected to the server
                                self.emergency_timer_icon_status = False
                                self.time_left_to_end_meeting_cooldown = 15
                                self.meeting_timer_cooldown_visible_status = False
                                pg.time.set_timer(self.meeting_timer_cooldown_event, 1000)

                                if self.invisible_play_count == 1:
                                    self.player.image = self.player.player_imgs_down[0]
                                    self.player.sync_img = "self.Players[p[0]].player_imgs_down"
                                    self.player.sync_img_index = "[0]"
                                    self.invisible_play_count = 0
                                self.timer_start = pygame.time.get_ticks()


                            # Report Dead Body - Emergency Meeting called from server player
                            # connected to the server
                            if self.emergency_sync < p[16] and p[20] != None:
                                self.emergency_sync = p[16]
                                self.emerg_meeting_report_status = 1
                                self.emergency = True
                                self.effect_sounds['dead_body_found'].play()
                                self.emergency_img_sync_report = p[20]
                                self.isdoingTask = False

                                # If some player from server reports dead body, meeting timer of
                                # 30 seconds will be displayed and decremented on voting screen but it does not
                                # decrements on ghost voting screen, the trick is to decrement meeting_timer_event
                                # when someone report dead body
                                pg.time.set_timer(self.meeting_timer_event, 1000)


                                # If some player from server reports dead body then hide
                                # meeting highlighted icon and meeting cooldown timer of 15 sec
                                # and when meeting is over decrement meeting_timer_cooldown_event
                                # for other client connected to the server
                                self.emergency_timer_icon_status = False
                                self.time_left_to_end_meeting_cooldown = 15
                                self.meeting_timer_cooldown_visible_status = False
                                pg.time.set_timer(self.meeting_timer_cooldown_event, 1000)

                                if self.invisible_play_count == 1:
                                    self.player.image = self.player.player_imgs_down[0]
                                    self.player.sync_img = "self.Players[p[0]].player_imgs_down"
                                    self.player.sync_img_index = "[0]"
                                    self.invisible_play_count = 0
                                self.timer_start = pygame.time.get_ticks()

                            # Eject Player
                            if self.eject_sync < p[23] and p[24] != None and (
                                    self.emerg_meeting_report_status == 1 or self.emerg_meeting_button_status == 1) and self.emergency == True:
                                self.eject_sync = p[23]
                                self.eject = True
                                self.eject_img = p[24]
                                self.eject_colour = p[10]
                                self.timer_start = pygame.time.get_ticks()

                            # Votes and Eject
                            if self.player.player_colour == p[17] and self.player.alive_status == True and p[0] not in self.voters:
                                self.player.got_votes += 1
                                self.voters.append(p[0])
                            # If player got equal or more than specified votes then eject him
                            if self.player.got_votes >= 2 and self.player.alive_status == True and (
                                    self.emerg_meeting_report_status == 1 or self.emerg_meeting_button_status == 1) and self.emergency == True:
                                self.player.alive_status = False
                                self.player.got_reported == True
                                self.player.image = self.invsible_player_image
                                self.eject_colour = self.player.player_colour
                                self.eject = True
                                self.eject_sync += 1
                                self.eject_img = self.player.eject_img
                                self.timer_start = pygame.time.get_ticks()

                            if p[0] > self.player_highest_id:
                                self.player_highest_id = p[0]
                            if self.player.player_id > self.player_highest_id and self.player.imposter == False:
                                print("yes")
                                self.player_highest_id = self.player.player_id
                                self.player.imposter = True
                            elif self.player.player_id < self.player_highest_id and self.player.imposter == True:
                                print("no")
                                self.player.imposter = False

            # now after receiving data from the server, time to send data to the server
            # update local player object in the list
            self.Players[self.player.player_id] = self.player
            if self.player.alive_status:
                ge = ['position update', player_id, self.player.pos.x, self.player.pos.y, self.player.alive_status,
                      self.player.sync_img, self.player.sync_img_index, self.player.left_img_index,
                      self.player.right_img_index, self.player.up_img_index, self.player.down_img_index,
                      self.player.player_colour, self.player.tasks_completed, self.night_sync, self.night_reactor_sync,
                      self.player.victim_id, self.player.imposter, self.emergency_sync, self.player.voted,
                      self.player.got_votes, self.emergency_img_sync, self.emergency_img_sync_report,
                      self.player.victim_id_report, self.player.got_reported, self.eject_sync, self.eject_img]
            elif self.player.alive_status == False and self.player.got_reported == False:
                ge = ['position update', player_id, self.player.pos_corpse.x, self.player.pos_corpse.y,
                      self.player.alive_status, self.player.pos_corpse_img, self.player.pos_corpse_img_index, 0, 0, 0,
                      0, self.player.player_colour, self.player.tasks_completed, self.night_sync,
                      self.night_reactor_sync, 0, self.player.imposter, self.emergency_sync, None, 0, None,
                      self.emergency_img_sync_report, 0, self.player.got_reported, self.eject_sync, self.eject_img]
            elif self.player.alive_status == False and self.player.got_reported == True:
                ge = ['position update', player_id, self.player.pos_corpse.x, self.player.pos_corpse.y,
                      self.player.alive_status, self.player.ghost_img, self.player.ghost_img_index, 0, 0, 0, 0,
                      self.player.player_colour, self.player.tasks_completed, self.night_sync, self.night_reactor_sync,
                      0, self.player.imposter, self.emergency_sync, None, 0, None, self.emergency_img_sync_report, 0,
                      self.player.got_reported, self.eject_sync, self.eject_img]

            # Add try exception block here
            #s.send(pickle.dumps(ge))

            try:
               s.send(pickle.dumps(ge))
            except Exception:
               print("very exception")

            # check for game end condition
            if len(self.Players) > 1:
                # For crew mate
                for p in self.Players.values():
                    if p.tasks_completed < 8 and p.imposter == False:
                        break
                else:
                    pg.mixer.music.stop()  # turn off background music
                    pg.mixer.Channel(0).stop()
                    for m in self.foot_sounds['footsteps']:
                        m.stop()
                    for m in self.effect_sounds.values():
                        m.stop()
                    for m in self.electric_shock_sounds['electric_shock']:
                        m.stop()
                    for m in self.comms_radio_sounds['comms_radio']:
                        m.stop()
                    for m in self.ambient_sounds.values():
                        m.stop()
                    self.effect_sounds["victory_crew"].play()
                    self.menu.game_over(self.score_list, '')
                    return
                # When imposter is ejecting
                for p in self.Players.values():
                    if p.alive_status == False and p.imposter == True and self.emergency == False:
                        pg.mixer.music.stop()  # turn off background music
                        pg.mixer.Channel(0).stop()
                        for m in self.foot_sounds['footsteps']:
                            m.stop()
                        for m in self.effect_sounds.values():
                            m.stop()
                        for m in self.electric_shock_sounds['electric_shock']:
                            m.stop()
                        for m in self.comms_radio_sounds['comms_radio']:
                            m.stop()
                        for m in self.ambient_sounds.values():
                            m.stop()
                        self.effect_sounds["victory_crew"].play()
                        # self.effect_sounds["victory_imposter"].play()
                        self.menu.game_over(self.score_list, '')
                        return

                # When imposter kills all players
                for p in self.Players.values():
                    if p.alive_status == True and p.imposter == False:
                        break
                else:
                    pass
                    if self.emergency == False and self.kill_victim_anim == False:
                        pg.mixer.music.stop()  # turn off background music
                        pg.mixer.Channel(0).stop()
                        for m in self.foot_sounds['footsteps']:
                            m.stop()
                        for m in self.effect_sounds.values():
                            m.stop()
                        for m in self.electric_shock_sounds['electric_shock']:
                            m.stop()
                        for m in self.comms_radio_sounds['comms_radio']:
                            m.stop()
                        for m in self.ambient_sounds.values():
                            m.stop()
                        self.effect_sounds["victory_imposter"].play()
                        self.menu.game_over_imposter(self.score_list, '')
                        return
                # For imposter - Critical Sabotage
                if self.sabotagecritical == True and (
                        self.sabotagecriticaltimer - self.sabotagecriticaltimer_start) > 20000:
                    pg.mixer.music.stop()  # turn off background music
                    pg.mixer.Channel(0).stop()
                    for m in self.foot_sounds['footsteps']:
                        m.stop()
                    for m in self.effect_sounds.values():
                        m.stop()
                    for m in self.electric_shock_sounds['electric_shock']:
                        m.stop()
                    for m in self.comms_radio_sounds['comms_radio']:
                        m.stop()
                    for m in self.ambient_sounds.values():
                        m.stop()
                    self.effect_sounds["victory_imposter"].play()
                    self.menu.game_over_imposter(self.score_list, '')
                    return



    # THIS METHOD QUITS THE GAME
    def quit(self):
        pg.quit()
        sys.exit()

    # THIS METHOD UPDATES ALL WE SEE & HEAR ON SCREEN CONTINUOUSLY

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()


        # Update camera in every loop
        # Flexibility provided by camera
        # Can use any sprite in place of player and camera will follow that sprite
        # Also camera will jump to any spawn location of player we set on map.txt file
        self.camera.update(self.player)

        hits = pg.sprite.spritecollide(self.player, self.items, False)
        """Player hits Item--------------------------"""
        #self.tasks.turn_on_the_lights()

        # Make player invisible on key press E (HIDE IN VENT)
        for hit in hits:
            if hit.type == 'vent':
                keys = pg.key.get_pressed()
                if keys[pg.K_SPACE]:
                    if self.invisible_play_count == 0 and self.player.imposter == True and self.player.alive_status == True and (
                            self.ventcooldown - self.ventcooldown_start) > 500 and self.emergency == False:
                        self.player.image = self.invsible_player_image
                        self.player.sync_img = "self.invsible_player_image"
                        self.player.sync_img_index = ""
                        self.effect_sounds['vent'].play()
                        self.invisible_play_count = 1
                        self.ventcooldown_start = pygame.time.get_ticks()
                        # self.invisibility_sound_playing = True
                    elif self.invisible_play_count == 1 and (self.ventcooldown - self.ventcooldown_start) > 500:
                        self.player.image = self.player.player_imgs_down[0]
                        self.player.sync_img = "self.player.player_imgs_down"
                        self.player.sync_img_index = "[0]"
                        self.effect_sounds['vent'].play()
                        self.invisible_play_count = 0
                        self.ventcooldown_start = self.ventcooldown

                if keys[pg.K_LALT] or keys[pg.K_RALT]:
                    if (
                            self.ventcooldown - self.ventcooldown_start) > 750 and self.invisible_play_count == 1 and self.player.imposter == True:
                        self.player.pos = vec(random.choice(self.vent))
                        self.effect_sounds['invisible'].play()
                        self.ventcooldown_start = self.ventcooldown


        hitz = pg.sprite.spritecollide(self.player, self.bots, False)
        for hit in hitz:
            if hit.type == 'bot1':
                keys = pg.key.get_pressed()
                if keys[pg.K_RETURN]:
                    if self.bot1.play_kill_count < 1 and self.bot1.alive_status and self.invisible_play_count == 0 and self.player.imposter:
                        if (self.killcooldown - self.killcooldown_start) > 15000:
                            self.effect_sounds['imposter_kill_sound'].play()
                            self.bot1.image = self.bot1.dead_player_img
                            self.bot_killed += 1
                            self.bot_count -= 1
                            self.bot1.alive_status = False
                            self.bot1.play_kill_count += 1
                            self.kill_timer_icon_status = True
                            # if time taken to cooldown for kill > 15, i.e time_to_kill = 0, means that now we can kill a bot, then again
                            # reset time_left_to_kill to 15 that will show time interval after, which we can again kill a bot.
                            self.time_left_to_kill = 15
                            # This is line that starts the time_event (USER EVENT) to display after time interval of
                            # 1 sec
                            pygame.time.set_timer(self.kill_timer_event, 1000)
                            self.killcooldown_start = self.killcooldown
                        else:
                            #self.kill_timer_icon_dim_status = False
                            self.kill_timer_icon_status = False
                            self.effect_sounds['imposter_kill_cooldown_sound'].play()


            if hit.type == 'bot2':
                keys = pg.key.get_pressed()
                if keys[pg.K_RETURN]:
                    if self.bot2.play_kill_count < 1 and self.bot2.alive_status and self.invisible_play_count == 0 and self.player.imposter:
                        if (self.killcooldown - self.killcooldown_start) > 15000:
                            self.bot2.alive_status = False
                            self.effect_sounds['imposter_kill_sound'].play()
                            self.bot2.image = self.bot2.dead_player_img
                            self.bot2.play_kill_count += 1
                            self.bot_killed += 1
                            self.bot_count -= 1
                            self.time_left_to_kill = 15
                            pygame.time.set_timer(self.kill_timer_event, 1000)
                            self.killcooldown_start = self.killcooldown
                        else:
                            self.effect_sounds['imposter_kill_cooldown_sound'].play()

            if hit.type == 'bot3':
                keys = pg.key.get_pressed()
                if keys[pg.K_RETURN]:
                    if self.bot3.play_kill_count < 1 and self.bot3.alive_status and self.invisible_play_count == 0 and self.player.imposter:
                        if (self.killcooldown - self.killcooldown_start) > 15000:
                            self.bot3.alive_status = False
                            self.effect_sounds['imposter_kill_sound'].play()
                            self.bot3.image = self.bot3.dead_player_img
                            self.bot3.play_kill_count += 1
                            self.bot_killed += 1
                            self.bot_count -= 1
                            self.time_left_to_kill = 15
                            pygame.time.set_timer(self.kill_timer_event, 1000)
                            self.killcooldown_start = self.killcooldown
                        else:
                            self.effect_sounds['imposter_kill_cooldown_sound'].play()

            if hit.type == 'bot4':
                keys = pg.key.get_pressed()
                if keys[pg.K_RETURN]:
                    if self.bot4.play_kill_count < 1 and self.bot4.alive_status and self.invisible_play_count == 0 and self.player.imposter:
                        if (self.killcooldown - self.killcooldown_start) > 15000:
                            self.bot4.alive_status = False
                            self.effect_sounds['imposter_kill_sound'].play()
                            self.bot4.image = self.bot4.dead_player_img
                            self.bot4.play_kill_count += 1
                            self.bot_killed += 1
                            self.bot_count -= 1
                            self.time_left_to_kill = 15
                            pygame.time.set_timer(self.kill_timer_event, 1000)
                            self.killcooldown_start = self.killcooldown
                        else:
                            self.effect_sounds['imposter_kill_cooldown_sound'].play()

            if hit.type == 'bot5':
                keys = pg.key.get_pressed()
                if keys[pg.K_RETURN]:
                    if self.bot5.play_kill_count < 1 and self.bot5.alive_status and self.invisible_play_count == 0 and self.player.imposter:
                        if (self.killcooldown - self.killcooldown_start) > 15000:
                            self.bot5.alive_status = False
                            self.effect_sounds['imposter_kill_sound'].play()
                            self.bot5.image = self.bot5.dead_player_img
                            self.bot5.play_kill_count += 1
                            self.bot_killed += 1
                            self.bot_count -= 1
                            self.time_left_to_kill = 15
                            pygame.time.set_timer(self.kill_timer_event, 1000)
                            self.killcooldown_start = self.killcooldown
                        else:
                            self.effect_sounds['imposter_kill_cooldown_sound'].play()

            if hit.type == 'bot6':
                keys = pg.key.get_pressed()
                if keys[pg.K_RETURN]:
                    if self.bot6.play_kill_count < 1 and self.bot6.alive_status and self.invisible_play_count == 0 and self.player.imposter:
                        if (self.killcooldown - self.killcooldown_start) > 15000:
                            self.effect_sounds['imposter_kill_sound'].play()
                            self.bot6.image = self.bot6.dead_player_img
                            self.bot_killed += 1
                            self.bot_count -= 1
                            self.bot6.alive_status = False
                            self.bot6.play_kill_count += 1
                            self.time_left_to_kill = 15
                            pygame.time.set_timer(self.kill_timer_event, 1000)
                            self.killcooldown_start = self.killcooldown
                        else:
                            self.effect_sounds['imposter_kill_cooldown_sound'].play()

            if hit.type == 'bot7':
                keys = pg.key.get_pressed()
                if keys[pg.K_RETURN]:
                    if self.bot7.play_kill_count < 1 and self.bot7.alive_status and self.invisible_play_count == 0 and self.player.imposter:
                        if (self.killcooldown - self.killcooldown_start) > 15000:
                            self.effect_sounds['imposter_kill_sound'].play()
                            self.bot7.image = self.bot7.dead_player_img
                            self.bot_killed += 1
                            self.bot_count -= 1
                            self.bot7.alive_status = False
                            self.bot7.play_kill_count += 1
                            self.time_left_to_kill = 15
                            pygame.time.set_timer(self.kill_timer_event, 1000)
                            self.killcooldown_start = self.killcooldown
                        else:
                            self.effect_sounds['imposter_kill_cooldown_sound'].play()

            if hit.type == 'bot8':
                keys = pg.key.get_pressed()
                if keys[pg.K_RETURN]:
                    if self.bot8.play_kill_count < 1 and self.bot8.alive_status and self.invisible_play_count == 0 and self.player.imposter:
                        if (self.killcooldown - self.killcooldown_start) > 15000:
                            self.effect_sounds['imposter_kill_sound'].play()
                            self.bot8.image = self.bot8.dead_player_img
                            self.bot_killed += 1
                            self.bot_count -= 1
                            # self.bot1.image.blit(dead_imgs[i], (0,0))
                            self.bot8.alive_status = False
                            self.bot8.play_kill_count += 1
                            self.time_left_to_kill = 15
                            pygame.time.set_timer(self.kill_timer_event, 1000)
                            self.killcooldown_start = self.killcooldown
                        else:
                            self.effect_sounds['imposter_kill_cooldown_sound'].play()

            if hit.type == 'bot9':
                keys = pg.key.get_pressed()
                if keys[pg.K_RETURN]:
                    if self.bot9.play_kill_count < 1 and self.bot9.alive_status and self.invisible_play_count == 0 and self.player.imposter:
                        if (self.killcooldown - self.killcooldown_start) > 15000:
                            self.effect_sounds['imposter_kill_sound'].play()
                            self.bot9.image = self.bot9.dead_player_img
                            self.bot_killed += 1
                            self.bot_count -= 1
                            self.bot9.alive_status = False
                            self.bot9.play_kill_count += 1
                            self.time_left_to_kill = 15
                            pygame.time.set_timer(self.kill_timer_event, 1000)
                            self.killcooldown_start = self.killcooldown
                        else:
                            self.effect_sounds['imposter_kill_cooldown_sound'].play()

            if hit.type == 'bot10':
                keys = pg.key.get_pressed()
                if keys[pg.K_RETURN]:
                    if self.bot10.play_kill_count < 1 and self.bot10.alive_status and self.invisible_play_count == 0 and self.player.imposter:
                        if (self.killcooldown - self.killcooldown_start) > 15000:
                            self.effect_sounds['imposter_kill_sound'].play()
                            self.bot10.image = self.bot10.dead_player_img
                            self.bot_killed += 1
                            self.bot_count -= 1
                            self.bot10.alive_status = False
                            self.bot10.play_kill_count += 1
                            self.time_left_to_kill = 15
                            pygame.time.set_timer(self.kill_timer_event, 1000)
                            self.killcooldown_start = self.killcooldown
                        else:
                            self.effect_sounds['imposter_kill_cooldown_sound'].play()

        # This section of code enables imposter to kill other server players
        # If imposter player hits other player picture or conceptual rectangle field
        # then kill that crew mate
        # THere is a delay of 15 seconds between killing a player
        hitp = pg.sprite.spritecollide(self.player, self.players_server, False)
        for hit in hitp:
            keys = pg.key.get_pressed()
            if keys[pg.K_RETURN]:
                if (self.killcooldown - self.killcooldown_start) > 15000 and hit.alive_status == True and self.player.imposter == True and self.invisible_play_count == 0 and self.emergency == False:
                    self.player.victim_id = hit.player_id
                    self.effect_sounds['imposter_kill_sound'].play()
                    self.server_player_killed += 1
                    self.server_player_alive -= 1

                    # if time taken to cooldown for kill > 15, i.e time_to_kill = 0, means that now we can kill a Player, then again
                    # reset time_left_to_kill to 15 so that when player hits K_space he shall be able to kill the player,
                    # time_left_to_kill = 15 shows time interval after, which we can again kill a Player.
                    self.time_left_to_kill = 15
                    # This is line that starts the kill_timer_event (USER EVENT) to display time after time interval of
                    # 1 sec
                    pygame.time.set_timer(self.kill_timer_event, 1000)

                    self.killcooldown_start = self.killcooldown
                elif (
                        self.killcooldown - self.killcooldown_start) > 2500 and hit.alive_status == False and self.sabotagecritical == False and self.player.alive_status == True and self.emergency == False:
                    self.player.victim_id_report = hit.player_id



        # Update mini map
        self.update_mini_map()

    # Change player position
    def update_mini_map(self):
        self.mini_map.blit(self.mini_map_img, (0, 0))
        # mini map player position indicator
        self.player_map_square.fill(self.player.player_colour)
        """self.mini_map.blit(player_map_square, (2*self.player.rect.x / 13, 2*self.player.rect.y / 13))"""
        self.mini_map.blit(self.player_map_square,
                           (int(3 * (self.player.rect.x / 15)), int(3 * (self.player.rect.y / 15))))



    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    # THIS METHOD DRAWS BLACK FOG ON SCREEN
    def render_fog(self):
        # Draw the light mask (gradient) onto fog image
        self.fog.fill(NIGHT_COLOR)
        self.light_rect.center = self.camera.apply(self.player).center
        self.fog.blit(self.light_mask, self.light_rect)
        self.screen.blit(self.fog, (0, 0), special_flags=pg.BLEND_MULT)

    # THIS METHOD DRAWS BLACK FOG ON SCREEN
    def render_fog_reactor(self):
        # Draw the light mask (gradient) onto fog image
        self.fog_reactor.fill(NIGHT_COLOR_REACTOR)
        self.screen.blit(self.fog_reactor, (0, 0), special_flags=pg.BLEND_MULT)

    # THIS METHOD DRAWS ALL WHAT WE SEE ON SCREEN
    def draw(self):
        FPS = self.clock.get_fps()
        pg.display.set_caption("Mutiplayer Game {:.2f}".format(FPS))
        # self.screen.fill(BGCOLOR)

        """ Player Camera is loaded 1st"""
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        # self.draw_grid()

        """ Sprites / Players / objects/ Items are loaded 2nd """
        # draw all sprites/sprite group on screen
        # Draw rectangle along all sprites/ tiles/ walls/ objects to debug
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
            # if debug button is ON (shows rectangle borders on sprite)
            if self.draw_debug:
                pg.draw.rect(self.screen, YELLOW, self.camera.apply_rect(sprite.hit_rect), 1)
            if self.draw_debug:
                for wall in self.walls:
                    pg.draw.rect(self.screen, YELLOW, self.camera.apply_rect(wall.rect), 1)
            if self.draw_debug:
                for x in range(0, WIDTH, TILESIZE):
                    pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
            if self.draw_debug:
                for y in range(0, HEIGHT, TILESIZE):
                    pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

        """ Fog is loaded 3rd """
        # Light Effect - Night Mode
        if self.night:
            self.render_fog()
        if self.night_reactor:
            self.render_fog_reactor()

        # If reactor is turned on by some crew mate in either game mode then
        # hide and reset the reactor_meltdown_timer, which displayed when imposter sabotages
        # the reactor, and finally stop the reactor_timer_event_client
        if not self.night_reactor and (self.gamemode == "Multiplayer" or self.gamemode == "Freeplay"):
            # if player turns on the reactor to stable it then
            # turn off the red light and hide the meltdown timer and stop
            # the reactor timer event
            self.time_left_to_boom_client = 20
            self.reactor_timer_visible_client_status = False
            pg.time.set_timer(self.reactor_timer_event_client, 0)


        if self.emerg_meeting_button_status:
            self.task_button_click_status = False
            if self.emergency_meeting_index == 0 and (self.timer - self.timer_start) < 1500:
                self.screen.blit(self.dim_screen, (0, 0))
                self.display_meeting_alert()  # this layer is beneath the screen
            elif self.emergency_meeting_index == 1 and (self.timer - self.timer_start) < 10000:
                self.screen.blit(self.dim_screen, (0, 0))
                self.display_chat()  # this layer is beneath the screen
            elif self.emergency_meeting_index == 2 and (self.timer - self.timer_start) < 30000:
                self.screen.blit(self.dim_screen, (0, 0))
                self.display_vote()  # this layer is beneath the screen

                # If voting screen appears then show timer only
                # however th timer will be running previously when
                # player calls the meeting
                self.meeting_timer_visible_status = True
            else:
                # When player calls and finish meeting for the 1st time code works
                # fine but when player calls meeting for the 2nd time, meeting timer
                # shows before voting window arrives. Trick is to False the meeting_timer_visible_status
                # when player has not called the meeting.So, If player has not called meeting then
                # hide the meeting timer if it is showing
                self.meeting_timer_visible_status = False

                self.emergency_meeting_index += 1
                self.timer_start = pygame.time.get_ticks()

            if (self.timer - self.timer_start) > 30000:
                # If meeting timer runs out so end the meeting
                # then reset and hide the meeting timer
                self.time_left_to_end_meeting = 30
                self.meeting_timer_visible_status = False
                pg.time.set_timer(self.meeting_timer_event, 0)

            if self.emergency_meeting_index > 2:
                self.emergency_meeting_index = 0
                self.emerg_meeting_button_status = 0
                self.emergency = False

                # show meeting cooldown timer only when voting window disappears
                # and meeting is closed
                self.meeting_timer_cooldown_visible_status = True

                self.meetingcooldown_start = self.meetingcooldown
                self.player.pos = vec(random.choice(self.player_pos))
                if self.player.alive_status == True:
                    self.player.image = self.player.player_imgs_down[0]
                    self.player.sync_img = "self.Players[p[0]].player_imgs_down"
                    self.player.sync_img_index = "[0]"
                self.emergency_img_sync = None
                self.player.got_votes = 0
                self.player.voted = None
                self.emerg_vote_red_checkbox_tick_status = False
                self.emerg_vote_orange_checkbox_tick_status = False
                self.emerg_vote_green_checkbox_tick_status = False
                self.emerg_vote_yellow_checkbox_tick_status = False
                self.emerg_vote_blue_checkbox_tick_status = False
                self.voters = []

        if self.emerg_meeting_report_status:
            if self.emergency_meeting_index == 0 and (self.timer - self.timer_start) < 1500:
                self.screen.blit(self.dim_screen, (0, 0))
                self.display_meeting_alert_report()  # this layer is beneath the screen
            elif self.emergency_meeting_index == 1 and (self.timer - self.timer_start) < 1500:
                self.screen.blit(self.dim_screen, (0, 0))
                self.display_chat()  # this layer is beneath the screen
            elif self.emergency_meeting_index == 2 and (self.timer - self.timer_start) < 30000:
                self.screen.blit(self.dim_screen, (0, 0))
                self.display_vote()  # this layer is beneath the screen

                # If voting screen appears then show timer only
                # however th timer will be running previously when
                # player calls the meeting
                self.meeting_timer_visible_status = True

            else:
                # When player calls and finish meeting for the 1st time code works
                # fine but when player calls meeting for the 2nd time, meeting timer
                # shows before voting window arrives. Trick is to False the meeting_timer_visible_status
                # when player has not called the meeting.So, If player has not called meeting then
                # hide the meeting timer if it is showing
                self.meeting_timer_visible_status = False

                self.emergency_meeting_index += 1
                self.timer_start = pygame.time.get_ticks()

            if (self.timer - self.timer_start) > 30000:
                # If meeting timer runs out so end the meeting
                # then reset and hide the meeting timer
                self.time_left_to_end_meeting = 30
                self.meeting_timer_visible_status = False
                pg.time.set_timer(self.meeting_timer_event, 0)

            if self.emergency_meeting_index > 2:
                self.emergency_meeting_index = 0
                self.emerg_meeting_report_status = 0
                self.emergency = False

                # When voting window disappears then show meeting cooldown timer only
                # means meeting is now closed
                self.meeting_timer_cooldown_visible_status = True

                self.meetingcooldown_start = self.meetingcooldown
                self.player.pos = vec(random.choice(self.player_pos))
                if self.player.alive_status == True:
                    self.player.image = self.player.player_imgs_down[0]
                    self.player.sync_img = "self.Players[p[0]].player_imgs_down"
                    self.player.sync_img_index = "[0]"
                self.emergency_img_sync_report = None
                self.player.got_votes = 0
                self.player.voted = None
                self.emerg_vote_red_checkbox_tick_status = False
                self.emerg_vote_orange_checkbox_tick_status = False
                self.emerg_vote_green_checkbox_tick_status = False
                self.emerg_vote_yellow_checkbox_tick_status = False
                self.emerg_vote_blue_checkbox_tick_status = False
                self.voters = []

        if self.eject == True:
            if (self.timer - self.timer_start) < 5000:
                self.display_eject_alert(self.eject_pos)  # this layer is beneath the screen
                self.eject_pos += 5
            else:
                # self.emergency_meeting_index = 3
                self.eject = False
                self.eject_img = None
                self.eject_colour = None
                self.eject_pos = 0
                if self.emergency:
                    self.emergency_meeting_index = 3


        # Emergency button and player collision detection
        hits = pg.sprite.spritecollide(self.player, self.items, False)
        for hit in hits:
            if hit.type == 'emerg_btn' and not self.mini_map_button_status and self.emerg_meeting_button_status == 0 and self.sabotagecritical == False and self.player.alive_status == True and self.emergency == False:
                keys = pg.key.get_pressed()
                if keys[pg.K_SPACE]:
                    if (self.meetingcooldown - self.meetingcooldown_start) > 15000:
                        # self.player.emerg_play_count = 0
                        self.emerg_meeting_button_status = 1
                        self.emergency = True
                        self.effect_sounds['emergency_alarm'].play()
                        self.emergency_sync += 1
                        self.emergency_img_sync = self.player.emergency_meeting_img_sync

                        # if meeting timer runs out so end the meeting
                        # then reset the meeting cooldown timer to 15 seconds
                        self.emergency_timer_icon_status = False
                        self.meeting_timer_cooldown_visible_status = False
                        self.time_left_to_end_meeting_cooldown = 15
                        pg.time.set_timer(self.meeting_timer_cooldown_event, 1000)

                        # Each time a player calls a meeting a 30 second timer
                        # will be displayed and meeting_timer_event is decremented
                        # each second
                        self.time_left_to_end_meeting = 30
                        pg.time.set_timer(self.meeting_timer_event, 1000)

                        self.timer_start = pygame.time.get_ticks()
                    else:
                        self.effect_sounds['imposter_kill_cooldown_sound'].play()

        """ Progress bar is loaded 5th """
        # if player is impostor then show him imposter progress bar else show normal task progress bar
        if self.player.imposter:
            if not self.clear_asteroid_task_window_status:
                self.draw_progress_bar_imposter(self.screen, 120, 10, self.bot_killed)
        else:
            if not self.clear_asteroid_task_window_status:
                self.draw_progress_bar(self.screen, 75, 10, self.missions_done)

        """UI ELEMENTS LOADED"""
        # Task Button is loaded 5th
        # Show task buttons only to crew mates
        # If task button show check is true and game mode is Freeplay and player is crewmate then show task button only
      
        if self.task_button_show_status and self.gamemode == "Freeplay" and not self.player.imposter:
            self.task_btn = Button(self, "Tasks", 14, 60, 33, 10, 10, "tsk_btn", WHITE, Transparent_Black, None, None,
                                   None, 0)
            self.task_btn.draw_text(self.screen)

        # If task button show check is true and game mode is Multiplayer and player is crewmate then show task button only
        if self.task_button_show_status and self.gamemode == "Multiplayer" and not self.player.imposter:
            self.task_btn = Button(self, "Tasks", 14, 60, 33, 10, 10, "tsk_btn", WHITE, Transparent_Black, None, None,
                                   None, 0)
            self.task_btn.draw_text(self.screen)

        if self.gamemode == "Multiplayer":
            if not self.task_button_show_status and not self.player.imposter:
                self.task_btn = Button(self, "Tasks", 14, 60, 33, 10, 10, "tsk_btn", WHITE, Transparent_Black, None,
                                       None,
                                       None, 0)
                self.task_btn.draw_text(self.screen)

        # Mini Map button
        # We show mini map only to alive players not ghosts
        self.map_btn = Button(self, None, None, 56, 56, WIDTH - 80, 20, "mp_btn", Transparent_Black,
                              Transparent_Black, "Assets/Images/UI/map_button.png", 56, 56, 255)
        if self.player.alive_status:
            self.map_btn.draw_Image(self.screen)

        # # AMBIENT SOUND CODE OPENS HERE -------------------------------------------------------------
        self.gamefuctions.load_ambient_sounds()
        # AMBIENT SOUND CODE CLOSES HERE -------------------------------------------------------------

        # GLOWING OBJECT CODE STARTS HERE ------------------------------------------------------------
        self.gamefuctions.load_glow_objects()
        # GLOWING OBJECT CODE CLOSES HERE--------------------------------------------------------



        # TASKS CODE OPENS HERE------------------------------------------------------------------

        # Open Cafeteria Computer and Toggle Imposter Status
        if self.open_cafe_comp_window_status and self.isdoingTask:
            self.screen.blit(self.dim_screen, (0,0))
            self.display_open_cafe_comp_window()
            if self.open_cafe_comp_check_btn_status:
                self.open_cafe_comp_check_btn.draw_Image(self.screen)
            if self.open_cafe_comp_check_pic_status:
                self.display_open_cafe_comp_check_window()
            if self.open_cafe_comp_close_btn_status:
                self.open_cafe_comp_close_btn.draw_Image(self.screen)

        # Open Cafeteria Computer Task trigger
        keys = pg.key.get_pressed()
        c = pygame.Vector2(3060, 385)
        d = pygame.Vector2(self.player.pos.x, self.player.pos.y)
        if d.distance_to(c) <= 200 and self.gamemode == "Freeplay":
            if keys[pg.K_SPACE] and self.open_cafe_comp_sound_play_count == 1:
                self.effect_sounds['selected'].play()
                self.open_cafe_comp_window_status = True
                self.open_cafe_comp_check_btn_status = True
                self.open_cafe_comp_close_btn_status = True
                self.isdoingTask = True
                self.open_cafe_comp_sound_play_count -= 1

        # Stabilize the Navigation Task
        self.i = WIDTH / 2 - 18
        self.j = HEIGHT / 2 - 4

        self.stabilize_target_btn1 = Button(self, None, None, 56, 56, WIDTH / 2, 60, "stbl_nav_btn",
                                            Transparent_Black,
                                            Transparent_Black,
                                            "Assets/Images/Tasks/Stabilize Steering/nav_stabilize_target.png", 128,
                                            128,
                                            255)
        self.stabilize_target_center_btn = Button(self, None, None, 10, 10, self.i, self.j, "target_center_btn",
                                                  Transparent_Black,
                                                  Transparent_Black,
                                                  "Assets/Images/Tasks/Stabilize Steering/target_center.png", 10,
                                                  10,
                                                  255)
        self.stabilize_close_btn = Button(self, None, None, 65, 65, WIDTH / 1.5 + 80, 40, "stbl_close_btn",
                                          Transparent_Black,
                                          Transparent_Black,
                                          "Assets/Images/Tasks/Stabilize Steering/close.png", 65, 65,
                                          255)

        if self.stabilize_steering_button_status and self.stabilize_steering_window_status and self.isdoingTask:
            self.screen.blit(self.dim_screen, (0, 0))
            self.display_stablize_navigation_window()
            self.stabilize_target_center_btn.draw_Image(self.screen)
            if self.stabilize_close_btn_status:
                self.stabilize_close_btn.draw_Image((self.screen))
            if self.stabilize_target_btn1_status:
                self.stabilize_target_btn1.draw_Image(self.screen)

        if self.target_center_bt_status:
            i = self.navigation_screen_img.get_width() / 3 + 20
            j = self.navigation_screen_img.get_height() / 3 + 20
            self.stabilize_target_btn1_status = False
            self.stabilize_target_btn2 = Button(self, None, None, 56, 56, i, j, "stbl_nav_btn", Transparent_Black,
                                                Transparent_Black,
                                                "Assets/Images/Tasks/Stabilize Steering/nav_stabilize_target.png",
                                                128, 128, 255)
            self.stabilize_target_btn2.draw_Image(self.navigation_screen_img)
            self.stabilize_task_play_count -= 1

        # Stabilize the Navigation Task trigger
        keys = pg.key.get_pressed()
        x = pygame.Vector2(5610, 1290)
        y = pygame.Vector2(self.player.pos.x, self.player.pos.y)
        if x.distance_to(y) <= STABILIZE_NAV_RADIUS:
            if keys[pg.K_SPACE] and self.stablize_sound_play_count == 1 and self.stabilize_task_play_count == 1 and not self.player.imposter:
                self.effect_sounds['selected'].play()
                self.effect_sounds['stabilize_nav_BG'].play(-1)
                self.stabilize_steering_button_status = True
                self.stabilize_steering_window_status = True
                self.stabilize_target_btn1_status = True
                self.stabilize_close_btn_status = True
                self.isdoingTask = True
                self.stablize_sound_play_count -= 1
        ''' Yes'''

        ''' Yes'''
        # Empty the Garbage - Task

        if self.empty_garbage_window_status and self.isdoingTask:
            self.screen.blit(self.dim_screen, (0, 0))
            self.display_full_garbage_window()
            if self.garbage_liver_Up_status:
                self.garbage_liver_Up.draw_Image(self.screen)
            if self.garbage_liver_Down_status:
                self.garbage_liver_Down.draw_Image(self.screen)
            if self.empty_garbage_img_status:
                self.display_empty_garbage_window()
            if self.empty_garbage_close_btn_status:
                self.empty_garbage_close_btn.draw_Image(self.screen)

        # Empty the garbage Task trigger
        keys = pg.key.get_pressed()
        x = pygame.Vector2(3940, 321)
        y = pygame.Vector2(self.player.pos.x, self.player.pos.y)
        if x.distance_to(y) <= EMPTY_GARBAGE_RADIUS:
            if keys[pg.K_SPACE] and self.empty_garbage_sound_play_count == 1 and self.empty_garbage_task_play_count == 1 and not self.player.imposter:
                self.effect_sounds['selected'].play()
                self.effect_sounds['emtpy_garbage_BG'].play(-1)
                self.empty_garbage_window_status = True
                self.garbage_liver_Up_status = True
                self.empty_garbage_close_btn_status = True
                self.isdoingTask = True
                self.empty_garbage_sound_play_count -= 1
        ''' Yes'''

        ''' Yes'''
        # Reboot Wifi Task

        if self.reboot_wifi_window_status and self.isdoingTask:
            self.screen.blit(self.dim_screen, (0, 0))
            self.display_reboot_wifi_window()
            self.reboot_wifi_close_btn.draw_Image(self.screen)
            if self.reboot_wifi_liver_up_status:
                self.reboot_wifi_liver.draw_Image(self.screen)
            if self.reboot_wifi_liver_down_status:
                self.display_reboot_wifi_liver_down()
            if self.rebooted_wifi_window_status:
                self.display_rebooted_wifi_window()

        # Reboot Wifi Task trigger
        keys = pg.key.get_pressed()
        x = pygame.Vector2(3700, 1554)
        y = pygame.Vector2(self.player.pos.x, self.player.pos.y)
        if x.distance_to(y) <= REBOOT_WIFI_RADIUS:
            if keys[pg.K_SPACE] and self.reboot_wifi_sound_play_count == 1 and self.reboot_wifi_task_play_count == 1 and not self.player.imposter:
                self.effect_sounds['selected'].play()
                self.effect_sounds['reboot_wifi_BG'].play(-1)
                self.reboot_wifi_window_status = True
                self.reboot_wifi_liver_up_status = True
                self.isdoingTask = True
                self.reboot_wifi_sound_play_count -= 1
        ''' Yes'''

        ''' Yes'''
        # Fix Electricity Wires Task
        if self.electricity_wire_window_status and self.isdoingTask:
            self.screen.blit(self.dim_screen, (0, 0))
            self.display_electricity_wire_window()
            if self.electricity_wire_close_btn_status:
                self.electricity_wire_close_btn.draw_Image(self.screen)
            if self.electricity_wire_btns_visible:
                self.electricity_wire_red_btn.draw_Image(self.screen)
                self.electricity_wire_blue_btn.draw_Image(self.screen)
                self.electricity_wire_yellow_btn.draw_Image(self.screen)
                self.electricity_wire_pink_btn.draw_Image(self.screen)
                if self.electricity_wire_red_btn_status:
                    self.display_electricity_red()
                if self.electricity_wire_blue_btn_status:
                    self.display_electricity_blue()
                if self.electricity_wire_yellow_btn_status:
                    self.display_electricity_yellow()
                if self.electricity_wire_pink_btn_status:
                    self.display_electricity_pink()

        # Fix Electricity Wires Task Trigger
        x = pygame.Vector2(3166, 1846)
        y = pygame.Vector2(self.player.pos.x, self.player.pos.y)
        if x.distance_to(y) <= FIX_ELECTRICITY_WIRES_RADIUS:
            if keys[pg.K_SPACE] and self.electricity_wire_sound_play_count == 1 and self.electricity_wire_task_play_count == 1 and not self.player.imposter:
                self.effect_sounds['selected'].play()
                self.effect_sounds['fix_electric_wires_BG'].play(-1)
                self.electricity_wire_window_status = True
                self.electricity_wire_close_btn_status = True
                self.electricity_wire_btns_visible = True
                self.electricity_wire_sound_play_count -= 1
                self.isdoingTask = True

        ''' Yes'''
        # Divert Power to Reactor Task
        if self.divert_power_to_reactor_window_status and self.isdoingTask:
            self.screen.blit(self.dim_screen, (0, 0))
            self.display_divert_power_to_reactor_window()
            if self.divert_power_to_reactor_livers_btn_status:
                self.divert_power_to_reactor_livers_btn.draw_Image(self.screen)
            if self.divert_power_to_reactor_liversUP_status:
                self.display_power_diverted_to_reactor_window()
                self.display_divert_power_to_reactor_liverUp_window()
            if self.divert_power_to_reactor_close_btn_status:
                self.divert_power_to_reactor_close_btn.draw_Image(self.screen)


        # Divert Power to Reactor Task Trigger
        x = pygame.Vector2(1031, 1216)
        y = pygame.Vector2(self.player.pos.x, self.player.pos.y)
        if x.distance_to(y) <= DIVERT_POWER_TOP_REACTOR_RADIUS:
            if keys[pg.K_SPACE] and self.divert_power_to_reactor_sound_play_count == 1 and self.divert_power_to_reactor_task_play_count == 1 and not self.player.imposter:
                self.effect_sounds['selected'].play()
                self.effect_sounds['fix_electric_wires_BG'].play(-1)
                self.divert_power_to_reactor_window_status = True
                self.divert_power_to_reactor_livers_btn_status = True
                self.divert_power_to_reactor_close_btn_status = True
                #self.electricity_wire_btns_visible = True
                self.divert_power_to_reactor_sound_play_count -= 1
                self.isdoingTask = True

        ''' Yes'''
        # Align Engine Output Task
        if self.align_engine_output_window_status and self.isdoingTask:
            self.display_align_engine_output_window()
            if self.align_engine_output_window2_status:
                self.display_align_engine_output_window2()
            if self.align_engine_output_window2_status:
                self.display_align_engine_output_window2()
            if self.align_engine_liver_status:
                self.display_align_engine_liver(WIDTH / 2 + 130, 100)
            if self.align_engine_output_window2_status:
                self.display_align_engine_output_window2()
            if self.align_engine_liver_pos_btn1_status:
                self.align_engine_liver_pos_btn1.draw_Image(self.screen)
            if self.align_engine_liver_pos_btn2_status:
                self.align_engine_liver_pos_btn2.draw_Image(self.screen)
            if self.align_engine_output_window3_status:
                self.display_align_engine_output_window3()
                self.display_align_engine_liver(WIDTH / 2 + 100, 195)
            if self.align_engine_output_window4_status:
                self.display_align_engine_output_window4()
                self.display_align_engine_liver(WIDTH / 2 + 100, 285)
            if self.align_engine_output_close_btn_status:
                self.align_engine_output_close_btn.draw_Image(self.screen)

        # Align Engine Output Task Trigger
        c = pygame.Vector2(1117, 837)
        d = pygame.Vector2(self.player.pos.x, self.player.pos.y)
        if c.distance_to(d) <= ALIGN_ENGINE_OUTPUT:
            if keys[pg.K_SPACE] and self.align_engine_output_task_play_count ==1 and self.align_engine_output_sound_play_count == 1 and not self.player.imposter:
                self.effect_sounds['selected'].play()
                self.align_engine_output_window_status = True
                self.align_engine_liver_status = True
                self.align_engine_liver_pos_btn1_status = True
                self.align_engine_liver_pos_btn2_status = True
                self.align_engine_output_window2_status = True
                self.align_engine_output_close_btn_status = True
                self.align_engine_output_sound_play_count -= 1
                self.isdoingTask = True
        ''' Yes'''


        ''' Yes'''
        # Fuel Engine Task
        self.fuel_engine_yellow_bg = pg.Surface((340, 495))
        self.fuel_engine_yellow_bg.fill((235, 195, 52))
        if self.fuel_level <= 0:
            self.fuel_level = 1
        self.fuel_engine_filled_black_reverse_bg = pg.Surface((340, self.fuel_level))
        self.fuel_engine_filled_black_reverse_bg.fill((0, 0, 0))

        if self.fuel_engine_window_status and self.isdoingTask:
            self.screen.blit(self.dim_screen, (0,0))
            self.screen.blit(self.fuel_engine_yellow_bg, (WIDTH / 3 - 45, 70))
            self.screen.blit(self.fuel_engine_filled_black_reverse_bg, (WIDTH / 3 - 45, 167))
            self.display_fuel_engine_window()
            if self.fuel_engine_fill_btn_status:
                self.fuel_engine_fill_btn.draw_Image(self.screen)
            if self.fuel_engine_close_btn_status:
                self.fuel_engine_close_btn.draw_Image(self.screen)
        if self.is_gas_can_picked and not self.isdoingTask:
            self.display_gas_can_picked()

        # IF player has not picked up gas can then show text
        GAME_FONT = pygame.font.Font(FONT, 34)
        if self.gas_can_not_picked_text_visible_status:
            self.screen.blit(self.fuel_engine_filled_black_bg, (WIDTH / 3 - 45, 70))
            self.display_fuel_engine_window()
            self.screen.blit(self.dim_screen, (0, 0))
            self.text = GAME_FONT.render(" Find a Gas Can Nearby", True, WHITE)
            self.screen.blit(self.text, (450, HEIGHT/2 - 30))
            self.fuel_engine_close_btn2.draw_Image(self.screen)

        # Pick Storage Gas Can Task Trigger
        n = pygame.Vector2(3056, 2443)
        m = pygame.Vector2(self.player.pos.x, self.player.pos.y)
        if n.distance_to(m) <= PICK_STORAGE_GAS_CAN_RADIUS:
            if keys[pg.K_SPACE] and self.fuel_engine_task_play_count == 1 and self.gas_can_picking_count == 1 and self.gas_can_picking_sound_play_count == 1 and self.player.imposter == False:
                self.effect_sounds['pick_gas_can'].play()
                self.is_gas_can_picked = True
                self.gas_can_not_picked_text_visible_status = False
                self.gas_can_picking_count -= 1
                self.gas_can_picking_sound_play_count -= 1

        # Fuel Engine Task Trigger
        c = pygame.Vector2(1226, 2300)
        d = pygame.Vector2(self.player.pos.x, self.player.pos.y)
        if c.distance_to(d) <= FUEL_ENGINE:
            if keys[pg.K_SPACE] and self.fuel_engine_sound_play_count == 1 and self.fuel_engine_task_play_count == 1 and not self.player.imposter:
                if self.is_gas_can_picked:
                    self.effect_sounds['selected'].play()
                    self.fuel_engine_window_status = True
                    self.fuel_engine_fill_btn_status = True
                    self.fuel_engine_close_btn_status = True
                    self.isdoingTask = True
                    self.fuel_engine_sound_play_count -= 1
                else:
                    self.gas_can_not_picked_text_visible_status = True
                    self.isdoingTask = True
                    self.fuel_engine_sound_play_count2 -= 1
        ''' Yes'''


        ''' Yes'''
        # Clear Asteroid Task
        if self.clear_asteroid_task_window_status and self.isdoingTask:
            self.task_button_click_status = False
            self.screen.blit(self.dim_screen, (0, 0))
            self.display_clear_asteroids_window()
            if self.clear_asteroid_task_available:
                self.starship_posX = self.starship_posX + self.starship_posX_change
                self.starship_posY = self.starship_posY + self.starship_posY_change

                # Set starship movement boundary of screen
                # horizontal position
                if self.starship_posX <= 0:
                    self.starship_posX = 0
                elif self.starship_posX >= 1185:
                    self.starship_posX = 1185
                # vertical position
                if self.starship_posY <= 0:
                    self.starship_posY = 0
                elif self.starship_posY > 550:
                    self.starship_posY = 550

                # enemy movement
                for i in range(self.num_of_asteroids):
                    # Game Over
                    if self.asteroid_kill_count == 30:
                        self.effect_sounds['task_completed'].play()
                        self.clear_asteroid_task_available = False
                        self.asteroid_bg.fadeout(500)
                        self.clear_asteroid_task_window_status = False
                        self.isdoingTask = False

                        if not self.player.imposter:
                            self.clear_asteroid_task_play_count -= 1
                            if self.increment_in_missions == 1:
                                self.missions_done += 1
                            self.increment_in_missions -= 1
                        break

                    # Asteroids vertical movement
                    if not self.paused:
                        self.asteroid_posY[i] = self.asteroid_posY[i] + self.asteroid_posY_change
                        if self.asteroid_posY[i] >= 640:
                            self.asteroid_posX[i] = random.randint(50, 1200)
                            self.asteroid_posY[i] = random.randint(-200, -150)

                    # Collisions detection
                    collision = self.isCollision(self.asteroid_posX[i], self.asteroid_posY[i], self.bulletX, self.bulletY, i)
                    if collision:
                        self.collision_sound.play()
                        self.bulletY = 550
                        self.bullet_state = "ready"
                        self.score_value = self.score_value - 1
                        self.total_num_of_asteroids -= 1
                        self.asteroid_posX[i] = random.randint(50, 1200)
                        self.asteroid_posY[i] = random.randint(-200, -150)
                    self.display_asteroid(self.asteroid_posX[i], self.asteroid_posY[i], i)

                # bullet movement
                if self.bulletY <= -100:
                    self.bulletY = 550
                    self.bullet_state = "ready"

                if self.bullet_state == "fire":
                    self.fire_bullet(self.bulletX, self.bulletY)
                    self.bulletY = self.bulletY - self.bulletY_change

                self.display_starship(self.starship_posX, self.starship_posY, self.starship_image_alignment)
                self.show_score(WIDTH / 2.5, 10)

        # Clear Asteroid Task Trigger
        c = pygame.Vector2(4513, 450)
        d = pygame.Vector2(self.player.pos.x, self.player.pos.y)
        if d.distance_to(c) <= DETECT_RADIUS and self.clear_asteroid_sound_play_count == 1 and self.clear_asteroid_task_play_count == 1:
            if self.player.imposter == False:
                if keys[pg.K_SPACE]:
                    self.asteroid_bg.play(-1, -1, 1500)
                    self.clear_asteroid_task_window_status = True
                    self.clear_asteroid_task_available = True
                    self.isdoingTask = True
                    self.clear_asteroid_sound_play_count -=1
        # TASKS CODE CLOSES HERE ------------------------------------------------------------



        """ Bots Left is loaded"""
        # Show bot alive count only to impostors
        # if game mode is Freeplay and player is imposter then show bot-alive
        if self.bot_count_show_status and self.gamemode == "Freeplay" and self.player.imposter and not self.clear_asteroid_task_window_status:
            self.bot_bg = pg.Surface((105, 33)).convert_alpha()
            self.bot_bg.fill((0, 0, 0))
            self.screen.blit(self.bot_bg, (10, 10))
            self.board.draw_bots_left(self.bot_count, 14)
        # if game mode is Multiplayer and player is imposter then show bot-alive
        if self.bot_count_show_status and self.gamemode == "Multiplayer" and self.player.imposter and not self.clear_asteroid_task_window_status:
            self.bot_bg = pg.Surface((105, 33)).convert_alpha()
            self.bot_bg.fill((0, 0, 0))
            self.screen.blit(self.bot_bg, (10, 10))
            # player connected +1 for that player who created server, it may be a bug
            # or something that we are missing, dont know.....
            # At least 1 player should be alive so that it will imposter
            # who had killed everybody on ship and won the game
            self.board.draw_bots_left(self.server_player_alive + 1, 14)

        """ Player Name is loaded"""
        # If player is imposter then its name will be Red in color
        if not self.clear_asteroid_task_window_status:
            if self.player.imposter:
                self.screen.blit(self.board.draw_player_name(self.menu.word, RED, 24), (WIDTH / 2 - 90, 10)).center
            # If player is crew mate then its name will be White in color
            else:
                self.screen.blit(self.board.draw_player_name(self.menu.word, WHITE, 24), (WIDTH / 2 - 90, 10)).center


        " TIMER is loaded---------------------------------------------------- OPEN HERE"
        # This code actually draws the timer of Lights bulb On/Off on screen
        if self.light_bulb_timer_icon_dim_status and self.time_left_to_light !=0 and self.player.imposter and not self.isdoingTask and not self.emerg_meeting_button_status and not self.eject:
            self.display_light_bulb_icon_dim()
        if self.light_bulb_timer_icon_status and self.time_left_to_light <= 0 and self.player.imposter and not self.isdoingTask and not self.emerg_meeting_button_status and not self.eject:
            self.display_light_bulb_icon()
        if self.light_timer_event and self.time_left_to_light !=0 and self.light_timer_visible_status and not self.emerg_meeting_button_status and self.player.imposter and not self.isdoingTask and not self.eject:
            self.screen.blit(self.board.draw_light_timer_text(self.time_left_to_light, YELLOW, 30), (WIDTH-135, HEIGHT-90))

        # ---------------------------------------------------------------------------

        # This code actually draws the timer of Emergency Meeting cool down on screen
        if self.emergency_timer_icon_dim_status and self.time_left_to_end_meeting_cooldown != 0 and self.player.alive_status and not self.isdoingTask and not self.emerg_meeting_button_status and not self.eject:
            self.display_emergency_icon_dim()
        if self.emergency_timer_icon_status and self.time_left_to_end_meeting_cooldown <= 0 and self.player.alive_status and not self.isdoingTask and not self.emerg_meeting_button_status and not self.eject:
            self.display_emergency_icon()
        # Emergency Meeting cool down Blit
        if self.time_left_to_end_meeting_cooldown !=0 and self.meeting_timer_cooldown_visible_status and not self.isdoingTask and not self.eject:
            self.screen.blit(self.board.draw_kill_timer_text(self.time_left_to_end_meeting_cooldown, YELLOW, 30), (WIDTH - 506, HEIGHT-90))

        # If emergency meeting is called then show this timer on voting screen
        if self.meeting_timer_event and self.time_left_to_end_meeting !=0 and self.meeting_timer_visible_status:
            self.screen.blit(self.board.draw_meeting_timer_text(self.time_left_to_end_meeting, BLACK, 18), (WIDTH/2 + 50, HEIGHT-180))
        
        # ---------------------------------------------------------------------------
        
        # This code actually draws the timer of kill cool down on screen
        if self.kill_timer_icon_dim_status and self.time_left_to_kill !=0 and self.player.imposter and self.player.alive_status and not self.isdoingTask and not self.emerg_meeting_button_status and not self.eject:
            self.display_kill_icon_dim()
        if self.kill_timer_icon_status and self.time_left_to_kill <= 0 and self.player.imposter and self.player.alive_status and not self.isdoingTask and not self.emerg_meeting_button_status and not self.eject:
            self.display_kill_icon()
        # Kill Timer Blit
        if self.kill_timer_event and self.time_left_to_kill !=0 and self.kill_timer_visible_status and not self.emerg_meeting_button_status and self.player.imposter and not self.isdoingTask and not self.eject:
            self.screen.blit(self.board.draw_kill_timer_text(self.time_left_to_kill, YELLOW, 30), (WIDTH-372, HEIGHT-90))

        # --------------------------------------------------------------------------

        # This code actually draws the timer of reactor_sabotage_cooldown on screen
        if self.sabotage_timer_icon_dim_status and self.time_left_to_boom_cooldown !=0 and self.player.imposter and self.player.alive_status and not self.isdoingTask and not self.emerg_meeting_button_status and not self.eject:
            self.display_sabotage_icon_dim()
        # This code actually draws the timer of reactor sabotage when players turn on the reactor
        if self.sabotage_timer_icon_status and self.time_left_to_boom_cooldown <= 0 and self.player.imposter and self.player.alive_status and not self.isdoingTask and not self.emerg_meeting_button_status and not self.eject:
            self.display_sabotage_icon()
        # Reactor Timer Blit
        if self.time_left_to_boom_cooldown != 0 and self.reactor_timer_cooldown_visible_status and self.player.imposter and not self.emerg_meeting_button_status and not self.isdoingTask and not self.eject:
            self.screen.blit(self.board.draw_reactor_timer_imposter_text(self.time_left_to_boom_cooldown, YELLOW, 30), (WIDTH - 250, HEIGHT - 90))

        # Sabotage Reactor Meltdown Timer Client Side Blit in Multiplayer mode - Slight adjustments in Height of timer
        if self.time_left_to_boom_client != 0 and self.reactor_timer_visible_client_status and self.gamemode == "Multiplayer" and not self.eject and not self.emerg_meeting_button_status:
            self.screen.blit(self.board.draw_reactor_timer_text(self.time_left_to_boom_client, YELLOW, 18), (WIDTH - 350, HEIGHT - 150))

        # Sabotage Reactor Meltdown Timer Client Side Blit in Freeplay mode - Slight adjustments in Height of timer
        if self.time_left_to_boom_client != 0 and self.reactor_timer_visible_client_status and self.gamemode == "Freeplay" and not self.eject and not self.emerg_meeting_button_status:
            self.screen.blit(self.board.draw_reactor_timer_text(self.time_left_to_boom_client, YELLOW, 18), (WIDTH - 350, HEIGHT - 150))

        " TIMER is loaded---------------------------------------------------- CLOSE HERE"


        # View Admin and Security Room Monitor
        """ Admin and Securitu Room Mini Map is loaded 2nd"""
        if self.view_admin_security_monitor_window_status and self.isdoingTask:
            self.screen.blit(self.dim_screen, (0, 0))
            self.screen.blit(self.mini_map, (25, 30))
            self.view_security_monitor_close_btn.draw_Image(self.screen)
            if self.gamemode == "Freeplay":
                if self.bot_count > 0:
                    for b in self.bots:
                        if b.alive_status == True:
                            self.player_map_square.fill(b.bot_colour)
                            self.screen.blit(self.player_map_square,
                                             (int(3 * (b.rect.x / 15)) + 25, int(3 * (b.rect.y / 15)) + 30))
            if self.gamemode == "Multiplayer":
                if len(self.Players) > 0:
                    for p in self.Players.values():
                        if p.got_reported == False:
                            self.player_map_square.fill(YELLOW)
                            self.screen.blit(self.player_map_square,
                                             (int(3 * (p.pos.x / 15)) + 25, int(3 * (p.pos.y / 15)) + 30))

        # View Admin and Security Room Monitor Task trigger
        keys = pg.key.get_pressed()
        x = pygame.Vector2(1756, 1062)  # security room monitor position
        y = pygame.Vector2(3820, 1806)  # admin room map control button position
        z = pygame.Vector2(self.player.pos.x, self.player.pos.y)
        if (x.distance_to(z) <= VIEW_SECURITY_MONITOR_RADIUS and not self.mini_map_button_status) or (y.distance_to(z) <= VIEW_ADMIN_MAP_CONTROL_RADIUS and not self.mini_map_button_status):
            if keys[pg.K_SPACE] and self.view_admin_security_monitor_sound_play_count == 1 and self.player.alive_status:
                self.effect_sounds['selected'].play()
                self.view_security_monitor_close_btn_status = True
                self.view_admin_security_monitor_window_status = True
                # If task window is open then close it when admin mini map opens
                self.task_button_click_status = False
                self.isdoingTask = True
                self.view_admin_security_monitor_sound_play_count -= 1

        """ Mini Map is loaded 2nd"""
        # If mini map button is pressed or clicked and player is alive i.e he is not ghost
        # then show him mini map. We only display mini map to alive players not ghosts
        if self.mini_map_button_status:
            # Mini map is loaded on board surface not screen at specific location on button press
            self.screen.blit(self.dim_screen, (0, 0))
            self.board.draw_adds(self.board.surface, 25, 30, self.mini_map)
            # self.board.draw_adds(self.board.surface, WIDTH - 340, HEIGHT - 160, self.mini_map)

        """ Missions_box is loaded 5th"""
        # If player clicks on task button then show missions box
        # if player is not imposter then show him normal mission box containing missions
        if self.task_button_click_status:
            if not self.player.imposter:
                self.draw_missions_box()

        """ Pause Menu is loaded 6th """
        if self.paused:
            self.screen.blit(self.dim_screen, (0, 0))
            self.pause_btns = Button(self, "Paused", 55, 220, 70, WIDTH / 2 - 80, HEIGHT / 3, "pause_btn", RED,
                                     Transparent_Black, None, None, None, 0)
            self.pause_btns.draw_text(self.screen)
            self.pause_btns = Button(self, "Quit", 40, 100, 50, WIDTH / 2 - 40, HEIGHT / 2, "pause_quit_btn", WHITE,
                                     Transparent_Black, None, None, None, 0)
            self.pause_btns.draw_text(self.screen)


        if self.imposter_among_us_status:
            self.display_imposter_among_us()  # this layer is beneath the screen

        if self.kill_victim_anim:
            if self.kill_victim_anim_index == -1:
                self.kill_victim_anim_index += 1
                self.effect_sounds['imposter_kill_victim_sound'].play()
                self.timer_start = pygame.time.get_ticks()
            elif self.kill_victim_anim_index == 17 and (self.timer - self.timer_start) > 20:
                self.kill_victim_anim_index = -1
                self.kill_victim_anim = False
            elif self.kill_victim_anim_index != -1 and (self.timer - self.timer_start) > 20:
                self.kill_victim_anim_index += 1
                self.timer_start = pygame.time.get_ticks()
            self.display_kill_victim_anim()  # this layer is beneath the screen

        pg.display.flip()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()

            # This is a custom user event which calculates time interval for light ON/OFF
            if event.type == self.light_timer_event and self.light_timer_visible_status:
                # decrement the timer that need to be displayed on screen
                self.time_left_to_light -= 1
                # stop the event if time_left_to_kill equals 0
                if self.time_left_to_light == 0:
                    pygame.time.set_timer(self.light_timer_event, 0)

            # This is a custom user event which calculates time interval to kill a bot
            if event.type == self.kill_timer_event and self.kill_timer_visible_status:
                # decrement the timer that need to be displayed on sceen
                self.time_left_to_kill -= 1
                # stop the event if time_left_to_kill equals 0
                if self.time_left_to_kill == 0:
                    pygame.time.set_timer(self.kill_timer_event, 0)

            # This is a custom user event for reactor sabotage cooldown
            if event.type == self.reactor_timer_cooldown_event and self.reactor_timer_cooldown_visible_status:
                self.time_left_to_boom_cooldown -= 1
                if self.time_left_to_boom_cooldown == 0:
                    self.sabotage_timer_icon_status = True
                    pygame.time.set_timer(self.reactor_timer_cooldown_event, 0)

            # This is a custom user event for reactor sabotage Client side
            if event.type == self.reactor_timer_event_client and self.reactor_timer_visible_client_status:
                self.time_left_to_boom_client -= 1
                if self.time_left_to_boom_client == 0:
                    pygame.time.set_timer(self.reactor_timer_event_client, 0)

            # This is a custom user event for emergency meeting
            if event.type == self.meeting_timer_event and self.meeting_timer_visible_status:
                self.time_left_to_end_meeting -= 1
                if self.time_left_to_end_meeting == 0:
                    pygame.time.set_timer(self.meeting_timer_event, 0)

            # This is a custom user event for emergency meeting timer cooldown
            if event.type == self.meeting_timer_cooldown_event and self.meeting_timer_cooldown_visible_status:
                self.time_left_to_end_meeting_cooldown -= 1
                if self.time_left_to_end_meeting_cooldown == 0:
                    self.emergency_timer_icon_status = True
                    pygame.time.set_timer(self.meeting_timer_cooldown_event, 0)


            if event.type == pg.KEYDOWN:
                # Create a toggle key for debugging collision
                # if key is H and game is not paused
                if event.key == pg.K_h and not self.paused:
                    self.draw_debug = not self.draw_debug
                # Create a toggle key for night fog switch
                # if key is ctrl and game is not paused
                if (event.key == pg.K_LCTRL or event.key == pg.K_RCTRL) and not self.paused and self.emerg_meeting_button_status == 0:

                    c = pygame.Vector2(2472, 1721)
                    d = pygame.Vector2(self.player.pos.x, self.player.pos.y)
                    if (self.sabotagecooldown - self.sabotagecooldown_start) > 15000 and self.night == False and self.night_reactor == False and self.player.imposter == True:
                        self.night = True
                        self.night_sync += 1
                        self.light_bulb_timer_icon_status = False

                    elif self.night == True and c.distance_to(d) <= DETECT_RADIUS_SABOTAGE_FIX:
                        self.night = False

                        # if player or imposter turn on the light then
                        # reset the light timer and decrement light_timer_event
                        self.time_left_to_light = 15
                        pygame.time.set_timer(self.light_timer_event, 1000)
                        self.light_bulb_timer_icon_status = True

                        # if imposter or player turn on the light then
                        # reset the ractor cooldown timer and decrement
                        # reactor_timer_cooldown_event
                        self.time_left_to_boom_cooldown = 15
                        pg.time.set_timer(self.reactor_timer_cooldown_event, 1000)

                        self.sabotagecooldown_start = self.sabotagecooldown
                        self.night_sync += 1

                    elif self.player.imposter == True:
                        self.effect_sounds['imposter_kill_cooldown_sound'].play()

                if (event.key == pg.K_LSHIFT or event.key == pg.K_RSHIFT) and not self.paused and self.emerg_meeting_button_status == 0:
                    c = pygame.Vector2(889, 999)
                    d = pygame.Vector2(self.player.pos.x, self.player.pos.y)

                    if (self.sabotagecooldown - self.sabotagecooldown_start) > 15000 and self.night_reactor == False and self.night == False and self.player.imposter == True:
                        self.night_reactor = True
                        self.night_reactor_sync += 1
                        self.sabotagecritical = True

                        # if sabotage_reactor is recharged and player presses K_shift in multiplayer mod then
                        # show him meltdown_reactor timer of 20 secs and drecrement reactor_timer_event_client
                        # by 1000 milliseconds
                        if self.night_reactor and self.player.imposter and self.gamemode == "Multiplayer":
                            self.reactor_timer_visible_client_status = True
                            pg.time.set_timer(self.reactor_timer_event_client, 1000)
                        if self.night_reactor and self.gamemode == "Freeplay":
                            self.reactor_timer_visible_client_status = True
                            pg.time.set_timer(self.reactor_timer_event_client, 1000)

                        # If kill timer is off or kill timer equals = 0 then on key press K_Shift show reactor timer
                        # on screen and start reactor_timer_event that decrements per second
                        self.sabotage_timer_icon_status = False
                        pygame.mixer.Channel(0).play(pygame.mixer.Sound(self.effect_sounds['crises_alarm']),
                                                     loops=-1)
                        self.sabotagecriticaltimer_start = pygame.time.get_ticks()

                    # To Trigger Reactor meltdown Sabotage - Freeplay Mode
                    elif self.night_reactor == True and c.distance_to(d) <= DETECT_RADIUS_SABOTAGE_FIX:
                        self.night_reactor = False

                        # if crew mates turns the reactor on then again reset the cooldown timer
                        # so that it can again recharge for imposter to press K_shift and 
                        # sabotage the reactor
                        self.time_left_to_boom_cooldown = 15
                        pg.time.set_timer(self.reactor_timer_cooldown_event, 1000)
                        # show the reactor cooldown timer to imposter
                        self.reactor_timer_cooldown_visible_status = True
                        # Hide the sabotage reactor highlighted icon
                        self.sabotage_timer_icon_status = False
                        # Show the sabotage reactor dimmed icon
                        self.sabotage_timer_icon_dim_status = True

                        # if imposter turn on the reactor then again reset the
                        # light timer to 15 so that it can be again used to turn
                        # off the lights and decrement the light_timer_event
                        self.time_left_to_light = 15
                        pg.time.set_timer(self.light_timer_event, 1000)
                        self.light_bulb_timer_icon_status = True

                        self.sabotagecooldown_start = self.sabotagecooldown
                        self.night_reactor_sync += 1
                        self.sabotagecritical = False
                        pygame.mixer.Channel(0).stop()

                    elif self.player.imposter == True:
                        self.effect_sounds['imposter_kill_cooldown_sound'].play()

                # if key is P or Esc then pause the game
                if event.key == pg.K_p or event.key == pg.K_ESCAPE:
                    if not self.emergency:
                        self.effect_sounds['go_back'].play()
                        self.paused = not self.paused

                # Show mini map on Keypress TAB
                if event.key == pg.K_TAB and not self.view_admin_security_monitor_window_status and self.player.alive_status:
                    self.effect_sounds['pause'].play()
                    self.mini_map_button_status = not self.mini_map_button_status
                    # If missions box is opened then close it when we press on TAB key to open mini map
                    self.task_button_click_status = False

            # Check Mouse clicks the mini map button
            # Open map, play sound, change mini_map_button_status
            # if left mouse button is pressed and game is not paused
            if event.type == pg.MOUSEBUTTONDOWN and event.button == LEFT_MOUSE_BUTTON and not self.paused and not self.emerg_meeting_button_status and not self.view_admin_security_monitor_window_status and self.player.alive_status:
                pos = pg.mouse.get_pos()
                if self.map_btn.click(pos):
                    if self.map_btn.button_type == "mp_btn":
                        self.effect_sounds['map_click2'].play()
                        self.mini_map_button_status = not self.mini_map_button_status
                        # If mission box is opened then close it when we click on mini map button
                        self.task_button_click_status = False
            # For Pause Menu Buttons
            if event.type == pg.MOUSEBUTTONDOWN and event.button == LEFT_MOUSE_BUTTON and self.paused:
                pos = pg.mouse.get_pos()
                if self.pause_btns.click(pos):
                    # If player clicks quit game button
                    if self.pause_btns.button_type == "pause_quit_btn":
                        # self.effect_sounds['go_back'].play()
                        # self.quit()
                        # self.pause_quit_button_status = True
                        self.menu.game_left(self.score_list, 'You Left The Game')
                        self.game_left = True

            # Task Button
            if event.type == pg.MOUSEBUTTONDOWN and event.button == LEFT_MOUSE_BUTTON and not self.paused and self.task_button_show_status and not self.view_admin_security_monitor_window_status and not self.mini_map_button_status:
                pos = pg.mouse.get_pos()
                if self.task_btn.click(pos):
                    if self.task_btn.button_type == "tsk_btn":
                        self.effect_sounds['map_click'].play()
                        self.task_button_click_status = not self.task_button_click_status

            if self.gamemode == "Multiplayer":
                if event.type == pg.MOUSEBUTTONDOWN and event.button == LEFT_MOUSE_BUTTON and not self.paused and not self.task_button_show_status:
                    pos = pg.mouse.get_pos()
                    if self.task_btn.click(pos):
                        if self.task_btn.button_type == "tsk_btn":
                            self.effect_sounds['map_click'].play()
                            self.task_button_click_status = not self.task_button_click_status


            """ OPEN CAFETERIA COMPUTER BUTTONS & EVENTS """
            # Open Cafe Computer and Toggle Imposter Status
            if event.type == pg.MOUSEBUTTONDOWN and event.button == LEFT_MOUSE_BUTTON and not self.paused and self.open_cafe_comp_window_status:
                pos = pg.mouse.get_pos()
                if self.open_cafe_comp_check_btn.click(pos):
                    self.open_cafe_comp_check_pic_status = not self.open_cafe_comp_check_pic_status
                    self.player.imposter = not self.player.imposter
                    self.bot_count_show_status = not self.bot_count_show_status
                    self.task_button_show_status = not self.task_button_show_status
                    self.effect_sounds['invisible'].play()
                elif self.open_cafe_comp_close_btn.click(pos):
                    self.effect_sounds['go_back'].play()
                    self.open_cafe_comp_window_status = False
                    self.open_cafe_comp_close_btn_status = False
                    #self.open_cafe_comp_check_pic_status = False
                    self.open_cafe_comp_sound_play_count += 1
                    self.isdoingTask = False


            """ VIEW SECURITY MINI MAP BUTTON & EVENTS """
            # View Security Monitor Mini Map - Buttons
            if event.type == pg.MOUSEBUTTONDOWN and event.button == LEFT_MOUSE_BUTTON and not self.paused and self.view_admin_security_monitor_window_status:
                pos = pg.mouse.get_pos()
                if self.view_security_monitor_close_btn.click(pos):
                    self.effect_sounds['go_back'].play()
                    self.view_admin_security_monitor_window_status = False
                    self.view_admin_security_monitor_sound_play_count += 1
                    self.isdoingTask = False


            """ STABILIZE NAVIGAITON TASK BUTTONS & EVENTS """
            # Stabilize Nav Button
            if event.type == pg.MOUSEBUTTONDOWN and event.button == LEFT_MOUSE_BUTTON and not self.paused and self.target_center_sel_count == 1 and self.stabilize_steering_window_status:
                pos = pg.mouse.get_pos()
                if self.stabilize_target_center_btn.click(pos):
                    self.effect_sounds['task_completed'].play()
                    self.target_center_bt_status = True
                    self.stabilize_target_btn1_status = False
                    self.target_center_sel_count -= 1
                    self.missions_done += 1
                    print(self.missions_done)
            if event.type == pg.MOUSEBUTTONDOWN and event.button == LEFT_MOUSE_BUTTON and not self.paused and self.stabilize_steering_window_status:
                pos = pg.mouse.get_pos()
                if self.stabilize_close_btn.click(pos):
                    self.effect_sounds['go_back'].play()
                    self.effect_sounds['stabilize_nav_BG'].stop()
                    self.target_center_bt_status = False
                    self.stabilize_steering_button_status = False
                    self.stabilize_steering_window_status = False
                    self.stabilize_target_btn1_status = False
                    self.stabilize_close_btn_status = False
                    self.stablize_sound_play_count += 1
                    self.isdoingTask = False


            """ EMPTY GARBAGE TASK BUTTONS & EVENTS """
            # Empty Garbage Button
            if event.type == pg.MOUSEBUTTONDOWN and event.button == LEFT_MOUSE_BUTTON and not self.paused and self.garbage_liver_Up_sel_count == 1 and self.empty_garbage_window_status:
                pos = pg.mouse.get_pos()
                if self.garbage_liver_Up.click(pos):
                    self.effect_sounds['task_completed'].play()
                    self.garbage_liver_Up_status = False
                    self.garbage_liver_Down_status = True
                    self.empty_garbage_img_status = True
                    self.garbage_liver_Up_sel_count -= 1
                    self.empty_garbage_task_play_count -= 1
                    self.missions_done += 1
                    print(self.missions_done)
            if event.type == pg.MOUSEBUTTONDOWN and event.button == LEFT_MOUSE_BUTTON and not self.paused and self.empty_garbage_window_status:
                pos = pg.mouse.get_pos()
                if self.empty_garbage_close_btn.click(pos):
                    self.effect_sounds['go_back'].play()
                    self.effect_sounds['emtpy_garbage_BG'].fadeout(500)
                    self.empty_garbage_window_status = False
                    self.empty_garbage_close_btn_status = False
                    self.empty_garbage_img_status = False
                    self.empty_garbage_sound_play_count += 1
                    self.isdoingTask = False


            """ REBOOT WIFI BUTTONS & EVENTS """
            # Reboot Wifi Button
            if event.type == pg.MOUSEBUTTONDOWN and event.button == LEFT_MOUSE_BUTTON and not self.paused and self.reboot_wifi_liver_sel_count == 1 and self.reboot_wifi_window_status:
                pos = pg.mouse.get_pos()
                if self.reboot_wifi_liver.click(pos):
                    self.effect_sounds['task_completed'].play()
                    self.effect_sounds['rebooted_wifi_BG'].play(-1)
                    self.reboot_wifi_close_btn_status = False
                    self.reboot_wifi_liver_up_status = False
                    self.reboot_wifi_liver_down_status = True
                    self.rebooted_wifi_window_status = True
                    self.reboot_wifi_liver_sel_count -= 1
                    self.reboot_wifi_task_play_count -= 1
                    self.missions_done += 1
                    print(self.missions_done)
            if event.type == pg.MOUSEBUTTONDOWN and event.button == LEFT_MOUSE_BUTTON and not self.paused and self.reboot_wifi_window_status:
                pos = pg.mouse.get_pos()
                if self.reboot_wifi_close_btn.click(pos):
                    self.effect_sounds['go_back'].play()
                    self.effect_sounds['reboot_wifi_BG'].fadeout(500)
                    self.effect_sounds['rebooted_wifi_BG'].fadeout(500)
                    self.reboot_wifi_window_status = False
                    self.reboot_wifi_liver_down_status = False
                    self.reboot_wifi_sound_play_count += 1
                    self.isdoingTask = False


            """ EMERGENCY MEETING & VOTING BUTTONS & EVENTS"""
            if event.type == pg.MOUSEBUTTONDOWN and event.button == LEFT_MOUSE_BUTTON and not self.paused and (
                    self.emerg_meeting_button_status or self.emerg_meeting_report_status) and self.emergency == True and self.player.alive_status == True:
                pos = pg.mouse.get_pos()
                if self.emerg_red_checkbox.click(pos):
                    if self.player.voted == None:
                        self.player.voted = "Red"
                        self.emerg_vote_red_checkbox_tick_status = True
                        self.emerg_vote_orange_checkbox_tick_status = False
                        self.emerg_vote_green_checkbox_tick_status = False
                        self.emerg_vote_yellow_checkbox_tick_status = False
                        self.emerg_vote_blue_checkbox_tick_status = False
                    #else:
                    #    self.player.voted = None
                    #    self.emerg_vote_red_checkbox_tick_status = False
                elif self.emerg_orange_checkbox.click(pos):
                    if self.player.voted == None:
                        self.player.voted = "Orange"
                        self.emerg_vote_red_checkbox_tick_status = False
                        self.emerg_vote_orange_checkbox_tick_status = True
                        self.emerg_vote_green_checkbox_tick_status = False
                        self.emerg_vote_yellow_checkbox_tick_status = False
                        self.emerg_vote_blue_checkbox_tick_status = False
                    #else:
                    #    self.player.voted = None
                    #    self.emerg_vote_orange_checkbox_tick_status = False
                elif self.emerg_green_checkbox.click(pos):
                    if self.player.voted == None:
                        self.player.voted = "Green"
                        self.emerg_vote_red_checkbox_tick_status = False
                        self.emerg_vote_orange_checkbox_tick_status = False
                        self.emerg_vote_green_checkbox_tick_status = True
                        self.emerg_vote_yellow_checkbox_tick_status = False
                        self.emerg_vote_blue_checkbox_tick_status = False
                    #else:
                    #    self.player.voted = None
                    #    self.emerg_vote_green_checkbox_tick_status = False
                elif self.emerg_yellow_checkbox.click(pos):
                    if self.player.voted == None:
                        self.player.voted = "Yellow"
                        self.emerg_vote_red_checkbox_tick_status = False
                        self.emerg_vote_orange_checkbox_tick_status = False
                        self.emerg_vote_green_checkbox_tick_status = False
                        self.emerg_vote_yellow_checkbox_tick_status = True
                        self.emerg_vote_blue_checkbox_tick_status = False
                    #else:
                    #    self.player.voted = None
                    #    self.emerg_vote_yellow_checkbox_tick_status = False
                elif self.emerg_blue_checkbox.click(pos):
                    if self.player.voted == None:
                        self.player.voted = "Blue"
                        self.emerg_vote_red_checkbox_tick_status = False
                        self.emerg_vote_orange_checkbox_tick_status = False
                        self.emerg_vote_green_checkbox_tick_status = False
                        self.emerg_vote_yellow_checkbox_tick_status = False
                        self.emerg_vote_blue_checkbox_tick_status = True
                    #else:
                    #    self.player.voted = None
                    #    self.emerg_vote_blue_checkbox_tick_status = False
                self.effect_sounds['vote_sound'].play()

            """ ELECTRIC WIRES TASK BUTTONS & EVENTS"""
            if event.type == pg.MOUSEBUTTONDOWN and event.button == LEFT_MOUSE_BUTTON and not self.paused and self.electricity_wire_window_status:
                pos = pg.mouse.get_pos()
                if self.electricity_wire_red_btn.click(pos) and self.electricity_wires_red_sel_count == 1:
                    random.choice(self.electric_shock_sounds['electric_shock']).play()
                    self.electricity_wires_red_sel_count -= 1
                    self.electricity_wires_fixed_count += 1
                    self.electricity_wire_red_btn_status = True
                elif self.electricity_wire_blue_btn.click(pos) and self.electricity_wires_blue_sel_count == 1:
                    random.choice(self.electric_shock_sounds['electric_shock']).play()
                    self.electricity_wires_fixed_count += 1
                    self.electricity_wires_blue_sel_count -= 1
                    self.electricity_wire_blue_btn_status = True
                elif self.electricity_wire_yellow_btn.click(pos) and self.electricity_wires_yellow_sel_count == 1:
                    random.choice(self.electric_shock_sounds['electric_shock']).play()
                    self.electricity_wires_yellow_sel_count -= 1
                    self.electricity_wires_fixed_count += 1
                    self.electricity_wire_yellow_btn_status = True
                elif self.electricity_wire_pink_btn.click(pos) and self.electricity_wires_pink_sel_count == 1:
                    random.choice(self.electric_shock_sounds['electric_shock']).play()
                    self.electricity_wires_pink_sel_count -= 1
                    self.electricity_wires_fixed_count += 1
                    self.electricity_wire_pink_btn_status = True
                if self.electricity_wires_fixed_count == 4:
                    self.effect_sounds['task_completed'].play()
                    self.effect_sounds['fix_electric_wires_BG'].fadeout(500)
                    self.effect_sounds['fixed_electric_wires_BG'].play(-1)
                    self.missions_done += 1
                    self.electricity_wire_task_play_count -= 1
                    self.electricity_wires_fixed_count += 1
                    print(self.electricity_wires_fixed_count)

            if event.type == pg.MOUSEBUTTONDOWN and event.button == LEFT_MOUSE_BUTTON and not self.paused and self.electricity_wire_window_status:
                pos = pg.mouse.get_pos()
                if self.electricity_wire_close_btn.click(pos):
                    self.effect_sounds['go_back'].play()
                    self.effect_sounds['fix_electric_wires_BG'].fadeout(500)
                    self.effect_sounds['fixed_electric_wires_BG'].fadeout(500)
                    self.electricity_wire_window_status = False
                    self.electricity_wire_close_btn_status = False
                    self.electricity_wire_btns_visible = False
                    self.electricity_wire_red_btn_status = False
                    self.electricity_wire_blue_btn_status = False
                    self.electricity_wire_yellow_btn_status = False
                    self.electricity_wire_pink_btn_status = False
                    self.electricity_wire_sound_play_count += 1
                    self.electricity_wires_red_sel_count = 1
                    self.electricity_wires_blue_sel_count = 1
                    self.electricity_wires_yellow_sel_count = 1
                    self.electricity_wires_pink_sel_count = 1
                    self.electricity_wires_fixed_count = 0
                    # self.missions_done += 1
                    self.isdoingTask = False
            """ ELECTRIC WIRES TASK BUTTONS CODE CLOSES HERE"""

            """ DIVERT POWER TO REACTOR TASK BUTTONS & EVENTS"""
            if event.type == pg.MOUSEBUTTONDOWN and event.button == LEFT_MOUSE_BUTTON and not self.paused and self.divert_power_to_reactor_window_status:
                pos = pg.mouse.get_pos()
                if self.divert_power_to_reactor_livers_btn.click(pos) and self.divert_power_to_reactor_liversUP_sel_count == 1:
                    self.effect_sounds['task_completed'].play()
                    self.divert_power_to_reactor_livers_btn_status = False
                    self.divert_power_to_reactor_liversUP_status = True
                    self.divert_power_to_reactor_task_play_count -= 1
                    self.divert_power_to_reactor_liversUP_sel_count -= 1
                    self.missions_done += 1
                elif self.divert_power_to_reactor_close_btn.click(pos):
                    self.effect_sounds['go_back'].play()
                    self.effect_sounds['fix_electric_wires_BG'].fadeout(500)
                    self.divert_power_to_reactor_window_status = False
                    self.divert_power_to_reactor_liversUP_status = False
                    self.divert_power_to_reactor_close_btn_status = False
                    self.divert_power_to_reactor_sound_play_count += 1
                    self.isdoingTask = False

            """ ALIGN ENGINE OUTPUT TASK BUTTONS & EVENTS"""
            if event.type == pg.MOUSEBUTTONDOWN and event.button == LEFT_MOUSE_BUTTON and not self.paused and self.align_engine_output_window_status:
                pos = pg.mouse.get_pos()
                if self.align_engine_liver_pos_btn1.click(pos) and self.align_engine_liver_pos_btn1_sel_count == 1:
                    self.effect_sounds['map_click'].play()
                    self.align_engine_output_window2_status = False
                    self.align_engine_liver_status = False
                    self.align_engine_output_window3_status = True
                    self.align_engine_liver_pos_btn1_sel_count -= 1
                elif self.align_engine_liver_pos_btn2.click(pos) and self.align_engine_liver_pos_btn2_sel_count == 1 and self.align_engine_liver_pos_btn1_sel_count < 1:
                    self.effect_sounds['task_completed'].play()
                    self.align_engine_output_window3_status = False
                    self.align_engine_liver_pos_btn1_status = False
                    self.align_engine_output_window4_status = True
                    self.align_engine_liver_pos_btn2_sel_count -= 1
                    self.align_engine_output_task_play_count -=1
                    self.missions_done += 1
                # if player has not click on button 1 and he then clicks button 2 then play error sound
                if self.align_engine_liver_pos_btn2.click(pos) and self.align_engine_liver_pos_btn1_sel_count == 1:
                    self.effect_sounds['imposter_kill_cooldown_sound'].play()

            if event.type == pg.MOUSEBUTTONDOWN and event.button == LEFT_MOUSE_BUTTON and not self.paused and self.align_engine_output_window_status:
                pos = pg.mouse.get_pos()
                if self.align_engine_output_close_btn.click(pos):
                    self.effect_sounds['go_back'].play()
                    self.align_engine_output_window_status = False
                    self.align_engine_liver_status = False
                    self.align_engine_output_window2_status = False
                    self.align_engine_output_window3_status = False
                    self.align_engine_output_window4_status = False
                    self.align_engine_liver_pos_btn1_status = False
                    self.align_engine_liver_pos_btn2_status = False
                    self.align_engine_output_close_btn_status = False
                    self.isdoingTask = False
                    if self.align_engine_liver_pos_btn1_sel_count > 1 or self.align_engine_liver_pos_btn1_sel_count < 1:
                        self.align_engine_liver_pos_btn1_sel_count = 1
                    self.align_engine_output_sound_play_count += 1

            """ FUEL ENGINE TASK BUTTONS & EVENTS"""
            if event.type == pg.MOUSEBUTTONDOWN and event.button == LEFT_MOUSE_BUTTON and self.fuel_engine_fill_btn_sel_count == 1 and not self.paused and self.fuel_engine_window_status:
                pos = pg.mouse.get_pos()
                if self.fuel_engine_fill_btn.click(pos):
                    self.effect_sounds['fill_gas_can'].play()
                    self.fuel_level -= 10
                    if self.fuel_level <= 0:
                        self.fuel_engine_fill_btn_sel_count -=1
                        self.effect_sounds['task_completed'].play()
                        self.missions_done += 1
                        self.is_gas_can_picked = False
                        self.fuel_engine_task_play_count -=1

            if event.type == pg.MOUSEBUTTONDOWN and event.button == LEFT_MOUSE_BUTTON and not self.paused and self.fuel_engine_window_status:
                pos = pg.mouse.get_pos()
                if self.fuel_engine_close_btn.click(pos):
                    self.effect_sounds['go_back'].play()
                    self.fuel_engine_window_status = False
                    self.fuel_engine_close_btn_status = False
                    self.isdoingTask = False
                    self.fuel_engine_sound_play_count +=1

            if event.type == pg.MOUSEBUTTONDOWN and event.button == LEFT_MOUSE_BUTTON and not self.paused and self.gas_can_not_picked_text_visible_status:
                pos = pg.mouse.get_pos()
                if self.fuel_engine_close_btn2.click(pos):
                    self.gas_can_not_picked_text_visible_status = False
                    self.isdoingTask = False
                    self.fuel_engine_sound_play_count2 += 1

            """ CLEAR ASTEROIDS TASK BUTTONS & EVENTS"""
            # Check if Left /Right /Up /Down key is pressed
            if self.clear_asteroid_task_available and not self.paused:
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_LEFT:
                        self.starship_posX_change = -10
                    if event.key == pg.K_RIGHT:
                        self.starship_posX_change = 10
                    #if event.key == pg.K_UP:
                    #    self.starship_posY_change = -10
                    #if event.key == pg.K_DOWN:
                    #    self.starship_posY_change = 10

                    if event.key == pg.K_SPACE and not self.paused:
                        if self.bullet_state == "ready":
                            self.bullet_sound.play()
                            self.bulletX = self.starship_posX + 27
                            self.bulletY = self.starship_posY - 20
                            self.fire_bullet(self.bulletX, self.bulletY)

                if event.type == pg.KEYUP:
                    if event.key == pg.K_LEFT or event.key == pg.K_RIGHT:
                        self.starship_posX_change = 0
                    if event.key == pg.K_UP or event.key == pg.K_DOWN:
                        self.starship_posY_change = 0




    # HUD Progress Bar - missions completed
    def draw_progress_bar(self, screen_surface, x, y, missions_done):

        if missions_done >= 7:
            missions_done = 7
        if missions_done >= 5:
            color = GREEN
        if missions_done < 2:
            color = RED
        if missions_done >= 2 and missions_done < 5:
            color = SKYBLUE
        width = 350
        height = 32
        # progress_width translucent black background bar
        self.bg_bar = pg.Surface((width, height)).convert_alpha()
        self.bg_bar.fill((0, 0, 0, 156))
        self.screen.blit(self.bg_bar, (x, y))

        # progress_width calculates percentage of missions completed, use to fill the bar
        progress_width = width * missions_done / NO_OF_MISSIONS
        # Outline rectangle for background and border effect
        outline_rect = pg.Rect(x, y, width, height)
        progress_bar = pg.Rect(x, y, progress_width, height)
        pg.draw.rect(screen_surface, color, progress_bar)

        taskbar_font = pg.font.Font(FONT, 14)
        if missions_done >= 5:
            # if mission completed is 4 or greater than 4 then font color is Black
            text_surface = taskbar_font.render("Total Tasks Completed", True, BLACK)
        else:
            # if mission completed is less than 4 then font color is White
            text_surface = taskbar_font.render("Total Tasks Completed", True, WHITE)
        self.screen.blit(text_surface, (90, 17))

        # 4th parameter is the thickness of border of rectangle
        pg.draw.rect(screen_surface, WHITE, outline_rect, 2)

    def draw_missions_box(self):
        self.GAME_FONT = pygame.font.Font(FONT, 18)
        self.mission_box = pg.Surface((415, 235)).convert_alpha()
        self.mission_box.fill((0, 0, 0, 96))
        self.screen.blit(self.mission_box, (10, 45))
        if not self.night:
            self.text = self.GAME_FONT.render(self.tasks.turn_on_the_lights_task_title, True, GREEN)
            self.screen.blit(self.text, (20, 50))
        else:
            self.text = self.GAME_FONT.render(self.tasks.turn_on_the_lights_task_title, True, WHITE)
            self.screen.blit(self.text, (20, 50))
        if self.reboot_wifi_task_play_count != 1:
            self.text = self.GAME_FONT.render(self.tasks.reboot_the_wifi_task_title, True, GREEN)
            self.screen.blit(self.text, (20, 75))
        else:
            self.text = self.GAME_FONT.render(self.tasks.reboot_the_wifi_task_title, True, WHITE)
            self.screen.blit(self.text, (20, 75))
        if self.garbage_liver_Up_sel_count != 1:
            self.text = self.GAME_FONT.render(self.tasks.empty_the_garbage_task_title, True, GREEN)
            self.screen.blit(self.text, (20, 100))
        else:
            self.text = self.GAME_FONT.render(self.tasks.empty_the_garbage_task_title, True, WHITE)
            self.screen.blit(self.text, (20, 100))
        if self.stabilize_task_play_count != 1:
            self.text = self.GAME_FONT.render(self.tasks.stabilize_nav_task_title, True, GREEN)
            self.screen.blit(self.text, (20, 125))
        else:
            self.text = self.GAME_FONT.render(self.tasks.stabilize_nav_task_title, True, WHITE)
            self.screen.blit(self.text, (20, 125))
        if self.electricity_wire_task_play_count != 1:
            self.text = self.GAME_FONT.render(self.tasks.fix_electircity_wires_task_title, True, GREEN)
            self.screen.blit(self.text, (20, 150))
        else:
            self.text = self.GAME_FONT.render(self.tasks.fix_electircity_wires_task_title, True, WHITE)
            self.screen.blit(self.text, (20, 150))
        if self.divert_power_to_reactor_task_play_count != 1:
            self.text = self.GAME_FONT.render(self.tasks.divert_power_to_reactor_task_title, True, GREEN)
            self.screen.blit(self.text, (20, 175))
        else:
            self.text = self.GAME_FONT.render(self.tasks.divert_power_to_reactor_task_title, True, WHITE)
            self.screen.blit(self.text, (20, 175))
        if self.align_engine_output_task_play_count != 1:
            self.text = self.GAME_FONT.render(self.tasks.align_engine_output_task_title, True, GREEN)
            self.screen.blit(self.text, (20, 200))
        else:
            self.text = self.GAME_FONT.render(self.tasks.align_engine_output_task_title, True, WHITE)
            self.screen.blit(self.text, (20, 200))

        if self.fuel_engine_task_play_count != 1:
            self.text = self.GAME_FONT.render(self.tasks.fuel_engine_task_title, True, GREEN)
            self.screen.blit(self.text, (20, 225))
        else:
            self.text = self.GAME_FONT.render(self.tasks.fuel_engine_task_title, True, WHITE)
            self.screen.blit(self.text, (20, 225))

        if self.clear_asteroid_task_play_count != 1:
            self.text = self.GAME_FONT.render(self.tasks.clear_asteroids_task_title, True, GREEN)
            self.screen.blit(self.text, (20, 250))
        else:
            self.text = self.GAME_FONT.render(self.tasks.clear_asteroids_task_title, True, WHITE)
            self.screen.blit(self.text, (20, 250))


        # HUD Progress Bar - player kills count

    def draw_progress_bar_imposter(self, screen_surface, x, y, players_killed):
        color = RED
        width = 350
        height = 32
        # progress_width translucent black background bar
        self.bg_bar2 = pg.Surface((width, height)).convert_alpha()
        self.bg_bar2.fill((0, 0, 0, 156))
        self.screen.blit(self.bg_bar2, (x, y))
        # progress_width calculates percentage of missions completed, use to fill the bar
        if self.gamemode == "Freeplay":
            progress_width = width * players_killed / NO_OF_BOTS
        if self.gamemode == "Multiplayer":
            progress_width = width * self.server_player_killed / self.server_players_connected
        # Outline rectangle for background and border effect
        outline_rect = pg.Rect(x, y, width, height)
        progress_bar = pg.Rect(x, y, progress_width, height)
        pg.draw.rect(screen_surface, color, progress_bar)

        # progress bar text
        taskbar_font = pg.font.Font(FONT, 14)
        text_surface = taskbar_font.render("K I L L   A L L   B O T S", True, WHITE)
        text_surface2 = taskbar_font.render("K I L L   A L L   P L A Y E R S", True, WHITE)
        if self.gamemode == "Freeplay":
            self.screen.blit(text_surface, (140, 17))
        else:
            self.screen.blit(text_surface2, (140, 17))

        # 4th parameter is the thickness of border of rectangle
        pg.draw.rect(screen_surface, WHITE, outline_rect, 2)

    def draw_missions_box_imposter(self):
        self.GAME_FONT = pygame.font.SysFont('Arial', 24)
        self.mission_box = pg.Surface((412, 140)).convert_alpha()
        self.mission_box.fill((0, 0, 0, 96))
        self.screen.blit(self.mission_box, (10, 45))
