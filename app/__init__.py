from flask import Flask, render_template, request, session, jsonify
from utils.clases import Producto, Cliente, Pedido
from gestion_pedidos import *
import sqlite3

import os
from dotenv import load_dotenv

load_dotenv()  # Carga las variables de entorno desde el archivo .env

clientes = []
productos = []

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'  # Reemplaza con una clave segura

def get_db_connection():
    conn = sqlite3.connect(os.path.join(app.instance_path, 'happy_burger.db'))
    conn.row_factory = sqlite3.Row  # Permite acceder a los resultados por nombre de columna
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    clientes = conn.execute('SELECT * FROM clientes').fetchall()  # Obtener clientes de la base de datos
    conn.close()
    return render_template('index.html', clientes=clientes)

@app.route('/comida')
def comida():
    conn = get_db_connection()
    productos = conn.execute('SELECT * FROM productos WHERE categoria = "comida"').fetchall()  # Obtener productos de comida
    conn.close()
    print(productos)
    return render_template('comida.html', productos=productos)

@app.route('/bebidas')
def bebidas():
    conn = get_db_connection()
    bebidas = conn.execute('SELECT * FROM productos WHERE categoria = "bebida"').fetchall()  # Obtener bebidas
    conn.close()
    print(productos)
    return render_template('bebidas.html', bebidas=bebidas)

@app.route('/snacks')
def snacks():
    conn = get_db_connection()
    snacks = conn.execute('SELECT * FROM productos WHERE categoria = "snack"').fetchall()  # Obtener snacks
    conn.close()
    return render_template('snacks.html', snacks=snacks)


@app.route('/finalizar_pedido')
def finalizar_pedido():
    carrito = session.get('carrito', {})
    productos_carrito = []
    total = 0

    if carrito:  # Verificar si el carrito no está vacío
        conn = get_db_connection()
        try:
            claves_productos = list(carrito.keys())
            productos = conn.execute('SELECT * FROM productos WHERE clave IN ({})'.format(','.join('?' * len(claves_productos))), claves_productos).fetchall()

            for producto in productos:
                cantidad = carrito.get(producto['clave'], 0)
                productos_carrito.append({'clave': producto['clave'], 'nombre': producto['nombre'], 'precio': producto['precio'], 'cantidad': cantidad})
                total += producto['precio'] * cantidad
        except sqlite3.Error as e:
            return jsonify({'error': f"Error al obtener productos del carrito: {e}"}), 500
        finally:
            conn.close()
    else:
        return jsonify({'error': 'El carrito está vacío'}), 400  # Bad Request

    return render_template('finalizar_pedido.html', carrito=productos_carrito, total=total)



@app.route('/agregar_al_carrito', methods=['POST'])
def agregar_al_carrito():
    data = request.get_json()
    clave_producto = data['clave_producto']
    cantidad = data['cantidad']

    if cantidad <= 0:
        return jsonify({'success': False, 'message': 'La cantidad debe ser mayor que cero'}), 400  # Bad Request

    if 'carrito' not in session:
        session['carrito'] = {}

    conn = get_db_connection()
    cursor = conn.cursor()
    producto = cursor.execute('SELECT * FROM productos WHERE clave = ?', (clave_producto,)).fetchone()
    conn.close()

    if producto:
        if clave_producto in session['carrito']:
            session['carrito'][clave_producto] += cantidad
        else:
            session['carrito'][clave_producto] = cantidad

        return jsonify({'success': True, 'productos': session['carrito']})
    else:
        return jsonify({'success': False, 'message': 'Producto no encontrado'}), 404  # Not Found



@app.route('/eliminar_del_carrito', methods=['POST'])
def eliminar_del_carrito():
    data = request.get_json()
    clave_producto = data['clave_producto']

    if 'carrito' not in session:
        return jsonify({'success': False, 'message': 'El carrito está vacío'}), 400  # Bad Request

    if clave_producto not in session['carrito']:
        return jsonify({'success': False, 'message': 'Producto no encontrado en el carrito'}), 404  # Not Found

    del session['carrito'][clave_producto]
    return jsonify({'success': True, 'productos': session.get('carrito', {})})


@app.route('/obtener_productos_carrito')
def obtener_productos_carrito():
    carrito = session.get('carrito', {})
    productos_carrito = []
    total = 0

    conn = get_db_connection()
    for clave, cantidad in carrito.items():
        try:
            producto = conn.execute('SELECT * FROM productos WHERE clave = ?', (clave,)).fetchone()
            if producto:
                productos_carrito.append({'clave': producto['clave'], 'nombre': producto['nombre'], 'precio': producto['precio'], 'cantidad': cantidad})
                total += producto['precio'] * cantidad
            else:
                return jsonify({'error': f"Producto '{clave}' no encontrado en la base de datos."}), 404  # Producto no encontrado
        except sqlite3.Error as e:
            return jsonify({'error': f"Error al obtener productos del carrito: {e}"}), 500  # Error interno del servidor
    conn.close()

    return jsonify({'productos': productos_carrito, 'total': total})

