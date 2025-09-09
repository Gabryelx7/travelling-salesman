import os
import statistics
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
    return lambda: TSPInstance(n), f"aleatória ({n} cidades)"

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

    def make_from_xml():
      return TSPInstance(xml_path=path)

    return make_from_xml, f"XML: {path}"

  else:
    print("Escolha inválida, usando aleatório (10 cidades).")
    return lambda: TSPInstance(10), "aleatória (10 cidades)"


if __name__ == '__main__':
  make_instance, desc = choose_instance()

  try:
    runs = int(input("Quantas execuções deseja rodar (padrão 1): ").strip() or "1")
  except ValueError:
    runs = 1

  # parâmetros padrão dos algoritmos
  sa_params = { 'initial_temp': 100, 'cooling_rate': 0.99, 'iterations': 300 }

  # coletores de estatísticas
  stats = {
    #'BFS': [],
    'SA': [],
    'GA': []
  }

  for run in range(1, runs+1):
    print(f"\nRun {run}/{runs} - instância: {desc}")
    tsp_problem = make_instance()

    #bfs = BreadthFirstSearch(tsp_problem)
    sa = SimulatedAnnealing(tsp_problem, sa_params['initial_temp'], sa_params['cooling_rate'], sa_params['iterations'])
    ga = GeneticAlgorithm(tsp_problem)

    #bfs_tour, bfs_dist = bfs.solve()
    sa_tour, sa_dist = sa.solve()
    ga_tour, ga_dist = ga.solve()

    #print("BFS distance:", bfs_dist)
    print("Simulated Annealing distance:", sa_dist)
    print("Genetic Algorithm distance:", ga_dist)

    #stats['BFS'].append(bfs_dist)
    stats['SA'].append(sa_dist)
    stats['GA'].append(ga_dist)

  # imprimir estatísticas
  def print_stats(name, values):
    if not values:
      return
    mean = statistics.mean(values)
    minimum = min(values)
    maximum = max(values)
    print(f"\n{name} — runs={len(values)}: media={mean:.4f}, min={minimum:.4f}, max={maximum:.4f}")

  #print_stats('BFS', stats['BFS'])
  print_stats('Simulated Annealing', stats['SA'])
  print_stats('Genetic Algorithm', stats['GA'])