import pygame
import config
import random
import brain

pygame.font.init()


class Bird:
    def __init__(self, xPos, yPos, radius):

        self.score = 0
        self.scoreText = pygame.font.Font(None, 20)
        self.radius = radius
        self.color = (
            random.randint(100, 255),
            random.randint(100, 255),
            random.randint(100, 255),
        )
        self.image = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (radius, radius), radius)

        self.rect = self.image.get_rect()
        self.rect.center = (xPos, yPos)
        self.velocity = 0
        self.flap = False
        self.alive = True
        self.passed_pipes = []
        self.lifespan = 0

        self.fitness = 0
        self.inputs = 3
        self.decision = None
        self.brain = brain.Brain(self.inputs)
        self.brain.generate_net()
        self.vision = [0.5, 0.5, 0.5]

    def update(self):
        if self.velocity < 4:
            self.velocity += 0.5
        self.rect.y += self.velocity
        if self.flap and self.velocity > 0:
            self.flap = False
        text_surface = self.scoreText.render(
            f"Score: {self.score}", True, "white", None
        )
        self.lifespan += 1
        config.screen.blit(text_surface, (self.rect.x, self.rect.y - 50))

    def can_jump(self):
        return self.velocity >= 0

    def jump(self):
        if self.can_jump():
            self.velocity = -8
            self.flap = True

    def closest_pipe(self, pipes):
        for i in range(0, len(pipes.top_pipes)):
            if not pipes.top_pipes[i] in self.passed_pipes:
                return (pipes.top_pipes[i], pipes.bottom_pipes[i])

    def look(self, pipes):
        if pipes.top_pipes:
            closest = self.closest_pipe(pipes)  # Get the closest top and bottom pipes
            top_pipe = closest[0]
            bottom_pipe = closest[1]

            # Vision 0: Distance from the bird's center to the bottom of the top pipe
            self.vision[0] = (
                max(0, self.rect.center[1] - top_pipe.rect.bottom) / config.window_y
            )
            pygame.draw.line(
                config.screen,
                self.color,
                self.rect.center,
                (self.rect.center[0], top_pipe.rect.bottom),
            )

            # Vision 1: Horizontal distance from the bird's center to the front of the top pipe
            self.vision[1] = (
                max(0, top_pipe.rect.x - self.rect.center[0]) / config.window_x
            )
            pygame.draw.line(
                config.screen,
                self.color,
                self.rect.center,
                (top_pipe.rect.x, self.rect.center[1]),
            )

            # Vision 2: Distance from the bird's center to the top of the bottom pipe
            self.vision[2] = (
                max(0, bottom_pipe.rect.top - self.rect.center[1]) / config.window_y
            )
            pygame.draw.line(
                config.screen,
                self.color,
                self.rect.center,
                (self.rect.center[0], bottom_pipe.rect.top),
            )

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def think(self):
        self.decision = self.brain.feed_forward(self.vision)
        if self.decision <= 0.5:
            self.jump()

    def calculate_fitness(self):
        self.fitness = self.lifespan

    def clone(self):
        clone = Bird(200, 400, 25)
        clone.fitness = self.fitness
        clone.brain = self.brain.clone()
        clone.brain.generate_net()
        return clone
