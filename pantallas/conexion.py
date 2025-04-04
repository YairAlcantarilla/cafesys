import mysql.connector
from PyQt6.QtWidgets import QMessageBox
import qrcode
import os


def conectar_db():
    try:
        conexion =mysql.connector.connect(
            host= "localhost",
            user = "root",
            passwd="1234",
            database="tienda"
        )
        return conexion
    except mysql.connector.Error as e:
        QMessageBox.information("Error", f"No se pudo conectar a la base de datos:{e}")
        return None
        
#Funcion para insertar en bd
def insertar_dato(tabla, datos):
    conexion = conectar_db()
    if conexion:
        cursor = conexion.cursor()
        columnas= ",".join(datos.keys())
        valores=",".join(["%s"]*len(datos))
        sql=f"INSERT INTO {tabla}({columnas}) VALUES ({valores})"
        cursor.execute(sql, list(datos.values()))
        conexion.commit()
        conexion.close()
        QMessageBox.information(None, "Éxito", "Producto agregado correctamente.")


        
#Funcion para eliminar
def eliminar_dato(tabla, columna_id, valor_id):
    conexion = conectar_db()
    if conexion:
        cursor = conexion.cursor()
        sql=f"DELETE FROM {tabla} WHERE {columna_id}=%s"
        cursor.execute(sql, (valor_id))
        conexion.commit()
        conexion.close()
        
#Funcion para modificar dato
def modificar_dato(tabla, columna_id, valor_id, dato_nuevo):
    conexion = conectar_db()
    if conexion:
        cursor = conexion.cursor()
        set_clause = ",".join([f"{col} = %s" for col in dato_nuevo.keys()])
        sql = f"UPDATE {tabla} SET {set_clause} WHERE {columna_id} = %s"
        valores=list(dato_nuevo.values())+[valor_id]
        cursor.execute()
        conexion.commit()
        cursor.close()
        
def mostrar_productos(ocultar_especiales=True):
    try:
        conexion = conectar_db()
        cursor = conexion.cursor()
        
        if ocultar_especiales:
            # Query que excluye productos con "Comida" o "Bebida" en el nombre
            query = """
                SELECT * FROM Producto 
                WHERE Nombre NOT LIKE '%Comida%' 
                AND Nombre NOT LIKE '%Bebida%'
                ORDER BY Nombre
            """
        else:
            # Query original que muestra todos los productos
            query = "SELECT * FROM Producto ORDER BY Nombre"
            
        cursor.execute(query)
        productos = cursor.fetchall()
        cursor.close()
        conexion.close()
        return productos
        
    except Exception as e:
        print(f"Error al mostrar productos: {e}")
        return []

def obtener_categorias():
    try:
        conexion = conectar_db() 
        if conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT DISTINCT Categoria FROM Producto")
            categorias = cursor.fetchall()
            conexion.close()
            return categorias
        return []
    except Exception as e:
        raise Exception(f"Error al obtener categorías: {str(e)}")

def mostrar_usuarios():
    conexion = conectar_db()
    if conexion:
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT id_usuario, contrasenna, nombre, telefono, Direccion, ID_Puesto FROM usuario")
            registros = cursor.fetchall()
            return registros
        except Exception as e:
            raise Exception(f"Error al obtener usuarios: {str(e)}")
        finally:
            conexion.close()
    return []

def insertar_usuario(datos):
    conexion = conectar_db()
    if conexion:
        try:
            cursor = conexion.cursor()
            # No incluimos el id_usuario ya que lo generará el trigger
            sql = """INSERT INTO usuario (contrasenna, nombre, telefono, Direccion, ID_Puesto) 
                     VALUES (%s, %s, %s, %s, %s)"""
            valores = (
                datos['contrasenna'],
                datos['nombre'],
                datos['telefono'],
                datos['Direccion'],
                datos['ID_Puesto']
            )
            cursor.execute(sql, valores)
            conexion.commit()
        except Exception as e:
            raise Exception(f"Error al insertar usuario: {str(e)}")
        finally:
            conexion.close()

"""def get_next_id(table_name, id_column):
    try:
        cursor = conectar_db().cursor()
        cursor.execute(f"SELECT MAX({id_column}) FROM {table_name}")
        max_id = cursor.fetchone()[0]
        return 1 if max_id is None else max_id + 1
    except Exception as e:
        raise Exception(f"Error getting next ID: {str(e)}")
"""
def get_next_id(table_name, id_column):
    try:
        conn = conectar_db()  # Abre la conexión correctamente
        if conn is None:
            raise Exception("Error: No se pudo establecer la conexión a la base de datos")
        
        cursor = conn.cursor()
        cursor.execute(f"SELECT MAX({id_column}) FROM {table_name}")
        max_id = cursor.fetchone()[0]
        
        cursor.close()  # Cierra el cursor
        conn.close()    # Cierra la conexión
        
        return 1 if max_id is None else max_id + 1

    except Exception as e:
        raise Exception(f"Error getting next ID: {str(e)}")

