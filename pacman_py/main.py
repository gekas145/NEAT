import numpy as np
import pygame

def main():
    (width, height) = (600, 600)
    screen = pygame.display.set_mode((width, height))
    pygame.display.update()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


if __name__ == "__main__":
    main()