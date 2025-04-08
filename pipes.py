import pygame
import random
import config


class Pipe:
    def __init__(self, width, height, x, y):
        self.surface = pygame.Surface((width, height))
        self.rect = self.surface.get_rect(topleft=(x, y))
        self.surface.fill("white")
        self.pipe_gap = 175


class Pipes:
    def __init__(self):
        self.top_pipes = []
        self.bottom_pipes = []
        self.pipe_spacing = 400
        self.pipe_width = 75
        self.pipes_speed = 2

        for i in range(7):
            self.add_pipe(100 + (i + 1) * self.pipe_spacing)

    def add_pipe(self, x):
        top_pipe_height = random.randint(100, 400)
        top_pipe = Pipe(self.pipe_width, top_pipe_height, x, 0)

        bottom_pipe_y = top_pipe_height + top_pipe.pipe_gap
        bottom_pipe_height = config.window_y - bottom_pipe_y
        bottom_pipe = Pipe(self.pipe_width, bottom_pipe_height, x, bottom_pipe_y)

        self.top_pipes.append(top_pipe)
        self.bottom_pipes.append(bottom_pipe)

    def remove_pipe(self, pipe_list, pipe):
        pipe_list.remove(pipe)

    def update(self):
        for pipe in self.top_pipes:
            pipe.rect.x -= self.pipes_speed
            if pipe.rect.x < -pipe.rect.width:
                self.top_pipes.remove(pipe)

        for pipe in self.bottom_pipes:
            pipe.rect.x -= self.pipes_speed
            if pipe.rect.x < -pipe.rect.width:
                self.bottom_pipes.remove(pipe)

        if (
            len(self.top_pipes) > 0
            and self.top_pipes[-1].rect.x < config.window_x - self.pipe_spacing
        ):
            self.add_pipe(config.window_x + self.pipe_spacing)

    def check_collision(self, bird):
        # Check collision with top pipes
        for pipe in self.top_pipes:
            if bird.rect.colliderect(pipe.rect):
                return True

        # Check collision with bottom pipes
        for pipe in self.bottom_pipes:
            if bird.rect.colliderect(pipe.rect):
                return True

        # Check if the bird goes out of screen bounds
        if bird.rect.top < 0 or bird.rect.bottom > config.window_y:
            return True

        return False

    def check_passed(self, bird):
        for pipe in self.top_pipes:
            if (
                pipe not in bird.passed_pipes
                and bird.rect.x > pipe.rect.x + pipe.rect.width
            ):
                bird.passed_pipes.append(pipe)
                bird.score += 1
                return True
        return False

    def clear_pipes(self):
        for pipe in self.top_pipes:
            self.remove_pipe(self.top_pipes, pipe)
        for pipe in self.bottom_pipes:
            self.remove_pipe(self.bottom_pipes, pipe)

    def draw(self, screen):
        for pipe in self.top_pipes:
            screen.blit(pipe.surface, pipe.rect)
        for pipe in self.bottom_pipes:
            screen.blit(pipe.surface, pipe.rect)
