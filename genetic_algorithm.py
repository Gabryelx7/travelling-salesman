import random
import math

class GeneticAlgorithm:
  def __init__(self, instance, pop_size=100, generations=100, crossover_rate=0.8, mutation_rate=0.05):
    """
    Inicializa o algoritmo genético canônico

    Args:
      tsp_instance: Um objeto que representa uma instância do problema do caixeiro viajante
      pop_size (int): O tamanho das populações
      generations (int): O número de iterações do algoritmo
      crossover_rate (float): A probabilidade de realizar crossovers
      mutation_rate (float): A probabilidade de realizar mutações
    """
    self.instance = instance
    self.pop_size = pop_size
    self.generations = generations
    self.crossover_rate = crossover_rate
    self.mutation_rate = mutation_rate
    self.population = []
    self.weights = []
    self.best_tour = []
    self.best_distance = float('inf')
  
  def _generate_initial_population(self):
    """
    Gera a população inicial aleatoriamente

    Retorna:
      Uma lista contendo {pop_size} tours
    """
    population = []

    for _ in range(self.pop_size):
      new_pop = list(range(self.instance.num_cities))
      random.shuffle(new_pop)
      population.append(new_pop)
    
    return population

  def _select_roulette(self, fitness_scores):
    """
    Seleciona um indivíduo usando o método da roleta

    Args:
      fitness_scores (list): A lista dos valores de fitness para cada população

    Retorna:
      O índice da população escolhida
    """
    total_fitness = sum(fitness_scores)
    if(total_fitness == 0):
      return random.choice(range(self.pop_size))

    pick = random.uniform(0, total_fitness)
    accum = 0.0

    for i in range(self.pop_size):
      accum += fitness_scores[i]
      if accum > pick:
        return i
      
    return self.pop_size-1
  
  def _apply_crossover(self, parent1, parent2):
    """
    Aplica o PMX (Partially Mapped Crossover) com o ponto de crossover escolhido
    aleatoriamente

    Args:
      parent1, parent2 (list): Dois indivíduos da população

    retorna:
      Duas listas contendo os índividuos após o crossover
    """

    route_size = self.instance.num_cities
    child1, child2 = [-1] * route_size, [-1] * route_size
    crossover_line = random.randint(1,route_size-1)

    child1[:crossover_line] = parent1[:crossover_line]
    child2[:crossover_line] = parent2[:crossover_line]

    def fill_child(child, parent1, parent2):
      mapping = {parent1[i]: parent2[i] for i in range(crossover_line)}
      for i in range(route_size):
        if child[i] == -1:
          city = parent2[i]
          while city in mapping:
            city = mapping[city]
          child[i] = city

    fill_child(child1, parent1, parent2)
    fill_child(child2, parent2, parent1)

    return child1, child2
  
  def _apply_mutation(self, route):
    """
    Aplica a mutação em um indivíduo com a operação swap (troca de dois elementos
    elementos aleatorios do indivíduo)

    Args:
      route (list): O indivíduo à ser mutado

    retorna:
      Uma lista contendo o indivíduo após a mutação
    """
    i, j = random.sample(range(self.instance.num_cities), 2)

    route[i], route[j] = route[j], route[i]

    return route
  
  def solve(self):
    """
    Executa o algoritmo genético

    Retorna:
      Uma tupla contendo o melhor tour encontrado e a distância percorrida por esse tour
      (list, float)
    """
    self.population = self._generate_initial_population()

    for gen in range(self.generations):
      next_population = []

      distances = [self.instance.get_tour_distance(tour) for tour in self.population]

      min_distance = min(distances)
      if min_distance < self.best_distance:
        self.best_distance = min_distance
        self.best_tour = self.population[distances.index(min_distance)]

      max_distance = max(distances)
      fitness_scores = [max_distance - d for d in distances]

      fittest_individual = self.population[distances.index(min_distance)]
      next_population.append(fittest_individual)

      while len(next_population) < self.pop_size:
        parent1_idx = self._select_roulette(fitness_scores)
        parent2_idx = self._select_roulette(fitness_scores)
        parent1 = self.population[parent1_idx]
        parent2 = self.population[parent2_idx]

        if random.random() < self.crossover_rate:
          child1, child2 = self._apply_crossover(parent1, parent2)
        else:
          child1, child2 = parent1, parent2

        if random.random() < self.mutation_rate:
          child1 = self._apply_mutation(child1)
        elif random.random() < self.mutation_rate:
          child2 = self._apply_mutation(child2)
        
        next_population.append(child1)
        if len(next_population) < self.pop_size:
          next_population.append(child2)
      
      self.population = next_population
    
    return self.best_tour, self.best_distance
