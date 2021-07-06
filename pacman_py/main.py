import numpy as np
import pygame
import pacman_py.map as map
import pacman_py.pacman as pacman
import time

def redraw(screen, pacman, map):
    black = [0, 0, 0]
    yellow = (255, 211, 67)

    screen.fill(black)
    pygame.draw.circle(screen, yellow, pacman.get_xy(), pacman.get_radius())
    for i in range(len(map)):
        pygame.draw.rect(screen, yellow, map[i])

    pygame.display.update()

def main():
    (width, height) = (420, 420)
    black = [0, 0, 0]
    yellow = (255,211,67)
    mp = map.Map().get_map()
    pc = pacman.Pacman()

    screen = pygame.display.set_mode((width, height))
    redraw(screen, pc, mp)

    running = True
    while running:
        time.sleep(0.01)
        redraw(screen, pc, mp)
        pc.move()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    pc.set_vector(3)
                    # pc.move()
                elif event.key == pygame.K_DOWN:
                    pc.set_vector(4)
                    # pc.move()
                elif event.key == pygame.K_LEFT:
                    pc.set_vector(1)
                    # pc.move()
                elif event.key == pygame.K_RIGHT:
                    pc.set_vector(2)
                    # pc.move()




if __name__ == "__main__":
    main()