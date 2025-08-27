from tsp_instance import TSPInstance
from uninformed_search import BreadthFirstSearch
from simulated_annealing import SimulatedAnnealing

if __name__ == '__main__':
  tsp_problem = TSPInstance(10)

  bfs = BreadthFirstSearch(tsp_problem)
  sa = SimulatedAnnealing(tsp_problem, 100, 0.99, 300)

  bfs_tour, bfs_dist = bfs.solve()
  sa_tour, sa_dist = sa.solve()

  print(bfs_tour)
  print(bfs_dist)

  print(sa_tour)
  print(sa_dist)