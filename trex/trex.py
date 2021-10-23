import pygame
import pymunk
from pymunk.pygame_util import DrawOptions
import sys
from random import uniform, randint
from actions import Actions
from copy import deepcopy


def quit_game():
    pygame.display.quit()
    pygame.quit()
    sys.exit()


def calculate_trex_hitbox_pos():
    x, y = trex.position
    if trex_down:
        trex_current_hitboxes[0] = pygame.Rect((x + 70, y + 40), (45, 30)).copy()
        trex_current_hitboxes[1] = pygame.Rect((x + 20, y + 45), (70, 30)).copy()
    else:
        trex_current_hitboxes[0] = pygame.Rect((x + 50, y + 5), (40, 30)).copy()
        trex_current_hitboxes[1] = pygame.Rect((x + 20, y + 25), (50, 45)).copy()


def draw_next_game_step(draw_hitboxes=True):
    screen.fill(gray)
    # space.debug_draw(draw_options)
    screen.blit(trex_current_images[current_image_num], trex.position)
    if draw_hitboxes:
        pygame.draw.rect(screen, black, trex_current_hitboxes[0], width=2)
        pygame.draw.rect(screen, black, trex_current_hitboxes[1], width=2)
        pygame.draw.rect(screen, black, current_hindrance, width=2)
        if not is_cactus:
            pygame.draw.rect(screen, black, pterodactylus_current_body_hitbox, width=2)
    clock.tick(100)


def collision_happened():
    for hitbox in trex_current_hitboxes:
        if hitbox.colliderect(current_hindrance):
            return True
        if not is_cactus and hitbox.colliderect(pterodactylus_current_body_hitbox):
            return True
    return False


space = pymunk.Space()
space.gravity = 0, 180
space.damping = 1

gray = (127, 127, 127)
black = (0, 0, 0)
red = (255, 0, 0)

field_width, field_height = 600, 600

trex = pymunk.Body(1, 1, pymunk.Body.DYNAMIC)
trex.position = (50, 510)
trex_shape = pymunk.Circle(trex, 80)
space.add(trex_shape, trex)

floor = pymunk.Body(1, 100, pymunk.Body.STATIC)
floor.position = 0, 590
floor_width, floor_height = field_width, 20
floor_shape = pymunk.Poly(floor, [(0, 0), (floor_width, 0), (floor_width, floor_height), (0, floor_height)])
floor_shape.elasticity = 0.7
floor_shape.friction = 0.3
space.add(floor, floor_shape)

pygame.init()
screen = pygame.display.set_mode((field_width, field_height))
clock = pygame.time.Clock()
draw_options = pymunk.pygame_util.DrawOptions(screen)

trex_up_images = [pygame.image.load('images/dino_right.png'), pygame.image.load('images/dino_left.png')]
trex_down_images = [pygame.image.load('images/dino_down_left.png'), pygame.image.load('images/dino_down_right.png')]
trex_current_images = trex_up_images.copy()
trex_down = False
trex_hitboxes = [[pygame.Rect((0, 0), (45, 30)), pygame.Rect((0, 0), (70, 30))],
                [pygame.Rect((0, 0), (40, 30)), pygame.Rect((0, 0), (50, 45))]]
trex_current_hitboxes = deepcopy(trex_hitboxes[0])
calculate_trex_hitbox_pos()
change_freq_trex_image = 20
freq_count_trex_image = 0
current_image_num = 0

cactuses = [pygame.transform.scale(pygame.image.load('images/cactuses.png'), (120, 80)),
            pygame.transform.scale(pygame.image.load('images/cactuses3.png'), (90, 80)),
            pygame.transform.scale(pygame.image.load('images/cactuses2.png'), (30, 50)),
            pygame.transform.scale(pygame.image.load('images/cactuses1.png'), (40, 70))]

cactuses_hitboxes = [pygame.Rect(field_width, 520, 120, 90),
                     pygame.Rect(field_width, 525, 85, 80),
                     pygame.Rect(field_width, 550, 30, 50),
                     pygame.Rect(field_width, 530, 35, 70)]

