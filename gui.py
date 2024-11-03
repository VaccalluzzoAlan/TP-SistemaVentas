try:
    import tkinter as tk
    from tkinter import messagebox, simpledialog, ttk
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

        self.boton_agregar_ruta = tk.Button(self.frame_izq, text="Establecer Ruta", command=self.agregar_ruta, bg="#3F407D", fg="white",font=("Arial", 12))
        self.boton_agregar_ruta.pack(pady=10, padx=10, fill="x")

        self.boton_realizar_orden = tk.Button(self.frame_izq, text="Realizar Orden", command=self.realizar_orden, bg="#3F407D", fg="white",font=("Arial", 12))
        self.boton_realizar_orden.pack(pady=10, padx=10, fill="x")

        self.boton_procesar_orden = tk.Button(self.frame_izq, text="Procesar Siguiente Orden", command=self.procesar_siguiente_orden, bg="#3F407D",fg="white", font=("Arial", 12))
        self.boton_procesar_orden.pack(pady=10, padx=10, fill="x")

        self.boton_mostrar_grafo = tk.Button(self.frame_izq, text="Mostrar Grafo", command=self.mostrar_grafo, bg="#3F407D", fg="white",font=("Arial", 12))
        self.boton_mostrar_grafo.pack(pady=10, padx=10, fill="x")

        self.boton_salir = tk.Button(self.frame_izq, text="Salir", command=self.root.quit, bg="#3F407D", fg="white",font=("Arial", 12))
        self.boton_salir.pack(pady=10, padx=10, fill="x")

        # Área para mostrar información
        self.frame_der = tk.Frame(self.root, bg="white")
        self.frame_der.pack(side="right", fill="both", expand=True)
        self.frame_der.pack_propagate(False)

        # self.texto_info = tk.Text(self.frame_der, bg="white", fg="black", font=("Arial", 12))
        # self.texto_info.pack(side="right", fill="both", expand=True, padx=30, pady=30)

        # Ventana de pestañas
        self.pestanias = ttk.Notebook(self.frame_der) 
  
        self.pesta_productos = ttk.Frame(self.pestanias)
        self.pesta_clientes = ttk.Frame(self.pestanias)
        self.pesta_distritos = ttk.Frame(self.pestanias)
        self.pesta_rutas = ttk.Frame(self.pestanias)
        self.pesta_ordenes = ttk.Frame(self.pestanias)
        
        self.pestanias.add(self.pesta_productos, text='Productos')
        self.pestanias.add(self.pesta_clientes, text='Clientes')
        self.pestanias.add(self.pesta_distritos, text='Distritos')
        self.pestanias.add(self.pesta_rutas, text='Rutas')
        self.pestanias.add(self.pesta_ordenes, text='Ordenes')
        self.pestanias.pack(expand=True, fill="both", padx=15, pady=15)

        # Pestaña de productos

        self.lista_productos = ttk.Treeview(self.pesta_productos, columns=("ID", "Nombre", "Precio"), show="headings")

        self.lista_productos.heading("ID", text="ID")
        self.lista_productos.column("ID", minwidth=0, width=75, stretch=False)
        self.lista_productos.heading("Nombre", text="Nombre")
        self.lista_productos.heading("Precio", text="Precio")
        self.lista_productos.column("Precio", minwidth=150, width=150, stretch=False)

        self.lista_productos.pack(side='left', fill="both", expand=True)

        self.list_prod_scrollbar = ttk.Scrollbar(self.pesta_productos, orient="vertical", command=self.lista_productos.yview)
        self.list_prod_scrollbar.pack(side='right', fill='y')
        self.lista_productos.configure(yscrollcommand=self.list_prod_scrollbar.set)

        # Pestaña de clientes

        self.lista_clientes = ttk.Treeview(self.pesta_clientes, columns=("ID", "DNI", "Nombre"), show="headings")
        self.lista_clientes.heading("ID", text="ID")
        self.lista_clientes.column("ID", minwidth=0, width=75, stretch=False)
        self.lista_clientes.heading("DNI", text="DNI")
        self.lista_clientes.heading("Nombre", text="Nombre")

        self.lista_clientes.pack(side='left', fill="both", expand=True)

        self.list_clie_scrollbar = ttk.Scrollbar(self.pesta_clientes, orient="vertical", command=self.lista_clientes.yview)
        self.list_clie_scrollbar.pack(side='right', fill='y')
        self.lista_clientes.configure(yscrollcommand=self.list_clie_scrollbar.set)

        # Pestaña de distritos

        self.lista_distritos = ttk.Treeview(self.pesta_distritos, columns=("ID", "Nombre"), show="headings")
        self.lista_distritos.heading("ID", text="ID")
        self.lista_distritos.column("ID", minwidth=0, width=75, stretch=False)
        self.lista_distritos.heading("Nombre", text="Nombre")

        self.lista_distritos.pack(side='left', fill="both", expand=True)

        self.list_dist_scrollbar = ttk.Scrollbar(self.pesta_distritos, orient="vertical", command=self.lista_distritos.yview)
        self.list_dist_scrollbar.pack(side='right', fill='y')
        self.lista_distritos.configure(yscrollcommand=self.list_dist_scrollbar.set)

        # Pestaña de rutas

        self.lista_rutas = ttk.Treeview(self.pesta_rutas, columns=("Origen", "Destino", "Distancia"), show="headings")
        self.lista_rutas.heading("Origen", text="Origen")
        self.lista_rutas.heading("Destino", text="Destino")
        self.lista_rutas.heading("Distancia", text="Distancia")
        self.lista_rutas.column("Distancia", minwidth=150, width=150, stretch=False)

        self.lista_rutas.pack(side='left', fill="both", expand=True)

        self.list_ruta_scrollbar = ttk.Scrollbar(self.pesta_rutas, orient="vertical", command=self.lista_rutas.yview)
        self.list_ruta_scrollbar.pack(side='right', fill='y')
        self.lista_rutas.configure(yscrollcommand=self.list_ruta_scrollbar.set)

        # Pestaña de ordenes

        self.lista_ordenes = ttk.Treeview(self.pesta_ordenes, columns=("Producto", "Cliente", "Distrito"), show="headings")
        self.lista_ordenes.heading("Producto", text="Producto")
        self.lista_ordenes.heading("Cliente", text="Cliente")
        self.lista_ordenes.heading("Distrito", text="Distrito")

        self.lista_ordenes.pack(side='left', fill="both", expand=True)

        self.list_orde_scrollbar = ttk.Scrollbar(self.pesta_ordenes, orient="vertical", command=self.lista_ordenes.yview)
        self.list_orde_scrollbar.pack(side='right', fill='y')
        self.lista_ordenes.configure(yscrollcommand=self.list_orde_scrollbar.set)

        # Mostrar filas de listas
        self.actualizar_listas()

    def actualizar_listas(self):
        self.lista_productos.delete(*self.lista_productos.get_children())
        self.lista_clientes.delete(*self.lista_clientes.get_children())
        self.lista_distritos.delete(*self.lista_distritos.get_children())
        self.lista_rutas.delete(*self.lista_rutas.get_children())
        self.lista_ordenes.delete(*self.lista_ordenes.get_children())

        for prod in self.sistema.productos.values():
            self.lista_productos.insert("", tk.END, values=(prod.id, prod.nombre, prod.precio))

        for clie in self.sistema.clientes.values():
            self.lista_clientes.insert("", tk.END, values=(clie.id, clie.dni, clie.nombre))

        for distr in self.sistema.grafo_distritos.vertices.values():
            self.lista_distritos.insert("", tk.END, values=(distr.id, distr.nombre))
            for conex, dista in distr.conexiones.items():
                self.lista_rutas.insert("", tk.END, values=(distr.nombre, conex, dista))

        for ord in self.sistema.ordenes.cola:
            ord: cmhmr.Orden
            self.lista_ordenes.insert("", tk.END, values=(ord.producto.nombre, ord.cliente.dni, ord.distrito.nombre))

    def agregar_producto(self):
        nombre = simpledialog.askstring("Agregar Producto", "Ingrese el nombre del producto:")
        if nombre == None: return
        precio = simpledialog.askinteger("Agregar Producto", "Ingrese el precio del producto:")
        if precio == None: return

        if self.sistema.agregar_producto(nombre, precio):
            messagebox.showinfo("Éxito", f"Producto '{nombre}' agregado con éxito.")
            self.actualizar_listas()
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
            self.actualizar_listas()
        else:
            messagebox.showwarning("Advertencia", "Cliente no pudo ser agregado.")

    def agregar_distrito(self):
        nombre = simpledialog.askstring("Agregar Distrito", "Ingrese el nombre del distrito:")
        if nombre == None: return

        if self.sistema.agregar_distrito(nombre):
            messagebox.showinfo("Éxito", f"Distrito '{nombre}' agregado con éxito.")
            self.actualizar_listas()
        else:
            messagebox.showwarning("Advertencia", "Distrito no pudo ser agregado.")

    def agregar_ruta(self):
        distritos = [d.nombre for d in self.sistema.grafo_distritos.vertices.values()]

        origen = simpledialog.askstring("Agregar Ruta", "Ingrese el nombre de un distrito:")
        if origen == None: return
        elif origen not in distritos:
            messagebox.showwarning("Advertencia", "No se pudo encontrar ese distrito.")
            return
        destino = simpledialog.askstring("Agregar Ruta", "Ingrese el nombre de otro distrito:")
        if destino == None: return
        elif destino not in distritos:
            messagebox.showwarning("Advertencia", "No se pudo encontrar ese distrito.")
            return
        distancia = simpledialog.askfloat("Agregar Ruta", "Ingrese la distancia entre los distritos:", minvalue=0.001)
        if distancia == None: return

        if self.sistema.agregar_ruta(origen, destino, distancia):
            messagebox.showinfo("Éxito", f"Ruta entre '{origen}' y '{destino}' agregado con éxito.")
            self.actualizar_listas()
        else:
            messagebox.showwarning("Advertencia", "Ruta no pudo ser agregada.")

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
            self.actualizar_listas()
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
            self.actualizar_listas()
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
        pos = nx.spring_layout(G)
        plt.figure(figsize=(10, 6))

        if destino and inicio:    # Si se especifico un inicio y destino, se enfatiza la ruta y el resto se ve menos.
            nodos_camino = self.sistema.ruta_mas_corta(destino=destino, inicio=inicio, solo_camino=True)
            if not nodos_camino: 
                messagebox.showwarning("Advertencia", "No existe ruta entre los dos distritos.")
                return
            aristas_camino = []
            aristas_buscar = [(a[0], a[1]) for a in aristas]
            for index, nodo in enumerate(nodos_camino):
                if index + 1 < len(nodos_camino):
                    nodo_siguiente = nodos_camino[index + 1]
                    arista_camino = (nodo, nodo_siguiente)
                    if arista_camino not in aristas_buscar: arista_camino = (nodo_siguiente, nodo)
                    aristas_camino.append(arista_camino)
                    
            # print(aristas_camino)
            # nodos_camino = {nodo for arista in aristas_camino for nodo in arista}    # Todo nodo en la ruta tomada
            nodos_otros = [distr for distr in distritos if distr not in nodos_camino]    # Todo nodo fuera de la ruta
            # print({n:n for n in nodos_camino}, {n:n for n in nodos_otros})

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
            nx.draw_networkx(G, pos, with_labels=True, node_color='lightblue', node_size=2000, font_size=12, font_color='black')
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
