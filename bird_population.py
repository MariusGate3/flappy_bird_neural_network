from bird import Bird
import math
import species
import operator


class Bird_population:
    def __init__(self, size):
        self.birds = []
        self.species = []
        self.generation = 1
        self.size = size

        for i in range(size):
            bird = Bird(200, 400, 25)
            self.birds.append(bird)

    def update_birds(self, screen, pipes):
        for bird in self.birds:
            if pipes.check_collision(bird):
                bird.alive = False
            pipes.check_passed(bird)
            if bird.alive:
                bird.look(pipes)
                bird.draw(screen)
                bird.update()
                bird.think()

    def extinct(self):
        for bird in self.birds:
            if bird.alive:
                return False
        return True

    def natural_selection(self):
        print("Specaiting...")
        self.speciate()

        print("calculating fitness...")
        self.calculate_fitness()

        print("killing off extinct species...")
        self.kill_extinct_species()

        print("Sorting species by fitness...")
        self.sort_species_by_fitness()

        print("Breeding children for next generation...")
        self.next_generation()

        print("Next generation ready!")

    def speciate(self):
        for s in self.species:
            s.birds = []

        for bird in self.birds:
            add_to_species = False
            for s in self.species:
                if s.similar_brain(bird.brain):
                    s.add_bird_to_species(bird)
                    add_to_species = True
                    break
            if not add_to_species:
                self.species.append(species.Species(bird))

        print(f"Number of species after speciation: {len(self.species)}")
        for i, s in enumerate(self.species):
            print(f"Species {i} has {len(s.birds)} birds")

    def calculate_fitness(self):
        for bird in self.birds:
            bird.calculate_fitness()

        for s in self.species:
            s.calculate_average_fitness()

    def kill_extinct_species(self):
        self.species = [s for s in self.species if len(s.birds) > 0]

    def sort_species_by_fitness(self):
        for s in self.species:
            s.sort_birds_by_fitness()

        self.species.sort(key=operator.attrgetter("benchmark_fitness"), reverse=True)

    def next_generation(self):
        children = []

        for s in self.species:
            children.append(s.champion.clone())

        children_per_species = math.floor(
            (self.size - len(self.species)) / len(self.species)
        )

        for s in self.species:
            for i in range(0, children_per_species):
                children.append(s.offspring())

        while len(children) < self.size:
            children.append(self.species[0].offspring())

        self.birds = []

        for child in children:
            self.birds.append(child)
        self.generation += 1
