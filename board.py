import pygame as pg
import pygame.font

from settings import *
from settings import *


# Board surface on screen to draw menus
class Board:

    def __init__(self, width: int, height: int, game):
        self.surface = pg.display.set_mode((width, height), 0, 32)
        pg.display.set_caption('Among Us')
        self.width = width
        self.height = height
        self.game = game
        self.intro_bg = pg.image.load("Assets/Images/Menu/back.png").convert_alpha()
        self.intro_bg2 = pg.image.load("Assets/Images/Menu/back2.png").convert_alpha()
        self.intro_title = pg.image.load("Assets/Images/Menu/title.png").convert_alpha()
        self.intro_menu1 = pg.image.load("Assets/Images/Menu/freeplay.png").convert_alpha()
        self.intro_menu2 = pg.image.load("Assets/Images/Menu/online.png").convert_alpha()
        self.intro_menu3 = pg.image.load("Assets/Images/Menu/help.png").convert_alpha()
        self.intro_menu4 = pg.image.load("Assets/Images/Menu/credits.png").convert_alpha()
        self.intro_menu5 = pg.image.load("Assets/Images/Menu/quit.png").convert_alpha()
        self.intro_color1 = pg.image.load("Assets/Images/Menu/blue.png").convert_alpha()
        self.intro_color2 = pg.image.load("Assets/Images/Menu/green.png").convert_alpha()
        self.intro_color3 = pg.image.load("Assets/Images/Menu/yellow.png").convert_alpha()
        self.intro_color4 = pg.image.load("Assets/Images/Menu/red.png").convert_alpha()
        self.intro_color5 = pg.image.load("Assets/Images/Menu/orange.png").convert_alpha()
        self.intro_choosecolour = pg.image.load("Assets/Images/Menu/choosecolour.png").convert_alpha()
        self.intro_return = pg.image.load("Assets/Images/Menu/return.png").convert_alpha()
        self.intro_entername = pg.image.load("Assets/Images/Menu/entername.png").convert_alpha()
        self.intro_enteraddress = pg.image.load("Assets/Images/Menu/enteraddress.png").convert_alpha()
        self.intro_input = pg.image.load("Assets/Images/Menu/input.png").convert_alpha()
        self.intro_help = []
        for i in range(0, 9):
            self.intro_help.append(pygame.image.load('Assets/Images/help/'+'help'+str(i+1)+'.png'))
        self.intro_credits = pg.image.load("Assets/Images/credits/credits.png")
        
        self.menu_font = pg.font.Font(FONT, 35)
        self.bonus_font = pg.font.Font(FONT, 30)
        self.title_font = pg.font.Font(FONT, 90)
        self.game_over_font = pg.font.Font(FONT, 120)
        self.game_left_font = pg.font.Font(FONT, 75)

    # Draw Main Menu - Intro Menu
    def draw_menu(self, *args):
        self.intro_bg = pg.transform.smoothscale(self.intro_bg, (self.width, self.height))
        self.surface.blit(self.intro_bg, (0, 0), (0, 0, self.width, self.height))
        self.intro_title = pg.transform.smoothscale(self.intro_title, (int(self.width / 2), int(self.height * 0.2)))
        self.surface.blit(self.intro_title, (self.width / 4, self.height * 0.1), (0, 0, self.width, self.height))
        self.intro_menu1 = pg.transform.smoothscale(self.intro_menu1, (int(self.width / 5), int(self.height * 0.1)))
        self.surface.blit(self.intro_menu1, (self.width / 2.5, self.height * 0.39), (0, 0, self.width, self.height))
        self.intro_menu2 = pg.transform.smoothscale(self.intro_menu2, (int(self.width / 5), int(self.height * 0.1)))
        self.surface.blit(self.intro_menu2, (self.width / 2.5, self.height * 0.51), (0, 0, self.width, self.height))
        self.intro_menu3 = pg.transform.smoothscale(self.intro_menu3, (int(self.width / 5), int(self.height * 0.1)))
        self.surface.blit(self.intro_menu3, (self.width / 2.5, self.height * 0.63), (0, 0, self.width, self.height))
        self.intro_menu4 = pg.transform.smoothscale(self.intro_menu4, (int(self.width / 5), int(self.height * 0.1)))
        self.surface.blit(self.intro_menu4, (self.width / 2.5, self.height * 0.75), (0, 0, self.width, self.height))
        self.intro_menu5 = pg.transform.smoothscale(self.intro_menu5, (int(self.width / 5), int(self.height * 0.1)))
        self.surface.blit(self.intro_menu5, (self.width / 2.5, self.height * 0.87), (0, 0, self.width, self.height))

        for drawable in args:
            drawable.draw_on(self.surface)
        pg.display.update()

    # Draw Choose Color/Character Menu
    def draw_choose_character(self, *args):
        self.intro_bg2 = pg.transform.smoothscale(self.intro_bg2, (self.width, self.height))
        self.surface.blit(self.intro_bg2, (0, 0), (0, 0, self.width, self.height))
        self.intro_choosecolour = pg.transform.smoothscale(self.intro_choosecolour, (int(self.width / 2), int(self.height * 0.1)))
        self.surface.blit(self.intro_choosecolour, (self.width / 3.9, self.height * 0.05), (0, 0, self.width, self.height))
        self.intro_color1 = pg.transform.smoothscale(self.intro_color1, (int(self.width / 4), int(self.height * 0.1)))
        self.surface.blit(self.intro_color4, (self.width / 2.6, self.height * 0.2), (0, 0, self.width, self.height))
        self.intro_color2 = pg.transform.smoothscale(self.intro_color2, (int(self.width / 4), int(self.height * 0.1)))
        self.surface.blit(self.intro_color1, (self.width / 2.6, self.height * 0.33), (0, 0, self.width, self.height))
        self.intro_color3 = pg.transform.smoothscale(self.intro_color3, (int(self.width / 4), int(self.height * 0.1)))
        self.surface.blit(self.intro_color5, (self.width / 2.6, self.height * 0.46), (0, 0, self.width, self.height))
        self.intro_color4 = pg.transform.smoothscale(self.intro_color4, (int(self.width / 4), int(self.height * 0.1)))
        self.surface.blit(self.intro_color3, (self.width / 2.6, self.height * 0.59), (0, 0, self.width, self.height))
        self.intro_color5 = pg.transform.smoothscale(self.intro_color5, (int(self.width / 4), int(self.height * 0.1)))
        self.surface.blit(self.intro_color2, (self.width / 2.6, self.height * 0.72), (0, 0, self.width, self.height))
        self.intro_return = pg.transform.smoothscale(self.intro_return, (int(self.width / 4), int(self.height * 0.1)))
        self.surface.blit(self.intro_return, (self.width / 2.6, self.height * 0.85), (0, 0, self.width, self.height))

        for drawable in args:
            drawable.draw_on(self.surface)
        pg.display.update()

    # Draw Gameover Menu
    def draw_game_over(self, scoreboard: list, message: str, *args):
        background = pg.image.load("Assets/Images/Alerts/victory.PNG")
        #self.surface.fill(background)
        self.surface.blit(background,(0,0))
        self.draw_text(self.surface, message, self.width / 2, self.height * 0.2, self.game_over_font)
        pos = 0.5
        for player in scoreboard:
            self.draw_text(self.surface, player[0], self.width / 3, self.height * pos, self.bonus_font)
            self.draw_text(self.surface, player[1], self.width * 2 / 3, self.height * pos, self.bonus_font)
            pos += 0.08
        for drawable in args:
            drawable.draw_on(self.surface)
        pg.display.update()
        
    def draw_game_over_imposter(self, scoreboard: list, message: str, *args):
        background = pg.image.load("Assets/Images/Alerts/defeat.PNG")
        #self.surface.fill(background)
        self.surface.blit(background,(0,0))
        self.draw_text(self.surface, message, self.width / 2, self.height * 0.2, self.game_over_font)
        pos = 0.5
        for player in scoreboard:
            self.draw_text(self.surface, player[0], self.width / 3, self.height * pos, self.bonus_font)
            self.draw_text(self.surface, player[1], self.width * 2 / 3, self.height * pos, self.bonus_font)
            pos += 0.08
        for drawable in args:
            drawable.draw_on(self.surface)
        pg.display.update()

    def draw_game_left(self, scoreboard: list, message: str, *args):
        background = (0, 0, 0)
        self.surface.fill(background)
        self.draw_text(self.surface, message, self.width / 2, self.height * 0.2, self.game_left_font)
        pos = 0.5
        for player in scoreboard:
            self.draw_text(self.surface, player[0], self.width / 3, self.height * pos, self.bonus_font)
            self.draw_text(self.surface, player[1], self.width * 2 / 3, self.height * pos, self.bonus_font)
            pos += 0.08
        for drawable in args:
            drawable.draw_on(self.surface)
        pg.display.update()

    #Draw Input Name field Menu
    def draw_input(self, word: str, x: int, y: int):
        self.intro_bg2 = pg.transform.scale(self.intro_bg2, (self.width, self.height))
        self.surface.blit(self.intro_bg2, (0, 0), (0, 0, self.width, self.height))
        self.intro_entername = pg.transform.smoothscale(self.intro_entername, (int(self.width / 2), int(self.height * 0.1)))
        self.surface.blit(self.intro_entername, (self.width / 3.9, self.height * 0.05), (0, 0, self.width, self.height))
        self.intro_input = pg.transform.smoothscale(self.intro_input, (int(self.width / 3), int(self.height * 0.2)))
        self.surface.blit(self.intro_input, (self.width / 3.0, self.height * 0.4), (0, 0, self.width, self.height))
        text = self.menu_font.render("{}".format(word), True, MENU_FONT_COLOR)
        rect = text.get_rect()
        rect.center = x, y
        pg.display.update()
        return self.surface.blit(text, rect)
    
    def draw_input_address(self, word: str, x: int, y: int):
        self.intro_bg2 = pg.transform.smoothscale(self.intro_bg2, (self.width, self.height))
        self.surface.blit(self.intro_bg2, (0, 0), (0, 0, self.width, self.height))
        self.intro_enteraddress = pg.transform.smoothscale(self.intro_enteraddress, (int(self.width / 2), int(self.height * 0.1)))
        self.surface.blit(self.intro_enteraddress, (self.width / 3.9, self.height * 0.05), (0, 0, self.width, self.height))
        self.intro_input = pg.transform.smoothscale(self.intro_input, (int(self.width / 3), int(self.height * 0.2)))
        self.surface.blit(self.intro_input, (self.width / 3.0, self.height * 0.4), (0, 0, self.width, self.height))
        text = self.menu_font.render("{}".format(word), True, MENU_FONT_COLOR)
        rect = text.get_rect()
        rect.center = x, y
        pg.display.update()
        return self.surface.blit(text, rect)
        
    def draw_help(self, i):
        #self.intro_help[i] = pg.transform.smoothscale(self.intro_help[i], (self.width, self.height))
        self.intro_help[i] = pg.transform.scale(self.intro_help[i], (self.width, self.height))
        self.surface.blit(self.intro_help[i], (0, 0), (0, 0, self.width, self.height))
        pg.display.update()
        
    def draw_credits(self):
        #self.intro_credits = pg.transform.smoothscale(self.intro_credits, (self.width, self.height))
        self.intro_credits = pg.transform.scale(self.intro_credits, (self.width, self.height))
        self.surface.blit(self.intro_credits, (0, 0), (0, 0, self.width, self.height))
        pg.display.update()

    def draw_pause(self):
        self.draw_text(self.surface, "Paused", self.width / 2, self.height / 2, self.title_font)

    def draw_bots_left(self, left: int, text_size):
        self.bots_left_font = pg.font.Font(FONT, text_size)
        if self.game.gamemode == "Freeplay":
            self.draw_text(self.surface, "Bots Alive: {}".format(left), 60, 25, self.bots_left_font)
        elif self.game.gamemode == "Multiplayer":
            self.draw_text(self.surface, "PLYR Alive: {}".format(left), 60 , 25, self.bots_left_font)

    def draw_player_name(self, player_name, text_color, text_size):
        self.player_name_font = pg.font.Font(FONT, text_size)
        text_surface = self.player_name_font.render(player_name + " - Imposter", True, text_color)
        text_surface2 = self.player_name_font.render(player_name+ " - Crewmate", True, text_color)
        if self.game.player.imposter:
            return text_surface
        else:
            return text_surface2

    def draw_ejected_text(self, p):
        self.draw_text(self.surface, p + " was ejected", self.width/2, self.height/2, self.bonus_font)

    def draw_light_timer_text(self, left: int, text_color, text_size):
        timer_font = pg.font.Font(FONT, text_size)
        text_surface = timer_font.render("{} ".format(left), True, text_color)
        return text_surface

    def draw_kill_timer_text(self, left: int, text_color, text_size):
        timer_font = pg.font.Font(FONT, text_size)
        text_surface = timer_font.render("{} ".format(left), True, text_color)
        return text_surface

    def draw_reactor_timer_imposter_text(self, left: int, text_color, text_size):
        timer_font = pg.font.Font(FONT, text_size)
        text_surface = timer_font.render("{} ".format(left), True, text_color)
        return text_surface

    def draw_reactor_timer_text(self, left: int, text_color, text_size):
        timer_font = pg.font.Font(FONT, text_size)
        text_surface = timer_font.render("Reactor Meltdown in: {} ".format(left) + " secs", True, text_color)
        return text_surface

    def draw_meeting_timer_text(self, left: int, text_color, text_size):
        timer_font = pg.font.Font(FONT, text_size)
        text_surface = timer_font.render("Voting Ends in: {} ".format(left), True, text_color)
        return text_surface

    @staticmethod
    def draw_adds(surface, x, y, image, amount=1):
        for i in range(amount):
            img_rect = image.get_rect()
            img_rect.x = x + 30 * i
            img_rect.y = y
            surface.blit(image, img_rect)

    @staticmethod

    def draw_text(surface, text, x, y, font):
        if text is not None:
            text = font.render(text, True, MENU_FONT_COLOR)
            rect = text.get_rect()
            rect.center = x, y
            surface.blit(text, rect)
