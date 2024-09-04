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
    
    print(G.edges(data=True))

def main():
    test()

if __name__ == "__main__":
    main()