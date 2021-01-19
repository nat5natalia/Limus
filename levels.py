import os
import sys
import random

import pygame

import screens


pygame.init()
size = WIDTH, HEIGHT = 800, 500
screen = pygame.display.set_mode(size)
pygame.display.set_mode(size)
pygame.display.set_caption('limus')
running = True
count = 0
level = None
sound_boom = pygame.mixer.Sound('data/zvuk-vzryva.mp3')
sound_start = pygame.mixer.Sound('data/roundstart_main.mp3')
pygame.mixer.music.load('data/ppk-voskreshenie (1).mp3')
pygame.mixer.music.set_volume(0.5)
sound_boom.set_volume(0.5)


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)

    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class City(pygame.sprite.Sprite):
    fon_image = load_image('city.png')

    def __init__(self, group):
        super().__init__(group)
        self.image = City.fon_image
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 300
        self.mask = pygame.mask.from_surface(self.image)


class Tarelka(pygame.sprite.Sprite):
    t_image = load_image('ufo.png')
    boom_image = load_image('boom.png')

    def __init__(self, group, x=random.randrange(0, 450)):
        super().__init__(group)
        self.image = Tarelka.t_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = - 200
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, *args):
        global count
        if not pygame.sprite.collide_mask(self, city):
            self.rect = self.rect.move(0, 1)
        else:
            screens.final_screen(count, WIDTH, HEIGHT, screen, False)  # вывод сообщения о проигрыше. выбор главное меню или повторить уровень
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            sound_boom.play()
            Tarelka.kill(self)
            count += 10


class BigTarelka(pygame.sprite.Sprite):
    t_image = load_image('ufo2.png')
    boom_image = load_image('boom.png')

    def __init__(self, group, x=random.randrange(0, 450)):
        super().__init__(group)
        self.image = BigTarelka.t_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = - 200
        self.mask = pygame.mask.from_surface(self.image)
        self.r = 0

    def update(self, *args):
        global count
        if not pygame.sprite.collide_mask(self, city):
            self.rect = self.rect.move(0, 1)
        else:
            screens.final_screen(count, WIDTH, HEIGHT, screen, False)  # вывод сообщения о проигрыше. выбор главное меню или повторить уровень
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            if self.r == 1:
                sound_boom.play()
                BigTarelka.kill(self)
                count += 20
            else:
                self.r += 1


all_sprites1 = pygame.sprite.Group()
city = City(all_sprites1)


def first_level():
    global count, level
    sound_start.play()
    pygame.mixer.music.play(-1)
    level = first_level
    TARELKA_EVENT = pygame.USEREVENT + 1
    n, r, v = 3000, 0, 10
    all_sprites = pygame.sprite.Group()
    pygame.time.set_timer(TARELKA_EVENT, n, 25)
    Tarelka(all_sprites)

    running = True

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                all_sprites.update(event)
            if event.type == TARELKA_EVENT:
                r += 1
                if r >= 20:
                    BigTarelka(all_sprites)
                else:
                    Tarelka(all_sprites)
                    if r in [5, 10, 15]:
                        n -= 900
                        v -= 2
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                screens.pausa(WIDTH, HEIGHT, screen)
                pygame.mixer.music.play(-1)
            if r >= 25:
                screens.final_screen(count, WIDTH, HEIGHT, screen, True)
                count = 0  # появляется окно "вы победили. следующий уровень. пройти уровень снова"
        fon = pygame.transform.scale(load_image('background_main.jpg'), (WIDTH, HEIGHT))
        screen.blit(fon, (0, 0))

        all_sprites.draw(screen)
        all_sprites1.draw(screen)
        all_sprites.update()
        pygame.time.delay(v)
        pygame.display.flip()

        font = pygame.font.Font(None, 100)
        t = font.render(str(count), True, pygame.Color('red'))
        screen.blit(t, (0, 0))

    terminate()


def second_level():
    global count, level
    sound_start.play()
    pygame.mixer.music.play(-1)
    level = second_level
    TARELKA_EVENT = pygame.USEREVENT + 1
    n, r, v = 3000, 0, 7
    all_sprites = pygame.sprite.Group()
    pygame.time.set_timer(TARELKA_EVENT, n, 25)
    Tarelka(all_sprites)

    running = True

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                all_sprites.update(event)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                screens.pausa(WIDTH, HEIGHT, screen)
                pygame.mixer.music.play(-1)
            if event.type == TARELKA_EVENT:
                r += 1
                if r in [5, 10, 15, 20, 25]:
                    BigTarelka(all_sprites)
                    n -= 900
                    v -= 1
                else:
                    Tarelka(all_sprites)
            if r >= 25:
                screens.final_screen(count, WIDTH, HEIGHT, screen, True)
                count = 0  # появляется окно "вы победили. следующий уровень. пройти уровень снова"
        fon = pygame.transform.scale(load_image('background_main.jpg'), (WIDTH, HEIGHT))
        screen.blit(fon, (0, 0))

        all_sprites.draw(screen)
        all_sprites1.draw(screen)
        all_sprites.update()
        pygame.time.delay(v)
        pygame.display.flip()

        font = pygame.font.Font(None, 100)
        t = font.render(str(count), True, pygame.Color('red'))
        screen.blit(t, (0, 0))

    terminate()