pterodactylus = [pygame.transform.scale(pygame.image.load('images/pterodactylus1.png'), (100, 60)),
                 pygame.transform.scale(pygame.image.load('images/pterodactylus2.png'), (100, 60))]

pterodactylus_hitboxes = [pygame.Rect(field_width, 440, 30, 30),
                          pygame.Rect(field_width, 540, 30, 30),
                          pygame.Rect(field_width, 480, 30, 30)]
pterodactylus_body_hitboxes = [pygame.Rect((field_width + 30, 455), (60, 30)),
                               pygame.Rect((field_width + 30, 555), (60, 30)),
                               pygame.Rect((field_width + 30, 495), (60, 30))]
pterodactylus_current_body_hitbox = pterodactylus_body_hitboxes[0].copy()

index = randint(0, len(cactuses) - 1)
current_hindrance = cactuses_hitboxes[index].copy()
current_hindrance_image = cactuses[index].copy()
hindrance_speed = 3
is_cactus = True

while True:
    calculate_trex_hitbox_pos()

    freq_count_trex_image += 1
    freq_count_trex_image = freq_count_trex_image % change_freq_trex_image
    if freq_count_trex_image == 0:
        current_image_num = 1 - current_image_num

    if not is_cactus:
        current_hindrance_image = pterodactylus[current_image_num].copy()

    action = None
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_game()
        if event.type == pygame.MOUSEBUTTONUP:
            pass
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                # print(trex.position)
                action = Actions.UP
            if event.key == pygame.K_DOWN:
                action = Actions.DOWN
        if event.type == pygame.KEYUP:
            action = Actions.RELEASE_DOWN

    if action == Actions.UP:
        if round(trex.position[1]) >= field_height - floor_height - trex_shape.radius:
            trex.apply_impulse_at_local_point((0, -230), (0, 0))
    elif action == Actions.DOWN:
        if round(trex.position[1]) <= field_height - floor_height - trex_shape.radius:
            trex.apply_impulse_at_local_point((0, 500), (0, 0))
        trex_current_images = trex_down_images.copy()
        trex_current_hitboxes = deepcopy(trex_hitboxes[1])
        trex_down = True
        calculate_trex_hitbox_pos()
    elif action == Actions.RELEASE_DOWN:
        trex_current_images = trex_up_images.copy()
        trex_current_hitboxes = deepcopy(trex_hitboxes[0])
        trex_down = False
        calculate_trex_hitbox_pos()

    draw_next_game_step(False)
    space.step(1 / 50)

    if is_cactus:
        width_to_add = current_hindrance.width
    else:
        width_to_add = pterodactylus_current_body_hitbox.width

    if current_hindrance.x + width_to_add <= 0:
        if uniform(0, 1) < 0.45:
            is_cactus = True
            new_hindrance_index = randint(0, len(cactuses) - 1)
            current_hindrance = cactuses_hitboxes[new_hindrance_index].copy()
            current_hindrance_image = cactuses[new_hindrance_index].copy()
        else:
            is_cactus = False
            if uniform(0, 1) < 0.55:
                current_hindrance = pterodactylus_hitboxes[-1].copy()
                pterodactylus_current_body_hitbox = pterodactylus_body_hitboxes[-1].copy()
            else:
                new_hindrance_index = randint(0, len(pterodactylus_hitboxes) - 2)
                current_hindrance = pterodactylus_hitboxes[new_hindrance_index].copy()
                pterodactylus_current_body_hitbox =pterodactylus_body_hitboxes[new_hindrance_index].copy()
            current_hindrance_image = pterodactylus[0].copy()
    else:
        current_hindrance.x -= hindrance_speed
        if not is_cactus:
            pterodactylus_current_body_hitbox.x -= hindrance_speed
        # pygame.draw.rect(screen, rect=current_cactus, color=[0, 0, 0])
        screen.blit(current_hindrance_image, (current_hindrance.x, current_hindrance.y))

    pygame.display.update()

    if collision_happened():
        quit_game()
