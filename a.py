import pygame
import os
import sys


size = width, height = 500, 500
screen = pygame.display.set_mode(size)
running = True
a = input()
if not os.path.exists('data/' + a):
    sys.exit()
sp = []
clock = pygame.time.Clock()

with open('data/' + a, 'r') as mapFile:
    le = [line.strip() for line in mapFile]
    level_map = le[-1].split()
    for el in range(len(le)):
        for ell in range(len(le[el])):
            if le[el][ell] == '#':
                sp.append([ell, el])

coords = [99, 99]

def start_screen():
    fon = pygame.transform.scale(load_image('game_over.jpg'), (500, 500))
    screen.blit(fon, (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert()
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
        image = image.convert_alpha()
    else:
        image = image.convert_alpha()
    return image


tile_images = {'wall': load_image('box.png'), 'empty': load_image('grass.png')}
player_image = load_image('mar.png', -1)
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
tile_width = tile_height = 50

FPS = 50


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(tile_width * pos_x + 15, tile_height * pos_y + 5)

    def rect(self):
        return self.rect.topleft

    def movel(self):
        global coords
        if self.rect.left - 50 > 0 and self.rect.left - 50 < 500 and [coords[0] - 1, coords[1]] not in sp and coords[0] - 1 != -1:
            self.rect.topleft = (self.rect.left - 50, self.rect.top)
            coords = [coords[0] - 1, coords[1]]

    def mover(self):
        global coords
        if self.rect.left + 50 > 0 and self.rect.left + 50 < 500 and [coords[0] + 1, coords[1]] not in sp and coords[0] + 1 != 100:
            self.rect.topleft = (self.rect.left + 50, self.rect.top)
            coords = [coords[0] + 1, coords[1]]


    def moveu(self):
        global coords
        if self.rect.top - 50 > 0 and self.rect.top - 50 < 500 and [coords[0], coords[1] - 1] not in sp and coords[1] - 1 != -1:
            self.rect.topleft = (self.rect.left, self.rect.top - 50)
            coords = [coords[0], coords[1] - 1]

    def moved(self):
        global coords
        if self.rect.top + 50 > 0 and self.rect.top + 50 < 500 and [coords[0], coords[1] + 1] not in sp and coords[1] + 1 != 100:
            self.rect.topleft = (self.rect.left, self.rect.top + 50)
            coords = [coords[0], coords[1] + 1]


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def terminate():
    pygame.quit()
    sys.exit()


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
                sp.append((x * 50 + 15, y * 50 + 5))
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
    return new_player, x, y


start_screen()
level_map = load_level(a)
player, level_x, level_y = generate_level(level_map)


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)


camera = Camera()
# изменяем ракурс камеры
camera.update(player)
# обновляем положение всех спрайтов
for sprite in all_sprites:
      camera.apply(sprite)
while True:
    for event in pygame.event.get():
        k = pygame.key.get_pressed()
        if event.type == pygame.QUIT:
            terminate()
        if k[pygame.K_LEFT]:
            Player.movel(player)
            camera.update(player)
            for sprite in all_sprites:
                camera.apply(sprite)
        elif k[pygame.K_RIGHT]:
            Player.mover(player)
            camera.update(player)
            for sprite in all_sprites:
                camera.apply(sprite)
        elif k[pygame.K_UP]:
            Player.moveu(player)
            camera.update(player)
            for sprite in all_sprites:
                camera.apply(sprite)
        elif k[pygame.K_DOWN]:
            Player.moved(player)
            camera.update(player)
            for sprite in all_sprites:
                camera.apply(sprite)
    screen.fill((0, 0, 0))
    all_sprites.draw(screen)
    tiles_group.draw(screen)
    player_group.draw(screen)
    pygame.display.flip()
