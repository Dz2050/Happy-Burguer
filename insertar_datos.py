import sqlite3

def insertar_productos():
    conn = sqlite3.connect('happy_burger.db')
    cursor = conn.cursor()

    cursor.execute('DELETE FROM productos')

    productos = [
        
    ]

    cursor.executemany('INSERT OR REPLACE INTO productos (clave, nombre, descripcion, precio, categoria) VALUES (?, ?, ?, ?, ?)', productos)

    conn.commit()
    conn.close()

if __name__ == '__main__':
    insertar_productos()
