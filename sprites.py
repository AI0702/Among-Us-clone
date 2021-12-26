import time
import pygame as pg
from os import path
import sys
from settings import *
vec = pg.math.Vector2
from os import path
import random


class Player(pg.sprite.Sprite):
    def __init__(self, game, pos, player_id, player_islocal, player_colour):
        self._layer = PLAYER_LAYER
        if player_islocal:
            self.groups = game.all_sprites
        else:
            self.groups = game.all_sprites, game.players_server
        #self.groupsplayer = game.players
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        #self.image = game.player_imgs_left[0]
        # wtf?
        self.player_id = player_id
        self.alive_status = True
        self.player_islocal = player_islocal
        self.player_imgs_left = []
        self.player_imgs_right = []
        self.player_imgs_down = []
        self.player_imgs_up = []
        self.image = red_player_imgs_down[0]
        self.sync_img = "self.Players[p[0]].player_imgs_down"
        self.sync_img_index = "[0]"
        self.left_img_index = 0
        self.right_img_index = 0
        self.up_img_index = 0
        self.down_img_index = 0
        self.image_dead = None
        self.player_colour = player_colour
        if self.player_colour == "Red":
            self.player_imgs_left = red_player_imgs_left
            self.player_imgs_right = red_player_imgs_right
            self.player_imgs_down = red_player_imgs_down
            self.player_imgs_up = red_player_imgs_up
            self.image = red_player_imgs_down[0]
            self.image_dead = red_player_imgs_dead
            self.image_ghost_left = red_player_imgs_ghost_left
            self.image_ghost_right = red_player_imgs_ghost_right
            self.emergency_meeting_img = red_player_emergency_meeting
            self.emergency_meeting_img_sync = "red_player_emergency_meeting"
            self.emergency_meeting_img_sync_report = "red_player_emergency_meeting_report"
            self.eject_img = "red_player_imgs_right[9]"
        if self.player_colour == "Blue":
            self.player_imgs_left = blue_player_imgs_left
            self.player_imgs_right = blue_player_imgs_right
            self.player_imgs_down = blue_player_imgs_down
            self.player_imgs_up = blue_player_imgs_up
            self.image = blue_player_imgs_down[0]
            self.image_dead = blue_player_imgs_dead
            self.image_ghost_left = blue_player_imgs_ghost_left
            self.image_ghost_right = blue_player_imgs_ghost_right
            self.emergency_meeting_img = blue_player_emergency_meeting
            self.emergency_meeting_img_sync = "blue_player_emergency_meeting"
            self.emergency_meeting_img_sync_report = "blue_player_emergency_meeting_report"
            self.eject_img = "blue_player_imgs_right[9]"
        if self.player_colour == "Orange":
            self.player_imgs_left = orange_player_imgs_left
            self.player_imgs_right = orange_player_imgs_right
            self.player_imgs_down = orange_player_imgs_down
            self.player_imgs_up = orange_player_imgs_up
            self.image = orange_player_imgs_down[0]
            self.image_dead = orange_player_imgs_dead
            self.image_ghost_left = orange_player_imgs_ghost_left
            self.image_ghost_right = orange_player_imgs_ghost_right
            self.emergency_meeting_img = orange_player_emergency_meeting
            self.emergency_meeting_img_sync = "orange_player_emergency_meeting"
            self.emergency_meeting_img_sync_report = "orange_player_emergency_meeting_report"
            self.eject_img = "orange_player_imgs_right[9]"
        if self.player_colour == "Yellow":
            self.player_imgs_left = yellow_player_imgs_left
            self.player_imgs_right = yellow_player_imgs_right
            self.player_imgs_down = yellow_player_imgs_down
            self.player_imgs_up = yellow_player_imgs_up
            self.image = yellow_player_imgs_down[0]
            self.image_dead = yellow_player_imgs_dead
            self.image_ghost_left = yellow_player_imgs_ghost_left
            self.image_ghost_right = yellow_player_imgs_ghost_right
            self.emergency_meeting_img = yellow_player_emergency_meeting
            self.emergency_meeting_img_sync = "yellow_player_emergency_meeting"
            self.emergency_meeting_img_sync_report = "yellow_player_emergency_meeting_report"
            self.eject_img = "yellow_player_imgs_right[9]"
        if self.player_colour == "Green":
            self.player_imgs_left = green_player_imgs_left
            self.player_imgs_right = green_player_imgs_right
            self.player_imgs_down = green_player_imgs_down
            self.player_imgs_up = green_player_imgs_up
            self.image = green_player_imgs_down[0]
            self.image_dead = green_player_imgs_dead
            self.image_ghost_left = green_player_imgs_ghost_left
            self.image_ghost_right = green_player_imgs_ghost_right
            self.emergency_meeting_img = green_player_emergency_meeting
            self.emergency_meeting_img_sync = "green_player_emergency_meeting"
            self.emergency_meeting_img_sync_report = "green_player_emergency_meeting_report"
            self.eject_img = "green_player_imgs_right[9]"
        #self.image = game.player_imgs_left[0]
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect
        self.vel = vec(0, 0)    # velocity init to zero
        #self.pos = vec(x, y) * TILESIZE
        #self.emerg_play_count = 1
        self.pos = vec(pos)
        self.pos_corpse = vec(0, 0)
        self.pos_corpse_img = "self.Players[p[0]].image_dead"
        self.pos_corpse_img_index = ""
        self.ghost_img = "self.invsible_player_image"
        self.ghost_img_index = ""
        self.last_played = 0
        self.now = 0
        self.tasks_completed = 0
        self.victim_id = 0
        self.victim_id_report = 0
        self.imposter = False
        self.voted = None
        self.got_votes = 0
        self.got_reported = False
        
    # Check which key or combination of keys are being pressed
    # Control player movement speed
    def get_keys(self):
        if self.player_islocal == True and self.alive_status == True and self.game.emergency == False:
            self.vel = vec(0, 0)
            keys = pg.key.get_pressed()
            # key f + L/R/U/D to allow move once hidden
            #self.game.invisible_play_count = 0
            if (keys[pg.K_LEFT] and not self.game.isdoingTask or keys[pg.K_a] and not self.game.isdoingTask) and self.game.invisible_play_count == 0:
                self.now = pg.time.get_ticks()
                self.image = self.player_imgs_left[self.left_img_index]
                self.sync_img = "self.Players[p[0]].player_imgs_left"
                self.sync_img_index = "[p[6]]"
                self.left_img_index += 1
                # if image is the last image of array then point it to 0 index means first image i.e restart
                if self.left_img_index >= len(self.player_imgs_left):
                    self.left_img_index = 0
                self.vel.x = - PLAYER_SPEED
                # Below statements are used to add interval between each footstep sound
                # if last footstep time is greater than Current time
                if self.now - self.last_played > stepping_rate:
                    self.last_played = self.now
                    random.choice(self.game.foot_sounds['footsteps']).play()
            if (keys[pg.K_RIGHT] and not self.game.isdoingTask or keys[pg.K_d] and not self.game.isdoingTask) and self.game.invisible_play_count == 0:
                self.now = pg.time.get_ticks()
                self.image = self.player_imgs_right[self.right_img_index]
                self.sync_img = "self.Players[p[0]].player_imgs_right"
                self.sync_img_index = "[p[7]]"
                self.right_img_index += 1
                # if image is the last image of array then point it to 0 index means first image i.e restart
                if self.right_img_index >= len(self.player_imgs_right):
                    self.right_img_index = 0
                self.vel.x = PLAYER_SPEED
                if self.now - self.last_played > stepping_rate:
                    self.last_played = self.now
                    random.choice(self.game.foot_sounds['footsteps']).play()
            if (keys[pg.K_UP] and not self.game.isdoingTask or keys[pg.K_w] and not self.game.isdoingTask) and self.game.invisible_play_count == 0:
                self.now = pg.time.get_ticks()
                self.image = self.player_imgs_up[self.up_img_index]
                self.sync_img = "self.Players[p[0]].player_imgs_up"
                self.sync_img_index = "[p[8]]"
                self.up_img_index += 1
                # if image is the last image of array then point it to 0 index means first image i.e restart
                if self.up_img_index >= len(self.player_imgs_up):
                    self.up_img_index = 0
                self.vel.y = - PLAYER_SPEED
                if self.now - self.last_played > stepping_rate:
                    self.last_played = self.now
                    random.choice(self.game.foot_sounds['footsteps']).play()
            if (keys[pg.K_DOWN] and not self.game.isdoingTask or keys[pg.K_s] and not self.game.isdoingTask) and self.game.invisible_play_count == 0:
                self.now = pg.time.get_ticks()
                self.image = self.player_imgs_down[self.down_img_index]
                self.sync_img = "self.Players[p[0]].player_imgs_down"
                self.sync_img_index = "[p[9]]"
                self.down_img_index += 1
                # if image is the last image of array then point it to 0 index means first image i.e restart
                if self.down_img_index >= len(self.player_imgs_down):
                    self.down_img_index = 0
                self.vel.y = PLAYER_SPEED
                if self.now - self.last_played > stepping_rate:
                    self.last_played = self.now
                    random.choice(self.game.foot_sounds['footsteps']).play()
            if (keys[pg.K_DOWN] and keys[pg.K_LEFT] and not self.game.isdoingTask or keys[pg.K_s] and keys[pg.K_a] and not self.game.isdoingTask or keys[pg.K_UP] and keys[pg.K_LEFT] and not self.game.isdoingTask or keys[pg.K_w] and keys[pg.K_a] and not self.game.isdoingTask) and self.game.invisible_play_count == 0:
                self.now = pg.time.get_ticks()
                self.image = self.player_imgs_left[self.left_img_index]
                self.sync_img = "self.Players[p[0]].player_imgs_left"
                self.sync_img_index = "[p[6]]"
                # left intentionally zero because upper loop is incremeting also
                # and if we also +1 in index it will double the speed of animation
                self.left_img_index += 0
                # if image is the last image of array then point it to 0 index means first image i.e restart
                if self.left_img_index >= len(self.player_imgs_left):
                    self.left_img_index = 0
                if self.now - self.last_played > stepping_rate:
                    self.last_played = self.now
                    random.choice(self.game.foot_sounds['footsteps']).play()
            if (keys[pg.K_DOWN] and keys[pg.K_RIGHT] and not self.game.isdoingTask or keys[pg.K_s] and keys[pg.K_d] and not self.game.isdoingTask or keys[pg.K_UP] and keys[pg.K_RIGHT] and not self.game.isdoingTask or keys[pg.K_w] and keys[pg.K_d] and not self.game.isdoingTask) and self.game.invisible_play_count == 0:
                self.now = pg.time.get_ticks()
                self.left_img_index = self.right_img_index
                self.image = self.player_imgs_right[self.right_img_index]
                self.sync_img = "self.Players[p[0]].player_imgs_right"
                self.sync_img_index = "[p[7]]"
                # left intentionally zero because upper loop is incremeting also
                # and if we also +1 in index it will double the speed of animation
                self.right_img_index += 0
                # if image is the last image of array then point it to 0 index means first image i.e restart
                if self.right_img_index >= len(self.player_imgs_right):
                    self.right_img_index = 0
                self.vel.x = PLAYER_SPEED
                if self.now - self.last_played > stepping_rate:
                    self.last_played = self.now
                    random.choice(self.game.foot_sounds['footsteps']).play()
            
            if self.vel.x != 0 and self.vel.y != 0:
                self.vel *= 0.7071
            
            
        elif self.player_islocal == True and self.alive_status == False and self.game.emergency == False:
            self.vel = vec(0, 0)
            keys = pg.key.get_pressed()
            # key f + L/R/U/D to allow move once hidden
            #self.game.invisible_play_count = 0
            
            if keys[pg.K_LEFT] or keys[pg.K_a]:
                self.vel.x = - PLAYER_SPEED
                self.image = self.image_ghost_left
            
            if keys[pg.K_RIGHT] or keys[pg.K_d]:
                self.vel.x = PLAYER_SPEED
                self.image = self.image_ghost_right
            
            if keys[pg.K_UP] or keys[pg.K_w]:
                self.vel.y = - PLAYER_SPEED
            
            if keys[pg.K_DOWN] or keys[pg.K_s]:
                self.vel.y = PLAYER_SPEED
            
            #if keys[pg.K_DOWN] and keys[pg.K_RIGHT] or keys[pg.K_s] and keys[pg.K_d] or keys[pg.K_UP] and keys[pg.K_RIGHT] or keys[pg.K_w] and keys[pg.K_d]:
            #    self.vel.x = PLAYER_SPEED

            if self.vel.x != 0 and self.vel.y != 0:
                self.vel *= 0.7071

    def collide_with_walls(self, dir):
        if self.alive_status == True:    
            if dir == 'x':
                hits = pg.sprite.spritecollide(self, self.game.walls, False)
                if hits:
                # if hits with object on left or right side
                # if we hit from right -- x is +ve for right direction
                    if self.vel.x > 0:
                        self.pos.x = hits[0].rect.left - self.rect.width
                # if we hit from left -- x is -ve for left direction
                    if self.vel.x < 0:
                        self.pos.x = hits[0].rect.right
                # regardless of which direction we hit vx = 0
                    self.vel.x = 0
                    self.rect.x = self.pos.x

            if dir == 'y':
                hits = pg.sprite.spritecollide(self, self.game.walls, False)
                # hit = item/object/sprite
                # hits = hit collide with object/ walls/ spites / sprites group
                if hits:
                # if hits with object on left or right side
                # if we hit from right
                    if self.vel.y > 0:
                        self.pos.y = hits[0].rect.top - self.rect.height
                # if we hit from left
                    if self.vel.y < 0:
                        self.pos.y = hits[0].rect.bottom
                # regardless of which direction we hit vx = 0
                    self.vel.y = 0
                    self.rect.y = self.pos.y


    def update(self):
        self.get_keys()
        # dt = delta time used for frame independent movements - Delta time (time since last tick)
        self.pos += self.vel * self.game.dt

        # 2 collision checks one for each axis x, y
        self.rect.x = self.pos.x    # pos is a vector containing x, y coordinates
        self.collide_with_walls('x')
        self.rect.y = self.pos.y
        self.collide_with_walls('y')

