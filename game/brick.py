import pygame
import random


pygame.init()
width, height = 1920, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Bricka moska")
clock = pygame.time.Clock()

num_line = 10
num_col = 30
brick_width = width / num_col
brick_height = height / num_line

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((10, 10, 10))
    y = 0
    for i in range(num_line):
        x = 0
        for z in range(num_col):
            x = z * brick_width
            color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
            pygame.draw.rect(screen, color, (x, y, brick_width, brick_height))
        y +=brick_height
        

    pygame.display.flip()
    clock.tick(10)

pygame.quit()