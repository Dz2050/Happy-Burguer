import sqlite3
from utils.clases import Producto, Cliente, Pedido

def get_db_connection():
    conn = sqlite3.connect('happy_burger.db')
    conn.row_factory = sqlite3.Row  # Permite acceder a los resultados por nombre de columna
    return conn

def agregar_cliente():
    """Agrega un nuevo cliente a la base de datos."""

    clave = input("Ingrese la clave del cliente: ")

    # Validación de clave única
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clientes WHERE clave = ?", (clave,))
    cliente_existente = cursor.fetchone()
    
    while cliente_existente:
        print("La clave ya existe. Por favor, ingrese una clave única.")
        clave = input("Ingrese la clave del cliente: ")
        cursor.execute("SELECT * FROM clientes WHERE clave = ?", (clave,))
        cliente_existente = cursor.fetchone()

    nombre = input("Ingrese el nombre del cliente: ")
    direccion = input("Ingrese la dirección del cliente: ")
    correo_electronico = input("Ingrese el correo electrónico del cliente: ")
    telefono = input("Ingrese el teléfono del cliente: ")

    try:
        cursor.execute("INSERT INTO clientes (clave, nombre, direccion, correo_electronico, telefono) VALUES (?, ?, ?, ?, ?)", 
                    (clave, nombre, direccion, correo_electronico, telefono))
        conn.commit()
        print("Cliente agregado correctamente.")
    except sqlite3.IntegrityError:
        print("Error: La clave del cliente ya existe.")
    
    conn.close()

def eliminar_cliente():
    """Elimina un cliente de la base de datos."""

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM clientes")
    clientes = cursor.fetchall()

    if not clientes:  # Verificar si hay clientes registrados
        print("No hay clientes registrados.")
        conn.close()
        return

    print("Clientes registrados:")
    for cliente in clientes:
        print(f"- {cliente['clave']}: {cliente['nombre']}")

    clave_eliminar = input("Ingrese la clave del cliente a eliminar: ")

    if any(cliente['clave'] == clave_eliminar for cliente in clientes):
        cursor.execute("DELETE FROM clientes WHERE clave = ?", (clave_eliminar,))
        conn.commit()
        print("Cliente eliminado correctamente.")
    else:
        print("No se encontró ningún cliente con esa clave.")
    
    conn.close()

def actualizar_cliente():
    """Actualiza los datos de un cliente existente en la base de datos."""

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM clientes")
    clientes = cursor.fetchall()

    if not clientes:
        print("No hay clientes registrados.")
        conn.close()
        return

    print("Clientes registrados:")
    for cliente in clientes:
        print(f"- {cliente['clave']}: {cliente['nombre']}")

    clave_actualizar = input("Ingrese la clave del cliente a actualizar: ")

    if any(cliente['clave'] == clave_actualizar for cliente in clientes):
        cliente = next(cliente for cliente in clientes if cliente['clave'] == clave_actualizar)

        print(f"Datos actuales del cliente {cliente['nombre']}:")
        print(f"- Clave: {cliente['clave']}")
        print(f"- Nombre: {cliente['nombre']}")
        print(f"- Dirección: {cliente['direccion']}")
        print(f"- Correo electrónico: {cliente['correo_electronico']}")
        print(f"- Teléfono: {cliente['telefono']}")

        nuevo_nombre = input("Ingrese el nuevo nombre (o presione Enter para mantener el actual): ")
        nueva_direccion = input("Ingrese la nueva dirección (o presione Enter para mantener la actual): ")
        nuevo_correo = input("Ingrese el nuevo correo electrónico (o presione Enter para mantener el actual): ")
        nuevo_telefono = input("Ingrese el nuevo teléfono (o presione Enter para mantener el actual): ")

        # Actualizar los datos del cliente si se proporcionaron nuevos valores
        if nuevo_nombre:
            cliente['nombre'] = nuevo_nombre
        if nueva_direccion:
            cliente['direccion'] = nueva_direccion
        if nuevo_correo:
            cliente['correo_electronico'] = nuevo_correo
        if nuevo_telefono:
            cliente['telefono'] = nuevo_telefono

        cursor.execute("UPDATE clientes SET nombre = ?, direccion = ?, correo_electronico = ?, telefono = ? WHERE clave = ?", 
                    (cliente['nombre'], cliente['direccion'], cliente['correo_electronico'], cliente['telefono'], clave_actualizar))
        conn.commit()
        print("Cliente actualizado correctamente.")

    else:
        print("No se encontró ningún cliente con esa clave.")

    conn.close()

