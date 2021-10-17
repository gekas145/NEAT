import pygame
import pymunk
from pymunk.pygame_util import DrawOptions
import sys
from random import uniform


# help function
def quit_game():
    pygame.display.quit()
    pygame.quit()
    sys.exit()

space = pymunk.Space()
space.gravity = 0, 180
space.damping = 1

gray = (127, 127, 127)
black = (0, 0, 0)
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
trex_hitbox = pygame.Rect(trex.position, (65, 70))
trex_down = False
change_freq_trex_image = 20
freq_count_trex_image = 0
current_trex_image_num = 0

cactuses = [pygame.transform.scale(pygame.image.load('images/cactuses.png'), (120, 80)),
            pygame.transform.scale(pygame.image.load('images/cactuses1.png'), (50, 80))]
cactuses_hitboxes = [pygame.Rect(field_width, 520, 120, 90),
                     pygame.Rect(field_width, 525, 47, 75)]
current_hindrance = cactuses_hitboxes[0].copy()
current_hindrance_image = cactuses[0].copy()
cactuses_speed = 3

while True:
    if trex_down:
        trex_hitbox.y = trex.position[1] + 45
    else:
        trex_hitbox.x = trex.position[0] + 10
        trex_hitbox.y = trex.position[1] + 7

    freq_count_trex_image += 1
    freq_count_trex_image = freq_count_trex_image % change_freq_trex_image
    if freq_count_trex_image == 0:
        current_trex_image_num = 1 - current_trex_image_num

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_game()
        if event.type == pygame.MOUSEBUTTONUP:
            pass
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                # print(trex.position)
                if round(trex.position[1]) >= field_height - floor_height - trex_shape.radius:
                    trex.apply_impulse_at_local_point((0, -230), (0, 0))
            if event.key == pygame.K_DOWN:
                if round(trex.position[1]) <= field_height - floor_height - trex_shape.radius:
                    trex.apply_impulse_at_local_point((0, 500), (0, 0))
                trex_current_images = trex_down_images.copy()
                trex_hitbox = pygame.Rect(trex.position, (120, 40))
                trex_down = True
                trex_hitbox.y = trex.position[1] + 45
        if event.type == pygame.KEYUP:
            trex_current_images = trex_up_images.copy()
            trex_hitbox = pygame.Rect(trex.position, (65, 70))
            trex_down = False
            trex_hitbox.x = trex.position[0] + 10
            trex_hitbox.y = trex.position[1] + 7

    screen.fill(gray)
    # space.debug_draw(draw_options)
    screen.blit(trex_current_images[current_trex_image_num], trex.position)
    pygame.draw.rect(screen, black, trex_hitbox, width=2)
    pygame.draw.rect(screen, black, current_hindrance, width=2)
    clock.tick(100)
    space.step(1 / 50)

    if current_hindrance.x + current_hindrance.width <= 0:
        if uniform(0, 1) < 0.5:
            current_hindrance = cactuses_hitboxes[0].copy()
            current_hindrance_image = cactuses[0].copy()
        else:
            current_hindrance = cactuses_hitboxes[1].copy()
            current_hindrance_image = cactuses[1].copy()
    else:
        current_hindrance.x -= cactuses_speed
        # pygame.draw.rect(screen, rect=current_cactus, color=[0, 0, 0])
        screen.blit(current_hindrance_image, (current_hindrance.x, current_hindrance.y))

    pygame.display.update()