def eliminar_producto(nombre_producto):
    try:
        conexion = conectar_db()
        cursor = conexion.cursor()
        
        # SQL para eliminar el producto
        sql = "DELETE FROM Producto WHERE Nombre = %s"
        cursor.execute(sql, (nombre_producto,))
        
        conexion.commit()
        cursor.close()
        conexion.close()
        
        return True
    except Exception as e:
        raise Exception(f"Error al eliminar el producto: {str(e)}")

def obtener_producto_por_nombre(nombre, ocultar_especiales=True):
    try:
        conexion = conectar_db()
        cursor = conexion.cursor()
        
        if ocultar_especiales:
            query = """
                SELECT * FROM Producto 
                WHERE Nombre = %s 
                AND Nombre NOT LIKE '%Comida%'
                AND Nombre NOT LIKE '%Bebida%'
            """
        else:
            query = "SELECT * FROM Producto WHERE Nombre = %s"
            
        cursor.execute(query, (nombre,))
        producto = cursor.fetchone()
        cursor.close()
        conexion.close()
        return producto
        
    except Exception as e:
        print(f"Error al obtener producto: {e}")
        return None

def actualizar_producto(nombre_original, datos):
    try:
        conexion = conectar_db()
        cursor = conexion.cursor()
        sql = """UPDATE Producto 
                 SET Nombre = %s, Precio = %s, Cantidad = %s, Categoria = %s 
                 WHERE Nombre = %s"""
        valores = (
            datos['Nombre'],
            datos['Precio'],
            datos['Cantidad'],
            datos['Categoria'],
            nombre_original
        )
        cursor.execute(sql, valores)
        conexion.commit()
        conexion.close()
    except Exception as e:
        raise Exception (f"Error al actualizar producto: {str(e)}")

def eliminar_usuario(id_usuario):
    try:
        conexion = conectar_db()
        with conexion.cursor() as cursor:
            consulta = "DELETE FROM usuario WHERE ID_usuario = %s"
            cursor.execute(consulta, (id_usuario,))
        conexion.commit()
    finally:
        conexion.close()

def verificar_credenciales(ID_usuario, contrasenna):
    try:
        conexion = conectar_db()
        cursor = conexion.cursor()
        
        # Consulta modificada para seleccionar los campos específicos
        consulta = """
            SELECT ID_usuario, Nombre, ID_Puesto 
            FROM usuario 
            WHERE ID_usuario = %s AND contrasenna = %s
        """
        cursor.execute(consulta, (ID_usuario, contrasenna))
        resultado = cursor.fetchone()
        
        # Agregar print para debug
        print(f"Consulta SQL: {consulta}")
        print(f"Parámetros: ID_usuario={ID_usuario}, contraseña={contrasenna}")
        print(f"Resultado de la consulta: {resultado}")
        
        cursor.close()
        conexion.close()
        
        return resultado
        
    except Exception as e:
        print(f"Error en verificar_credenciales: {e}")
        return None

def generar_qr_usuario(id_usuario, contrasenna):
    try:
        # Crear directorio si no existe
        qr_dir = "./qr_codes"
        if not os.path.exists(qr_dir):
            os.makedirs(qr_dir)

        # Crear los datos en formato "usuario:contraseña"
        datos = f"{id_usuario}:{contrasenna}"
        
        # Generar QR
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(datos)
        qr.make(fit=True)

        # Crear imagen
        qr_image = qr.make_image(fill_color="black", back_color="white")
        
        # Guardar imagen
        qr_path = f"{qr_dir}/usuario_{id_usuario}.png"
        qr_image.save(qr_path)
        return qr_path
        
    except Exception as e:
        print(f"Error al generar QR: {e}")
        return None

def obtener_datos_usuario(ID_usuario):
    try:
        conexion = conectar_db()
        cursor = conexion.cursor()
        
        # Consulta para obtener los datos necesarios
        consulta = """
            SELECT ID_usuario, contrasenna, Nombre, ID_Puesto 
            FROM usuario 
            WHERE ID_usuario = %s
        """
        cursor.execute(consulta, (ID_usuario,))
        resultado = cursor.fetchone()
        
        cursor.close()
        conexion.close()
        
        return resultado
        
    except Exception as e:
        print(f"Error al obtener datos del usuario: {e}")
        return None


