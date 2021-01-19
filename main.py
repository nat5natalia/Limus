import pygame

import screens

pygame.init()
size = WIDTH, HEIGHT = 800, 500
screen = pygame.display.set_mode(size)
pygame.display.set_mode(size)
pygame.display.set_caption('limus')
running = True
count = 0

screens.start_screen(WIDTH, HEIGHT, screen)