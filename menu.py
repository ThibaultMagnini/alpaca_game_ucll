import pygame, os
import pygame.freetype
import pygame.mixer
from pygame_vkeyboard import *

pygame.init()
pygame.mixer.init()
jef = pygame.mixer.Sound("select.wav")
delete = pygame.mixer.Sound("delete.wav")
pygame.mixer.music.set_volume(0.7)
screen = pygame.display.set_mode([640, 480])

letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W' , 'X', 'Y', 'Z', '<']

font = pygame.freetype.Font('ARCADE_N.TTF', 44)
running = True
selected = 0
username = ''
img = 0

while running:

    pygame.key.set_repeat()
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            if selected < 26:
                selected += 1

        if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            if selected > 0:
                selected -= 1

        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            if selected - 9 >= 0:
                selected -= 9

        if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            if selected + 9 <= 26:
                selected += 9

        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            print(f"username: {username}")

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            print(selected)
            if selected != 26 and len(username) < 11:
                username += letters[selected]
                jef.play()
            elif 11 > len(username) > 0:
                username = username[:-1]
                delete.play()
                pygame.draw.rect(screen, (0, 0, 0), (80, 140, 600, 60))

            img, f = font.render(username, (0, 250, 0))
            screen.blit(img, (80, 140))

    counter = 80
    line = 240
    for letter in letters:
        if letters[selected] == letter:
            surface, rect = font.render(letter, (220, 0, 0))
        else:
            surface, recta = font.render(letter, (0, 0, 220))
        screen.blit(surface, (counter, line))
        counter += 55
        if counter == 575:
            counter = 80
            line += 50

    font2 = pygame.freetype.Font('ARCADE_N.TTF', 20)
    font2.render_to(screen, (80, 400), "Press Enter To Continue", (0, 0, 220))
    font2.render_to(screen, (80, 50), "Please enter your username!", (0, 0, 220))
    pygame.display.update()
    pygame.display.flip()
