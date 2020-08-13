from math import radians, tan, cos, sin

import pygame
from pygame.transform import scale

from player import Player
from game_math import *
from menu import *
import pygame.freetype
import database
import game_math


class Game:
    def __init__(self, window, clock, WIDTH, HEIGHT):
        self.window = window
        self.clock = clock
        self.grid_height = 64
        self.grid_width = 64
        self.wall_height = 64
        self.wall_width = 64
        self.player = Player(100, 'sprites/loop1.png', 15, [160, 224], self.wall_height/2)
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.running = True
        self.tree = pygame.image.load('sprites/bush.png').convert_alpha()
        self.pizza = pygame.image.load('sprites/burger.png').convert()
        self.texture = pygame.image.load('sprites/stripes.png').convert()
        self.texture = pygame.transform.scale(self.texture, (WIDTH, self.texture.get_height()))
        self.road_texture = pygame.image.load('sprites/road3.png').convert()
        self.road_width = self.road_texture.get_width()
        self.road_height = self.road_texture.get_height()
        self.player_car = pygame.image.load(self.player.sprite)
        self.player_car = pygame.transform.scale(self.player_car, (100, 150))
        self.ground = pygame.Surface((640, 240)).convert()
        self.ground.fill((0, 100, 0))
        self.resolution = 1
        self.wall_hit = 0
        self.fov = 60
        self.view_angle = 90
        self.projection_plane = [WIDTH, HEIGHT]
        self.plane_center = HEIGHT // 2
        self.to_plane_dist = int((WIDTH / 2) / tan(radians(self.fov / 2)))
        self.angle_increment = self.fov / WIDTH
        self.ray_angle = 90
        self.x_move = int(self.player.move_speed * cos(radians(self.view_angle)))
        self.y_move = - int(self.player.move_speed * sin(radians(self.view_angle)))
        self.rotation_speed = 3
        self.player_location = [240,340]
        self.changesprite = 0
        self.menu = Menu()
        self.userSelected = True
        self.eye_viewplane_distance = 1
        self.eye_height = 0.6
        self.road_size = 4
        self.player_z = 0
        self.background = pygame.image.load('sprites/background.jpg').convert()
        # self.readytoplay = True

    ################################################# Gameplay ###################################################

    def play(self):
        pygame.key.set_repeat()
        self.clock.tick(30)

        self.changesprite += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        keys = pygame.key.get_pressed()

        pygame.draw.rect(self.window, (255, 0, 0), (220, 0, self.player.food*2, 30))

        if self.player.food <= 0:
            self.running = False

        self.player.move_speed = 15

    ################################################   Movement   ###########################################

        if keys[pygame.K_d]:
            if self.player_location[0] + 100 < self.WIDTH:
                self.player_location[0] += 10
        if keys[pygame.K_a]:
            if self.player_location[0] > 0 < self.WIDTH:
                self.player_location[0] -= 10
        if keys[pygame.K_w]:
            self.eye_viewplane_distance *= 1.1
            print(f'd={self.eye_viewplane_distance}')
        if keys[pygame.K_s]:
            self.eye_viewplane_distance *= 0.9
            print(f'd={self.eye_viewplane_distance}')


        if keys[pygame.K_UP]:
            if self.player.sprite == 'sprites/loop4.png':
                if self.changesprite >= 3:
                    self.player.sprite = 'sprites/loop1.png'
                    self.changesprite = 0
            elif self.player.sprite == 'sprites/loop1.png':
                if self.changesprite >= 3:
                    self.player.sprite = 'sprites/loop2.png'
                    self.changesprite = 0
            elif self.player.sprite == 'sprites/loop2.png':
                if self.changesprite >= 3:
                    self.player.sprite = 'sprites/loop3.png'
                    self.changesprite = 0
            else:
                if self.changesprite >= 3:
                    self.player.sprite = 'sprites/loop4.png'
                    self.changesprite = 0

            self.player_car = pygame.image.load(self.player.sprite)
            self.player_car = pygame.transform.scale(self.player_car, (100, 150))
            self.player.player_pos[0] += self.x_move
            self.player.player_pos[1] += self.y_move
            self.player_z += 0.2
            self.player.food -= 0.1

        if keys[pygame.K_SPACE]:
            if self.player.sprite == 'sprites/loop4.png':
                self.player.sprite = 'sprites/loop1.png'
            elif self.player.sprite == 'sprites/loop1.png':
                self.player.sprite = 'sprites/loop2.png'
            elif self.player.sprite == 'sprites/loop2.png':
                self.player.sprite = 'sprites/loop3.png'
            else:
                self.player.sprite = 'sprites/loop4.png'

            self.player_car = pygame.image.load(self.player.sprite)
            self.player_car = pygame.transform.scale(self.player_car, (100, 150))
            self.player.move_speed = 30
            self.player.player_pos[0] += self.x_move
            self.player.player_pos[1] += self.y_move
            self.player.food -= 2

        if keys[pygame.K_RIGHT]:
            if self.player_location[0] + 100 < self.WIDTH:
                self.player_location[0] += 10
        if keys[pygame.K_LEFT]:
            if self.player_location[0] > 0:
                self.player_location[0] -= 10

        beta = radians(self.view_angle - self.ray_angle)
        cos_beta = cos(beta)
        cos_angle = cos(radians(self.ray_angle))
        sin_angle = - sin(radians(self.ray_angle))

    ###############################################  Drawing  ###################################################

        wall_bottom = self.HEIGHT

        self.window.blit(self.background, (0, 0))

        for y in range(int(self.HEIGHT * 0.5), self.HEIGHT):
            vpx, vpy = game_math.screen_to_viewplane_coordinates(self.WIDTH, self.HEIGHT, 0, y)
            wx, wy, wz = game_math.viewplane_to_world_coordinates(self.eye_viewplane_distance, self.eye_height, vpx, vpy)
            vpx, vpy, vpz = game_math.world_to_viewplane_coordinates(self.eye_viewplane_distance, self.eye_height, -self.road_size / 2, 0, wz)
            sx1, sy1 = game_math.viewplane_to_screen_coordinates(self.WIDTH, self.HEIGHT, vpx, vpy)
            sx2, sy2 = game_math.viewplane_to_screen_coordinates(self.WIDTH, self.HEIGHT, -vpx, vpy)

            if sx1 < sx2:
                row = scale(self.road_texture.subsurface(0, 0, self.road_width, 1), (sx2 - sx1, 1))
                self.window.blit(row, (sx1, y))

        object_size = 0.5
        for distance in range(20, 1, -1):
            z = distance - self.player_z % 1
            i, j, f = game_math.world_to_viewplane_coordinates(self.eye_viewplane_distance, self.eye_height, -self.road_size * 0.4, -0.4, z)
            k, f = game_math.viewplane_to_screen_coordinates(self.WIDTH, self.HEIGHT, i, j)
            if self.HEIGHT * 0.5 <= f <= self.HEIGHT:
                game_math.draw_object(self, self.tree, (-self.road_size * 0.4, -0.4, z), (object_size, object_size))
                game_math.draw_object(self, self.tree, (self.road_size * 0.42, -0.4, z), (object_size, object_size))
                game_math.draw_object(self, self.pizza, (0, -0.4, 5 - self.player_z % 1), (0.4, 0.4))

        self.window.blit(self.player_car, self.player_location)

        pygame.display.flip()
        self.window.fill((0, 0, 255))

    ############################################   MENU   ###################################################

    def showmenu(self):
        pygame.mixer.init()
        pygame.mixer.music.set_volume(0.7)
        pygame.key.set_repeat()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                if self.menu.selected < 26:
                    self.menu.selected += 1

            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                if self.menu.selected > 0:
                    self.menu.selected -= 1

            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                if self.menu.selected - 9 >= 0:
                    self.menu.selected -= 9

            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                if self.menu.selected + 9 <= 26:
                    self.menu.selected += 9

            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                if database.get_alpaca_with_username(self.menu.username.lower()) is not None:
                    self.userSelected = False
                    print(database.get_alpaca_with_username(self.menu.username.lower()))
                else:
                    self.menu.errorSound.play()
                    self.menu.font3.render_to(self.window, (40, 80), "The entered username does not exist!", (250, 0, 0))

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:

                if self.menu.selected != 26 and len(self.menu.username) < 11:
                    self.menu.username += self.menu.letters[self.menu.selected]
                    self.menu.selectSound.play()
                elif 11 > len(self.menu.username) > 0:
                    self.menu.username = self.menu.username[:-1]
                    self.menu.deleteSound.play()
                    pygame.draw.rect(self.window, (0, 0, 0), (80, 140, 600, 60))

                img, f = self.menu.font.render(self.menu.username, (0, 250, 0))
                self.window.blit(img, (80, 140))

        counter = 80
        line = 240
        for letter in self.menu.letters:
            if self.menu.letters[self.menu.selected] == letter:
                surface, rect = self.menu.font.render(letter, (220, 0, 0))
            else:
                surface, recta = self.menu.font.render(letter, (0, 0, 220))
            self.window.blit(surface, (counter, line))
            counter += 55
            if counter == 575:
                counter = 80
                line += 50

        self.menu.font2.render_to(self.window, (80, 400), "Press Enter To Continue", (0, 0, 220))
        self.menu.font2.render_to(self.window, (60, 50), "Please enter your username!", (0, 0, 220))
        pygame.display.update()
        pygame.display.flip()


    ########################################    WELCOME SCREEN    ###########################################

    # def welcomeScreen(self):
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             self.running = False
    #
    #         if event.type == pygame.KEYDOWN:
    #             pygame.draw.rect(self.window, (0, 0, 0), (50, 300, 1000, 100))
    #             self.readytoplay = False
    #             self.userSelected = True
    #
    #     font = pygame.freetype.Font('ARCADE_N.TTF', 25)
    #     img, f = font.render("Press Any Key TO start!!", (0, 0, 250))
    #     self.window.blit(img, (50, 300))
    #     pygame.display.update()
    #     pygame.display.flip()

