import pygame
import pygame.freetype
import pygame.mixer


class Menu:
    def __init__(self):
        self.font = pygame.freetype.Font('fonts/ARCADE_N.TTF', 44)
        self.font2 = pygame.freetype.Font('fonts/ARCADE_N.TTF', 20)
        self.font3 = pygame.freetype.Font('fonts/ARCADE_N.TTF', 16)
        self.letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '<']
        self.running = True
        self.selected = 0
        self.username = ''
        self.img = 0
        self.selectSound = pygame.mixer.Sound("sounds/select.wav")
        self.deleteSound = pygame.mixer.Sound("sounds/delete.wav")
        self.errorSound = pygame.mixer.Sound("sounds/errordb.wav")

