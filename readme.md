# QR Lector y Gestor de Productos

Este proyecto es una aplicación de consola en Python que permite gestionar una base de datos de productos utilizando códigos QR. La aplicación permite crear, actualizar, consultar y deshabilitar productos en una base de datos SQLite.

## Requisitos

Para ejecutar este proyecto, necesitarás tener instalado Python y las siguientes bibliotecas:

- `sqlite3`: Para manejar la base de datos.
- `opencv-python`: Para leer códigos QR.

## Instalación

### 1. Clonar el Repositorio

Clona el repositorio en tu máquina local:

```bash
git clone https://github.com/Juanpase27/lectorQRPython.git
```

### 2. Crear un Entorno Virtual

Es recomendable crear un entorno virtual para gestionar las dependencias del proyecto. Puedes hacerlo con los siguientes comandos:

```bash
# Crear un entorno virtual
python -m venv venv

# Activar el entorno virtual
# En Windows
venv\Scripts\activate
# En Linux o MacOS
source venv/bin/activate
```

### 3. Instalar Dependencias

Instala las bibliotecas necesarias usando `pip`:

```bash
pip install opencv-python
```

## Uso
**Para ejecutar el proyecto se recomienda usar el entorno virtual previamente dicho y utilizar el comando**
```bash
py <nombre_del_archivo>.py
```

1. **Crear código QR**: Para realizar pruebas de forma correcta en el sistema se incorpora un módulo para generar códigos QR a partir de texto plano. Para hacer uso de este módulo se debe de ejecutar el archivo `crear.py`, en dicho archivo se pedirá que se registre la información que contendrá el QR, para ello se debe de generar un texto similar al siguiente: "4,Mandarinas,0.2,400", siendo su estructura: ID,Nombre,Precio,Cantidad 
2. **Crear la base de datos**: Se debe de usar el archivo `main.py` . Al ejecutar el programa, se creará automáticamente una base de datos llamada `qr_lector.db` si no existe.
3. **Menú de Opciones**: El programa presenta un menú interactivo donde puedes elegir entre las siguientes opciones:
   - Crear Producto
   - Actualizar Producto
   - Consultar Productos
   - Consultar Producto por ID
   - Deshabilitar Producto
   - Reactivar Producto
   - Salir

4. **Leer Códigos QR**: Para crear o actualizar un producto, el programa leerá un código QR de un archivo de imagen. Asegúrate de que el archivo `prbQR.png` se halla generado en el paso 1.

## Funciones Principales

- `crear_base_datos()`: Crea la base de datos y la tabla si no existen.
- `agregar_producto(id, nombre, precio, cantidad, estado)`: Agrega un nuevo producto a la base de datos.
- `actualizar_producto(id)`: Actualiza la cantidad de un producto existente.
- `cambiar_estado_producto(id, nuevo_estado)`: Cambia el estado de un producto (Activo/Deshabilitado).
- `leer_qr_y_guardar(ruta_qr, accion)`: Lee un código QR y guarda o actualiza un producto basado en la información del código.
- `consultar_productos()`: Muestra todos los productos en la base de datos.
- `consultar_producto_por_id(id)`: Muestra la información de un producto específico por su ID.

## Contribuciones

Las contribuciones son bienvenidas. Si deseas contribuir, por favor abre un issue o envía un pull request.

