import numpy as np
import pygame
import map as map
import pacman as pacman
import time
import random
import ghost as ghost


def check_collision(mp, pc, width, height):
    """
    :return: bool, True if there is collision
    """

    x, y = pc.get_front_xy()
    for i in range(1, len(mp)):
        if mp[i].collidepoint([x, y]):
            return True

    if x >= width - 3 or x <= 3:
        return True
    elif y >= height - 1 or y <= 3:
        return True

    return False


def check_corners_collision(pc, corners):
    x, y = pc.get_xy()
    for i in range(len(corners)):
        if np.sqrt((x - corners[i][0]) ** 2 + (y - corners[i][1]) ** 2) <= 1.5:
            return True
    return False


def check_turn(old_vector, new_vector):
    if np.abs(old_vector - new_vector) == 1 and old_vector + new_vector != 5:
        return False
    return True


def check_new_vector(new_vector, mp, pc, corners, width, height):
    old_vector = pc.get_vector()

    if not check_turn(old_vector, new_vector):
        pc.set_vector(new_vector)
        return pc

    pc.set_vector(new_vector)
    if check_corners_collision(pc, corners) and not check_collision(mp, pc, width, height):
        return pc

    pc.set_vector(old_vector)
    return None


def check_points(pc, points, score):
    x, y = pc.get_xy()
    index = None
    for i in range(len(points)):
        if np.sqrt((x - points[i][0]) ** 2 + (y - points[i][1]) ** 2) <= pc.get_radius():
            index = i
            score += 1
            break

    if index is not None:
        points.pop(index)

    return points, score




def redraw(screen, pacman, ghosts, map, points, width, height):
    black = [0, 0, 0]
    yellow = [255, 211, 67]
    blue = [0, 0, 255]
    red = [255, 0, 0]

    pygame.draw.rect(screen, black, [0, 0, width, height])
    pygame.draw.circle(screen, yellow, pacman.get_xy(), pacman.get_radius())
    for i in range(len(map)):
        if i != 0 and i != len(map) - 1:
            pygame.draw.rect(screen, blue, map[i])
        else:
            pygame.draw.rect(screen, blue, map[i], width=3)

    for i in range(len(points)):
        pygame.draw.circle(screen, yellow, points[i], 3)

    for i in range(len(ghosts)):
        pygame.draw.circle(screen, red, ghosts[i].get_xy(), ghosts[i].get_radius())

    pygame.display.update()


def redraw_labels(screen, score):
    pygame.draw.rect(screen, [0, 0, 0], [0, 426, 420, 40])

    font = pygame.font.SysFont("monospace", 20)

    text = font.render("Epoc number: ", 0, [255, 255, 255])
    screen.blit(text, (30, 430))

    text1 = font.render("Score: " + str(score), 0, [255, 255, 255])
    screen.blit(text1, (300, 430))

    pygame.display.update()


def main():
    (width, height) = (420, 424)
    bottom_margin = 30
    mp, corners, points = map.Map(width, height).get_attributes()
    pc = pacman.Pacman(13, 13)
    ghosts = [ghost.Ghost(234, 13), ghost.Ghost(93, 274)]

    pygame.init()
    screen = pygame.display.set_mode((width, height + bottom_margin))
    score = 0
    old_score = 0
    points, score = check_points(pc, points, score)
    redraw(screen, pc, ghosts, mp, points, width, height)

    redraw_labels(screen, score)

    running = True
    memorized_vector = None
    iter_count = 0
    while running:
        iter_count += 1
        if not check_collision(mp, pc, width, height):
            pc.move()
        for i in range(len(ghosts)):
            if not check_collision(mp, ghosts[i], width, height):
                ghosts[i].move()
        time.sleep(0.01)
        points, score = check_points(pc, points, score)
        if old_score != score:
            redraw_labels(screen, score)
            old_score = score
        redraw(screen, pc, ghosts, mp, points, width, height)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if iter_count % 20 == 0:
            new_vector = random.randint(1, 5)
            if new_vector == 3:
                tmp = check_new_vector(3, mp, pc, corners, width, height)
                if tmp is not None:
                    pc = tmp
                    memorized_vector = None
                else:
                    memorized_vector = 3
            elif new_vector == 4:
                tmp = check_new_vector(4, mp, pc, corners, width, height)
                if tmp is not None:
                    pc = tmp
                    memorized_vector = None
                else:
                    memorized_vector = 4
            elif new_vector == 1:
                tmp = check_new_vector(1, mp, pc, corners, width, height)
                if tmp is not None:
                    pc = tmp
                    memorized_vector = None
                else:
                    memorized_vector = 1
            elif new_vector == 2:
                tmp = check_new_vector(2, mp, pc, corners, width, height)
                if tmp is not None:
                    pc = tmp
                    memorized_vector = None
                else:
                    memorized_vector = 2
        tmp = None
        if memorized_vector is not None:
            tmp = check_new_vector(memorized_vector, mp, pc, corners, width, height)
        if tmp is not None:
            pc = tmp
        for i in range(len(ghosts)):
            if check_corners_collision(ghosts[i], corners) and random.randint(1, 4) == 1:
                ghosts[i].set_vector(random.randint(1, 5))


if __name__ == "__main__":
    main()