def third_level():
    global count, level
    sound_start.play()
    pygame.mixer.music.play(-1)
    level = third_level
    TARELKA_EVENT = pygame.USEREVENT + 1
    n, r, v = 3000, 0, 6
    all_sprites = pygame.sprite.Group()
    pygame.time.set_timer(TARELKA_EVENT, n, 25)
    Tarelka(all_sprites)

    running = True

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                all_sprites.update(event)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                screens.pausa(WIDTH, HEIGHT, screen)
                pygame.mixer.music.play(-1)
            if event.type == TARELKA_EVENT:
                r += 1
                if r in [5, 10, 13, 15, 20, 23, 25]:
                    BigTarelka(all_sprites)
                    n -= 900
                    v -= 1
                elif r in [3, 17]:
                    x = 90
                    Tarelka(all_sprites, x)
                    Tarelka(all_sprites, x + 350)
                else:
                    Tarelka(all_sprites)
            if r >= 25:
                screens.final_screen(count, WIDTH, HEIGHT, screen, True)
                count = 0  # появляется окно "вы победили. следующий уровень. пройти уровень снова"
        fon = pygame.transform.scale(load_image('background_main.jpg'), (WIDTH, HEIGHT))
        screen.blit(fon, (0, 0))

        all_sprites.draw(screen)
        all_sprites1.draw(screen)
        all_sprites.update()
        pygame.time.delay(v)
        pygame.display.flip()

        font = pygame.font.Font(None, 100)
        t = font.render(str(count), True, pygame.Color('red'))
        screen.blit(t, (0, 0))

    terminate()


def fourth_level():
    global count, level
    sound_start.play()
    pygame.mixer.music.play(-1)
    level = fourth_level
    TARELKA_EVENT = pygame.USEREVENT + 1
    n, r, v = 3000, 0, 4
    all_sprites = pygame.sprite.Group()
    pygame.time.set_timer(TARELKA_EVENT, n, 25)
    Tarelka(all_sprites)

    running = True

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                all_sprites.update(event)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                screens.pausa(WIDTH, HEIGHT, screen)
                pygame.mixer.music.play(-1)
            if event.type == TARELKA_EVENT:
                r += 1
                if r in [5, 10, 13, 15, 20, 23, 25]:
                    BigTarelka(all_sprites)
                    n -= 1000
                    v -= 1
                elif r in [3, 17]:
                    x = 90
                    Tarelka(all_sprites, x)
                    Tarelka(all_sprites, x + 350)
                elif r == 23:
                    x = 20
                    BigTarelka(all_sprites, x)
                    BigTarelka(all_sprites, x + 370)
                else:
                    Tarelka(all_sprites)
            if r >= 25:
                screens.final_screen(count, WIDTH, HEIGHT, screen, True)
                count = 0  # появляется окно "вы победили. следующий уровень. пройти уровень снова"
        fon = pygame.transform.scale(load_image('background_main.jpg'), (WIDTH, HEIGHT))
        screen.blit(fon, (0, 0))

        all_sprites.draw(screen)
        all_sprites1.draw(screen)
        all_sprites.update()
        pygame.time.delay(v)
        pygame.display.flip()

        font = pygame.font.Font(None, 450)
        t = font.render(str(count), True, pygame.Color('black'))
        screen.blit(t, (0, 0))

    terminate()


def endless_level():
    global count, level
    sound_start.play()
    pygame.mixer.music.play(-1)
    level = endless_level
    TARELKA_EVENT = pygame.USEREVENT + 1
    n, r, v = 3000, 0, 4
    all_sprites = pygame.sprite.Group()
    pygame.time.set_timer(TARELKA_EVENT, n, 25)
    Tarelka(all_sprites)

    running = True

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                all_sprites.update(event)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                screens.pausa(WIDTH, HEIGHT, screen)
                pygame.mixer.music.play(-1)
            if event.type == TARELKA_EVENT:
                r += 1
                if r in [5, 10, 13, 15, 20, 23, 25]:
                    BigTarelka(all_sprites)
                    n -= 1000
                    v -= 1
                elif r in [3, 17]:
                    x = 90
                    Tarelka(all_sprites, x)
                    Tarelka(all_sprites, x + 350)
                elif r == 23:
                    x = 20
                    BigTarelka(all_sprites, x)
                    BigTarelka(all_sprites, x + 370)
                else:
                    Tarelka(all_sprites)
        fon = pygame.transform.scale(load_image('background_main.jpg'), (WIDTH, HEIGHT))
        screen.blit(fon, (0, 0))

        all_sprites.draw(screen)
        all_sprites1.draw(screen)
        all_sprites.update()
        pygame.time.delay(v)
        pygame.display.flip()

        font = pygame.font.Font(None, 450)
        t = font.render(str(count), True, pygame.Color('black'))
        screen.blit(t, (0, 0))

    terminate()

