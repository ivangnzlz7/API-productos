CARRITO = {}

def obtener_carrito(session_id):
    if session_id not in CARRITO:
        CARRITO[session_id] = {
            'items': {},
            'total': 0,
            'items_count': 0
        }
    return CARRITO[session_id]

def calcular_carrito(carrito):
    """ Recalcula el total y cantidad de items del carrito"""
    total = 0
    items_count = 0

    for item_data in carrito['items'].values():
        subtotal = item_data['cantidad'] * item_data['precio']
        total += subtotal
        items_count += item_data['cantidad']

    carrito['total'] = total
    carrito['items_count'] = items_count
    return carrito

def guardar_carrito(session_id, carrito):
    """Guarda el carrito en el almacenamiento persistente"""
    CARRITO[session_id] = carrito