try:
    import tkinter as tk
    from tkinter import messagebox, simpledialog
    import networkx as nx
    import matplotlib.pyplot as plt
    import cmhmr  # Asegúrate de que tu módulo está en el mismo directorio o en PYTHONPATH
except ModuleNotFoundError as e:
    raise

class GUI:
    def __init__(self, root : tk.Tk):
        self.root = root
        self.root.title("Sistema de Ventas")
        self.root.geometry("960x560")
        self.root.config(bg="#E3F2FD")

        self.sistema = cmhmr.SistemaVentas()

        # Frame izquierdo (logo y botones)
        self.frame_izq = tk.Frame(self.root, width=300, height=560, bg="#3C5BBA")
        self.frame_izq.pack(side="left", fill="y")
        self.frame_izq.pack_propagate(False)

        # Título
        self.titulo = tk.Label(self.frame_izq, text="Sistema de Ventas", bg="#3C5BBA", fg="white", font=("Arial", 16))
        self.titulo.pack(pady=20)

        # Botones
        self.boton_agregar_producto = tk.Button(self.frame_izq, text="Agregar Producto", command=self.agregar_producto, bg="#3F407D",fg="white", font=("Arial", 12))
        self.boton_agregar_producto.pack(pady=10, padx=10, fill="x")

        self.boton_agregar_cliente = tk.Button(self.frame_izq, text="Agregar Cliente", command=self.agregar_cliente, bg="#3F407D",fg="white", font=("Arial", 12))
        self.boton_agregar_cliente.pack(pady=10, padx=10, fill="x")

        self.boton_agregar_distrito = tk.Button(self.frame_izq, text="Agregar Distrito", command=self.agregar_distrito, bg="#3F407D", fg="white",font=("Arial", 12))
        self.boton_agregar_distrito.pack(pady=10, padx=10, fill="x")

        self.boton_realizar_orden = tk.Button(self.frame_izq, text="Realizar Orden", command=self.realizar_orden, bg="#3F407D", fg="white",font=("Arial", 12))
        self.boton_realizar_orden.pack(pady=10, padx=10, fill="x")

        self.boton_procesar_orden = tk.Button(self.frame_izq, text="Procesar Siguiente Orden", command=self.procesar_siguiente_orden, bg="#3F407D",fg="white", font=("Arial", 12))
        self.boton_procesar_orden.pack(pady=10, padx=10, fill="x")

        self.boton_mostrar_grafo = tk.Button(self.frame_izq, text="Mostrar Grafo", command=self.mostrar_grafo, bg="#3F407D", fg="white",font=("Arial", 12))
        self.boton_mostrar_grafo.pack(pady=10, padx=10, fill="x")

        self.boton_salir = tk.Button(self.frame_izq, text="Salir", command=self.root.quit, bg="#3F407D", fg="white",font=("Arial", 12))
        self.boton_salir.pack(pady=10, padx=10, fill="x")

        # Área para mostrar información
        self.texto_info = tk.Text(self.root, bg="white", fg="black", font=("Arial", 12))
        self.texto_info.pack(side="right", fill="both", expand=True)

    def agregar_producto(self):
        nombre = simpledialog.askstring("Agregar Producto", "Ingrese el nombre del producto:")
        if nombre == None: return
        precio = simpledialog.askinteger("Agregar Producto", "Ingrese el precio del producto:")
        if precio == None: return

        if self.sistema.agregar_producto(nombre, precio):
            messagebox.showinfo("Éxito", f"Producto '{nombre}' agregado con éxito.")
        else:
            messagebox.showwarning("Advertencia", "Producto no pudo ser agregado.")

    def agregar_cliente(self, dni_input : str = None):
        if dni_input: dni = dni_input
        else:
            dni = simpledialog.askstring("Agregar Cliente", "Ingrese el DNI del cliente:")
            if dni == None: return
        nombre = simpledialog.askstring("Agregar Cliente", "Ingrese el nombre del cliente:")
        if nombre == None: return

        if self.sistema.agregar_cliente(dni, nombre):
            messagebox.showinfo("Éxito", f"Cliente '{nombre}' agregado con éxito.")
        else:
            messagebox.showwarning("Advertencia", "Cliente no pudo ser agregado.")

    def agregar_distrito(self):
        nombre = simpledialog.askstring("Agregar Distrito", "Ingrese el nombre del distrito:")
        if nombre == None: return

        if self.sistema.agregar_distrito(nombre):
            messagebox.showinfo("Éxito", f"Distrito '{nombre}' agregado con éxito.")
        else:
            messagebox.showwarning("Advertencia", "Distrito no pudo ser agregado.")

    def realizar_orden(self):
        lista_dni = [c.dni for c in self.sistema.clientes.values()]
        lista_prod = [p.nombre for p in self.sistema.productos.values()]
        lista_distr = [d.nombre for d in self.sistema.grafo_distritos.vertices.values()]

        dni_cliente = simpledialog.askstring("Realizar Orden", "Ingrese el DNI del cliente:")
        if dni_cliente == None: return
        elif dni_cliente not in lista_dni:
            if messagebox.askyesno("Advertencia", "No se pudo encontrar ese cliente. ¿Crear uno con este DNI?"):
                self.agregar_cliente(dni_cliente)
            else:
                return
        nombre_producto = simpledialog.askstring("Realizar Orden", "Ingrese el nombre del producto:")
        if nombre_producto == None: return
        elif nombre_producto not in lista_prod:
            messagebox.showwarning("Advertencia", "No se pudo encontrar ese producto.")
            return
        nombre_distrito = simpledialog.askstring("Realizar Orden", "Ingrese el nombre del distrito:")
        if nombre_distrito == None: return
        elif nombre_distrito not in lista_distr:
            messagebox.showwarning("Advertencia", "No se pudo encontrar ese distrito.")
            return

        if not self.sistema.ruta_mas_corta(nombre_distrito):
            messagebox.showwarning("Advertencia", "No existe ruta hacia este distrito.")
            return
        if self.sistema.realizar_orden(dni_cliente, nombre_producto, nombre_distrito):
            messagebox.showinfo("Éxito", "Orden realizada con éxito.")
            self.mostrar_grafo(nombre_distrito, self.sistema.local)
        else:
            messagebox.showwarning("Advertencia", "Orden no pudo ser agregada.")

    def procesar_siguiente_orden(self):
        orden_procesada = self.sistema.procesar_orden()
        if orden_procesada:
            mensaje = (f"Orden procesada:\n"
                       f"Producto: {orden_procesada.producto.nombre}\n"
                       f"Cliente: {orden_procesada.cliente.nombre}\n"
                       f"Distrito: {orden_procesada.distrito.nombre}")
            messagebox.showinfo("Orden Procesada", mensaje)
        else:
            messagebox.showinfo("Sin Órdenes", "No hay órdenes para procesar.")

    def mostrar_grafo(self, destino : str = None, inicio : str = None):
        distritos = [distr.nombre for distr in self.sistema.grafo_distritos.vertices.values()]

        if not (destino and inicio):
            if messagebox.askyesno("Mostrar Grafo", "¿Mostrar ruta especifica?"):
                if not inicio:
                    inicio = simpledialog.askstring("Mostrar Grafo", f"Ingrese el nombre del distrito donde comienza la ruta (el local es {self.sistema.local}):")
                    if inicio == None: return
                    elif inicio not in distritos:
                        messagebox.showwarning("Advertencia", "No se pudo encontrar ese distrito.")
                        return
                if not destino:
                    destino = simpledialog.askstring("Mostrar Grafo", "Ingrese el nombre del distrito donde termina la ruta:")
                    if destino == None: return
                    elif destino not in distritos:
                        messagebox.showwarning("Advertencia", "No se pudo encontrar ese distrito.")
                        return

        if inicio and destino:
            if inicio == destino:
                messagebox.showwarning("Advertencia", "Una ruta no puede comenzar y terminar en el mismo distrito.")
                return

        G = nx.Graph()
        G.add_nodes_from(distritos)

        aristas = []
        for distrNombre in distritos:
            distr: cmhmr.Distrito = self.sistema.grafo_distritos.get(distrNombre)
            for conex, dist in distr.conexiones.items():
                arista = (distrNombre, conex, dist)
                aristaReves = (conex, distrNombre, dist)
                if arista not in aristas and aristaReves not in aristas:
                    aristas.append(arista)

        G.add_weighted_edges_from(aristas)
        plt.figure(figsize=(10, 6))
        pos = nx.spring_layout(G)

        if destino and inicio:    # Si se especifico un inicio y destino, se enfatiza la ruta y el resto se ve menos.
            aristas_camino = self.sistema.ruta_mas_corta(destino=destino, inicio=inicio, solo_camino=True)
            if not aristas_camino: 
                messagebox.showwarning("Advertencia", "No existe ruta entre los dos distritos.")
                return
            nodos_camino = {nodo for arista in aristas_camino for nodo in arista}    # Todo nodo en la ruta tomada
            nodos_otros = {distr for distr in distritos if distr not in nodos_camino}    # Todo nodo fuera de la ruta

            # Mostrar el grafo
            nx.draw_networkx(G, pos, with_labels=False, node_color='grey', edge_color='grey', style='dashed') # Grafo general

            nx.draw_networkx_labels(G, pos, labels={n:n for n in nodos_otros}, font_size=10) # Nombre de nodos fuera del camino
            nx.draw_networkx_labels(G, pos, labels={n:n for n in nodos_camino}, font_weight='bold') # Nombre de nodos en el camino

            nx.draw_networkx_nodes(G, pos, nodelist=nodos_camino, node_size=750, node_color='orange') # Nodos en el camino
            nx.draw_networkx_nodes(G, pos, nodelist=[inicio], node_size=1200, node_color='red') # Nodo origen
            nx.draw_networkx_nodes(G, pos, nodelist=[destino], node_size=1200, node_color='green') # Nodo destino

            nx.draw_networkx_edges(G, pos, edgelist=aristas_camino, width=3, edge_color='blue') # Rutas tomadas

            edge_labels = nx.get_edge_attributes(G, "weight")
            edge_labels_camino = {e:d for e, d in edge_labels.items() if e in aristas_camino}
            edge_labels_fuera = {e:d for e, d in edge_labels.items() if e not in aristas_camino}
            nx.draw_networkx_edge_labels(G, pos, edge_labels_fuera) # Distancias entre nodos fuera del camino
            nx.draw_networkx_edge_labels(G, pos, edge_labels_camino, font_weight='bold') # Distancias entre nodos en el camino
        else:
            # Mostrar el grafo
            nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=2000, font_size=12, font_color='black')
            edge_labels = nx.get_edge_attributes(G, 'weight')
            nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
        plt.title("Grafo de Distritos y Conexiones")
        plt.show()

def main():
    root = tk.Tk()
    app = GUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