class Bot(pg.sprite.Sprite):
    def __init__(self, game, x, y, bot_direction, bot_type, bot_colour):
        self._layer = BOT_LAYER
        self.groups = game.all_sprites, game.bots
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.alive_status = True
        # self.image = game.player_left_img
        """if direction == "Left":
            self.image = game.player_imgs_left[0]
        else:
            self.image = game.player_imgs_right[0]"""
        
        self.bot_direction = bot_direction
        self.bot_colour = bot_colour
        
        if bot_direction == "Left":
            if bot_colour == "Red":
                self.image = red_player_imgs_left[0]
                self.dead_player_img = red_player_imgs_dead.convert_alpha()
            elif bot_colour == "Blue":
                self.image = blue_player_imgs_left[0]
                self.dead_player_img = blue_player_imgs_dead.convert_alpha()
            elif bot_colour == "Orange":
                self.image = orange_player_imgs_left[0]
                self.dead_player_img = orange_player_imgs_dead.convert_alpha()
            elif bot_colour == "Yellow":
                self.image = yellow_player_imgs_left[0]
                self.dead_player_img = yellow_player_imgs_dead.convert_alpha()
            elif bot_colour == "Green":
                self.image = green_player_imgs_left[0]
                self.dead_player_img = green_player_imgs_dead.convert_alpha()
            elif bot_colour == "Black":
                self.image = black_player_imgs_left[0]
                self.dead_player_img = black_player_imgs_dead.convert_alpha()
            elif bot_colour == "Brown":
                self.image = brown_player_imgs_left[0]
                self.dead_player_img = brown_player_imgs_dead.convert_alpha()
            elif bot_colour == "Pink":
                self.image = pink_player_imgs_left[0]
                self.dead_player_img = pink_player_imgs_dead.convert_alpha()
            elif bot_colour == "Purple":
                self.image = purple_player_imgs_left[0]
                self.dead_player_img = purple_player_imgs_dead.convert_alpha()
            elif bot_colour == "White":
                self.image = white_player_imgs_left[0]
                self.dead_player_img = white_player_imgs_dead.convert_alpha()
        elif bot_direction == "Right":
            if bot_colour == "Red":
                self.image = red_player_imgs_right[0]
                self.dead_player_img = red_player_imgs_dead.convert_alpha()
            elif bot_colour == "Blue":
                self.image = blue_player_imgs_right[0]
                self.dead_player_img = blue_player_imgs_dead.convert_alpha()
            elif bot_colour == "Orange":
                self.image = orange_player_imgs_right[0]
                self.dead_player_img = orange_player_imgs_dead.convert_alpha()
            elif bot_colour == "Yellow":
                self.image = yellow_player_imgs_right[0]
                self.dead_player_img = yellow_player_imgs_dead.convert_alpha()
            elif bot_colour == "Green":
                self.image = green_player_imgs_right[0]
                self.dead_player_img = green_player_imgs_dead.convert_alpha()
            elif bot_colour == "Black":
                self.image = black_player_imgs_right[0]
                self.dead_player_img = black_player_imgs_dead.convert_alpha()
            elif bot_colour == "Brown":
                self.image = brown_player_imgs_right[0]
                self.dead_player_img = brown_player_imgs_dead.convert_alpha()
            elif bot_colour == "Pink":
                self.image = pink_player_imgs_right[0]
                self.dead_player_img = pink_player_imgs_dead.convert_alpha()
            elif bot_colour == "Purple":
                self.image = purple_player_imgs_right[0]
                self.dead_player_img = purple_player_imgs_dead.convert_alpha()
            elif bot_colour == "White":
                self.image = white_player_imgs_right[0]
                self.dead_player_img = white_player_imgs_dead.convert_alpha()
        elif bot_direction == "Up":
            if bot_colour == "Red":
                self.image = red_player_imgs_up[0]
                self.dead_player_img = red_player_imgs_dead.convert_alpha()
            elif bot_colour == "Blue":
                self.image = blue_player_imgs_up[0]
                self.dead_player_img = blue_player_imgs_dead.convert_alpha()
            elif bot_colour == "Orange":
                self.image = orange_player_imgs_up[0]
                self.dead_player_img = orange_player_imgs_dead.convert_alpha()
            elif bot_colour == "Yellow":
                self.image = yellow_player_imgs_up[0]
                self.dead_player_img = yellow_player_imgs_dead.convert_alpha()
            elif bot_colour == "Green":
                self.image = green_player_imgs_up[0]
                self.dead_player_img = green_player_imgs_dead.convert_alpha()
            elif bot_colour == "Black":
                self.image = black_player_imgs_up[0]
                self.dead_player_img = black_player_imgs_dead.convert_alpha()
            elif bot_colour == "Brown":
                self.image = brown_player_imgs_up[0]
                self.dead_player_img = brown_player_imgs_dead.convert_alpha()
            elif bot_colour == "Pink":
                self.image = pink_player_imgs_up[0]
                self.dead_player_img = pink_player_imgs_dead.convert_alpha()
            elif bot_colour == "Purple":
                self.image = purple_player_imgs_up[0]
                self.dead_player_img = purple_player_imgs_dead.convert_alpha()
            elif bot_colour == "White":
                self.image = white_player_imgs_up[0]
                self.dead_player_img = white_player_imgs_dead.convert_alpha()
        elif bot_direction == "Down":
            if bot_colour == "Red":
                self.image = red_player_imgs_down[0]
                self.dead_player_img = red_player_imgs_dead.convert_alpha()
            elif bot_colour == "Blue":
                self.image = blue_player_imgs_down[0]
                self.dead_player_img = blue_player_imgs_dead.convert_alpha()
            elif bot_colour == "Orange":
                self.image = orange_player_imgs_down[0]
                self.dead_player_img = orange_player_imgs_dead.convert_alpha()
            elif bot_colour == "Yellow":
                self.image = yellow_player_imgs_down[0]
                self.dead_player_img = yellow_player_imgs_dead.convert_alpha()
            elif bot_colour == "Green":
                self.image = green_player_imgs_down[0]
                self.dead_player_img = green_player_imgs_dead.convert_alpha()
            elif bot_colour == "Black":
                self.image = black_player_imgs_down[0]
                self.dead_player_img = black_player_imgs_dead.convert_alpha()
            elif bot_colour == "Brown":
                self.image = brown_player_imgs_down[0]
                self.dead_player_img = brown_player_imgs_dead.convert_alpha()
            elif bot_colour == "Pink":
                self.image = pink_player_imgs_down[0]
                self.dead_player_img = pink_player_imgs_dead.convert_alpha()
            elif bot_colour == "Purple":
                self.image = purple_player_imgs_down[0]
                self.dead_player_img = purple_player_imgs_dead.convert_alpha()
            elif bot_colour == "White":
                self.image = white_player_imgs_down[0]
                self.dead_player_img = white_player_imgs_dead.convert_alpha()
        
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect
        self.vel = vec(0, 0)    # velocity init to zero
        self.pos = vec(x, y)
        self.type = bot_type
        self.play_kill_count = 0
        


    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
            # if hits with object on left or right side
            # if we hit from right -- x is +ve for right direction
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - self.rect.width
            # if we hit from left -- x is -ve for left direction
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right
            # regardless of which direction we hit vx = 0
                self.vel.x = 0
                self.rect.x = self.pos.x

        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            # hit = item/object/sprite
            # hits = hit collide with object/ walls/ spites / sprites group
            if hits:
            # if hits with object on left or right side
            # if we hit from right
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - self.rect.height
            # if we hit from left
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom
            # regardless of which direction we hit vx = 0
                self.vel.y = 0
                self.rect.y = self.pos.y


    def update(self):
        # dt = delta time used for frame independent movements - Delta time (time since last tick)
        self.pos += self.vel * self.game.dt
        # 2 collision checks one for each axis x, y
        self.rect.x = self.pos.x    # pos is a vector containing x, y coordinates
        self.collide_with_walls('x')
        self.rect.y = self.pos.y
        self.collide_with_walls('y')

