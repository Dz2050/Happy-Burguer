import sqlite3

def crear_tablas():
    conn = sqlite3.connect('happy_burger.db')  # Conexión a la base de datos
    cursor = conn.cursor()

    # Tabla clientes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            clave TEXT UNIQUE NOT NULL,
            nombre TEXT NOT NULL,
            direccion TEXT NOT NULL,
            correo_electronico TEXT NOT NULL,
            telefono TEXT NOT NULL
        )
    ''')

    # Tabla productos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            clave TEXT UNIQUE NOT NULL,
            nombre TEXT NOT NULL,
            descripcion TEXT,
            precio REAL NOT NULL,
            categoria TEXT NOT NULL
        )
    ''')

    # Tabla pedidos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pedidos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER,
            fecha_hora TEXT,
            total REAL,
            FOREIGN KEY(cliente_id) REFERENCES clientes(id)
        )
    ''')

    # Tabla detalles_pedido
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS detalles_pedido (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pedido_id INTEGER,
            producto_id INTEGER,
            cantidad INTEGER,
            FOREIGN KEY(pedido_id) REFERENCES pedidos(id),
            FOREIGN KEY(producto_id) REFERENCES productos(id)
        )
    ''')

    conn.commit()  # Guardar los cambios
    conn.close()  # Cerrar la conexión

if __name__ == '__main__':
    crear_tablas()  # Ejecutar la función para crear las tablas
