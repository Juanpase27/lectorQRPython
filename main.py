import sqlite3
import cv2

# Crear base de datos y tabla si no existen
def crear_base_datos():
    conn = sqlite3.connect("qr_lector.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Productos(
            id INTEGER PRIMARY KEY, 
            nombre TEXT NOT NULL, 
            precio REAL NOT NULL, 
            cantidad INTEGER NOT NULL
        );
    """)
    conn.commit()
    conn.close()

# Agregar producto a la base de datos
def agregar_producto(id, nombre, precio, cantidad):
    conn = sqlite3.connect("qr_lector.db")
    cursor = conn.cursor()
    
    # Verificar si el producto ya existe
    cursor.execute("SELECT cantidad FROM Productos WHERE id = ?", (id,))
    resultado = cursor.fetchone()
    
    if resultado:
        nueva_cantidad = resultado[0] + cantidad
        cursor.execute("UPDATE Productos SET cantidad = ? WHERE id = ?", (nueva_cantidad, id))
        print(f"🔄 Producto '{nombre}' actualizado. Nueva cantidad: {nueva_cantidad}")
    else:
        cursor.execute("INSERT INTO Productos (id, nombre, precio, cantidad) VALUES (?, ?, ?, ?)",
                       (id, nombre, precio, cantidad))
        print(f"✅ Producto '{nombre}' agregado con éxito.")
    
    conn.commit()
    conn.close()

# Leer código QR e insertar en la base de datos
def leer_qr_y_guardar(ruta_qr):
    img = cv2.imread(ruta_qr)
    detector = cv2.QRCodeDetector()
    data, _, _ = detector.detectAndDecode(img)
    
    if data:
        try:
            # Suponiendo que el QR tiene el formato "ID,Nombre,Precio,Cantidad"
            id, nombre, precio, cantidad = data.split(',')
            agregar_producto(int(id), nombre, float(precio), int(cantidad))
        except ValueError:
            print("⚠ Error: El formato del QR no es válido.")
    else:
        print("⚠ No se pudo leer el código QR.")

# Consultar todos los productos en la base de datos
def consultar_productos():
    conn = sqlite3.connect("qr_lector.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Productos")
    productos = cursor.fetchall()
    
    if productos:
        print("\n📋 Listado de Productos:")
        for id, nombre, precio, cantidad in productos:
            print(f"🆔 ID: {id} | 📌 Nombre: {nombre} | 💲 Precio: {precio} | 📦 Cantidad: {cantidad}")
    else:
        print("\n📭 No hay productos en la base de datos.")
    
    conn.close()

# Crear la base de datos si no existe
crear_base_datos()

# 📷 Leer QR y guardar información
leer_qr_y_guardar('prbQR.png')

# 🔍 Consultar productos para verificar la inserción
consultar_productos()
