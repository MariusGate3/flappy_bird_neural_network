import pygame
import config
from bird import Bird
from bird_population import Bird_population
from pipes import Pipes

pygame.init()

clock = pygame.time.Clock()
running = True

# Single bird
# bird = Bird(200, 400, 25, "yellow")

pipes = Pipes()
population = Bird_population(30)
while running:
    dt = clock.tick(60) / 1000
    ct = pygame.time.get_ticks() / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # if bird.can_jump(ct) and keys[pygame.K_SPACE]:
    #     bird.jump(ct)
    # elif keys[pygame.K_ESCAPE]:
    #     pygame.event.post(pygame.event.Event(pygame.QUIT))

    if keys[pygame.K_ESCAPE]:
        pygame.event.post(pygame.event.Event(pygame.QUIT))

    config.screen.fill("black")

    if not population.extinct():
        population.update_birds(config.screen, pipes)
    else:
        pipes.clear_pipes()
        pipes = Pipes()
        population.natural_selection()
    pipes.update()
    pipes.draw(config.screen)
    pygame.display.flip()


pygame.quit()
