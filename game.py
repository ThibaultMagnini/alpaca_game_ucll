import pygame
from pygame.transform import scale
from player import Player
from math import *


class Game:
    def __init__(self, window, clock, WIDTH, HEIGHT):
        self.window = window
        self.clock = clock
        self.grid_height = 64
        self.grid_width = 64
        self.wall_height = 64
        self.wall_width = 64
        self.player = Player(100, 'sprites/stand.png', 15, [160, 224], self.wall_height/2)
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.running = True
        self.texture = pygame.image.load('sprites/stripes.png').convert()
        self.texture = pygame.transform.scale(self.texture, (WIDTH, self.texture.get_height()))
        self.tree = pygame.image.load('sprites/tree.png').convert_alpha()
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

        self.eye_viewplane_distance = 1
        self.eye_height = 0.6
        self.road_size = 4
        self.player_z = 0


    def play (self):
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

        if keys[pygame.K_UP]:
            if (self.player.sprite == 'sprites/stand.png'):
                if (self.changesprite >= 3):
                    self.player.sprite = 'sprites/start.png'
                    self.changesprite = 0
            elif (self.player.sprite == 'sprites/start.png'):
                if (self.changesprite >= 3):
                    self.player.sprite = 'sprites/wandelen.png'
                    self.changesprite = 0
            else:
                if (self.changesprite >= 3):
                    self.player.sprite = 'sprites/stand.png'
                    self.changesprite = 0
            self.player_car = pygame.image.load(self.player.sprite)
            self.player_car = pygame.transform.scale(self.player_car, (100, 150))
            self.player.player_pos[0] += self.x_move
            self. player.player_pos[1] += self.y_move
            self.player_z += 0.2
            self.player.food -= 0.1
        if keys[pygame.K_SPACE]:
            if (self.player.sprite == 'sprites/stand.png'):
                self.player.sprite = 'sprites/start.png'
            elif (self.player.sprite == 'sprites/start.png'):
                self.player.sprite = 'sprites/wandelen.png'
            else:
                self.player.sprite = 'sprites/stand.png'

            self.player_car = pygame.image.load(self.player.sprite)
            self.player_car = pygame.transform.scale(self.player_car, (100, 150))
            self.player.move_speed = 30
            self.player.player_pos[0] += self.x_move
            self.player.player_pos[1] += self.y_move
            self.player.food -= 2
        if keys[pygame.K_RIGHT]:
            if (self.player_location[0] + 100 < self.WIDTH):
                self.player_location[0] += 10
        if keys[pygame.K_LEFT]:
            if (self.player_location[0] > 0):
                self.player_location[0] -= 10

        beta = radians(self.view_angle - self.ray_angle)
        cos_beta = cos(beta)
        cos_angle = cos(radians(self.ray_angle))
        sin_angle = - sin(radians(self.ray_angle))

        wall_bottom = self.HEIGHT

        for y in range(int(self.HEIGHT * 0.5), self.HEIGHT):
            vpx, vpy = self.screen_to_viewplane_coordinates(0, y)
            wx, wy, wz = self.viewplane_to_world_coordinates(vpx, vpy)
            vpx, vpy, vpz = self.world_to_viewplane_coordinates(-self.road_size / 2, 0, wz)
            sx1, sy1 = self.viewplane_to_screen_coordinates(vpx, vpy)
            sx2, sy2 = self.viewplane_to_screen_coordinates(-vpx, vpy)

            if sx1 < sx2:
                row = scale(self.road_texture.subsurface(0, 0, self.road_width, 1), (sx2 - sx1, 1))
                self.window.blit(row, (sx1, y))


        object_size = 4
        for distance in range(10, 1, -1):
            z = distance - self.player_z % 1
            self.draw_object(self.tree, (-self.road_size * 0.4, 0, z), (object_size, object_size))
            self.draw_object(self.tree, (self.road_size * 0.4, 0, z), (object_size, object_size))

        # assert False


        self.window.blit(self.player_car, self.player_location)

        pygame.display.flip()
        self.window.fill((0, 0, 255))

    def world_to_viewplane_coordinates(self, px, py, pz):
        d = self.eye_viewplane_distance
        h = self.eye_height
        t = d / (pz + d)
        x = px * t
        y = h + (py -h) * t
        z = 0
        return (x, y, z)

    def viewplane_to_world_coordinates(self, px, py):
        d = self.eye_viewplane_distance
        h = self.eye_height
        t = h / (h - py)
        x = px * t
        y = 0
        z = (t - 1) * d
        return (x, y, z)

    def screen_to_viewplane_coordinates(self, px, py):
        x = (px - self.WIDTH / 2) / self.WIDTH
        y = 1 - py / self.HEIGHT
        return (x, y)

    def viewplane_to_screen_coordinates(self, px, py):
        x = int(px * self.WIDTH + self.WIDTH // 2)
        y = int((1 - py) * self.HEIGHT)
        return (x, y)

    def draw_object(self, image, position, size):
        x, y, z = position
        w, h = size
        vpx1, vpy1, vpz1 = self.world_to_viewplane_coordinates(x, y, z)
        vpx1, vpy1, vpz1 = self.world_to_viewplane_coordinates(x - w / 2, y, z)
        vpx2, vpy2, vpz2 = self.world_to_viewplane_coordinates(x + w / 2, y + h, z)
        sx1, sy1 = self.viewplane_to_screen_coordinates(vpx1, vpy1)
        sx2, sy2 = self.viewplane_to_screen_coordinates(vpx2, vpy2)
        # pygame.draw.rect(self.window, (255, 0, 0), pygame.Rect((sx1, sy1), (abs(sx2-sx1), abs(sy2-sy1))))
        # pygame.draw.circle(self.window, (255, 0, 0), (sx1, sy1), 2)
        scaled = scale(image, (abs(sx2 - sx1), abs(sy2 - sy1)))
        self.window.blit(scaled, (sx1, sy2))
