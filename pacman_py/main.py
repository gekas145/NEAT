import numpy as np
import pygame
import pacman_py.map as map
import pacman_py.pacman as pacman
import time


def check_collision(mp, pc, width, height):
    """
    :return: bool, True if there is collision
    """
    for i in range(1, len(mp)):
        if mp[i].collidepoint(pc.get_front_xy()):
            return True

    x, y = pc.get_front_xy()
    if x >= width - 3 or x <= 3:
        return True
    elif y >= height - 1 or y <= 3:
        return True

    return False


def check_corner(corners, pc):
    for i in range(len(corners)):
        x, y = corners[i]
        a, b = pc.get_xy()
        if np.sqrt((x - a)**2 + (y - b)**2) <= 0.01:
            return True
        # if corners[i] == pc.get_xy():
        #     return True
    return False


def redraw(screen, pacman, map, corners):
    black = [0, 0, 0]
    yellow = [255, 211, 67]
    blue = [0, 0, 255]

    screen.fill(black)
    pygame.draw.circle(screen, yellow, pacman.get_xy(), pacman.get_radius())
    for i in range(len(map)):
        if i != 0 and i != len(map) - 1:
            pygame.draw.rect(screen, blue, map[i])
        else:
            pygame.draw.rect(screen, blue, map[i], width=3)

    for i in range(len(corners)):
        pygame.draw.circle(screen, yellow, corners[i], 4)

    pygame.display.update()


def main():
    (width, height) = (420, 424)
    mp, corners = map.Map(width, height).get_attributes()
    pc = pacman.Pacman()

    screen = pygame.display.set_mode((width, height))
    redraw(screen, pc, mp, corners)

    running = True
    memorized_vector = None
    while running:
        if not check_collision(mp, pc, width, height):
            pc.move()
        time.sleep(0.01)
        redraw(screen, pc, mp, corners)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                old_vector = pc.get_vector()
                if event.key == pygame.K_UP:
                    pc.set_vector(3)
                    if check_collision(mp, pc, width, height):
                        pc.set_vector(old_vector)
                    memorized_vector = 3
                elif event.key == pygame.K_DOWN:
                    pc.set_vector(4)
                    if check_collision(mp, pc, width, height):
                        pc.set_vector(old_vector)
                    memorized_vector = 4
                elif event.key == pygame.K_LEFT:
                    pc.set_vector(1)
                    if check_collision(mp, pc, width, height):
                        pc.set_vector(old_vector)
                    memorized_vector = 1
                elif event.key == pygame.K_RIGHT:
                    pc.set_vector(2)
                    if check_collision(mp, pc, width, height):
                        pc.set_vector(old_vector)
                    memorized_vector = 2
        if check_corner(corners, pc) and memorized_vector is not None:
            pc.set_vector(memorized_vector)
            print(memorized_vector)
            memorized_vector = None
            # print(check_corner(corners, pc))
        # print(pc.get_vector())
        # print(memorized_vector)


if __name__ == "__main__":
    main()
