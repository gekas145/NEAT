import pygame
import pymunk
import sys
from random import uniform, randint
from actions import Actions
from copy import deepcopy


class TRexGameSimulator:

    def __init__(self, agent):
        self.agent = agent

    def play_game(self):

        def calculate_trex_hitbox_pos():
            x, y = trex.position
            if trex_down:
                trex_current_hitboxes[0] = pygame.Rect((x + 70, y + 40), (45, 30)).copy()
                trex_current_hitboxes[1] = pygame.Rect((x + 20, y + 45), (70, 30)).copy()
            else:
                trex_current_hitboxes[0] = pygame.Rect((x + 50, y + 5), (40, 30)).copy()
                trex_current_hitboxes[1] = pygame.Rect((x + 20, y + 25), (50, 45)).copy()

        def collision_happened():
            for hitbox in trex_current_hitboxes:
                if hitbox.colliderect(current_hindrance):
                    return True
                if not is_cactus and hitbox.colliderect(pterodactylus_current_body_hitbox):
                    return True
            return False

        field_width, field_height = 600, 600

        space = pymunk.Space()
        space.gravity = 0, 180
        space.damping = 1

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

        trex_down = False
        trex_hitboxes = [[pygame.Rect((0, 0), (45, 30)), pygame.Rect((0, 0), (70, 30))],
                         [pygame.Rect((0, 0), (40, 30)), pygame.Rect((0, 0), (50, 45))]]
        trex_current_hitboxes = deepcopy(trex_hitboxes[0])
        calculate_trex_hitbox_pos()
        freq = 20
        freq_count = 0

        cactuses_hitboxes = [pygame.Rect(field_width, 520, 120, 90),
                             pygame.Rect(field_width, 525, 85, 80),
                             pygame.Rect(field_width, 550, 30, 50),
                             pygame.Rect(field_width, 530, 35, 70)]

        pterodactylus_hitboxes = [pygame.Rect(field_width, 440, 30, 30),
                                  pygame.Rect(field_width, 540, 30, 30),
                                  pygame.Rect(field_width, 480, 30, 30)]
        pterodactylus_body_hitboxes = [pygame.Rect((field_width + 30, 455), (60, 30)),
                                       pygame.Rect((field_width + 30, 555), (60, 30)),
                                       pygame.Rect((field_width + 30, 495), (60, 30))]
        pterodactylus_current_body_hitbox = pterodactylus_body_hitboxes[0].copy()

        index = randint(0, len(cactuses_hitboxes) - 1)
        current_hindrance = cactuses_hitboxes[index].copy()
        hindrance_speed = 3
        is_cactus = True
        score = 0

        continue_game = True
        while continue_game:

            calculate_trex_hitbox_pos()

            freq_count += 1

            freq_count = freq_count % freq
            if freq_count == 0:
                score += 1
                if score % 50 == 0:
                    hindrance_speed += 1

            action = None
            if round(trex.position[1]) >= field_height - floor_height - trex_shape.radius:
                action = Actions.UP

            if action == Actions.UP:
                if round(trex.position[1]) >= field_height - floor_height - trex_shape.radius:
                    trex.apply_impulse_at_local_point((0, -230), (0, 0))
            if action == Actions.DOWN:
                if round(trex.position[1]) <= field_height - floor_height - trex_shape.radius:
                    trex.apply_impulse_at_local_point((0, 500), (0, 0))
                trex_current_hitboxes = deepcopy(trex_hitboxes[1])
                trex_down = True
                calculate_trex_hitbox_pos()
            elif action == Actions.RELEASE_DOWN or action == Actions.UP:
                trex_current_hitboxes = deepcopy(trex_hitboxes[0])
                trex_down = False
                calculate_trex_hitbox_pos()

            space.step(1 / 50)

            if is_cactus:
                width_to_add = current_hindrance.width
            else:
                width_to_add = pterodactylus_current_body_hitbox.width

            if current_hindrance.x + width_to_add <= 0:
                if uniform(0, 1) < 0.45:
                    is_cactus = True
                    new_hindrance_index = randint(0, len(cactuses_hitboxes) - 1)
                    current_hindrance = cactuses_hitboxes[new_hindrance_index].copy()
                else:
                    is_cactus = False
                    if uniform(0, 1) < 0.55:
                        current_hindrance = pterodactylus_hitboxes[-1].copy()
                        pterodactylus_current_body_hitbox = pterodactylus_body_hitboxes[-1].copy()
                    else:
                        new_hindrance_index = randint(0, len(pterodactylus_hitboxes) - 2)
                        current_hindrance = pterodactylus_hitboxes[new_hindrance_index].copy()
                        pterodactylus_current_body_hitbox = pterodactylus_body_hitboxes[new_hindrance_index].copy()
            else:
                current_hindrance.x -= hindrance_speed
                if not is_cactus:
                    pterodactylus_current_body_hitbox.x -= hindrance_speed

            if collision_happened():
                continue_game = False