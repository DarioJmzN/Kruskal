#Pablo Darío Jiménez Nuño

import networkx as nx
import matplotlib.pyplot as plt
import heapq

# Función auxiliar para encontrar el conjunto al que pertenece un nodo
def find(parent, i):
    if parent[i] == i:  # Si el nodo es su propio padre, es la raíz del conjunto
        return i
    return find(parent, parent[i])  # Recursivamente encontrar la raíz del conjunto

# Función auxiliar para unir dos conjuntos utilizando Union-Find
def union(parent, rank, x, y):
    xroot = find(parent, x)  # Encontrar la raíz del conjunto de x
    yroot = find(parent, y)  # Encontrar la raíz del conjunto de y

    if rank[xroot] < rank[yroot]:  # Unir por rango: unir el árbol más pequeño debajo del más grande
        parent[xroot] = yroot
    elif rank[xroot] > rank[yroot]:
        parent[yroot] = xroot
    else:
        parent[yroot] = xroot
        rank[xroot] += 1

# Algoritmo de Kruskal para encontrar el MST y el Maximum Spanning Tree (MST máximo)
def kruskal_mst(graph):
    edges = []
    for u, v, weight in graph.edges(data='weight'):
        edges.append((weight, u, v))  # Recoger todas las aristas con sus pesos

    edges.sort()  # Ordenar las aristas por peso

    parent = {}  # Diccionario para mantener el padre de cada nodo
    rank = {}    # Diccionario para mantener el rango de cada nodo (utilizado en Union-Find)

    # Inicializar Union-Find: cada nodo es su propio padre y su rango es 0
    for node in graph.nodes():
        parent[node] = node
        rank[node] = 0

    mst_edges = []       # Lista para almacenar las aristas del MST
    mst_max_edges = []   # Lista para almacenar las aristas del MST máximo

    for weight, u, v in edges:
        if find(parent, u) != find(parent, v):  # Si u y v pertenecen a diferentes conjuntos
            union(parent, rank, u, v)           # Unir los conjuntos de u y v
            mst_edges.append((u, v))            # Agregar la arista al MST
            mst_max_edges.append((u, v))        # Agregar la misma arista al MST máximo

    return mst_edges, mst_max_edges  # Devolver las listas de aristas del MST y MST máximo

# Función para visualizar el grafo original y los árboles de expansión mínima y máxima
def visualize_graph(graph, mst_edges, mst_max_edges):
    pos = nx.spring_layout(graph)  # Calcular la disposición de los nodos para dibujar el grafo

    plt.figure(figsize=(12, 8))   # Tamaño de la figura

    # Dibujar el grafo original con etiquetas de nodos, color de nodo azul claro y tamaño 700
    nx.draw_networkx(graph, pos, with_labels=True, node_color='skyblue', node_size=700, font_size=12, font_color='black')
    
    # Dibujar aristas del MST en azul con un ancho de 2 y opacidad 0.7
    nx.draw_networkx_edges(graph, pos, edgelist=mst_edges, width=2.0, edge_color='blue', alpha=0.7)
    
    # Dibujar aristas del MST máximo en rojo con un ancho de 2 y opacidad 0.7
    nx.draw_networkx_edges(graph, pos, edgelist=mst_max_edges, width=2.0, edge_color='red', alpha=0.7)
    
    plt.title("Árbol de Expansión Mínima y Máxima de Kruskal")  # Título del gráfico
    plt.axis('off')  # Ocultar ejes
    plt.show()       # Mostrar el gráfico

# Ejemplo de uso
if __name__ == "__main__":
    # Crear un grafo de ejemplo (no dirigido y ponderado)
    graph = nx.Graph()
    graph.add_weighted_edges_from([
        ('casa', 'trabajo', 5), ('casa', 'escuela', 10), ('casa', 'parque', 20),
        ('trabajo', 'escuela', 5), ('trabajo', 'supermercado', 10),
        ('escuela', 'parque', 3), ('escuela', 'supermercado', 15),
        ('parque', 'supermercado', 5)
    ])

    # Obtener los árboles de expansión mínima y máxima utilizando Kruskal
    mst_edges, mst_max_edges = kruskal_mst(graph)

    # Visualizar el grafo original con los árboles de expansión mínima y máxima
    visualize_graph(graph, mst_edges, mst_max_edges)
