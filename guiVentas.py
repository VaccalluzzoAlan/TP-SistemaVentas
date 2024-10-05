try:
    import tkinter as tk
    from tkinter import messagebox, ttk
    import networkx as nx
    import matplotlib.pyplot as plt
    import cmhmr
except ModuleNotFoundError as e:
    raise

class GUI:
    def __init__(self):
        pass

def test():
    sistema = cmhmr.testSistemaVentas()
    distritos = [distr.nombre for distr in sistema.grafo_distritos.vertices.values()]
    print([f"{nombre}: {distr.conexiones}" for nombre, distr in sistema.grafo_distritos.vertices.items()])
    
    print("--------------------------")

    G = nx.Graph()
    G.add_nodes_from(distritos)
    
    aristas = []
    for distrNombre in distritos:
        distr : cmhmr.Distrito = sistema.grafo_distritos.get(distrNombre)
        for conex, dist in distr.conexiones.items():
            arista = (distrNombre, conex, dist)
            aristaReves = (conex, distrNombre, dist)
            if arista not in aristas and aristaReves not in aristas:
                aristas.append(arista)

    G.add_weighted_edges_from(aristas)
    aristas_camino = sistema.ruta_mas_corta(destino='Palermo', solo_camino=True)
    nodos_camino = {x for l in aristas_camino for x in l}
    nodos_otros = {x for x in distritos if x not in nodos_camino}
    print(nodos_camino)
    print(nodos_otros)
    
    pos = nx.spring_layout(G)
    nx.draw_networkx(G, pos, with_labels=False, node_color='grey', edge_color='grey', style='dashed')
    nx.draw_networkx_labels(G, pos, labels={n:n for n in nodos_otros}, font_size=10)
    nx.draw_networkx_labels(G, pos, labels={n:n for n in nodos_camino}, font_weight='bold')
    nx.draw_networkx_nodes(G, pos, nodelist=nodos_camino, node_size=450, node_color='orange')
    nx.draw_networkx_nodes(G, pos, nodelist=[sistema.local], node_size=600, node_color='red')
    nx.draw_networkx_nodes(G, pos, nodelist=['Palermo'], node_size=600, node_color='green')
    nx.draw_networkx_edges(G, pos, edgelist=aristas_camino, width=3, edge_color='blue')
    edge_labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels)
    plt.show()

def main():
    test()

if __name__ == "__main__":
    main()