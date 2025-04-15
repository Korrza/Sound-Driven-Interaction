import pygame
import random


pygame.init()
width, height = 800, 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Equalizer")
clock = pygame.time.Clock()


bar_width = 20
spacing = 5
num_bars = width // (bar_width + spacing)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((10, 10, 10))

    for i in range(num_bars):
        h = random.randint(10, height)
        x = i * (bar_width + spacing)
        y = height - h
        color = (100, 200, 255)
        pygame.draw.rect(screen, color, (x, y, bar_width, h))

    pygame.display.flip()
    clock.tick(10)

pygame.quit()
