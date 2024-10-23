import customtkinter as ctk
import cmhmr  # Asegúrate de que tu módulo está en el mismo directorio o en PYTHONPATH
import networkx as nx
import matplotlib.pyplot as plt

class GUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configuración de la apariencia
        ctk.set_appearance_mode("dark")  # Modo oscuro
        ctk.set_default_color_theme("blue")  # Tema azul

        self.title("Sistema de Ventas")
        self.geometry("960x560")

        self.sistema = cmhmr.SistemaVentas()

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

        self.boton_mostrar_grafo = ctk.CTkButton(self.frame_izq, text="Mostrar Grafo", command=self.mostrar_grafo)
        self.boton_mostrar_grafo.pack(pady=10, padx=10, fill="x")

        self.boton_salir = ctk.CTkButton(self.frame_izq, text="Salir", command=self.quit)
        self.boton_salir.pack(pady=10, padx=10, fill="x")

        # Área para mostrar información
        self.texto_info = ctk.CTkTextbox(self, width=400, height=560)
        self.texto_info.pack(side="right", fill="both", expand=True)

    # Métodos de comando
    def agregar_producto(self):
        nombre = ctk.CTkInputDialog(text="Agregar Producto", title="Ingrese el nombre del producto:")
        precio = ctk.CTkInputDialog(text="Agregar Producto", title="Ingrese el precio del producto:")
        if nombre and precio:
            try:
                precio = int(precio)
                if self.sistema.agregar_producto(nombre, precio):
                    ctk.CTkMessageBox.show_info("Éxito", f"Producto '{nombre}' agregado con éxito.")
                else:
                    ctk.CTkMessageBox.show_warning("Advertencia", "Producto no pudo ser agregado.")
            except ValueError:
                ctk.CTkMessageBox.show_warning("Advertencia", "Por favor, ingrese un precio válido.")

    def agregar_cliente(self):
        dni = ctk.CTkInputDialog(text="Agregar Cliente", title="Ingrese el DNI del cliente:")
        nombre = ctk.CTkInputDialog(text="Agregar Cliente", title="Ingrese el nombre del cliente:")
        if dni and nombre:
            if self.sistema.agregar_cliente(dni, nombre):
                ctk.CTkMessageBox.show_info("Éxito", f"Cliente '{nombre}' agregado con éxito.")
            else:
                ctk.CTkMessageBox.show_warning("Advertencia", "Cliente no pudo ser agregado.")

    def agregar_distrito(self):
        nombre = ctk.CTkInputDialog(text="Agregar Distrito", title="Ingrese el nombre del distrito:")
        if nombre:
            if self.sistema.agregar_distrito(nombre):
                ctk.CTkMessageBox.show_info("Éxito", f"Distrito '{nombre}' agregado con éxito.")
            else:
                ctk.CTkMessageBox.show_warning("Advertencia", "Distrito no pudo ser agregado.")

    def agregar_ruta(self):
        origen = ctk.CTkInputDialog(text="Agregar Ruta", title="Ingrese el nombre del distrito de origen:")
        destino = ctk.CTkInputDialog(text="Agregar Ruta", title="Ingrese el nombre del distrito de destino:")
        distancia = ctk.CTkInputDialog(text="Agregar Ruta", title="Ingrese la distancia entre los distritos:")
        if origen and destino and distancia:
            try:
                distancia = float(distancia)
                if self.sistema.agregar_ruta(origen, destino, distancia):
                    ctk.CTkMessageBox.show_info("Éxito", f"Ruta entre '{origen}' y '{destino}' agregada con éxito.")
                else:
                    ctk.CTkMessageBox.show_warning("Advertencia", "Ruta no pudo ser agregada.")
            except ValueError:
                ctk.CTkMessageBox.show_warning("Advertencia", "Por favor, ingrese una distancia válida.")

    def realizar_orden(self):
        dni_cliente = ctk.CTkInputDialog(text="Realizar Orden", title="Ingrese el DNI del cliente:")
        nombre_producto = ctk.CTkInputDialog(text="Realizar Orden", title="Ingrese el nombre del producto:")
        nombre_distrito = ctk.CTkInputDialog(text="Realizar Orden", title="Ingrese el nombre del distrito:")
        if dni_cliente and nombre_producto and nombre_distrito:
            if self.sistema.realizar_orden(dni_cliente, nombre_producto, nombre_distrito):
                ctk.CTkMessageBox.show_info("Éxito", "Orden realizada con éxito.")
            else:
                ctk.CTkMessageBox.show_warning("Advertencia", "Orden no pudo ser agregada.")

    def procesar_siguiente_orden(self):
        orden_procesada = self.sistema.procesar_orden()
        if orden_procesada:
            mensaje = (f"Orden procesada:\n"
                       f"Producto: {orden_procesada.producto.nombre}\n"
                       f"Cliente: {orden_procesada.cliente.nombre}\n"
                       f"Distrito: {orden_procesada.distrito.nombre}")
            ctk.CTkMessageBox.show_info("Orden Procesada", mensaje)
        else:
            ctk.CTkMessageBox.show_info("Sin Órdenes", "No hay órdenes para procesar.")

    def mostrar_grafo(self):
        # Lógica para mostrar el grafo
        distritos = [distr.nombre for distr in self.sistema.grafo_distritos.vertices.values()]
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

        # Mostrar el grafo
        pos = nx.spring_layout(G)
        nx.draw_networkx(G, pos, with_labels=True, node_color='lightblue', node_size=2000, font_size=12, font_color='black')
        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
        plt.title("Grafo de Distritos y Conexiones")
        plt.show()

if __name__ == "__main__":
    app = GUI()
    app.mainloop()
