import mysql.connector
from PyQt6.QtWidgets import QMessageBox
import qrcode
import os


def conectar_db():
    try:
        conexion =mysql.connector.connect(
            host= "localhost",
            user = "root",
            passwd="12345678",
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
        
def mostrar_productos():
    conexion = conectar_db()
    if conexion:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM Producto")
        registros = cursor.fetchall()
        conexion.close()
        return registros
    return[]

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

def get_next_id(table_name, id_column):
    try:
        cursor = conectar_db().cursor()
        cursor.execute(f"SELECT MAX({id_column}) FROM {table_name}")
        max_id = cursor.fetchone()[0]
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

def obtener_producto_por_nombre(nombre):
    try:
        conexion = conectar_db()
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT ID_Producto, Nombre, Precio, Cantidad, Categoria 
            FROM Producto 
            WHERE Nombre = %s
        """, (nombre,))
        producto = cursor.fetchone()
        conexion.close()
        return producto
    except Exception as e:
        raise Exception(f"Error al obtener producto: {str(e)}")

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
