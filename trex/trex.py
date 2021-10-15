import pygame
import pymunk
from pymunk.pygame_util import DrawOptions
import sys


# help function
def quit_game():
    pygame.display.quit()
    pygame.quit()
    sys.exit()

space = pymunk.Space()
space.gravity = 0, 180
space.damping = 1

gray = (127, 127, 127)
field_width, field_height = 600, 600

trex = pymunk.Body(1, 1, pymunk.Body.DYNAMIC)
trex.position = (100, 300)
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

trex_up_images = []
trex_down_images = []
trex_up_images.append(pygame.image.load('dino_right.png'))
trex_up_images.append(pygame.image.load('dino_left.png'))
trex_down_images.append(pygame.image.load('dino_down_left.png'))
trex_down_images.append(pygame.image.load('dino_down_right.png'))
trex_current_images = trex_up_images.copy()
# trex_img = pygame.transform.scale(trex_img, (70, 70))
change_freq_trex_image = 20
freq_count_trex_image = 0
current_trex_image_num = 0

cactuses = []
cactuses_speed = 3

while True:
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
                # print(trex.position[1])
                if round(trex.position[1]) >= field_height - floor_height - trex_shape.radius:
                    trex.apply_impulse_at_local_point((0, -210), (0, 0))
            if event.key == pygame.K_DOWN:
                if round(trex.position[1]) <= field_height - floor_height - trex_shape.radius:
                    trex.apply_impulse_at_local_point((0, 500), (0, 0))
                trex_current_images = trex_down_images.copy()
        if event.type == pygame.KEYUP:
            trex_current_images = trex_up_images.copy()

    screen.fill(gray)
    # space.debug_draw(draw_options)
    screen.blit(trex_current_images[current_trex_image_num], trex.position)
    clock.tick(100)
    space.step(1 / 50)

    cactuses_to_pop = -1
    if len(cactuses) == 0:
        cactuses.append(pygame.Rect(field_width, 570, 30, 30))
    if len(cactuses) != 0:
        for index, cactus in enumerate(cactuses):
            cactus.x -= cactuses_speed
            if cactus.x < 0:
                cactuses_to_pop = index
            pygame.draw.rect(screen, rect=cactuses[0], color=[0, 0, 0])
    if cactuses_to_pop != -1:
        cactuses.pop(cactuses_to_pop)

    pygame.display.update()
