import pygame as pg
from settings import *

class Task():
    def __init__(self, game):
        self.game = game
        self.task_array = []
        self.turn_on_the_lights_mission_status = False
        self.clear_asteroids_mission_status = False
        self.turn_on_the_lights_task_title = "Turn On The Lights"
        self.turn_on_the_lights_task_title_visibility_status = False
        self.stabilize_nav_task_title = "Stabilize The Ship's Navigation"
        self.stabilize_nav_task_title_visibility_status = False
        self.reboot_the_wifi_task_title = "Reboot The Wifi"
        self.reboot_the_wifi_task_title_visibility_status = False
        self.empty_the_garbage_task_title = "Empty The Garbage"
        self.empty_the_garbage_task_title_visibility_status = False
        self.fix_electircity_wires_task_title = "Fix The Electricity Wires"
        self.fix_electircity_wires_task_title_visibility_status = False
        self.divert_power_to_reactor_task_title = "Divert Power To Reactor"
        self.divert_power_to_reactor_task_title_visibility_status = False
        self.align_engine_output_task_title = "Align Engine Output"
        self.align_engine_output_title_visibility_status = False
        self.fuel_engine_task_title = "Fuel Lower Engine"
        self.fuel_engine_task_title_visibility_status = False
        self.clear_asteroids_task_title = "Clear the Asteroids (30)"
        self.clear_asteroids_task_title_visibility_status = False


    def turn_on_the_lights(self):
        hits = pg.sprite.spritecollide(self.game.player, self.game.items, False)
        # hit is the object being collided with player
        # hit name is the object name in tiled map
        # Turn on the light through button
        for hit in hits:
            if hit.type == 'health' and self.game.night == True:
                self.game.night = False
                hit.kill()
                self.game.effect_sounds['task_completed'].play()
        for hit in hits:
            if hit.type == 'weapon' and self.game.night == True:
                self.game.night = False
                self.game.effect_sounds['task_completed'].play()
                hit.kill()
        for hit in hits:
            if hit.type == 'weapon' and self.game.night == True:
                self.game.night = False
                self.game.effect_sounds['task_completed'].play()
                hit.kill()




