from flask import session, jsonify, Blueprint
from uuid import uuid4
from utils.aux import calcular_carrito, guardar_carrito, obtener_carrito

user = Blueprint("user", __name__)

# Base de datos en memoria (simulada)
PRODUCTOS = {
    '1': {'nombre': 'Laptop', 'precio': 800, 'stock': 10},
    '2': {'nombre': 'Mouse', 'precio': 25, 'stock': 50},
    '3': {'nombre': 'Teclado', 'precio': 45, 'stock': 30},
    '4': {'nombre': 'Monitor', 'precio': 300, 'stock': 5}
}

#Mostrar todos los productos
@user.route('/products')
def productsGets():
    return jsonify({
        'productos': PRODUCTOS,
        'mensaje': 'Usa /agregar/producto_id para agregar al carrito'
    })

#Carrito actual
@user.route('/carrito')
def view_carrito():
    session_id = session.get('session_id')
    if not session_id:
        session['session_id'] = str(uuid4())
        session_id = session['session_id']
    carrito = obtener_carrito(session_id)
    return jsonify({
        'session_id': session_id,
        'items': carrito['items'],
        'total': carrito['total'],
        'cantidad_total_items': carrito['items_count']
    })


#Agregar productos al carrito
@user.route('/agregar/<string:producto_id>', methods=['POST'])
def add_carrito(producto_id):
    """Agrega un producto al carrito"""
    session_id = session.get('session_id')
    if not session_id:
        session['session_id'] = str(uuid4())
        session_id = session['session_id']
    #Verificar si existe el producto
    if producto_id not in PRODUCTOS:
        return jsonify({'error': 'Producto no encontrado'}), 404
    
    #Obtener carrito actual
    carrito = obtener_carrito(session_id)

    #Obtener el producto
    producto = PRODUCTOS[producto_id]
    print(carrito['items'])
    
    #Agregar o actualizar item
    if producto_id in carrito['items']:
        carrito['items'][producto_id]['cantidad'] += 1
        carrito['total'] += producto['precio']
    else:
        carrito['items'][producto_id] = {
            'nombre': producto['nombre'],
            'precio': producto['precio'],
            'cantidad': 1
        }

    #Recalcular totales
    carrito = calcular_carrito(carrito)

    #Guardar cambios
    guardar_carrito(session_id,carrito)

    return jsonify({
        'message': f'Agregado 1 x {producto["nombre"]} al carrito',
        'carrito': {
            'items': carrito['items'],
            'total': carrito['total']
        }
    })


#Eliminar productos del carrito
@user.route('/eliminar/<producto_id>', methods=['DELETE'])
def eliminar_del_carrito(producto_id):
    """Elimina un producto del carrito"""
    session_id = session.get('session_id')
    if not session_id:
        return jsonify({'error': 'No hay carrito activo'}), 404
    
    carrito = obtener_carrito(session_id)

    if producto_id not in carrito['items']:
        return jsonify({'error': 'Producto no encontrado en el carrito'}), 404
    
    #Eliminar producto
    if carrito['items'][producto_id]['cantidad'] > 1:
        carrito['items'][producto_id]['cantidad'] -= 1
    else:
        del carrito['items'][producto_id]

    #Recalcular y guardar
    carrito = calcular_carrito(carrito)
    guardar_carrito(session_id,carrito)

    return jsonify({
        'mensaje': 'Producto eliminado del carrito',
        'carrito': carrito
    })
#Calcular el total de la compra
@user.route('/total-compra')
def total_compra():
    session_id = session.get('session_id')
    if not session_id:
        session['session_id'] = str(uuid4())
        session_id = session['session_id']
    
    carrito = obtener_carrito(session_id)
    total = carrito['total']
    
    return jsonify({'Total de la compra: ': f'${total}'})