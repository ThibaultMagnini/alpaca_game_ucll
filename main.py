import pygame
from math import *
pygame.init()

CLOCK = pygame.time.Clock()
WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode([WIDTH, HEIGHT], pygame.RESIZABLE)
pygame.display.set_caption("Alapaca game!")

texture = pygame.image.load('sprites/stripes.png').convert()
texture = pygame.transform.scale(texture, (WIDTH,texture.get_height()))
road_texture = pygame.image.load('sprites/road3.png').convert()
road_width = road_texture.get_width()
road_height = road_texture.get_height()
player_car = pygame.image.load('sprites/download.png')
player_car = pygame.transform.scale(player_car, (150, 250))
ground = pygame.Surface((640, 240)).convert()
ground.fill((0, 100, 0))

food = 100

resolution = 1
wall_hit = 0

fov = 60
grid_height = 64
grid_width = 64
wall_height = 64
wall_width = 64
player_height = wall_height/2

player_pos = [160, 224]

view_angle = 90

projection_plane = [WIDTH, HEIGHT]

plane_center = HEIGHT//2

to_plane_dist = int((WIDTH/2)/tan(radians(fov/2)))

angle_increment = fov/WIDTH

ray_angle = 90

move_speed = 15
x_move = int(move_speed*cos(radians(view_angle)))
y_move = - int(move_speed*sin(radians(view_angle)))
rotation_speed = 3

pygame.key.set_repeat()

running = True

while running:
    CLOCK.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if food == 0:
        running = False

    move_speed = 15

    if keys[pygame.K_UP]:
        player_pos[0] += x_move
        player_pos[1] += y_move
        food -= 0.1
    if keys[pygame.K_SPACE]:
        move_speed = 30
        player_pos[0] += x_move
        player_pos[1] += y_move
        food -= 2

    beta = radians(view_angle-ray_angle)
    cos_beta = cos(beta)
    cos_angle = cos(radians(ray_angle))
    sin_angle = - sin(radians(ray_angle))

    wall_bottom = HEIGHT

    while wall_bottom > plane_center+10:
        wall_bottom -= resolution
        row = wall_bottom-plane_center
        straight_p_dist = (player_height/row*to_plane_dist)
        to_floor_dist = (straight_p_dist/cos_beta)
        ray_x = int(player_pos[0] + (to_floor_dist * cos_angle))
        ray_y = int(player_pos[1] + (to_floor_dist * sin_angle))
        floor_x = (ray_x % road_width)
        floor_y = (ray_y % road_height)
        slice_width = int(road_width/to_floor_dist*to_plane_dist)
        slice_x = (WIDTH / 2) - (slice_width//2)
        dx = slice_x
        row_slice = road_texture.subsurface(0, floor_y, road_width, 1)
        row_slice = pygame.transform.scale(row_slice, (slice_width, resolution))
        screen.blit(texture, (0, wall_bottom), (0, floor_y, WIDTH, resolution))
        screen.blit(row_slice, (slice_x, wall_bottom))
        screen.blit(player_car, (240, 320))

    pygame.display.flip()
    screen.fill((0, 0, 255))
