import pygame as pg
from settings import *


class GameFunctions:
    def __init__(self, game):
        self.game = game
        # Ambient Sounds Checks
        self.cafeteria_sound_play_check = True
        self.medbay_sound_play_check = True
        self.security_room_sound_play_check = True
        self.reactor_room_sound_play_check = True
        self.upper_engine_room_sound_play_check = True
        self.lower_engine_room_sound_play_check = True
        self.electrical_room_sound_play_check = True
        self.storage_room_sound_play_check = True
        self.admin_room_sound_play_check = True
        self.communication_room_sound_play_check = True
        self.oxygen_room_sound_play_check = True
        self.cockpit_room_sound_play_check = True
        self.weapons_room_sound_play_check = True
        self.bg_music_playing = True

        # Load all images that will be used for glowing objects
        self.load_image_data()

    # This function load all images that will be used for glowing objects
    def load_image_data(self):
        # GLOW OBJECT IMAGES LOADING HERE
        self.cafeteria_comp_img = pg.image.load("Assets/Images/Items/cafeteria_comp.png").convert_alpha()
        self.cafeteria_comp_highlighted_img = pg.image.load(
            "Assets/Images/Items/cafeteria_comp_highlight.png").convert_alpha()
        self.emergency_button_img = pg.image.load("Assets/Images/Items/emergency_button.png").convert_alpha()
        self.emergency_button_highlighted_img = pg.image.load(
            "Assets/Images/Items/emergency_button_highlight.png").convert_alpha()
        self.nav_img = pg.image.load("Assets/Images/Items/nav.png").convert_alpha()
        self.nav_highlighted_img = pg.image.load("Assets/Images/Items/nav_highlight.png").convert_alpha()
        self.reactor_btn_img = pg.image.load("Assets/Images/Items/reactor_btn.png").convert_alpha()
        self.reactor_highlight_btn_img = pg.image.load("Assets/Images/Items/reactor_btn_highlight.png").convert_alpha()
        self.lower_engine_img = pg.image.load("Assets/Images/Items/lower_engine.png").convert_alpha()
        self.lower_highlight_engine_img = pg.image.load(
            "Assets/Images/Items/lower_engine_highlight.png").convert_alpha()
        self.upper_engine_img = pg.image.load("Assets/Images/Items/upper_engine.png").convert_alpha()
        self.upper_engine_highlight_img = pg.image.load(
            "Assets/Images/Items/upper_engine_highlight.png").convert_alpha()
        self.navigation_img = pg.image.load("Assets/Images/Items/navigation.png").convert_alpha()
        self.navigation_highlight_img = pg.image.load("Assets/Images/Items/navigation_highlight.png").convert_alpha()
        self.generator_btn_img = pg.image.load("Assets/Images/Items/generator.png").convert_alpha()
        self.generator_highlight_btn_img = pg.image.load("Assets/Images/Items/generator_highlight.png").convert_alpha()
        self.admin_control_btn1_img = pg.image.load("Assets/Images/Items/admin_control1.png").convert_alpha()
        self.admin_control_highlight_btn1_img = pg.image.load(
            "Assets/Images/Items/admin_control1_highlight.png").convert_alpha()
        self.admin_control_btn2_img = pg.image.load("Assets/Images/Items/admin_control2.png").convert_alpha()
        self.admin_control_highlight_btn2_img = pg.image.load(
            "Assets/Images/Items/admin_control2_highlight.png").convert_alpha()
        self.garbage_liver_img = pg.image.load("Assets/Images/Items/garbage_liver.png").convert_alpha()
        self.garbage_liver_highlight_img = pg.image.load(
            "Assets/Images/Items/garbage_liver_highlight.png").convert_alpha()
        self.wifi_highlight_img = pg.image.load("Assets/Images/Items/wifi_highlight.png").convert_alpha()
        self.wifi_img = pg.image.load("Assets/Images/Items/wifi.png").convert_alpha()
        self.wifi_connected_img = pg.image.load("Assets/Images/Items/wifi_connected.png").convert_alpha()
        self.electricity_wire_switch_highlight_img = pg.image.load(
            "Assets/Images/Items/electricity_wires_highlight.png").convert_alpha()
        self.electricity_wire_switch_img = pg.image.load("Assets/Images/Items/electricity_wires.png").convert_alpha()
        self.electricity_wire_switch_connected_img = pg.image.load(
            "Assets/Images/Items/electricity_wires_connected.png").convert_alpha()
        self.view_security_monitor_img = pg.image.load("Assets/Images/Items/security_monitor.png").convert_alpha()
        self.view_security_monitor_highlight_img = pg.image.load(
            "Assets/Images/Items/security_monitor_highlight.png").convert_alpha()
        self.divert_power_to_reactor_highlight_img = pg.image.load(
            "Assets/Images/Items/power_divert_highlight.png").convert_alpha()
        self.divert_power_to_reactor_img = pg.image.load("Assets/Images/Items/power_divert.png").convert_alpha()
        self.divert_power_to_reactor_diverted_img = pg.image.load(
            "Assets/Images/Items/power_diverted.png").convert_alpha()
        self.gas_can_img = pg.image.load("Assets/Images/Items/gas_can.png").convert_alpha()
        self.gas_can_highlight_img = pg.image.load("Assets/Images/Items/gas_can_highlighted.png").convert_alpha()
        self.fuel_engine_hoze_img = pg.image.load("Assets/Images/Items/fuel_engine.png").convert_alpha()
        self.fuel_engine_hoze_highlight_img = pg.image.load(
            "Assets/Images/Items/fuel_engine_highlighted.png").convert_alpha()

    def load_ambient_sounds(self):
        """Cafeteria Ambient Sound"""
        c = pg.Vector2(3277, 658)
        d = pg.Vector2(self.game.player.pos.x, self.game.player.pos.y)
        if d.distance_to(c) <= CAFETERIA_AMBIENT_DETECT_RADIUS:
            if self.cafeteria_sound_play_check:
                self.game.ambient_sounds['cafeteria'].play(-1, -1, 500)
                self.cafeteria_sound_play_check = False
                # pg.mixer.music.set_volume(0.5)
                # pg.mixer.music.pause()
        else:
            self.game.ambient_sounds['cafeteria'].fadeout(1000)
            self.cafeteria_sound_play_check = True
            # pg.mixer.music.unpause()
            # pg.mixer.music.set_volume(1)

        """Medbay Ambient Sound"""
        i = pygame.Vector2(2338, 1147)
        j = pygame.Vector2(self.game.player.pos.x, self.game.player.pos.y)
        if i.distance_to(j) <= MEDBAY_AMBIENT_DETECT_RADIUS:
            if self.medbay_sound_play_check:
                self.game.ambient_sounds['medbay_room'].play(-1, -1, 500)
                self.medbay_sound_play_check = False
        else:
            self.game.ambient_sounds['medbay_room'].fadeout(1000)
            # self.ambient_sounds['cafeteria'].stop()
            self.medbay_sound_play_check = True

        """Security Room Ambient Sound"""
        s = pygame.Vector2(1806, 1279)
        t = pygame.Vector2(self.game.player.pos.x, self.game.player.pos.y)
        if s.distance_to(t) <= SECURITY_ROOM_AMBIENT_DETECT_RADIUS:
            if self.security_room_sound_play_check:
                self.game.ambient_sounds['security_room'].play(-1, -1, 1000)
                self.security_room_sound_play_check = False

        else:
            self.game.ambient_sounds['security_room'].fadeout(1500)
            # self.ambient_sounds['cafeteria'].stop()
            self.security_room_sound_play_check = True

        """Reactor Room Ambient Sound"""
        s = pygame.Vector2(880, 1474)
        t = pygame.Vector2(self.game.player.pos.x, self.game.player.pos.y)
        if s.distance_to(t) <= REACTOR_ROOM_AMBIENT_DETECT_RADIUS:
            if self.reactor_room_sound_play_check:
                self.game.ambient_sounds['reactor_room'].play(-1, -1, 1000)
                self.reactor_room_sound_play_check = False
        else:
            self.game.ambient_sounds['reactor_room'].fadeout(1500)
            # self.ambient_sounds['cafeteria'].stop()
            self.reactor_room_sound_play_check = True

        """Upper Engine Room Ambient Sound"""
        s = pygame.Vector2(1360, 699)
        t = pygame.Vector2(self.game.player.pos.x, self.game.player.pos.y)
        if s.distance_to(t) <= ENGINE_ROOM_AMBIENT_DETECT_RADIUS:
            if self.upper_engine_room_sound_play_check:
                self.game.ambient_sounds['u_engine_room'].play(-1, -1, 1000)
                self.upper_engine_room_sound_play_check = False
        else:
            self.game.ambient_sounds['u_engine_room'].fadeout(1500)
            # self.ambient_sounds['cafeteria'].stop()
            self.upper_engine_room_sound_play_check = True

        """Lower Engine Room Ambient Sound"""
        u = pygame.Vector2(1360, 2180)
        v = pygame.Vector2(self.game.player.pos.x, self.game.player.pos.y)
        # But if player has picked a gas can and he is in lower engine room
        # then keep ambient sound stop until he fills the fuel
        if u.distance_to(v) <= ENGINE_ROOM_AMBIENT_DETECT_RADIUS and not self.game.is_gas_can_picked:
            if self.lower_engine_room_sound_play_check:
                self.game.ambient_sounds['l_engine_room'].play(-1, -1, 1000)
                self.lower_engine_room_sound_play_check = False
        else:
            # if player is not in radius of lower engine but has not picked up
            # gas can then fadeout ambient sound as usual on leaving the room
            self.game.ambient_sounds['l_engine_room'].fadeout(1500)
            self.lower_engine_room_sound_play_check = True

            # But if player has picked a gas can and he is not in room OR he is
            # in the room then keep ambient sound stop until he fills the fuel
            if self.game.is_gas_can_picked:
                self.game.ambient_sounds['l_engine_room'].fadeout(1500)
                # self.ambient_sounds['cafeteria'].stop()
                self.lower_engine_room_sound_play_check = True

        """Electrical Room Ambient Sound"""
        x = pygame.Vector2(2425, 1950)
        y = pygame.Vector2(self.game.player.pos.x, self.game.player.pos.y)
        if x.distance_to(y) <= ELECTRICAL_ROOM_AMBIENT_DETECT_RADIUS:
            if self.electrical_room_sound_play_check:
                self.game.ambient_sounds['electrical_room'].play(-1, -1, 1000)
                self.electrical_room_sound_play_check = False
        else:
            self.game.ambient_sounds['electrical_room'].fadeout(1500)
            # self.ambient_sounds['cafeteria'].stop()
            self.electrical_room_sound_play_check = True

        """Storage Room Ambient Sound"""
        strg_rm = pygame.Vector2(3175, 2308)
        plyr_pos = pygame.Vector2(self.game.player.pos.x, self.game.player.pos.y)
        if strg_rm.distance_to(plyr_pos) <= STORAGE_ROOM_AMBIENT_DETECT_RADIUS:
            if self.storage_room_sound_play_check:
                self.game.ambient_sounds['storage_room'].play(-1, -1, 1000)
                self.storage_room_sound_play_check = False
        else:
            self.game.ambient_sounds['storage_room'].fadeout(1500)
            # self.ambient_sounds['cafeteria'].stop()
            self.storage_room_sound_play_check = True

        """Admin Room Ambient Sound"""
        g = pygame.Vector2(3920, 1775)
        q = pygame.Vector2(self.game.player.pos.x, self.game.player.pos.y)
        if g.distance_to(q) <= ADMIN_ROOM_AMBIENT_DETECT_RADIUS:
            if self.admin_room_sound_play_check:
                self.game.ambient_sounds['admin_room'].play(-1, -1, 1000)
                self.admin_room_sound_play_check = False
        else:
            self.game.ambient_sounds['admin_room'].fadeout(1500)
            self.admin_room_sound_play_check = True

        """Communication Room Ambient Sound"""
        comms_rm = pygame.Vector2(3865, 2650)
        plyr_pos = pygame.Vector2(self.game.player.pos.x, self.game.player.pos.y)
        if comms_rm.distance_to(plyr_pos) <= COMMUNICATION_ROOM_AMBIENT_DETECT_RADIUS:
            if self.communication_room_sound_play_check:
                self.game.ambient_sounds['comms3'].play(-1, -1, 1000)
                self.communication_room_sound_play_check = False
        else:
            self.game.ambient_sounds['comms3'].fadeout(1500)
            self.communication_room_sound_play_check = True

        """OXYGEN Room Ambient Sound"""
        oxygen_rm = pygame.Vector2(4190, 1220)
        plyr_posz = pygame.Vector2(self.game.player.pos.x, self.game.player.pos.y)
        if oxygen_rm.distance_to(plyr_posz) <= OXYGEN_ROOM_AMBIENT_DETECT_RADIUS:
            if self.oxygen_room_sound_play_check:
                print("p ppos:" + str(plyr_posz))
                self.game.ambient_sounds['oxygen_room'].play(-1, -1, 1000)
                self.oxygen_room_sound_play_check = False
        else:
            self.game.ambient_sounds['oxygen_room'].fadeout(1500)
            self.oxygen_room_sound_play_check = True

        """Cockpit Room Ambient Sound"""
        ckpit_rm = pygame.Vector2(5405, 1340)
        plyr_posx = pygame.Vector2(self.game.player.pos.x, self.game.player.pos.y)
        if ckpit_rm.distance_to(plyr_posx) <= COCKPIT_ROOM_AMBIENT_DETECT_RADIUS:
            if self.cockpit_room_sound_play_check:
                self.game.ambient_sounds['cockpit'].play(-1, -1, 1000)
                self.cockpit_room_sound_play_check = False
        else:
            self.game.ambient_sounds['cockpit'].fadeout(1500)
            self.cockpit_room_sound_play_check = True

        """Weapon Room Ambient Sound"""
        wpn_rm = pygame.Vector2(4500, 600)
        plyr_posu = pygame.Vector2(self.game.player.pos.x, self.game.player.pos.y)
        if wpn_rm.distance_to(plyr_posu) <= WEAPON_ROOM_AMBIENT_DETECT_RADIUS:
            if self.weapons_room_sound_play_check and self.game.clear_asteroid_task_play_count ==1:
                self.game.ambient_sounds['weapons'].play(-1, -1, 1000)
                self.weapons_room_sound_play_check = False
        else:
            self.game.ambient_sounds['weapons'].fadeout(1500)
            self.weapons_room_sound_play_check = True

    def load_glow_objects(self):
        """YES"""
        """Cafeteria Computer Glow object"""
        c = pygame.Vector2(3060, 385)
        d = pygame.Vector2(self.game.player.pos.x, self.game.player.pos.y)
        # if player is in range of object to glow, and game mod is freeplay only then, that object will glow
        if d.distance_to(c) <= 400 and self.game.gamemode == "Freeplay":
            self.game.map_img.blit(self.cafeteria_comp_highlighted_img, (3062, 387))
        else:
            self.game.map_img.blit(self.cafeteria_comp_img, (3062, 387))
        """YES"""

        """YES"""
        """Emergency Meeting Glow object"""
        c = pygame.Vector2(3284, 669)
        d = pygame.Vector2(self.game.player.pos.x, self.game.player.pos.y)
        if d.distance_to(c) <= DETECT_RADIUS:
            self.game.map_img.blit(self.emergency_button_highlighted_img, (3284, 669))
        else:
            self.game.map_img.blit(self.emergency_button_img, (3284, 669))
        """YES"""

        """Task - Clear Asteroid Glow object"""
        c = pygame.Vector2(4513, 450)
        d = pygame.Vector2(self.game.player.pos.x, self.game.player.pos.y)
        if d.distance_to(c) <= DETECT_RADIUS and self.game.clear_asteroid_task_play_count == 1:
            self.game.map_img.blit(self.nav_highlighted_img, (4513, 452))
        else:
            self.game.map_img.blit(self.nav_img, (4513, 452))

        """Task - Turn On Reactor Glow object"""
        c = pygame.Vector2(889, 999)
        d = pygame.Vector2(self.game.player.pos.x, self.game.player.pos.y)

        if self.game.night_reactor == True:
            self.Turn_On_Reactor_is_available = True
        else:
            self.Turn_On_Reactor_is_available = False

        if c.distance_to(d) <= DETECT_RADIUS:
            self.game.map_img.blit(self.reactor_highlight_btn_img, (889, 996))
        else:
            self.game.map_img.blit(self.reactor_btn_img, (889, 996))

        """Task - Turn On Lower Engine Glow object"""
        c = pygame.Vector2(1127, 2318)
        d = pygame.Vector2(self.game.player.pos.x, self.game.player.pos.y)
        if c.distance_to(d) <= DETECT_RADIUS:
            self.game.map_img.blit(self.lower_highlight_engine_img, (1127, 2318))
        else:
            self.game.map_img.blit(self.lower_engine_img, (1127, 2318))

        """Task - Align Engine Output Glow object"""
        c = pygame.Vector2(1117, 837)
        d = pygame.Vector2(self.game.player.pos.x, self.game.player.pos.y)
        if c.distance_to(d) <= DETECT_RADIUS and self.game.align_engine_output_task_play_count == 1:
            self.game.map_img.blit(self.upper_engine_highlight_img, (1117, 837))
        else:
            self.game.map_img.blit(self.upper_engine_img, (1117, 837))

        """Task - Stabilize Navigation Glow object"""
        self.stabilize_steering_button_status = True
        c = pygame.Vector2(5610, 1290)
        d = pygame.Vector2(self.game.player.pos.x, self.game.player.pos.y)
        if c.distance_to(d) <= DETECT_RADIUS and self.game.stabilize_task_play_count == 1:
            self.game.map_img.blit(self.navigation_highlight_img, (5610, 1290))
        else:
            self.game.map_img.blit(self.navigation_img, (5610, 1290))
        if self.game.stabilize_task_play_count !=1:
            self.game.map_img.blit(self.navigation_img, (5610, 1290))


        """Task - Turn On Generator Glow object"""
        if self.game.night == True:
            self.turn_on_generator_is_available = True
        else:
            self.turn_on_generator_is_available = False

        c = pygame.Vector2(2472, 1721)
        d = pygame.Vector2(self.game.player.pos.x, self.game.player.pos.y)
        if c.distance_to(d) <= DETECT_RADIUS:
            self.game.map_img.blit(self.generator_highlight_btn_img, (2472, 1721))
        else:
            self.game.map_img.blit(self.generator_btn_img, (2472, 1721))

        """Task - Admin Control Buttons Glow object"""
        c = pygame.Vector2(3817, 1806)
        d = pygame.Vector2(self.game.player.pos.x, self.game.player.pos.y)
        e = pygame.Vector2(4070, 1804)
        if c.distance_to(d) <= DETECT_RADIUS:
            self.game.map_img.blit(self.admin_control_highlight_btn1_img, (3815, 1804))
        else:
            self.game.map_img.blit(self.admin_control_btn1_img, (3815, 1804))
        if e.distance_to(d) <= DETECT_RADIUS:
            self.game.map_img.blit(self.admin_control_highlight_btn2_img, (4068, 1803))
        else:
            self.game.map_img.blit(self.admin_control_btn2_img, (4068, 1803))

        """Task - Empty the Garbage Glow object"""
        c = pygame.Vector2(3940, 321)
        d = pygame.Vector2(self.game.player.pos.x, self.game.player.pos.y)
        if c.distance_to(d) <= DETECT_RADIUS and self.game.empty_garbage_task_play_count == 1:
            self.game.map_img.blit(self.garbage_liver_highlight_img, (3940, 321))
        else:
            self.game.map_img.blit(self.garbage_liver_img, (3940, 321))

        """Task - Reboot Wifi Glow object"""
        x = pygame.Vector2(3700, 1554)
        y = pygame.Vector2(self.game.player.pos.x, self.game.player.pos.y)
        if x.distance_to(y) <= DETECT_RADIUS and self.game.reboot_wifi_task_play_count == 1:
            self.game.map_img.blit(self.wifi_highlight_img, (3700, 1554))
        else:
            self.game.map_img.blit(self.wifi_img, (3699, 1553))
        if self.game.reboot_wifi_task_play_count !=1:
            self.game.map_img.blit(self.wifi_connected_img, (3699, 1553))

        """Task - Fix Electricity Wires Glow object"""
        x = pygame.Vector2(3166, 1846)
        y = pygame.Vector2(self.game.player.pos.x, self.game.player.pos.y)
        if x.distance_to(y) <= DETECT_RADIUS and self.game.electricity_wire_task_play_count == 1:
            self.game.map_img.blit(self.electricity_wire_switch_highlight_img, (3166, 1846))
        else:
            self.game.map_img.blit(self.electricity_wire_switch_img, (3166, 1846))
        if self.game.electricity_wire_task_play_count !=1:
            self.game.map_img.blit(self.electricity_wire_switch_connected_img, (3166, 1846))

        """View Security Room Monitor Glow object"""
        sec_rm = pygame.Vector2(1756, 1056)
        plyrposs = pygame.Vector2(self.game.player.pos.x, self.game.player.pos.y)
        if sec_rm.distance_to(plyrposs) <= VIEW_SECURITY_MONITOR_RADIUS:
            self.game.map_img.blit(self.view_security_monitor_highlight_img, (1756, 1062))
        else:
            self.game.map_img.blit(self.view_security_monitor_img, (1756, 1056))

        """Divert Power to Reactor Glow object"""
        pwr_rec_rm = pygame.Vector2(1031, 1216)
        plyrposs = pygame.Vector2(self.game.player.pos.x, self.game.player.pos.y)
        if pwr_rec_rm.distance_to(plyrposs) <= DETECT_RADIUS:
            self.game.map_img.blit(self.divert_power_to_reactor_highlight_img, (1031, 1213))
        else:
            self.game.map_img.blit(self.divert_power_to_reactor_img, (1031, 1213))
        if self.game.divert_power_to_reactor_task_play_count !=1:
            self.game.map_img.blit(self.divert_power_to_reactor_diverted_img, (1031, 1213))

        """Task - Storage Gas Can Glow object"""
        x = pygame.Vector2(3056, 2443)
        y = pygame.Vector2(self.game.player.pos.x, self.game.player.pos.y)
        if x.distance_to(y) <= DETECT_RADIUS and self.game.fuel_engine_task_play_count == 1:
            self.game.map_img.blit(self.gas_can_highlight_img, (3056, 2443))
        else:
            self.game.map_img.blit(self.gas_can_img, (3056, 2443))

        """Task - Fuel Engine Glow object"""
        x = pygame.Vector2(1226, 2300)
        y = pygame.Vector2(self.game.player.pos.x, self.game.player.pos.y)
        if x.distance_to(y) <= DETECT_RADIUS and self.game.fuel_engine_task_play_count ==1:
            self.game.map_img.blit(self.fuel_engine_hoze_highlight_img, (1226, 2300))
        else:
            self.game.map_img.blit(self.fuel_engine_hoze_img, (1226, 2300))