def agregar_combo(nombre, producto1, producto2, precio):
    try:
        conexion = conectar_db()
        cursor = conexion.cursor()

        # Obtener los IDs de los productos seleccionados
        cursor.execute("SELECT ID_producto FROM producto WHERE Nombre = %s", (producto1,))
        id_producto1 = cursor.fetchone()

        cursor.execute("SELECT ID_producto FROM producto WHERE Nombre = %s", (producto2,))
        id_producto2 = cursor.fetchone()

        if not id_producto1 or not id_producto2:
            raise Exception("Uno o ambos productos no existen en la base de datos.")

        # Insertar el combo en la tabla 'combos'
        cursor.execute("""
            INSERT INTO combos (Nombre, Producto1_ID, Producto2_ID, Precio)
            VALUES (%s, %s, %s, %s)
        """, (nombre, id_producto1[0], id_producto2[0], precio))

        conexion.commit()
        cursor.close()
        conexion.close()
    except Exception as e:
        raise Exception(f"Error al agregar el combo: {str(e)}")


def mostrar_combos():
    try:
        
        conexion = conectar_db()
        cursor = conexion.cursor()

        consulta = """
        SELECT c.Nombre, p1.Nombre AS Producto1, p2.Nombre AS Producto2, c.Precio
        FROM combos c
        JOIN producto p1 ON c.Producto1_ID = p1.ID_producto
        JOIN producto p2 ON c.Producto2_ID = p2.ID_producto
        """
        cursor.execute(consulta)
        combos = cursor.fetchall()

        conexion.close()
        return combos

    except mysql.connector.Error as e:
        print(f"Error al obtener los combos: {e}")
        return []


from mysql.connector import Error  # Asegúrate de importar Error correctamente


def eliminar_combo(nombre_combo):
    try:
        conexion = conectar_db()
        cursor= conexion.cursor()
        if conexion.is_connected():
            cursor = conexion.cursor()

            # Verifica si el combo existe antes de intentar eliminarlo
            check_query = "SELECT COUNT(*) FROM combos WHERE nombre_combo = %s"
            cursor.execute(check_query, (nombre_combo,))
            result = cursor.fetchone()
            if result[0] == 0:
                print(f"Combo '{nombre_combo}' no encontrado.")
                return

            # SQL para eliminar el combo
            query = "DELETE FROM combos WHERE nombre_combo = %s"
            cursor.execute(query, (nombre_combo,))
            
            # Confirmamos que la operación fue exitosa
            conexion.commit()

            # Verificamos cuántas filas fueron afectadas
            if cursor.rowcount > 0:
                print(f"Combo '{nombre_combo}' eliminado correctamente.")
            else:
                print(f"Combo '{nombre_combo}' no encontrado.")

    except Error as e:
        print(f"Error al eliminar combo: {e}")
        raise Exception(f"Error al eliminar combo: {e}")
    finally:
        # Cerramos la conexión
        if conexion.is_connected():
            cursor.close()
            conexion.close()
def obtener_precio_producto(nombre_producto):
    try:
        connection = conectar_db()
        cursor = connection.cursor()
        
        # Cambiar 'productos' a 'Producto'
        cursor.execute("SELECT Precio FROM Producto WHERE Nombre = %s", (nombre_producto,))
        resultado = cursor.fetchone()
        
        if resultado:
            return resultado[0]
        return 0.0
        
    except Exception as e:
        print(f"Error al obtener precio: {e}")
        return 0.0
    finally:
        if connection:
            connection.close()

def insertar_venta(datos_venta):
    connection = None
    try:
        connection = conectar_db()
        cursor = connection.cursor()
        
        # Define SQL statement with exact column names
        sql = """
            INSERT INTO ventas (
                producto,
                fecha,
                cantidad,
                precio_total,
                forma_pago,
                id_usuario
            ) VALUES (%s, %s, %s, %s, %s, %s)
        """
        
        # Create tuple of values in the same order
        params = (
            datos_venta['producto'],
            datos_venta['fecha'],
            datos_venta['cantidad'],
            float(datos_venta['precio_total']),  # Convert Decimal to float
            datos_venta['forma_pago'],
            datos_venta['id_usuario']
        )
        
        # Debug information
        print("\nSQL Query:")
        print(sql)
        print("\nParámetros SQL:")
        print(f"Cantidad de parámetros: {len(params)}")
        for i, param in enumerate(params):
            print(f"Param {i+1}: {param} ({type(param)})")
            
        # Execute with parameterized query
        cursor.execute(sql, params)
        connection.commit()
        return True
        
    except Exception as e:
        print(f"\nError detallado en insertar_venta:")
        print(f"Tipo de error: {type(e)}")
        print(f"Mensaje de error: {str(e)}")
        raise e
    finally:
        if connection:
            connection.close()

def obtener_usuario_activo():
    """Obtiene un ID de usuario válido de la base de datos"""
    connection = None
    try:
        connection = conectar_db()
        cursor = connection.cursor()
        
        # Get first available user ID
        cursor.execute("SELECT ID_usuario FROM usuario LIMIT 1")
        result = cursor.fetchone()
        
        if result:
            return result[0]
        return None
        
    except Exception as e:
        print(f"Error al obtener usuario: {e}")
        return None
    finally:
        if connection:
            connection.close()