def agregar_producto():
    """Agrega un nuevo producto a la base de datos."""

    clave = input("Ingrese la clave del producto: ")

    # Validación de clave única
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos WHERE clave = ?", (clave,))
    producto_existente = cursor.fetchone()

    while producto_existente:
        print("La clave ya existe. Por favor, ingrese una clave única.")
        clave = input("Ingrese la clave del producto: ")
        cursor.execute("SELECT * FROM productos WHERE clave = ?", (clave,))
        producto_existente = cursor.fetchone()

    nombre = input("Ingrese el nombre del producto: ")
    descripcion = input("Ingrese la descripción del producto: ")
    while True:
        try:
            precio = float(input("Ingrese el precio del producto: "))
            if precio > 0:
                break
            else:
                print("El precio debe ser mayor a cero.")
        except ValueError:
            print("Ingrese un valor numérico válido para el precio.")
    categoria = input("Ingrese la categoría del producto (comida, bebida, snack): ")

    try:
        cursor.execute("INSERT INTO productos (clave, nombre, descripcion, precio, categoria) VALUES (?, ?, ?, ?, ?)", 
                    (clave, nombre, descripcion, precio, categoria))
        conn.commit()
        print("Producto agregado correctamente.")
    except sqlite3.IntegrityError:
        print("Error: La clave del producto ya existe.")
    finally:
        conn.close()

def eliminar_producto():
    """Elimina un producto de la base de datos."""

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()

    if not productos:
        print("No hay productos registrados.")
        conn.close()
        return

    print("Productos registrados:")
    for producto in productos:
        print(f"- {producto['clave']}: {producto['nombre']} - ${producto['precio']}")

    clave_eliminar = input("Ingrese la clave del producto a eliminar: ")

    if any(producto['clave'] == clave_eliminar for producto in productos):
        cursor.execute("DELETE FROM productos WHERE clave = ?", (clave_eliminar,))
        conn.commit()
        print("Producto eliminado correctamente.")
    else:
        print("No se encontró ningún producto con esa clave.")
    conn.close()

def crear_pedido():
    """Crea un nuevo pedido y lo agrega a la base de datos."""

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM clientes")
    clientes = cursor.fetchall()

    if not clientes:
        print("No hay clientes registrados. Debe agregar clientes antes de crear un pedido.")
        conn.close()
        return

    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()

    if not productos:
        print("No hay productos registrados. Debe agregar productos antes de crear un pedido.")
        conn.close()
        return

    print("Clientes disponibles:")
    for cliente in clientes:
        print(f"- {cliente['clave']}: {cliente['nombre']}")

    productos_pedido = []
    while True:
        clave_cliente = input("Ingrese la clave del cliente para este pedido: ")
        if any(cliente['clave'] == clave_cliente for cliente in clientes):
            cliente = next(cliente for cliente in clientes if cliente['clave'] == clave_cliente)
            break
        else:
            print("Clave de cliente no válida. Intente nuevamente")


    conn = get_db_connection()
    cursor = conn.cursor()

    # Insertar el pedido en la tabla 'pedidos'
    cursor.execute("INSERT INTO pedidos (cliente_id, fecha_hora, total) VALUES (?, datetime('now'), 0)", (cliente.id,))
    pedido_id = cursor.lastrowid

    total = 0
    # Insertar los detalles del pedido en la tabla 'detalles_pedido'
    for producto, cantidad in productos_pedido:
        cursor.execute("INSERT INTO detalles_pedido (pedido_id, producto_id, cantidad) VALUES (?, ?, ?)",
                    (pedido_id, producto.id, cantidad))
        total += producto.precio * cantidad

    # Actualizar el total del pedido
    cursor.execute("UPDATE pedidos SET total = ? WHERE id = ?", (total, pedido_id))

    conn.commit()
    conn.close()
    print("Pedido creado correctamente.")

