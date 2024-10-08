import sqlite3
from typing import List, Tuple

def crear_conexion():
    """Crea una conexión a la base de datos SQLite."""
    try:
        conn = sqlite3.connect('sistema_ventas.db')
        return conn
    except sqlite3.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

def crear_tablas(conn : sqlite3.Connection):
    """Crea las tablas necesarias si no existen."""
    try:
        cursor = conn.cursor()
        
        # Tabla Productos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY,
                nombre TEXT NOT NULL UNIQUE,
                precio INT NOT NULL
            )
        ''')
        
        # Tabla Clientes
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY,
                dni TEXT UNIQUE,
                nombre TEXT NOT NULL
            )
        ''')
        
        # Tabla Distritos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS distritos (
                id INTEGER PRIMARY KEY,
                nombre TEXT NOT NULL UNIQUE
            )
        ''')
        
        # Tabla Rutas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS rutas (
                origen_id INTEGER,
                destino_id INTEGER,
                distancia REAL,
                PRIMARY KEY (origen_id, destino_id),
                FOREIGN KEY (origen_id) REFERENCES distritos (id),
                FOREIGN KEY (destino_id) REFERENCES distritos (id)
            )
        ''')
        
        # Tabla Ordenes
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ordenes (
                id INTEGER PRIMARY KEY,
                producto_id INTEGER,
                cliente_id INTEGER,
                distrito_id INTEGER,
                FOREIGN KEY (producto_id) REFERENCES productos (id),
                FOREIGN KEY (cliente_id) REFERENCES clientes (id),
                FOREIGN KEY (distrito_id) REFERENCES distritos (id)
            )
        ''')
        
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error al crear las tablas: {e}")

# Funciones para Productos

def agregar_producto(conn : sqlite3.Connection, nombre: str, precio: int) -> int | None:
    """Agrega un nuevo producto a la base de datos."""
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO productos (nombre, precio) VALUES (?, ?)", (nombre, precio))
        conn.commit()
        return cursor.lastrowid
    except sqlite3.Error as e:
        print(f"Error al agregar producto: {e}")
        return None

def obtener_productos(conn : sqlite3.Connection) -> List[Tuple[int, str, int]]:
    """Obtiene todos los productos de la base de datos."""
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM productos")
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Error al obtener productos: {e}")
        return []
    
def obtener_producto_nombre_por_id(conn : sqlite3.Connection, id : int) -> List[Tuple[str]]:
    """Obtiene el nombre de un cliente de la base de datos por su ID."""
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT nombre FROM productos WHERE id = ?", (id,))
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Error al obtener distritos: {e}")
        return []

def actualizar_producto(conn : sqlite3.Connection, id: int, nombre: str, precio: int) -> bool:
    """Actualiza un producto existente en la base de datos."""
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE productos SET nombre = ?, precio = ? WHERE id = ?", (nombre, precio, id))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error al actualizar producto: {e}")
        return False

def eliminar_producto(conn : sqlite3.Connection, id: int) -> bool:
    """Elimina un producto de la base de datos."""
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM productos WHERE id = ?", (id,))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error al eliminar producto: {e}")
        return False

# Funciones para Clientes

def agregar_cliente(conn : sqlite3.Connection, dni: str, nombre: str) -> int | None:
    """Agrega un nuevo cliente a la base de datos."""
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO clientes (dni, nombre) VALUES (?, ?)", (dni, nombre))
        conn.commit()
        return cursor.lastrowid
    except sqlite3.Error as e:
        print(f"Error al agregar cliente: {e}")
        return None

def obtener_clientes(conn : sqlite3.Connection) -> List[Tuple[int, str, str]]:
    """Obtiene todos los clientes de la base de datos."""
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clientes")
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Error al obtener clientes: {e}")
        return []

def obtener_cliente_dni_por_id(conn : sqlite3.Connection, id : int) -> List[Tuple[str]]:
    """Obtiene el DNI de un cliente de la base de datos por su ID."""
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT dni FROM clientes WHERE id = ?", (id,))
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Error al obtener distritos: {e}")
        return []

def actualizar_cliente(conn : sqlite3.Connection, id: int, dni: str, nombre: str) -> bool:
    """Actualiza un cliente existente en la base de datos."""
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE clientes SET dni = ?, nombre = ? WHERE id = ?", (dni, nombre, id))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error al actualizar cliente: {e}")
        return False

def eliminar_cliente(conn : sqlite3.Connection, dni: str) -> bool:
    """Elimina un cliente de la base de datos."""
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM clientes WHERE dni = ?", (dni,))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error al eliminar cliente: {e}")
        return False

# Funciones para Distrito
    
def agregar_distrito(conn : sqlite3.Connection, nombre: str) -> int | None:
    """Agrega un nuevo distrito a la base de datos."""
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO distritos (nombre) VALUES (?)", (nombre,))
        conn.commit()
        return cursor.lastrowid
    except sqlite3.Error as e:
        print(f"Error al agregar distrito: {e}")
        return None
    
def obtener_distritos(conn : sqlite3.Connection) -> List[Tuple[int, str]]:
    """Obtiene todos los distritos de la base de datos."""
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM distritos")
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Error al obtener distritos: {e}")
        return []

def obtener_distrito_nombre_por_id(conn : sqlite3.Connection, id : int) -> List[Tuple[str]]:
    """Obtiene el nombre de un distrito de la base de datos por su ID."""
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT nombre FROM distritos WHERE id = ?", (id,))
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Error al obtener distritos: {e}")
        return []

def actualizar_distritos(conn : sqlite3.Connection, id: int, nombre: str) -> bool:
    """Actualiza un distrito existente en la base de datos."""
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE distritos SET nombre = ? WHERE id = ?", (nombre, id))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error al actualizar distrito: {e}")
        return False

def eliminar_distrito(conn : sqlite3.Connection, id: int) -> bool:
    """Elimina un distrito de la base de datos."""
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM distrito WHERE id = ?", (id,))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error al eliminar distrito: {e}")
        return False

# Funciones para Rutas

def agregar_ruta(conn : sqlite3.Connection, origen_id : int, destino_id : int, distancia : float) -> bool:
    """Agrega una nueva ruta entre distritos a la base de datos."""
    try:
        cursor = conn.cursor()
        datos = [(origen_id, destino_id, distancia), (destino_id, origen_id, distancia)]
        cursor.executemany("INSERT INTO rutas (origen_id, destino_id, distancia) VALUES (?,?,?)", datos)
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error al agregar ruta: {e}")
        return False
    
def obtener_rutas(conn : sqlite3.Connection) -> List[Tuple[int, int, float]]:
    """Obtiene todas las rutas de la base de datos."""
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM rutas")
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Error al obtener rutas: {e}")
        return []

def actualizar_rutas(conn : sqlite3.Connection, origen_id : int, destino_id : int, distancia : float) -> bool:
    """Actualiza una ruta existente en la base de datos."""
    try:
        cursor = conn.cursor()
        datos = [(distancia, origen_id, destino_id), (distancia, destino_id, origen_id)]
        cursor.executemany("UPDATE rutas SET distancia = ? WHERE origen_id = ? AND destino_id = ?", datos)
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error al actualizar ruta: {e}")
        return False

def eliminar_ruta(conn : sqlite3.Connection, origen_id: int, destino_id: int) -> bool:
    """Elimina una ruta de la base de datos."""
    try:
        cursor = conn.cursor()
        datos = [(origen_id, destino_id), (destino_id, origen_id)]
        cursor.executemany("DELETE FROM rutas WHERE origen_id = ? AND destino_id = ?", datos)
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error al eliminar ruta: {e}")
        return False

# Funciones para Ordenes

def agregar_orden(conn : sqlite3.Connection, producto_id : int, cliente_id : int, distrito_id : int) -> int | None:
    """Agrega una nueva orden a la base de datos."""
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO ordenes (producto_id, cliente_id, distrito_id) VALUES (?, ?, ?)", (producto_id, cliente_id, distrito_id))
        conn.commit()
        return cursor.lastrowid
    except sqlite3.Error as e:
        print(f"Error al agregar orden: {e}")
        return None

def obtener_ordenes(conn : sqlite3.Connection) -> List[Tuple[int, int, int, int]]:
    """Obtiene todas las ordenes de la base de datos."""
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM ordenes")
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Error al obtener ordenes: {e}")
        return []

def actualizar_orden(conn : sqlite3.Connection, id: int, producto_id : int, cliente_id : int, distrito_id : int) -> bool:
    """Actualiza una orden existente en la base de datos."""
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE ordenes SET producto_id = ?, cliente_id = ?, distrito_id = ? WHERE id = ?", (producto_id, cliente_id, distrito_id, id))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error al actualizar orden: {e}")
        return False

def eliminar_orden(conn : sqlite3.Connection, id: int) -> bool:
    """Elimina una orden de la base de datos."""
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM ordenes WHERE id = ?", (id,))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error al eliminar orden: {e}")
        return False

def eliminar_orden_mas_antigua(conn : sqlite3.Connection) -> bool:
    """Elimina una orden de la base de datos."""
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM ordenes WHERE id = (SELECT id FROM ordenes ORDER BY rowid LIMIT 1)")
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error al eliminar orden: {e}")
        return False

# Test

if __name__ == "__main__":
    conn = crear_conexion()
    crear_tablas(conn)
    prod1 = agregar_producto(conn, "Objeto", 4567)
    prod2 = agregar_producto(conn, "Comida", 56)
    print(prod1, prod2)
    print(obtener_productos(conn))
    eliminar_producto(conn, 1)
    print(obtener_productos(conn))
    prod3 = agregar_producto(conn, "Objeto2", 12345)
    print(prod3)
    print(obtener_productos(conn))
    agregar_cliente(conn, "12345678", "Persona")
    agregar_cliente(conn, "89012345", "Persona 3")
    agregar_cliente(conn, "45678901", "Persona 2")
    print(obtener_clientes(conn))