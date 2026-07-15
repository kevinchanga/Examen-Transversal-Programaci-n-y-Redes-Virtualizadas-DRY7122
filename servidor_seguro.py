# servidor_seguro.py


import os
import sqlite3
import hashlib
from flask import Flask, request, jsonify

# --- CONFIGURACIÓN DE LA BASE DE DATOS (SQLite) ---
DB_NAME = "usuarios_examen.db"

def inicializar_base_de_datos():
    """Crea la tabla de usuarios y carga los integrantes del grupo con hashes seguros."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Crear tabla de usuarios
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_usuario TEXT UNIQUE NOT NULL,
            contrasena_hash TEXT NOT NULL
        )
    ''')
    
    # Integrantes del grupo y sus contraseñas elegidas para el examen
    # (¡Puedes cambiar las contraseñas de esta lista a tu elección!)
    integrantes = {
        "Kevin Chu-Han": "Duoc.2026",
    }
    
    print("\n--- Inicializando base de datos SQLite ---")
    for usuario, clave in integrantes.items():
        # Generar hash SHA-256 de la contraseña
        hash_objeto = hashlib.sha256(clave.encode('utf-8'))
        hash_resultado = hash_objeto.hexdigest()
        
        try:
            # Insertar los usuarios en la base de datos
            cursor.execute('''
                INSERT INTO usuarios (nombre_usuario, contrasena_hash)
                VALUES (?, ?)
            ''', (usuario, hash_resultado))
            print(f"Usuario '{usuario}' insertado con Hash: {hash_resultado[:15]}...")
        except sqlite3.IntegrityError:
            # Evita duplicar usuarios si el script se corre más de una vez
            print(f"El usuario '{usuario}' ya existe en la base de datos.")
            
    conn.commit()
    conn.close()
    print("Base de datos inicializada correctamente.\n")

# --- CONFIGURACIÓN DEL SITIO WEB (Flask) ---
app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <html>
        <head><title>Examen DRY7122</title></head>
        <body style="font-family: Arial; margin: 40px; background-color: #f4f4f9;">
            <h2>Servidor Web Seguro - Examen Transversal DRY7122</h2>
            <p>Bienvenido al portal de autenticación del grupo.</p>
            <p>Para probar las credenciales, use el endpoint API POST a <code>/login</code> con JSON: 
               <br><code>{"usuario": "tu_nombre", "contrasena": "tu_clave"}</code></p>
        </body>
    </html>
    '''

@app.route('/login', methods=['POST'])
def login():
    """Valida los usuarios consultando los hashes en la base de datos SQLite."""
    datos = request.get_json()
    
    if not datos or 'usuario' not in datos or 'contrasena' not in datos:
        return jsonify({"estado": "Error", "mensaje": "Datos insuficientes (requiere 'usuario' y 'contrasena')"}), 400
        
    usuario = datos['usuario'].strip().lower()
    contrasena = datos['contrasena']
    
    # Calcular el hash de la contraseña ingresada para compararla
    hash_objeto = hashlib.sha256(contrasena.encode('utf-8'))
    hash_ingresado = hash_objeto.hexdigest()
    
    # Consultar base de datos
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT contrasena_hash FROM usuarios WHERE nombre_usuario = ?', (usuario,))
    resultado = cursor.fetchone()
    conn.close()
    
    if resultado:
        hash_almacenado = resultado[0]
        if hash_ingresado == hash_almacenado:
            return jsonify({
                "estado": "Éxito", 
                "mensaje": f"Autenticación exitosa. ¡Bienvenido integrante {usuario.capitalize()}!"
            }), 200
        else:
            return jsonify({"estado": "Error", "mensaje": "Contraseña incorrecta."}), 401
    else:
        return jsonify({"estado": "Error", "mensaje": "Usuario no registrado como integrante."}), 404



if __name__ == '__main__':
    
    inicializar_base_de_datos()
    
    
    print("Iniciando servidor Flask en el puerto 7500...")
    app.run(host='0.0.0.0', port=7500, debug=True)
