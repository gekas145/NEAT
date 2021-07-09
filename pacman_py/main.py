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


def redraw(screen, pacman, map):
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

    pygame.display.update()


def main():
    (width, height) = (420, 424)
    mp = map.Map(width, height).get_map()
    pc = pacman.Pacman()

    screen = pygame.display.set_mode((width, height))
    redraw(screen, pc, mp)

    running = True
    while running:
        if not check_collision(mp, pc, width, height):
            pc.move()
        time.sleep(0.01)
        redraw(screen, pc, mp)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                old_vector = pc.get_vector()
                if event.key == pygame.K_UP:
                    pc.set_vector(3)
                    if check_collision(mp, pc, width, height):
                        pc.set_vector(old_vector)
                elif event.key == pygame.K_DOWN:
                    pc.set_vector(4)
                    if check_collision(mp, pc, width, height):
                        pc.set_vector(old_vector)
                elif event.key == pygame.K_LEFT:
                    pc.set_vector(1)
                    if check_collision(mp, pc, width, height):
                        pc.set_vector(old_vector)
                elif event.key == pygame.K_RIGHT:
                    pc.set_vector(2)
                    if check_collision(mp, pc, width, height):
                        pc.set_vector(old_vector)


if __name__ == "__main__":
    main()
