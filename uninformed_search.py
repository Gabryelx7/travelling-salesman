import collections

class BreadthFirstSearch:
  def __init__(self, tsp_instance):
    """
    Inicializa o algoritmo de busca por largura

    Args:
      tsp_instance: Um objeto que representa uma instância do problema do caixeiro viajante
    """
    self.instance = tsp_instance
    self.best_tour = []
    self.best_distance = float('inf')
  
  def solve(self):
    """
    Executa o algoritmo de busca

    Retorna:
      Uma tupla contendo o melhor caminho encontrado e a distância percorrida por esse caminho
      (list, float)
    """
    queue = collections.deque()

    for start_city in range(self.instance.num_cities):
      initial_tour = [start_city]
      initial_distance = 0.0
      queue.append((initial_tour, initial_distance)) 

      while queue:
        current_tour, current_distance = queue.popleft()

        if len(current_tour) == self.instance.num_cities:
          add_distance = self.instance.distance_matrix[current_tour[-1]][start_city]
          final_distance = current_distance + add_distance

          if final_distance < self.best_distance:
            self.best_distance = final_distance
            self.best_tour = current_tour
          
          continue

        for next_city in range(self.instance.num_cities):
          if next_city not in current_tour:
            new_tour = list(current_tour)
            new_tour.append(next_city)

            add_distance = self.instance.distance_matrix[current_tour[-1]][next_city]
            new_distance = current_distance + add_distance

            queue.append((new_tour, new_distance))
    
    return self.best_tour, self.best_distance



