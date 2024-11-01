import customtkinter as ctk
import cmhmr  # Asegúrate de que tu módulo está en el mismo directorio o en PYTHONPATH
import networkx as nx
import matplotlib.pyplot as plt
from tkinter import messagebox


class GUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configuración de la apariencia
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.title("Sistema de Ventas")
        self.geometry("960x560")

        self.sistema = cmhmr.SistemaVentas()  # Instancia de tu sistema de ventas

        # Frame izquierdo (logo y botones)
        self.frame_izq = ctk.CTkFrame(self)
        self.frame_izq.pack(side="left", fill="y")
        self.frame_izq.pack_propagate(False)

        # Título
        self.titulo = ctk.CTkLabel(self.frame_izq, text="Sistema de Ventas", font=("Arial", 16))
        self.titulo.pack(pady=20)

        # Botones
        self.boton_agregar_producto = ctk.CTkButton(self.frame_izq, text="Agregar Producto", command=self.agregar_producto)
        self.boton_agregar_producto.pack(pady=10, padx=10, fill="x")

        self.boton_agregar_cliente = ctk.CTkButton(self.frame_izq, text="Agregar Cliente", command=self.agregar_cliente)
        self.boton_agregar_cliente.pack(pady=10, padx=10, fill="x")

        self.boton_agregar_distrito = ctk.CTkButton(self.frame_izq, text="Agregar Distrito", command=self.agregar_distrito)
        self.boton_agregar_distrito.pack(pady=10, padx=10, fill="x")

        self.boton_agregar_ruta = ctk.CTkButton(self.frame_izq, text="Agregar Ruta", command=self.agregar_ruta)
        self.boton_agregar_ruta.pack(pady=10, padx=10, fill="x")

        self.boton_realizar_orden = ctk.CTkButton(self.frame_izq, text="Realizar Orden", command=self.realizar_orden)
        self.boton_realizar_orden.pack(pady=10, padx=10, fill="x")

        self.boton_procesar_orden = ctk.CTkButton(self.frame_izq, text="Procesar Siguiente Orden", command=self.procesar_siguiente_orden)
        self.boton_procesar_orden.pack(pady=10, padx=10, fill="x")

        self.boton_mostrar_grafo = ctk.CTkButton(self.frame_izq, text="Mostrar Grafo", command=self.seleccionar_grafo)  # TODO: Probar
        self.boton_mostrar_grafo.pack(pady=10, padx=10, fill="x")

        self.boton_mostrar_listas = ctk.CTkButton(self.frame_izq, text="Mostrar Listados", command=self.mostrar_listados)
        self.boton_mostrar_listas.pack(pady=10, padx=10, fill="x")

        self.boton_salir = ctk.CTkButton(self.frame_izq, text="Salir", command=self.quit)
        self.boton_salir.pack(pady=10, padx=10, fill="x")

        # Frame derecho dinámico para mostrar diferentes interfaces
        self.frame_derecho = ctk.CTkFrame(self, width=400, height=560, fg_color="#111", corner_radius=None)
        self.frame_derecho.pack(side="right", fill="both", expand=True)

    def limpiar_frame_derecho(self):
        for widget in self.frame_derecho.winfo_children():
            widget.destroy()

   
    
    def agregar_producto(self):
        self.limpiar_frame_derecho()
        ctk.CTkLabel(self.frame_derecho, text="Agregar Producto", font=("Arial", 16)).pack(pady=10)
        # Campos de entrada para nombre y precio
        nombre_entry = ctk.CTkEntry(self.frame_derecho, placeholder_text="Nombre del producto")
        nombre_entry.pack(pady=5)
        precio_entry = ctk.CTkEntry(self.frame_derecho, placeholder_text="Precio del producto")
        precio_entry.pack(pady=5)
        mensaje = ctk.CTkLabel(self.frame_derecho, text="")
        mensaje.pack(pady=5)
        # Botón de guardar con lógica de validación directamente dentro del comando
        ctk.CTkButton(
            self.frame_derecho, 
            text="Guardar", 
            command=lambda: (
                # Obtención de los valores de entrada
                (nombre := nombre_entry.get()),
                (precio := precio_entry.get()),
                # Validación de que los campos no estén vacíos
                (mensaje.configure(text="Complete todos los campos.") if not nombre or not precio else None),
                # (ctk.CTkMessageBox.show_warning("Advertencia", "Complete todos los campos.") if not nombre or not precio else None),
                # Conversión de precio y validación adicional
                (
                    None if not nombre or not precio else
                    (mensaje.configure(text="Por favor, ingrese un precio válido.") if not precio.isdigit() else 
                    # (ctk.CTkMessageBox.show_warning("Advertencia", "Por favor, ingrese un precio válido.") if not precio.isdigit() else 
                    # Si el precio es válido, intenta agregar el producto al sistema
                    (mensaje.configure(text=f"Producto '{nombre}' agregado con éxito.") if self.sistema.agregar_producto(nombre, int(precio)) else
                    mensaje.configure(text="El producto no pudo ser agregado."))
                ))
            )
        ).pack(pady=10)


    def agregar_cliente(self):
        self.limpiar_frame_derecho()
        ctk.CTkLabel(self.frame_derecho, text="Agregar Cliente", font=("Arial", 16)).pack(pady=10)

        # Campos de entrada para DNI y nombre
        dni_entry = ctk.CTkEntry(self.frame_derecho, placeholder_text="DNI del cliente")
        dni_entry.pack(pady=5)
        nombre_entry = ctk.CTkEntry(self.frame_derecho, placeholder_text="Nombre del cliente")
        nombre_entry.pack(pady=5)
        mensaje = ctk.CTkLabel(self.frame_derecho, text="")
        mensaje.pack(pady=5)

        # Lógica para el botón Guardar
        ctk.CTkButton(
            self.frame_derecho, 
            text="Guardar", 
            command=lambda: (
                # Obtención de los valores de entrada
                (dni := dni_entry.get()),
                (nombre := nombre_entry.get()),
                # Verificación de que ambos campos no estén vacíos
                (mensaje.configure(text="Complete todos los campos.") if not dni or not nombre else 
                # Intento de agregar el cliente
                (mensaje.configure(text=f"Cliente '{nombre}' agregado con éxito.") if self.sistema.agregar_cliente(dni, nombre) else 
                mensaje.configure(text="Cliente no pudo ser agregado."))
                )
            )
        ).pack(pady=10)



    def agregar_distrito(self):
        self.limpiar_frame_derecho()
        ctk.CTkLabel(self.frame_derecho, text="Agregar Distrito", font=("Arial", 16)).pack(pady=10)
        
        # Campo de entrada para el nombre del distrito
        nombre_entry = ctk.CTkEntry(self.frame_derecho, placeholder_text="Nombre del distrito")
        nombre_entry.pack(pady=5)
        mensaje = ctk.CTkLabel(self.frame_derecho, text="")
        mensaje.pack(pady=5)
        
        # Lógica para el botón Guardar
        ctk.CTkButton(
            self.frame_derecho, 
            text="Guardar", 
            command=lambda: (
                # Obtención del valor de entrada
                (nombre := nombre_entry.get()),
                # Verificación de que el campo no esté vacío
                (mensaje.configure(text="Por favor, ingrese un nombre válido.") if not nombre else 
                # Intento de agregar el distrito
                mensaje.configure(text=f"Distrito '{nombre}' agregado con éxito.") if self.sistema.agregar_distrito(nombre) else 
                mensaje.configure(text="Distrito no pudo ser agregado.")
                )
            )
        ).pack(pady=10)



    def agregar_ruta(self):    # TODO: Verificar existencia de distritos
        distritos = [d.nombre for d in self.sistema.grafo_distritos.vertices.values()]

        self.limpiar_frame_derecho()
        ctk.CTkLabel(self.frame_derecho, text="Agregar Ruta", font=("Arial", 16)).pack(pady=10)

        # Campos de entrada para origen, destino y distancia
        origen_entry = ctk.CTkEntry(self.frame_derecho, placeholder_text="Distrito de origen")
        origen_entry.pack(pady=5)
        destino_entry = ctk.CTkEntry(self.frame_derecho, placeholder_text="Distrito de destino")
        destino_entry.pack(pady=5)
        distancia_entry = ctk.CTkEntry(self.frame_derecho, placeholder_text="Distancia entre distritos")
        distancia_entry.pack(pady=5)
        mensaje = ctk.CTkLabel(self.frame_derecho, text="")
        mensaje.pack(pady=5)

        # Lógica para el botón Guardar
        ctk.CTkButton(
            self.frame_derecho, 
            text="Guardar", 
            command=lambda: (
                # Obtención de los valores de entrada
                (origen := origen_entry.get()),
                (destino := destino_entry.get()),
                (distancia := distancia_entry.get()),
                # Verificación de que los campos no estén vacíos
                (mensaje.configure(text="Complete todos los campos.") if not origen or not destino or not distancia else 
                # Verificar que existan los distritos
                (mensaje.configure(text="Por favor, ingrese solo distritos registrados.") if (origen not in distritos) or (destino not in distritos) else
                # Verificar que no sean iguales los campos
                (mensaje.configure(text="Los distritos no pueden ser iguales.") if origen == destino else
                # Intento de convertir la distancia a float
                (mensaje.configure(text="Por favor, ingrese una distancia válida.") if not distancia.replace('.', '', 1).isdigit() else 
                # Verificar si se puede agregar la ruta
                    (mensaje.configure(text=f"Ruta entre '{origen}' y '{destino}' agregada con éxito.") if self.sistema.agregar_ruta(origen, destino, float(distancia)) else 
                    mensaje.configure(text="Ruta no pudo ser agregada."))
                    )
                )
                )
                )
            )
        ).pack(pady=10)


    def realizar_orden(self):
        self.limpiar_frame_derecho()
        ctk.CTkLabel(self.frame_derecho, text="Realizar Orden", font=("Arial", 16)).pack(pady=10)

        # Entradas para DNI del cliente, nombre del producto y nombre del distrito
        dni_cliente_entry = ctk.CTkEntry(self.frame_derecho, placeholder_text="DNI del cliente")
        dni_cliente_entry.pack(pady=5)
        
        nombre_producto_entry = ctk.CTkEntry(self.frame_derecho, placeholder_text="Nombre del producto")
        nombre_producto_entry.pack(pady=5)
        
        nombre_distrito_entry = ctk.CTkEntry(self.frame_derecho, placeholder_text="Nombre del distrito")
        nombre_distrito_entry.pack(pady=5)
        
        mensaje = ctk.CTkLabel(self.frame_derecho, text="")
        mensaje.pack(pady=5)

        # Botón para realizar la orden
        ctk.CTkButton(
            self.frame_derecho, 
            text="Guardar", 
            command=lambda: (
                # Obtención de los valores de entrada
                (dni_cliente := dni_cliente_entry.get()),
                (nombre_producto := nombre_producto_entry.get()),
                (nombre_distrito := nombre_distrito_entry.get()),
                # Verificación de que los campos no estén vacíos
                (mensaje.configure(text="Complete todos los campos.") if not dni_cliente or not nombre_producto or not nombre_distrito else 
                # Intento de realizar la orden
                (
                    mensaje.configure(text="Orden realizada con éxito.") if self.sistema.realizar_orden(dni_cliente, nombre_producto, nombre_distrito) else 
                    mensaje.configure(text="Orden no pudo ser agregada.")
                )
                )
            )
        ).pack(pady=10)


    def procesar_siguiente_orden(self):
        self.limpiar_frame_derecho()
        ctk.CTkLabel(self.frame_derecho, text="Procesar Siguiente Orden", font=("Arial", 16)).pack(pady=10)
        
        mensaje_label = ctk.CTkLabel(self.frame_derecho, text="")
        mensaje_label.pack(pady=5)

        # Procesar orden
        orden_procesada = self.sistema.procesar_orden()

        if orden_procesada:
            mensaje = (f"Orden procesada:\n"
                    f"Producto: {orden_procesada.producto.nombre}\n"
                    f"Cliente: {orden_procesada.cliente.nombre}\n"
                    f"Distrito: {orden_procesada.distrito.nombre}")
            mensaje_label.configure(text=mensaje)

            grafo_mensaje = ctk.CTkLabel(self.frame_derecho, text="")
            grafo_mensaje.pack(pady=5)
            ctk.CTkButton(self.frame_derecho, 
                          text="Mostrar grafo de ruta", 
                          command=lambda: (self.mostrar_grafo(destino=orden_procesada.distrito.nombre, 
                                                              label_mensaje=grafo_mensaje)
                                          )
                         ).pack()
        else:
            mensaje_label.configure(text="No hay órdenes para procesar.")

    def seleccionar_grafo(self):
        self.limpiar_frame_derecho()
        ctk.CTkLabel(self.frame_derecho, text="Grafo de Distritos", font=("Arial", 16)).pack(pady=10)

        # Lógica para mostrar el grafo
        distritos = [distr.nombre for distr in self.sistema.grafo_distritos.vertices.values()]

        check_ruta = ctk.CTkCheckBox(self.frame_derecho, text="Mostrar ruta especifica")
        check_ruta.pack(pady=5)
        origen_entry = ctk.CTkEntry(self.frame_derecho, placeholder_text="Distrito de origen")
        origen_entry.pack(pady=5)
        destino_entry = ctk.CTkEntry(self.frame_derecho, placeholder_text="Distrito de destino")
        destino_entry.pack(pady=5)
        mensaje = ctk.CTkLabel(self.frame_derecho, text="")
        mensaje.pack(pady=5)

        ctk.CTkButton(
            self.frame_derecho, 
            text="Mostrar", 
            command=lambda: (
                # Obtención de los valores de entrada
                (buscar_ruta := check_ruta.get()),
                (self.mostrar_grafo(label_mensaje=mensaje) if not buscar_ruta else 
                (
                    (inicio := origen_entry.get()),
                    (destino := destino_entry.get()),
                    # Verificación de que los campos no estén vacíos
                    (mensaje.configure(text="Complete todos los campos.") if not inicio or not destino else 
                    # Verificar que existan los distritos
                    (mensaje.configure(text="Por favor, ingrese solo distritos registrados.") if (inicio not in distritos) or (destino not in distritos) else
                    # Verificar que no sean iguales los campos
                    (mensaje.configure(text="Los distritos no pueden ser iguales.") if inicio == destino else
                    # Verificar si se puede agregar la ruta
                        self.mostrar_grafo(destino, inicio, label_mensaje=mensaje))
                    )
                    )
                )
                )
            )
        ).pack(pady=10)


    def mostrar_grafo(self, destino : str = None, inicio : str = None, label_mensaje : ctk.CTkLabel = None):
        # Lógica para mostrar el grafo
        distritos = [distr.nombre for distr in self.sistema.grafo_distritos.vertices.values()]

        if inicio and destino and (inicio == destino):
            if label_mensaje: label_mensaje.configure(text="Los distritos no pueden ser iguales.")
            return
        
        if destino and not inicio:
            inicio = self.sistema.local

        G = nx.Graph()
        G.add_nodes_from(distritos)

        aristas = []
        for distrNombre in distritos:
            distr = self.sistema.grafo_distritos.get(distrNombre)
            for conex, dist in distr.conexiones.items():
                arista = (distrNombre, conex, dist)
                aristaReves = (conex, distrNombre, dist)
                if arista not in aristas and aristaReves not in aristas:
                    aristas.append(arista)

        G.add_weighted_edges_from(aristas)
        pos = nx.spring_layout(G)
        plt.figure(figsize=(10, 6))  # Ajustar el tamaño de la figura

        # Mostrar el grafo
        if destino and inicio:    # Si se especifico un inicio y destino, se enfatiza la ruta y el resto se ve menos.
            nodos_camino = self.sistema.ruta_mas_corta(destino=destino, inicio=inicio, solo_camino=True)
            if not nodos_camino:
                if label_mensaje: label_mensaje.configure(text="No existe ruta entre los dos distritos.")
                return
            if label_mensaje: label_mensaje.configure(text=f"Mostrando grafo de ruta entre '{inicio}' y '{destino}'...")
            aristas_camino = []
            aristas_buscar = [(a[0], a[1]) for a in aristas]
            for index, nodo in enumerate(nodos_camino):
                if index + 1 < len(nodos_camino):
                    nodo_siguiente = nodos_camino[index + 1]
                    arista_camino = (nodo, nodo_siguiente)
                    if arista_camino not in aristas_buscar: arista_camino = (nodo_siguiente, nodo)
                    aristas_camino.append(arista_camino)
                    
            # print(aristas_camino)
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
            if label_mensaje: label_mensaje.configure(text=f"Mostrando grafo general...")
            # Mostrar el grafo simple
            nx.draw_networkx(G, pos, with_labels=True, node_color='lightblue', node_size=2000, font_size=12, font_color='black')
            edge_labels = nx.get_edge_attributes(G, 'weight')
            nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
        plt.title("Grafo de Distritos y Conexiones")
        # Mostar en una ventana diferente
        plt.show()

    def mostrar_listados(self):
        self.limpiar_frame_derecho()
        ctk.CTkLabel(self.frame_derecho, text="Listados", font=("Arial", 16)).pack(pady=10)


if __name__ == "__main__":
    app = GUI()
    app.mainloop()
