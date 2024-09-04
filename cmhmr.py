import heapq
from collections import deque

class Producto:
    def __init__(self, nombre, precio):
        self.nombre = nombre
        self.precio = precio

class Cliente:
    def __init__(self, dni, nombre):
        self.dni = dni
        self.nombre = nombre

class Distrito:
    def __init__(self, nombre):
        self.nombre = nombre
        self.conexiones : dict[str, int] = {}

class Orden:
    def __init__(self, producto, cliente, distrito):
        self.producto : Producto = producto
        self.cliente : Cliente = cliente
        self.distrito : Distrito = distrito

class Grafo:
    def __init__(self):
        self.vertices : dict[str, Distrito] = {}

    def get(self, nombre):
        return self.vertices.get(nombre)

    def agregar_distrito(self, nombre : str):
        if nombre not in self.vertices:
            distrito = Distrito(nombre)
            self.vertices[nombre] = distrito

    def agregar_camino(self, origen, destino, distancia):
        if origen in self.vertices and destino in self.vertices:
            self.vertices[origen].conexiones[destino] = distancia
            self.vertices[destino].conexiones[origen] = distancia  # Grafo no dirigido

    def dijkstra(self, inicio, destino : str = None):
        distancias = {v: float('inf') for v in self.vertices}
        distancias[inicio] = 0
        queue = [(0, inicio)]

        while queue:
            distancia_actual, vertice_actual = heapq.heappop(queue)

            if distancia_actual > distancias[vertice_actual]:
                continue

            for vecino, peso in self.vertices[vertice_actual].conexiones.items():
                distancia = distancia_actual + peso

                if distancia < distancias[vecino]:
                    distancias[vecino] = distancia
                    heapq.heappush(queue, (distancia, vecino))

        if destino:
            return distancias[destino] if distancias[destino] != float('inf') else None
        else:
            return distancias
    
class ColaFIFO:
    def __init__(self):
        self.cola = deque()

    def encolar(self, orden):
        self.cola.append(orden)

    def desencolar(self):
        if len(self.cola) > 0:
            return self.cola.popleft()
        else:
            return None

    def esta_vacia(self):
        return len(self.cola) == 0
    
class SistemaVentas:
    def __init__(self, localidad : str = "Flores"):
        self.productos : dict[str, Producto] = {}
        self.clientes : dict[str, Cliente] = {}
        self.grafo_distritos = Grafo()
        self.ordenes = ColaFIFO()
        self.local = localidad

        self.agregar_distrito(self.local)

    def agregar_producto(self, nombre, precio):
        if nombre not in self.productos:
            producto = Producto(nombre, precio)
            self.productos[nombre] = producto

    def agregar_cliente(self, dni, nombre):
        if dni not in self.clientes:
            cliente = Cliente(dni, nombre)
            self.clientes[dni] = cliente

    def agregar_distrito(self, nombre):
        self.grafo_distritos.agregar_distrito(nombre)

    def agregar_ruta(self, origen, destino, distancia):
        self.grafo_distritos.agregar_camino(origen, destino, distancia)

    def realizar_orden(self, dni_cliente, nombre_producto, nombre_distrito):
        cliente = self.clientes.get(dni_cliente)
        producto = self.productos.get(nombre_producto)
        distrito = self.grafo_distritos.get(nombre_distrito)

        # Mover la funcionalidad de esta parte al GUI:
        if not cliente:
            # print(f"Cliente con DNI {dni_cliente} no encontrado, registrando nuevo cliente.")
            self.agregar_cliente(dni_cliente, f"Cliente {dni_cliente}")
            cliente = self.clientes[dni_cliente]

        if not producto:
            # print(f"Producto {nombre_producto} no disponible.")
            return

        if not distrito:
            # print(f"Distrito {nombre_distrito} no disponible.")
            return

        orden = Orden(producto, cliente, distrito)
        self.ordenes.encolar(orden)
        # print(f"Orden para {producto.nombre} de {cliente.nombre} en {distrito.nombre} ha sido creada.")

    def procesar_orden(self):
        if self.ordenes.esta_vacia():
            return None
        else:
            orden : Orden = self.ordenes.desencolar()
            return orden
        
    def ruta_mas_corta(self, destino, inicio = None):
        if not inicio:
            inicio = self.local
        distancia = self.grafo_distritos.dijkstra(inicio, destino)
        return distancia
    
    def procesar_ordenes(self):
        ordenes = []
        distancias = {}
        while not self.ordenes.esta_vacia():
            orden : Orden = self.procesar_orden()
            if orden:
                ordenes.append(orden)
                distancia = self.ruta_mas_corta(orden.distrito.nombre)
                distancias[orden.distrito.nombre] = distancia
                # print(f"Procesando orden de {orden.producto.nombre} para {orden.cliente.nombre}.")
                # print(f"Ruta más corta a {orden.distrito.nombre} es de {distancia} km.")
            
        return ordenes, distancias

def testSistemaVentas():

    # Crear el sistema
    sistema = SistemaVentas()

    # Agregar distritos y rutas
    sistema.agregar_distrito("Flores")
    sistema.agregar_distrito("Palermo")
    sistema.agregar_distrito("Belgrano")

    sistema.agregar_ruta("Flores", "Palermo", 5)
    sistema.agregar_ruta("Flores", "Belgrano", 8)
    sistema.agregar_ruta("Palermo", "Belgrano", 3)

    # Agregar productos
    sistema.agregar_producto("Laptop", 1500)
    sistema.agregar_producto("Smartphone", 700)

    # Agregar clientes
    sistema.agregar_cliente("12345678", "Juan Perez")

    # Realizar y procesar órdenes
    sistema.realizar_orden("12345678", "Laptop", "Palermo")
    print(sistema.procesar_ordenes())

    return sistema

if __name__ == "__main__":
    testSistemaVentas()