import pygame
from game import Game


pygame.init()

CLOCK = pygame.time.Clock()
WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode([WIDTH, HEIGHT], pygame.RESIZABLE)
pygame.display.set_caption("Alapaca game!")

game = Game(screen, CLOCK, WIDTH, HEIGHT)

while game.running:
    game.play()
