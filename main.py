from tsp_instance import TSPInstance
from uninformed_search import BreadthFirstSearch
from simulated_annealing import SimulatedAnnealing
from genetic_algorithm import GeneticAlgorithm

if __name__ == '__main__':
  tsp_problem = TSPInstance(10)

  bfs = BreadthFirstSearch(tsp_problem)
  sa = SimulatedAnnealing(tsp_problem, 100, 0.99, 300)
  ga = GeneticAlgorithm(tsp_problem)

  bfs_tour, bfs_dist = bfs.solve()
  sa_tour, sa_dist = sa.solve()
  ga_tour, ga_dist = ga.solve()

  print("BFS result:")
  print(bfs_tour)
  print(bfs_dist)

  print("Simulated Annealing result:")
  print(sa_tour)
  print(sa_dist)

  print("Genetic Algorithm result:")
  print(ga_tour)
  print(ga_dist)