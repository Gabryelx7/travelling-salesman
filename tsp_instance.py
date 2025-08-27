import random
import math

class TSPInstance:
  def __init__(self, num_cities=None):
    """
    Inicializa uma instância do problema do caixeiro viajante

    Args:
      num_cities (int): O número de cidades que serão geradas
    """
    self.num_cities = num_cities
    self.cities = []
    self.distance_matrix = []

    if self.num_cities:
      self.generate_uniform_instance()
  
  def generate_uniform_instance(self, max_coord=100):
    """
    Preenche a instância com um conjunto aleatório de cidades utilizando a distribuição uniforme

    Args:
      max_coord (int): O valor máximo que uma coordenada pode ter
    """
    for _ in range(self.num_cities):
      x = random.uniform(0,max_coord)
      y = random.uniform(0,max_coord)
      self.cities.append((x,y))
    
    self._build_distance_matrix()
    
  def _build_distance_matrix(self):
    """
    Método interno para calcular e criar a matriz de distâncias
    """
    self.distance_matrix = [[0 for _ in range(self.num_cities)] for _ in range(self.num_cities)]

    for i in range(self.num_cities):
      for j in range(self.num_cities):
        x1, y1 = self.cities[i]
        x2, y2 = self.cities[j]
        self.distance_matrix[i][j] = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
  
  def get_tour_distance(self, tour):
    """
    Calcula a distância percorrida por um caminho
    
    Args:
      tour (list): Um caminho possível para a instância
    """
    
    total_distance = self.distance_matrix[tour[self.num_cities-1]][tour[0]]

    for i in range(self.num_cities-1):
      total_distance += self.distance_matrix[tour[i]][tour[i+1]]
    
    return total_distance