@app.route('/confirmar_pedido', methods=['POST'])
def confirmar_pedido():
    data = request.get_json()
    cliente_data = data['cliente']
    carrito = data['carrito']

    cliente = Cliente(
        cliente_data.get('clave'),  # Obtener clave (o None si no existe)
        cliente_data.get('nombre'),  # Obtener nombre (o None si no existe)
        cliente_data.get('direccion'),  # Obtener direccion (o None si no existe)
        cliente_data.get('correo'),  # Obtener correo (o None si no existe)
        cliente_data.get('telefono')   # Obtener telefono (o None si no existe)
    )

    conn = get_db_connection()
    productos_pedido = []
    for clave, cantidad in carrito.items():
        producto = conn.execute('SELECT * FROM productos WHERE clave = ?', (clave,)).fetchone()
        if producto:
            productos_pedido.append(Producto(producto['clave'], producto['nombre'], producto['precio'], producto['categoria']))

    pedido = Pedido(cliente, productos_pedido)

    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO pedidos (cliente_id, fecha_hora, total) VALUES (?, datetime('now'), ?)", 
                    (cliente.id, pedido.calcular_total()))
        pedido_id = cursor.lastrowid

        for producto in pedido.productos:
            cursor.execute("INSERT INTO detalles_pedido (pedido_id, producto_id, cantidad) VALUES (?, ?, ?)",
                        (pedido_id, producto.id, carrito[producto.clave]))

        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
        return jsonify({'success': False, 'message': f'Error al procesar el pedido: {e}'}), 500
    finally:
        conn.close()

    session.pop('carrito', None) 

    return jsonify({'success': True, 'message': 'Pedido confirmado correctamente'})

#///////////////////////////////////////////////////////////////////


@app.route('/agregar_cliente', methods=['POST'])
def agregar_cliente_api():
    data = request.get_json()
    clave = data['clave']
    nombre = data['nombre']
    direccion = data['direccion']
    correo = data['correo']
    telefono = data['telefono']


    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO clientes (clave, nombre, direccion, correo_electronico, telefono) VALUES (?, ?, ?, ?, ?)", 
                    (clave, nombre, direccion, correo, telefono))
        conn.commit()
        conn.close()
        return jsonify({'success': True})  # Cliente agregado correctamente
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({'success': False, 'message': 'La clave del cliente ya existe'})

@app.route('/actualizar_cliente', methods=['POST'])
def actualizar_cliente_api():
    data = request.get_json()
    clave = data['clave']
    nombre = data['nombre']
    direccion = data['direccion']
    correo = data['correo']
    telefono = data['telefono']

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("UPDATE clientes SET nombre = ?, direccion = ?, correo_electronico = ?, telefono = ? WHERE clave = ?",
                    (nombre, direccion, correo, telefono, clave))
        conn.commit()
        success = True  # Indicar que la actualización fue exitosa
    except sqlite3.Error as e:
        print(f"Error al actualizar cliente: {e}")
        success = False
    finally:
        conn.close()

    return jsonify({'success': success, 'message': 'Cliente actualizado correctamente' if success else 'Error al actualizar cliente'})

@app.route('/eliminar_cliente', methods=['POST'])
def eliminar_cliente_api():
    data = request.get_json()
    clave = data['clave']

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM clientes WHERE clave = ?", (clave,))
        conn.commit()
        success = True  # Indicar que la eliminación fue exitosa
    except sqlite3.Error as e:
        print(f"Error al eliminar cliente: {e}")
        success = False
    finally:
        conn.close()

    return jsonify({'success': success, 'message': 'Cliente eliminado correctamente' if success else 'Error al eliminar cliente'})



def mostrar_menu():
    print("\n--- Menú Principal ---")
    print("1. Agregar Cliente")
    print("2. Eliminar Cliente")
    print("3. Actualizar Cliente")
    print("4. Agregar Producto")
    print("5. Eliminar Producto")
    print("6. Actualizar Producto")
    print("7. Pedidos")
    print("8. Salir")

def main():
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            agregar_cliente(clientes)
        elif opcion == '2':
            eliminar_cliente(clientes)
        elif opcion == '3':
            actualizar_cliente(clientes)
        elif opcion == '4':
            agregar_producto(productos)
        elif opcion == '5':
            eliminar_producto(productos)
        elif opcion == '6':
            actualizar_producto(productos)
        elif opcion == '7':
            actualizar_estado_pedido()
        elif opcion == '8':
            ver_pedidos()
        elif opcion == '9':
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida. Por favor, seleccione una opción válida.")

app.secret_key = os.getenv('SECRET_KEY')

if __name__ == "__main__":
    app.run(debug=True)  # Iniciar el servidor Flask