def actualizar_estado_pedido():
    """Actualiza el estado de un pedido existente en la base de datos."""

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT p.id, p.fecha_hora, c.nombre AS cliente_nombre, p.total
        FROM pedidos p
        JOIN clientes c ON p.cliente_id = c.id
    """)

    pedidos = cursor.fetchall()

    if not pedidos:
        print("No hay pedidos registrados.")
        conn.close()
        return

    print("Pedidos registrados:")
    for pedido in pedidos:
        print(f"- {pedido['id']}: Cliente: {pedido['cliente_nombre']}, Total: ${pedido['total']:.2f}")

    while True:
        try:
            pedido_id = int(input("Ingrese el número del pedido a actualizar: "))
            if any(pedido['id'] == pedido_id for pedido in pedidos):
                nuevo_estado = input("Ingrese el nuevo estado del pedido (Pendiente, En preparación, Listo, Entregado): ")
                cursor.execute("UPDATE pedidos SET estado = ? WHERE id = ?", (nuevo_estado, pedido_id))
                conn.commit()
                print("Estado del pedido actualizado correctamente.")
                break
            else:
                print("No se encontró ningún pedido con ese número. Intente nuevamente.")
        except ValueError:
            print("Ingrese un número válido.")

    conn.close()

def ver_pedidos():
    """Muestra todos los pedidos registrados en la base de datos."""

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT p.id, p.fecha_hora, c.nombre AS cliente_nombre, p.total
        FROM pedidos p
        JOIN clientes c ON p.cliente_id = c.id
    """)

    pedidos = cursor.fetchall()

    if not pedidos:
        print("No hay pedidos registrados.")
        conn.close()
        return

    for pedido in pedidos:
        print(f"Pedido {pedido['id']}:")
        print(f"  Cliente: {pedido['cliente_nombre']}")
        print(f"  Fecha y hora: {pedido['fecha_hora']}")
        print(f"  Total: ${pedido['total']:.2f}")

        # Obtener detalles del pedido
        cursor.execute("SELECT dp.cantidad, pr.nombre, pr.precio FROM detalles_pedido dp JOIN productos pr ON dp.producto_id = pr.id WHERE dp.pedido_id = ?", (pedido['id'],))
        detalles = cursor.fetchall()

        print("  Productos:")
        for detalle in detalles:
            print(f"    - {detalle['nombre']} x {detalle['cantidad']} - ${detalle['precio']:.2f}")

        print("-" * 20)  # Separador entre pedidos

    conn.close()

def actualizar_producto():
    """Actualiza los datos de un producto existente en la base de datos."""

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()

    if not productos:
        print("No hay productos registrados.")
        conn.close()
        return

    print("Productos registrados:")
    for producto in productos:
        print(f"- {producto['clave']}: {producto['nombre']} - ${producto['precio']}")

    clave_actualizar = input("Ingrese la clave del producto a actualizar: ")

    if any(producto['clave'] == clave_actualizar for producto in productos):
        producto = next(producto for producto in productos if producto['clave'] == clave_actualizar)

        print(f"Datos actuales del producto {producto['nombre']}:")
        print(f"- Clave: {producto['clave']}")
        print(f"- Nombre: {producto['nombre']}")
        print(f"- Descripción: {producto['descripcion']}")
        print(f"- Precio: ${producto['precio']}")
        print(f"- Categoría: {producto['categoria']}")

        nuevo_nombre = input("Ingrese el nuevo nombre (o presione Enter para mantener el actual): ")
        nueva_descripcion = input("Ingrese la nueva descripción (o presione Enter para mantener la actual): ")
        while True:
            try:
                nuevo_precio = float(input("Ingrese el nuevo precio (o presione Enter para mantener el actual): "))
                if nuevo_precio > 0:
                    break
                else:
                    print("El precio debe ser mayor a cero.")
            except ValueError:
                print("Ingrese un valor numérico válido para el precio.")
        nueva_categoria = input("Ingrese la nueva categoría (o presione Enter para mantener la actual): ")

        # Actualizar los datos del producto si se proporcionaron nuevos valores
        if nuevo_nombre:
            producto['nombre'] = nuevo_nombre
        if nueva_descripcion:
            producto['descripcion'] = nueva_descripcion
        if nuevo_precio:
            producto['precio'] = nuevo_precio
        if nueva_categoria:
            producto['categoria'] = nueva_categoria

        cursor.execute("UPDATE productos SET nombre = ?, descripcion = ?, precio = ?, categoria = ? WHERE clave = ?", 
                    (producto['nombre'], producto['descripcion'], producto['precio'], producto['categoria'], clave_actualizar))
        conn.commit()
        print("Producto actualizado correctamente.")

    else:
        print("No se encontró ningún producto con esa clave.")
    conn.close()

# Función principal para controlar el flujo del programa
def main():
    while True:
        print("Bienvenido al sistema de pedidos del restaurante de franquicia:")
        print("1. Agregar Cliente")
        print("2. Agregar Producto")
        print("3. Realizar Pedido")
        print("4. Ver Pedidos")
        print("5. Actualizar Estado de Pedido")
        print("6. Salir")

        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            agregar_cliente()
        elif opcion == "2":
            agregar_producto()
        elif opcion == "3":
            crear_pedido()
        elif opcion == "4":
            ver_pedidos()
        elif opcion == "5":
            actualizar_estado_pedido()
        elif opcion == "6":
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida. Por favor, seleccione una opción válida.")

if __name__ == "__main__":
    main()