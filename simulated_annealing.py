import random
import math

class SimulatedAnnealing:
  def __init__(self, tsp_instance, initial_temp, cooling_rate, iterations):
    """
    Inicializa o algoritmo de têmpera simulada

    Args:
      tsp_instance: Um objeto que representa uma instância do problema do caixeiro viajante
      initial_temp (float): A temperatura inicial do algoritmo
      cooling_rate (float): A taxa de decrescimento da temperatura
      iterations (int): O número máximo de iterações do algoritmo
    """
    self.instance = tsp_instance
    self.initial_temp = initial_temp
    self.cooling_rate = cooling_rate
    self.iterations = iterations
    self.best_tour = []
    self.best_distance = float('inf')
  
  def solve(self):
    """
    Executa o algoritmo de busca

    Retorna:
      Uma tupla contendo o melhor caminho encontrado e a distância percorrida por esse caminho
      (list, float)
    """
    if self.instance.num_cities < 2:
      return [], 0.0

    current_tour = list(range(self.instance.num_cities))
    random.shuffle(current_tour)
    current_distance = self.instance.get_tour_distance(current_tour)

    self.best_tour = list(current_tour)
    self.best_distance = current_distance

    temp = self.initial_temp

    for i in range(self.iterations):

      if temp <= 0:
        break

      i, j = random.sample(range(self.instance.num_cities), 2)
      next_tour = list(current_tour)
      next_tour[i], next_tour[j] = current_tour[j], current_tour[i]

      next_distance = self.instance.get_tour_distance(next_tour)
      distance_diff = next_distance - current_distance

      if distance_diff < 0:
        current_tour = next_tour
        current_distance = next_distance

        if current_distance < self.best_distance:
          self.best_tour = list(current_tour)
          self.best_distance = current_distance
          
      elif random.random() < math.exp(-distance_diff / temp):
        current_tour = list(next_tour)
        current_distance = next_distance
      
      temp *= self.cooling_rate
    
    return self.best_tour, self.best_distance
