import sqlite3
import os
import cv2

def crear_base_datos():
    if not os.path.exists("qr_lector.db"):  # Verificar si el archivo de la BD existe
        print("\U0001F4C2 Creando base de datos...")
    
    conn = sqlite3.connect("qr_lector.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Productos(
            id INTEGER PRIMARY KEY, 
            nombre TEXT NOT NULL, 
            precio REAL NOT NULL, 
            cantidad INTEGER NOT NULL,
            estado TEXT NOT NULL DEFAULT 'Activo'
        );
    """)
    
    conn.commit()
    conn.close()

def agregar_producto(id, nombre, precio, cantidad, estado="Activo"):
    conn = sqlite3.connect("qr_lector.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT cantidad, estado FROM Productos WHERE id = ?", (id,))
    resultado = cursor.fetchone()
    
    if resultado:
        print(f"\U0001F504 Producto '{nombre}' ya existe.")
        print(f"\U0001F197 ID: {id} | \U0001F4CC Nombre: {nombre} | \U0001F4B2 Precio: {precio} | \U0001F4E6 Cantidad: {cantidad} | \U0001F534 Estado: {estado}")
    else:
        cursor.execute("INSERT INTO Productos (id, nombre, precio, cantidad, estado) VALUES (?, ?, ?, ?, 'Activo')",
                       (id, nombre, precio, cantidad))
        print(f"\u2705 Producto '{nombre}' agregado con éxito.")
    
    conn.commit()
    conn.close()

def actualizar_producto(id):
    conn = sqlite3.connect("qr_lector.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT cantidad FROM Productos WHERE id = ?", (id,))
    resultado = cursor.fetchone()
    
    if resultado:
        cantidad_actual = resultado[0]
        accion = input("¿Desea agregar (A) o eliminar (E) cantidad?: ").strip().upper()
        if accion == 'A':
            cantidad = int(input("Ingrese la cantidad a agregar: "))
            nueva_cantidad = cantidad_actual + cantidad
        elif accion == 'E':
            cantidad = int(input("Ingrese la cantidad a eliminar: "))
            nueva_cantidad = max(0, cantidad_actual - cantidad)
        else:
            print("\u26A0 Opción inválida. No se realizaron cambios.")
            return
        
        cursor.execute("UPDATE Productos SET cantidad = ? WHERE id = ?", (nueva_cantidad, id))
        print("\u2705 Producto actualizado correctamente.")
    else:
        print("\u26A0 No se encontró el producto.")
    
    conn.commit()
    conn.close()

def cambiar_estado_producto(id, nuevo_estado):
    conn = sqlite3.connect("qr_lector.db")
    cursor = conn.cursor()
    
    cursor.execute("UPDATE Productos SET estado = ? WHERE id = ?", (nuevo_estado, id))
    
    if cursor.rowcount > 0:
        print(f"\u2705 Producto con ID {id} cambiado a estado '{nuevo_estado}' correctamente.")
    else:
        print("\u26A0 No se encontró el producto.")
    
    conn.commit()
    conn.close()

def leer_qr_y_guardar(ruta_qr, accion):
    img = cv2.imread(ruta_qr)
    detector = cv2.QRCodeDetector()
    data, _, _ = detector.detectAndDecode(img)
    
    if data:
        try:
            id, nombre, precio, cantidad = data.split(',')
            id, precio, cantidad = int(id), float(precio), int(cantidad)
            
            if accion == 'Crear':
                agregar_producto(id, nombre, precio, cantidad)
            elif accion == 'Actualizar':
                actualizar_producto(id)
        except ValueError:
            print("\u26A0 Error: El formato del QR no es válido.")
    else:
        print("\u26A0 No se pudo leer el código QR.")

def consultar_productos():
    conn = sqlite3.connect("qr_lector.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Productos")
    productos = cursor.fetchall()
    
    if productos:
        print("\n\U0001F4CB Listado de Productos:")
        for id, nombre, precio, cantidad, estado in productos:
            print(f"\U0001F194 ID: {id} | \U0001F4CC Nombre: {nombre} | \U0001F4B2 Precio: {precio} | \U0001F4E6 Cantidad: {cantidad} | \U0001F518 Estado: {estado}")
    else:
        print("\n\U0001F4ED No hay productos en la base de datos.")
    
    conn.close()
    
def consultar_producto_por_id(id):
    conn = sqlite3.connect("qr_lector.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Productos WHERE id = ?", (id,))
    producto = cursor.fetchone()
    
    if producto:
        id, nombre, precio, cantidad, estado = producto
        print(f"\n \U0001F50D Producto encontrado:")
        print(f"\U0001F194 ID: {id} | \U0001F4CC Nombre: {nombre} | \U0001F4B2 Precio: {precio} | \U0001F4E6 Cantidad: {cantidad} | \U0001F518 Estado: {estado}")
    else:
        print("\u26A0 No se encontró un producto con ese ID.")
    
    conn.close()

def menu():
    while True:
        print("\n\U0001F4CC Menú de Opciones:")
        print("\U00000031\U000020E3 Crear Producto")
        print("\U00000032\U000020E3 Actualizar Producto")
        print("\U00000033\U000020E3 Consultar Productos")
        print("\U00000034\U000020E3 Consultar Producto por ID")
        print("\U00000035\U000020E3 Deshabilitar Producto")
        print("\U00000036\U000020E3 Reactivar Producto")
        print("\U00000030\U000020E3 Salir")
        
        opcion = input("🔹 Seleccione una opción: ")
        
        if opcion == '1':
            leer_qr_y_guardar('prbQR.png', 'Crear')
        elif opcion == '2':
            try:
                id_producto = int(input("Ingrese el ID del producto a actualizar: "))
                actualizar_producto(id_producto)
            except ValueError:
                print("\u26A0 Entrada inválida. Ingrese un número válido.")
        elif opcion == '3':
            consultar_productos()
        elif opcion == '4':
            try:
                id_producto = int(input("Ingrese el ID del producto a consultar: "))
                consultar_producto_por_id(id_producto)
            except ValueError:
                print("\u26A0 Entrada inválida. Ingrese un número válido.")
        elif opcion == '5':
            try:
                id_producto = int(input("Ingrese el ID del producto a deshabilitar: "))
                cambiar_estado_producto(id_producto, 'Deshabilitado')
            except ValueError:
                print("\u26A0 Entrada inválida. Ingrese un número válido.")
        elif opcion == '6':
            try:
                id_producto = int(input("Ingrese el ID del producto a reactivar: "))
                cambiar_estado_producto(id_producto, 'Activo')
            except ValueError:
                print("\u26A0 Entrada inválida. Ingrese un número válido.")
        elif opcion == '0':
            print("\U0001F44B Saliendo...")
            break
        else:
            print("\u26A0 Opción inválida, intente de nuevo.")

# Ejecutar
crear_base_datos()
menu()
