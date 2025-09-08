import os
from tsp_instance import TSPInstance
from uninformed_search import BreadthFirstSearch
from simulated_annealing import SimulatedAnnealing
from genetic_algorithm import GeneticAlgorithm

def choose_instance():
  print("Escolha a origem da instância TSP:")
  print("1) Aleatória")
  print("2) Carregar de XML")
  choice = input("Digite 1 ou 2: ").strip()

  if choice == '1':
    try:
      n = int(input("Número de cidades (padrão 10): ").strip() or "10")
    except ValueError:
      n = 10
    return TSPInstance(n)

  elif choice == '2':
    patterns_dir = os.path.join(os.path.dirname(__file__), 'TSPPatterns')
    files = []
    if os.path.isdir(patterns_dir):
      files = [f for f in os.listdir(patterns_dir) if f.lower().endswith('.xml')]

    if files:
      print("Arquivos XML disponíveis:")
      for idx, f in enumerate(files):
        print(f"{idx+1}) {f}")
      sel = input("Selecione o número do arquivo ou digite um caminho: ").strip()
      path = None
      if sel.isdigit():
        i = int(sel) - 1
        if 0 <= i < len(files):
          path = os.path.join(patterns_dir, files[i])
      if not path:
        path = sel or input("Digite o caminho para o arquivo XML: ").strip()
    else:
      path = input("Nenhum XML em TSPPatterns. Digite o caminho para o arquivo XML: ").strip()

    try:
      return TSPInstance(xml_path=path)
    except Exception as e:
      print(f"Erro ao carregar XML: {e}")
      print("Voltando para geração aleatória (10 cidades).")
      return TSPInstance(10)

  else:
    print("Escolha inválida, usando aleatório (10 cidades).")
    return TSPInstance(10)


if __name__ == '__main__':
  tsp_problem = choose_instance()

  print(f"Instância com {tsp_problem.num_cities} cidades criada.")

  # bfs = BreadthFirstSearch(tsp_problem)
  sa = SimulatedAnnealing(tsp_problem, 100, 0.99, 300)
  ga = GeneticAlgorithm(tsp_problem)

  # bfs_tour, bfs_dist = bfs.solve()
  sa_tour, sa_dist = sa.solve()
  ga_tour, ga_dist = ga.solve()

  #print("BFS result:") ## ta demorando demais pra num_cities > 10
  #print(bfs_tour)
  #print(bfs_dist)

  print("Simulated Annealing result:")
  print(sa_tour)
  print(sa_dist)

  print("Genetic Algorithm result:")
  print(ga_tour)
  print(ga_dist)