import heapq
from collections import deque
import bbdd

class Producto:
    def __init__(self, nombre : str, precio : int, id: int = None):
        self.nombre = nombre
        self.precio = precio
        self.id = id

    def setId(self, id : int):
        self.id = id

class Cliente:
    def __init__(self, dni : str, nombre : str, id: int = None):
        self.dni = dni
        self.nombre = nombre
        self.id = id

    def setId(self, id : int):
        self.id = id

class Distrito:
    def __init__(self, nombre : str, id: int = None):
        self.nombre = nombre
        self.conexiones : dict[str, float] = {}
        self.id = id

    def setId(self, id : int):
        self.id = id

class Orden:
    def __init__(self, producto, cliente, distrito, id: int = None):
        self.producto : Producto = producto
        self.cliente : Cliente = cliente
        self.distrito : Distrito = distrito
        self.id = id

    def setId(self, id : int):
        self.id = id

class Grafo:
    def __init__(self):
        self.vertices : dict[str, Distrito] = {}

    def get(self, nombre):
        return self.vertices.get(nombre)

    def agregar_distrito(self, nombre : str, id : int = None): 
        if nombre not in self.vertices:
            distrito = Distrito(nombre, id)
            self.vertices[nombre] = distrito

    def agregar_camino(self, origen, destino, distancia) -> tuple[int, int]|None:
        if origen in self.vertices and destino in self.vertices:
            self.vertices[origen].conexiones[destino] = distancia
            self.vertices[destino].conexiones[origen] = distancia  # Grafo no dirigido
            return self.vertices[origen].id, self.vertices[destino].id
        else:
            return None

    def dijkstra(self, inicio, destino : str = None, camino : bool = False):
        distancias = {v: float('inf') for v in self.vertices}
        caminos = [[(inicio, v, self.vertices[v].conexiones[inicio])] for v in self.vertices if (v != inicio) and (inicio in self.vertices[v].conexiones.keys())]
        distancias[inicio] = 0
        queue = [(0, inicio)]
        if camino:
            nodo_anterior = inicio
        # print("CAMINOS:", caminos)

        while queue:
            # print('1', queue, distancias)
            distancia_actual, vertice_actual = heapq.heappop(queue)

            if distancia_actual > distancias[vertice_actual]:
                continue

            for vecino, peso in self.vertices[vertice_actual].conexiones.items():
                distancia = distancia_actual + peso

                if distancia < distancias[vecino]:
                    if camino:
                        for c in caminos:
                            print(vertice_actual, vecino, distancia)
                            if c[-1][1] == nodo_anterior and c[-1][1] != destino and c[-1][0] != vecino:
                                c.append((nodo_anterior, vecino, self.vertices[nodo_anterior].conexiones[vecino] + c[-1][2]))
                    distancias[vecino] = distancia
                    heapq.heappush(queue, (distancia, vecino))
                    if camino:
                        nodo_anterior = vecino
                        print("CAMINOS:", caminos)
                print('2', queue, vertice_actual, vecino, self.vertices[vertice_actual].conexiones.items())

        if camino:
            caminosDist = [(i, c[-1][2]) for i, c in enumerate(caminos)]
            caminoMinimoIndex = min(caminosDist, key=lambda x: x[1])[0]
            caminoMinimo = [(arista[0], arista[1]) for arista in caminos[caminoMinimoIndex]]
            return caminoMinimo
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
        
    def primero(self):
        if len(self.cola) > 0:
            return self.cola[0]
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
        
        self.conn = bbdd.crear_conexion()
        bbdd.crear_tablas(self.conn)
        self.importar_datos()

        self.local = localidad
        if not self.grafo_distritos.get(self.local):
            self.agregar_distrito(self.local)

    def importar_datos(self):
        productos_bbdd = bbdd.obtener_productos(self.conn)
        for prod in productos_bbdd:
            id_producto, nombre, precio = prod
            self.productos[nombre] = Producto(nombre, precio, id_producto)
        
        clientes_bbdd = bbdd.obtener_clientes(self.conn)
        for client in clientes_bbdd:
            id_cliente, dni, nombre = client
            self.clientes[dni] = Cliente(dni, nombre, id_cliente)

        distritos_bbdd = bbdd.obtener_distritos(self.conn)
        for distr in distritos_bbdd:
            id_distrito, nombre = distr
            self.grafo_distritos.agregar_distrito(nombre, id_distrito)

        rutas_bbdd = bbdd.obtener_rutas(self.conn)
        for ruta in rutas_bbdd:
            id_origen, id_destino, distancia = ruta
            nom_origen = bbdd.obtener_distrito_nombre_por_id(self.conn, id_origen)[0][0]
            nom_destino = bbdd.obtener_distrito_nombre_por_id(self.conn, id_destino)[0][0]
            self.grafo_distritos.agregar_camino(nom_origen, nom_destino, distancia)

        ordenes_bbdd = bbdd.obtener_ordenes(self.conn)
        for orden in ordenes_bbdd:
            id_orden, id_producto, id_cliente, id_distrito = orden
            nom_producto = bbdd.obtener_producto_nombre_por_id(self.conn, id_producto)
            dni_cliente = bbdd.obtener_cliente_dni_por_id(self.conn, id_cliente)
            nom_distrito = bbdd.obtener_distrito_nombre_por_id(self.conn, id_distrito)

            orden_producto = self.productos.get(nom_producto)
            orden_cliente = self.clientes.get(dni_cliente)
            orden_distrito = self.grafo_distritos.get(nom_distrito)
            self.ordenes.encolar(Orden(orden_producto, orden_cliente, orden_distrito, id_orden))

    def agregar_producto(self, nombre, precio) -> bool:
        if nombre not in self.productos:
            id_producto = bbdd.agregar_producto(self.conn, nombre, precio)
            if not id_producto: return False
            producto = Producto(nombre, precio, id_producto)
            self.productos[nombre] = producto
            return True
        else: return False

    def agregar_cliente(self, dni, nombre) -> bool:
        if dni not in self.clientes:
            id_cliente = bbdd.agregar_cliente(self.conn, dni, nombre)
            if not id_cliente: return False
            cliente = Cliente(dni, nombre, id_cliente)
            self.clientes[dni] = cliente
            return True
        else: return False

    def agregar_distrito(self, nombre) -> bool:
        if self.grafo_distritos.get(nombre): return False
        id_distrito = bbdd.agregar_distrito(self.conn, nombre)
        if not id_distrito: return False
        self.grafo_distritos.agregar_distrito(nombre, id_distrito)
        return True
            
    def agregar_ruta(self, origen, destino, distancia) -> bool:
        id_origen = self.grafo_distritos.get(origen).id
        id_destino = self.grafo_distritos.get(destino).id
        if (not id_origen) or (not id_destino): return False
        if bbdd.agregar_ruta(self.conn, id_origen, id_destino, distancia):
            if self.grafo_distritos.agregar_camino(origen, destino, distancia):
                return True
            else: return False
        else: return False

    def realizar_orden(self, dni_cliente, nombre_producto, nombre_distrito) -> bool:
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
            return False

        if not distrito:
            # print(f"Distrito {nombre_distrito} no disponible.")
            return False
        
        if not self.ruta_mas_corta(nombre_distrito):
            return False
        
        id_orden = bbdd.agregar_orden(self.conn, producto.id, cliente.id, distrito.id)
        if not id_orden: return False
        orden = Orden(producto, cliente, distrito, id_orden)
        self.ordenes.encolar(orden)
        return True
        # print(f"Orden para {producto.nombre} de {cliente.nombre} en {distrito.nombre} ha sido creada.")

    def procesar_orden(self):
        if self.ordenes.esta_vacia():
            return None
        else:
            print(self.ordenes.primero())
            # if not self.ruta_mas_corta(orden.distrito.nombre):
            #     return None
            orden : Orden = self.ordenes.desencolar()
            if orden:
                bbdd.eliminar_orden(self.conn, orden.id)
            return orden
        
    def ruta_mas_corta(self, destino, inicio = None, solo_camino = False):
        '''
        Si solo_camino es False, devuelve la distancia minima entre dos distritos.
        Si solo_camino es True, devuelve cada paso del camino mas corto entre los distritos.
        Por default, comienza desde el distrito local.
        '''
        if not inicio:
            inicio = self.local
        ruta = self.grafo_distritos.dijkstra(inicio, destino, camino = solo_camino)
        return ruta
    
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
            else:
                print("!!!")
            
        return ordenes, distancias

def test_sistema_ventas():

    # Crear el sistema
    sistema = SistemaVentas()

    # Agregar distritos y rutas
    sistema.agregar_distrito("Flores")
    sistema.agregar_distrito("Palermo")
    sistema.agregar_distrito("Belgrano")
    sistema.agregar_distrito("4")
    sistema.agregar_distrito("5")

    sistema.agregar_ruta("Flores", "Palermo", 5)
    sistema.agregar_ruta("Flores", "Belgrano", 9)
    sistema.agregar_ruta("Flores", "4", 2)
    sistema.agregar_ruta("4", "Belgrano", 11)
    sistema.agregar_ruta("Palermo", "4", 3)
    sistema.agregar_ruta("Palermo", "Belgrano", 3)

    # Agregar productos
    sistema.agregar_producto("Laptop", 1500)
    sistema.agregar_producto("Smartphone", 700)

    # Agregar clientes
    sistema.agregar_cliente("12345678", "Juan Perez")

    # Realizar y procesar órdenes
    sistema.realizar_orden("12345678", "Laptop", "5")
    print(sistema.procesar_ordenes())

    return sistema

if __name__ == "__main__":
    test_sistema_ventas()
    # sistema = SistemaVentas()
    # print(sistema.clientes)