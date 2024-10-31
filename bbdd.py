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

def crear_tablas(conn):
    """Crea las tablas necesarias si no existen."""
    try:
        cursor = conn.cursor()
        
        # Tabla Productos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY,
                nombre TEXT NOT NULL,
                precio REAL NOT NULL
            )
        ''')
        
        # Tabla Clientes
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clientes (
                dni TEXT PRIMARY KEY,
                nombre TEXT NOT NULL
            )
        ''')
        
        # Tabla Distritos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS distritos (
                id INTEGER PRIMARY KEY,
                nombre TEXT NOT NULL
            )
        ''')
        
        # Tabla Rutas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS rutas (
                id INTEGER PRIMARY KEY,
                origen_id INTEGER,
                destino_id INTEGER,
                distancia INTEGER,
                FOREIGN KEY (origen_id) REFERENCES distritos (id),
                FOREIGN KEY (destino_id) REFERENCES distritos (id)
            )
        ''')
        
        # Tabla Ordenes
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ordenes (
                id INTEGER PRIMARY KEY,
                producto_id INTEGER,
                cliente_dni TEXT,
                distrito_id INTEGER,
                FOREIGN KEY (producto_id) REFERENCES productos (id),
                FOREIGN KEY (cliente_dni) REFERENCES clientes (dni),
                FOREIGN KEY (distrito_id) REFERENCES distritos (id)
            )
        ''')
        
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error al crear las tablas: {e}")

# Funciones para Productos

def agregar_producto(conn, nombre: str, precio: float) -> bool:
    """Agrega un nuevo producto a la base de datos."""
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO productos (nombre, precio) VALUES (?, ?)", (nombre, precio))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error al agregar producto: {e}")
        return False

def obtener_productos(conn) -> List[Tuple[int, str, float]]:
    """Obtiene todos los productos de la base de datos."""
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM productos")
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Error al obtener productos: {e}")
        return []

def actualizar_producto(conn, id: int, nombre: str, precio: float) -> bool:
    """Actualiza un producto existente en la base de datos."""
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE productos SET nombre = ?, precio = ? WHERE id = ?", (nombre, precio, id))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error al actualizar producto: {e}")
        return False

def eliminar_producto(conn, id: int) -> bool:
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

def agregar_cliente(conn, dni: str, nombre: str) -> bool:
    """Agrega un nuevo cliente a la base de datos."""
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO clientes (dni, nombre) VALUES (?, ?)", (dni, nombre))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error al agregar cliente: {e}")
        return False

def obtener_clientes(conn) -> List[Tuple[str, str]]:
    """Obtiene todos los clientes de la base de datos."""
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clientes")
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Error al obtener clientes: {e}")
        return []

def actualizar_cliente(conn, dni: str, nombre: str) -> bool:
    """Actualiza un cliente existente en la base de datos."""
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE clientes SET nombre = ? WHERE dni = ?", (nombre, dni))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error al actualizar cliente: {e}")
        return False

def eliminar_cliente(conn, dni: str) -> bool:
    """Elimina un cliente de la base de datos."""
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM clientes WHERE dni = ?", (dni,))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error al eliminar cliente: {e}")
        return False
                            