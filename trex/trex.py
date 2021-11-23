import pygame
import pymunk
import sys
from random import uniform, randint
from actions import Actions
from copy import deepcopy


class TRexGame:

    def __init__(self, agent=None, screen=None, font=None, clock=None, min_speed=3, max_speed=10):
        if agent is None and (screen is None or font is None or clock is None):
            raise Exception("When human is playing screen, font and clock have to be defined!")
        self.agent = agent
        self.screen = screen
        self.font = font
        self.clock = clock
        self.max_speed = max_speed
        self.min_speed = min_speed

    def play_game(self):

        def calculate_trex_hitbox_pos():
            x, y = trex.position
            if trex_down:
                trex_current_hitboxes[0] = pygame.Rect((x + 70, y + 40), (45, 30)).copy()
                trex_current_hitboxes[1] = pygame.Rect((x + 20, y + 45), (70, 30)).copy()
            else:
                trex_current_hitboxes[0] = pygame.Rect((x + 50, y + 5), (40, 30)).copy()
                trex_current_hitboxes[1] = pygame.Rect((x + 20, y + 25), (50, 45)).copy()

        def draw_next_game_step(screen, clock, draw_hitboxes=True):
            screen.fill(gray)
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

        def get_game_data():
            data = {
                "own_height": 1 - (trex.position[1] - 360) / (510 - 360),
                "distance_to_hindrance": (current_hindrance.x - trex.position[0]) / (600 - trex.position[0]),
                "hindrance_height": current_hindrance.height / 90,
                "hindrance_width": current_hindrance.width / 120,
                "hindrance_flight_height": (580 - current_hindrance.y - current_hindrance.height) / 130,
                "hindrance_speed": (hindrance_speed - self.min_speed) / self.max_speed
            }
            if not is_cactus:
                data["hindrance_width"] += pterodactylus_current_body_hitbox.width / 120
            else:
                data["hindrance_flight_height"] = 0
            return data

        space = pymunk.Space()
        space.gravity = 0, 180
        space.damping = 1

        gray = (127, 127, 127)
        black = (0, 0, 0)
        dino_color = (54, 54, 54)

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

        game_over_image = pygame.transform.scale(pygame.image.load('images/game_over.png'), (270, 40))

        trex_game_over_image = pygame.transform.scale(pygame.image.load('images/dino_game_over.png'), (90, 95))

        trex_up_images = [pygame.image.load('images/dino_right.png'), pygame.image.load('images/dino_left.png')]
        trex_down_images = [pygame.image.load('images/dino_down_left.png'),
                            pygame.image.load('images/dino_down_right.png')]
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
        hindrance_speed = self.min_speed
        is_cactus = True
        score = 0

        continue_game = True
        while continue_game:

            calculate_trex_hitbox_pos()

            freq_count_trex_image += 1

            freq_count_trex_image = freq_count_trex_image % change_freq_trex_image
            if freq_count_trex_image == 0:
                current_image_num = 1 - current_image_num
                score += 1
                if score % 50 == 0 and hindrance_speed < self.max_speed:
                    hindrance_speed += 1

            if not is_cactus:
                current_hindrance_image = pterodactylus[current_image_num].copy()

            action = None
            if self.agent is None:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        continue_game = False
                    if event.type == pygame.MOUSEBUTTONUP:
                        pass
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            action = Actions.UP
                        if event.key == pygame.K_DOWN:
                            action = Actions.DOWN
                    if event.type == pygame.KEYUP:
                        action = Actions.RELEASE_DOWN
            else:
                if freq_count_trex_image == 0:
                    action = self.agent.get_decision()

            if action == Actions.UP:
                if round(trex.position[1]) >= field_height - floor_height - trex_shape.radius:
                    trex.apply_impulse_at_local_point((0, -230), (0, 0))
            if action == Actions.DOWN:
                if round(trex.position[1]) <= field_height - floor_height - trex_shape.radius:
                    trex.apply_impulse_at_local_point((0, 500), (0, 0))
                trex_current_images = trex_down_images.copy()
                trex_current_hitboxes = deepcopy(trex_hitboxes[1])
                trex_down = True
                calculate_trex_hitbox_pos()
            elif action == Actions.RELEASE_DOWN or action == Actions.UP:
                trex_current_images = trex_up_images.copy()
                trex_current_hitboxes = deepcopy(trex_hitboxes[0])
                trex_down = False
                calculate_trex_hitbox_pos()

            if self.screen is not None:
                draw_next_game_step(self.screen, self.clock, False)
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
                        pterodactylus_current_body_hitbox = pterodactylus_body_hitboxes[new_hindrance_index].copy()
                    current_hindrance_image = pterodactylus[0].copy()
            else:
                current_hindrance.x -= hindrance_speed
                if not is_cactus:
                    pterodactylus_current_body_hitbox.x -= hindrance_speed
                if self.screen is not None:
                    self.screen.blit(current_hindrance_image, (current_hindrance.x, current_hindrance.y))

            if self.screen is not None:
                self.screen.blit(self.font.render('Score: ' + str(score), False, dino_color),
                                 (field_width - 150, field_height / 3))
                pygame.display.update()

            if collision_happened():
                trex_current_images = [trex_game_over_image.copy(), trex_game_over_image.copy()]
                if self.screen is not None:
                    draw_next_game_step(self.screen, self.clock, False)
                    self.screen.blit(current_hindrance_image, (current_hindrance.x, current_hindrance.y))
                    self.screen.blit(game_over_image, (field_width / 2 - 120, field_height / 2))
                    pygame.display.update()
                    wait = True
                    while wait:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                wait = False
                continue_game = False

            if freq_count_trex_image == 0:
                print("----------------------------------")
                print(get_game_data())
