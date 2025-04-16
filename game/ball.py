import pygame
import random


pygame.init()
width, height = 800, 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Equalizer")
clock = pygame.time.Clock()


ball = pygame.Rect(400, 0, 10, 10)
vely = 20
accelx = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    
    ball.y += vely 
    ball.x += accelx
    if ball.y >= height -10:
        ball.y = height - 10
        vely = -vely
        accelx = random.randint(-20 , 20)

    if ball.y <= 0:
        ball.y =  0
        vely = -vely
        accelx = random.randint(-20 , 20)

    if ball.x <= 0:
        accelx = 20
    
    if ball.x >= width -10:
        accelx = -20
    
    screen.fill((10, 10, 10))
    pygame.draw.circle(screen, "White", ball.center, 5, 5)
    pygame.display.flip()   
    clock.tick(60)

pygame.quit()
