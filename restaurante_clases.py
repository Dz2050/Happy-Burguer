class Producto:
    def __init__(self, clave, nombre, precio, categoria):
        self.clave = clave
        self.nombre = nombre
        self.precio = precio
        self.categoria = categoria
    def __str__(self):
        return f"Producto(clave={self.clave}, nombre={self.nombre}, precio={self.precio}, categoria={self.categoria})"
    
class Cliente:
    def __str__(self):
        return f"Cliente(nombre={self.nombre}, telefono={self.telefono})"
        
def agregar_cliente():
    # Implementación de la función agregar_cliente
    pass

def agregar_producto():
    # Implementación de la función agregar_producto
    pass

def realizar_pedido():
    # Implementación de la función realizar_pedido
    pass

def ver_pedidos():
    # Implementación de la función ver_pedidos
    pass

def actualizar_estado_pedido():
    # Implementación de la función actualizar_estado_pedido
    pass

class Pedido:
    def __init__(self, cliente, productos):
        self.cliente = cliente
        self.productos = productos
        self.estado = "Pendiente"  # Estado por defecto

    def __str__(self):
        return f"Pedido(cliente={self.cliente}, productos={self.productos}, estado={self.estado}, total={self.calcular_total()})"