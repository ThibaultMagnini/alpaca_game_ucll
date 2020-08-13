from game_math import *

from pygame.transform import scale


def world_to_viewplane_coordinates(eye_viewplane_distance, eye_height, px, py, pz):
    d = eye_viewplane_distance
    h = eye_height
    t = d / (pz + d)
    x = px * t
    y = h + (py - h) * t
    z = 0
    return x, y, z


def viewplane_to_world_coordinates(eye_viewplane_distance, eye_height, px, py):
    d = eye_viewplane_distance
    h = eye_height
    t = h / (h - py)
    x = px * t
    y = 0
    z = (t - 1) * d
    return x, y, z


def screen_to_viewplane_coordinates(w, h, px, py):
    x = (px - w / 2) / w
    y = 1 - py / h
    return x, y


def viewplane_to_screen_coordinates(w, h, px, py):
    x = int(px * w + w // 2)
    y = int((1 - py) * h)
    return x, y


def draw_object(self, image, position, size):
    x, y, z = position
    w, h = size
    vpx1, vpy1, vpz1 = world_to_viewplane_coordinates(x, y, z)
    vpx1, vpy1, vpz1 = world_to_viewplane_coordinates(x - w / 2, y, z)
    vpx2, vpy2, vpz2 = world_to_viewplane_coordinates(x + w / 2, y + h, z)
    sx1, sy1 = viewplane_to_screen_coordinates(vpx1, vpy1)
    sx2, sy2 = viewplane_to_screen_coordinates(vpx2, vpy2)
    scaled = scale(image, (abs(sx2 - sx1), abs(sy2 - sy1)))
    self.window.blit(scaled, (sx1, sy2))