class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = WALL_LAYER
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.wall_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

# Obstacles are not drawn, are invisible sprites at specific locations
# use to make boundaries and walls
class Obstacle(pg.sprite.Sprite):
    def __init__(self, game, x, y, width, height):
        self.groups = game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        # pg.Rect is used so it can cause collisions
        self.rect = pg.Rect(x, y, width, height)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y


class Item(pg.sprite.Sprite):
    def __init__(self, game, pos, item_type):
        self._layer = ITEM_LAYER
        self.groups = game.all_sprites, game.items
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.item_images[item_type]
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect
        # type = is the name of tile object on tiled map i.e health in this case
        self.type = item_type
        self.rect.center = pos

class Button:
    def __init__(self, game, text, text_size, width, height, x, y, button_type, text_color, color, img_addr, a,b,opacity):
        self.text = text
        self.button_type = button_type
        self.game = game
        self.text_size = text_size
        self.x = x
        self.y = y
        self.color = color
        self.text_color = text_color
        self.width = width
        self.height = height
        #self.image = pg.image.load(path.join(self.game.game_folder, img_addr))
        if img_addr is not None:
            self.image = pg.image.load(path.join(self.game.game_folder, img_addr)).convert_alpha()
            self.image = pg.transform.smoothscale(self.image, (a,b)).convert_alpha()
            self.image.set_alpha(opacity)

            #self.image = pg.image.load(img_addr)
        else:
            self.image = self.game.mini_map_button_img

        self.rect = self.image.get_rect()

    def draw_text(self, win):
        # Draw button on screen
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        # font = pygame.font.SysFont("comicsans", self.text_size)
        font = pg.font.Font(FONT, self.text_size)
        text = font.render(self.text, 1, self.text_color)
        win.blit(text, (self.x + round(self.width / 2) - round(text.get_width() / 2),
                                self.y + round(self.height / 2) - round(text.get_height() / 2)))
    def draw_Image(self, screen):
        # Draw button on screen
        #pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        screen.blit(self.image, (self.x , self.y ))

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False

