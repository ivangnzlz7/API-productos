from flask import Flask, jsonify
from routes.user import user
from dotenv import load_dotenv
import os
from flask_swagger_ui import get_swaggerui_blueprint

#Carga variable de entorno
load_dotenv()

# Configuración de Swagger
SWAGGER_URL = '/api/docs'
API_URL = '/swagger.json'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': "Mi API"}
)


app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
app.register_blueprint(user, url_prefix='/api/user')
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

@app.route('/')
def home():
    return 'Bienvenido a la tienda'

@app.route('/swagger.json')
def swagger():
    return jsonify({
        "swagger": "2.0",
        "info": {
            "title": "Mi API",
            "description": "Documentación de mi API",
            "version": "1.0.0"
        },
        "paths": {
            "/api/user/products": {
                "get": {
                    "summary": "Mostrar todos los productos",
                    "responses": {
                        "200": {
                            "description": "OK"
                        }
                    }
                }
            },
            "/api/user/carrito": {
                "get": {
                    "summary": "Mostrar el carrito",
                    "responses": {
                        "200": {
                            "description": "OK"
                        }
                    }
                }
            },
            "/api/user/agregar/{producto_id}": {
                "post": {
                    "summary": "Agregar producto al carrito",
                    "parameters": [
                        {
                            "name": "producto_id",
                            "in": "path",
                            "description": "ID del producto",
                            "required": True,
                            "type": "string"
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "OK"
                        },
                        "404": {
                            "description": "Producto No Encontrado"
                        }
                    
                    }
                }
            },
            "/api/user/total-compra": {
                "get": {
                "summary": "Total De La Compra",
                "responses": {
                    "200": {
                        "description": "OK"
                    }
                }
                }
            },
            "/api/user/eliminar/{producto_id}": {
                "delete": {
                "summary": "Eliminar un producto",
                "parameters": [
                        {
                            "name": "producto_id",
                            "in": "path",
                            "description": "ID del producto a eliminar",
                            "required": True,
                            "type": "string"
                        }
                    ],
                "responses": {
                    "200": {
                        "description": "OK"
                    },
                    "404": {
                        "description": "Producto No Encontrado En El Carrito"
                    }
                }
                }
            }
        }
    })

