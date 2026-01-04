import random
import numpy as np
from copy import deepcopy


class ArtificialBeeColony:
    def __init__(self, num_bees, num_exams, num_timeslots, limit, max_iter, fitness_func):
        self.num_bees = num_bees
        self.num_exams = num_exams
        self.num_timeslots = num_timeslots
        self.limit = limit
        self.max_iter = max_iter
        self.fitness_func = fitness_func

        self.food_sources = []
        self.fitness = []
        self.trial_counters = []
        self.best_solution = None
        self.best_fitness = float("inf")
        self.fitness_history = []

    # =========================
    # Initialization
    # =========================
    def initialize(self):
        self.food_sources = []
        self.fitness = []
        self.trial_counters = [0] * self.num_bees

        for _ in range(self.num_bees):
            solution = self.random_solution()
            fit = self.fitness_func(solution)

            self.food_sources.append(solution)
            self.fitness.append(fit)

            if fit < self.best_fitness:
                self.best_fitness = fit
                self.best_solution = solution

    def random_solution(self):
        return [random.randint(0, self.num_timeslots - 1)
                for _ in range(self.num_exams)]

    # =========================
    # Employed Bee Phase
    # =========================
    def employed_bee_phase(self):
        for i in range(self.num_bees):
            candidate = self.generate_neighbor(self.food_sources[i])
            candidate_fitness = self.fitness_func(candidate)

            if candidate_fitness < self.fitness[i]:
                self.food_sources[i] = candidate
                self.fitness[i] = candidate_fitness
                self.trial_counters[i] = 0
            else:
                self.trial_counters[i] += 1

    # =========================
    # Onlooker Bee Phase
    # =========================
    def onlooker_bee_phase(self):
        probabilities = self.calculate_probabilities()

        for _ in range(self.num_bees):
            i = self.roulette_wheel_selection(probabilities)
            candidate = self.generate_neighbor(self.food_sources[i])
            candidate_fitness = self.fitness_func(candidate)

            if candidate_fitness < self.fitness[i]:
                self.food_sources[i] = candidate
                self.fitness[i] = candidate_fitness
                self.trial_counters[i] = 0
            else:
                self.trial_counters[i] += 1

    def calculate_probabilities(self):
        fitness_inv = [1 / (f + 1e-6) for f in self.fitness]
        total = sum(fitness_inv)
        return [f / total for f in fitness_inv]

    def roulette_wheel_selection(self, probabilities):
        r = random.random()
        cumulative = 0
        for i, p in enumerate(probabilities):
            cumulative += p
            if r <= cumulative:
                return i
        return len(probabilities) - 1

    # =========================
    # Scout Bee Phase
    # =========================
    def scout_bee_phase(self):
        for i in range(self.num_bees):
            if self.trial_counters[i] >= self.limit:
                self.food_sources[i] = self.random_solution()
                self.fitness[i] = self.fitness_func(self.food_sources[i])
                self.trial_counters[i] = 0

    # =========================
    # Neighborhood Search
    # =========================
    def generate_neighbor(self, solution):
        neighbor = deepcopy(solution)
        exam_idx = random.randint(0, self.num_exams - 1)
        neighbor[exam_idx] = random.randint(0, self.num_timeslots - 1)
        return neighbor

    # =========================
    # Main Loop
    # =========================
    def run(self):
        self.initialize()

        for iteration in range(self.max_iter):
            self.employed_bee_phase()
            self.onlooker_bee_phase()
            self.scout_bee_phase()

            current_best = min(self.fitness)
            self.fitness_history.append(current_best)

            if current_best < self.best_fitness:
                self.best_fitness = current_best
                self.best_solution = self.food_sources[self.fitness.index(current_best)]

        return self.best_solution, self.best_fitness, self.fitness_history
