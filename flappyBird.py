import pygame
import config
from bird import Bird
from bird_population import Bird_population
from pipes import Pipes

pygame.init()

font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()
running = True

pipes = Pipes()
population = Bird_population(10)


def draw_info_box():

    info_x = config.window_x - 310
    info_y = 10
    info_width = 300
    line_height = 25

    base_height = 100
    species_info_height = len(population.species) * line_height
    graph_height = 100
    info_height = base_height + species_info_height + graph_height + 20  # Add padding

    pygame.draw.rect(
        config.screen, (50, 50, 50), (info_x, info_y, info_width, info_height)
    )
    pygame.draw.rect(
        config.screen, (255, 255, 255), (info_x, info_y, info_width, info_height), 2
    )

    small_font = pygame.font.Font(None, 20)
    general_info_lines = [
        f"Generation: {population.generation}",
        f"Species: {len(population.species)}",
        f"Birds alive: {sum(1 for bird in population.birds if bird.alive)}",
        f"Best Score: {population.best_score}",
        f"Best Bird's Generation: {population.best_generation}",
    ]
    text_x = info_x + 10
    text_y = info_y + 10
    for line in general_info_lines:
        info_text = small_font.render(line, True, (255, 255, 255))
        config.screen.blit(info_text, (text_x, text_y))
        text_y += line_height

    pygame.draw.line(
        config.screen,
        (255, 255, 255),
        (info_x + 10, text_y),
        (info_x + info_width - 10, text_y),
        1,
    )
    text_y += 10

    for i, species in enumerate(population.species):
        pygame.draw.circle(
            config.screen, species.species_color, (text_x, text_y + 10), 8
        )

        species_info = f"Species {i + 1} | Best fit: {species.benchmark_fitness} | Avg: {species.average_fitness} | Stale: {species.staleness}"
        info_text = small_font.render(species_info, True, (200, 200, 200))
        config.screen.blit(info_text, (text_x + 20, text_y))  # Add padding for the text
        text_y += line_height


while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_ESCAPE]:
        pygame.event.post(pygame.event.Event(pygame.QUIT))

    config.screen.fill("black")
    draw_info_box()

    if not population.extinct():
        population.update_birds(config.screen, pipes)
    else:
        pipes.clear_pipes()
        pipes = Pipes()
        population.natural_selection()
    population.update_best_bird()
    pipes.update()
    pipes.draw(config.screen)
    pygame.display.flip()


pygame.quit()
