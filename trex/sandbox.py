import sys

import pygame

from trex import TRexGame
from simple_agent import SimpleAgent

pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', 20)
pygame.init()
screen = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()

for i in range(2):
    game = TRexGame(agent=SimpleAgent(), screen=screen, font=font, clock=clock)
    # game = TRexGame(agent=SimpleAgent())
    game.play_game()
    print("ALOHA")

pygame.display.quit()
pygame.quit()
sys.exit()
