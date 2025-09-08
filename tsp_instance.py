import random
import math
import xml.etree.ElementTree as ET

class TSPInstance:
  def __init__(self, num_cities=None, xml_path=None):
    """
    Inicializa uma instância do problema do caixeiro viajante

    Args:
      num_cities (int): O número de cidades que serão geradas (se xml_path for None)
      xml_path (str): caminho para um arquivo XML no formato fornecido. Se presente, carrega a matriz de custos do XML.
    """
    self.num_cities = num_cities
    self.cities = []
    self.distance_matrix = []

    if xml_path:
      self.load_from_xml(xml_path)
    elif self.num_cities:
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
    
  def load_from_xml(self, xml_path):
    """
    Carrega uma instância TSP a partir de um arquivo XML no formato fornecido.
    O método preenche a matriz de distâncias diretamente a partir dos atributos 'cost' dos elementos <edge>.

    Args:
      xml_path (str): caminho para o arquivo XML
    """
    tree = ET.parse(xml_path)
    root = tree.getroot()

    graph = root.find('graph')
    if graph is None:
      raise ValueError('XML inválido: elemento <graph> não encontrado')

    vertices = graph.findall('vertex')
    n = len(vertices)
    if n == 0:
      raise ValueError('XML inválido: não foram encontradas cidades (vertex)')

    self.num_cities = n
    # não temos coordenadas no XML; manter lista vazia ou indices
    self.cities = [(None, None) for _ in range(n)]
    self.distance_matrix = [[0.0 for _ in range(n)] for _ in range(n)]

    for i, vertex in enumerate(vertices):
      edges = vertex.findall('edge')
      for edge in edges:
        # texto do edge representa o índice do vértice destino
        try:
          j = int(edge.text.strip())
        except Exception:
          continue

        # custo pode estar no atributo 'cost' ou no texto do elemento
        cost_attr = edge.attrib.get('cost')
        if cost_attr is not None:
          cost = float(cost_attr)
        else:
          # tentar interpretar o conteúdo adicional (fallback)
          try:
            cost = float(edge.text)
          except Exception:
            cost = 0.0

        self.distance_matrix[i][j] = cost

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
    Calcula a distância percorrida por um tour
    
    Args:
      tour (list): Um tour possível para a instância
    """
    if not tour:
      return 0.0

    total_distance = self.distance_matrix[tour[self.num_cities-1]][tour[0]]

    for i in range(self.num_cities-1):
      total_distance += self.distance_matrix[tour[i]][tour[i+1]]
    
    return total_distance

