import operator
import random


class Species:
    def __init__(self, bird):
        self.birds = []
        self.average_fitness = 0
        self.threshold = 1.2
        self.birds.append(bird)
        self.benchmark_fitness = bird.fitness
        self.benchmark_brain = bird.brain.clone()
        self.champion = bird.clone()

    def similar_brain(self, brain):
        similarity = self.weight_difference(self.benchmark_brain, brain)
        return similarity < self.threshold

    @staticmethod
    def weight_difference(brain1, brain2):
        total_difference = 0
        for i in range(len(brain1.connections)):
            for j in range(len(brain2.connections)):
                if i == j:
                    total_difference += abs(
                        brain1.connections[i].weight - brain2.connections[j].weight
                    )
        return total_difference

    def add_bird_to_species(self, bird):
        self.birds.append(bird)

    def sort_birds_by_fitness(self):
        self.birds.sort(key=operator.attrgetter("fitness"), reverse=True)
        if self.birds[0].fitness > self.benchmark_fitness:
            self.benchmark_fitness = self.birds[0].fitness
            self.champion = self.birds[0].clone()

    def calculate_average_fitness(self):
        total_fitness = 0
        for bird in self.birds:
            total_fitness += bird.fitness

        if self.birds:
            self.average_fitness = int(total_fitness / len(self.birds))
        else:
            self.average_fitness = 0

    def offspring(self):
        if len(self.birds) == 1:
            baby = self.birds[0].clone()
        else:
            baby = self.birds[random.randint(1, len(self.birds) - 1)].clone()

        baby.brain.mutate()
        return baby
