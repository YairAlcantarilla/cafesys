import mysql.connector
from PyQt6.QtWidgets import QMessageBox
import qrcode
import os
from PIL import Image, ImageDraw, ImageFont


def obtener_credenciales_db():
    return {
        'host': "localhost",
        'user': "root",
        'passwd': "894388",
        'database': "tienda"
    }


def conectar_db():
    try:
        credenciales = obtener_credenciales_db()
        conexion = mysql.connector.connect(
            host=credenciales['host'],
            user=credenciales['user'],
            passwd=credenciales['passwd'],
            database=credenciales['database']
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
            query = """
                SELECT * FROM Producto 
                WHERE oculto = 0
                AND Nombre NOT LIKE '%Comida%' 
                AND Nombre NOT LIKE '%Bebida%'
                ORDER BY Nombre
            """
        else:
            query = """
                SELECT * FROM Producto 
                WHERE oculto = 0 
                ORDER BY Nombre
            """
            
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
            cursor.execute("SELECT id_usuario, contrasenna, nombre, correo, Direccion, ID_Puesto FROM usuario")
            registros = cursor.fetchall()
            return registros
        except Exception as e:
            raise Exception(f"Error al obtener usuarios: {str(e)}")
        finally:
            conexion.close()
    return []

def mostrar_usuarios_activos():
    """Muestra solo los usuarios que no están ocultos"""
    try:
        conexion = conectar_db()
        if conexion:
            cursor = conexion.cursor()
            cursor.execute("""
                SELECT id_usuario, contrasenna, nombre, correo, Direccion, ID_Puesto 
                FROM usuario 
                WHERE oculto = 0
            """)
            usuarios = cursor.fetchall()
            cursor.close()
            conexion.close()
            return usuarios
    except Exception as e:
        raise Exception(f"Error al obtener usuarios activos: {str(e)}")
    return []

def ocultar_usuario(id_usuario):
    """Marca un usuario como oculto en lugar de eliminarlo"""
    try:
        conexion = conectar_db()
        if conexion:
            cursor = conexion.cursor()
            cursor.execute("UPDATE usuario SET oculto = 1 WHERE ID_usuario = %s", (id_usuario,))
            conexion.commit()
            cursor.close()
            conexion.close()
    except Exception as e:
        raise Exception(f"Error al ocultar usuario: {str(e)}")

def contar_administradores_activos():
    """Cuenta cuántos administradores activos hay en el sistema"""
    try:
        conexion = conectar_db()
        if conexion:
            cursor = conexion.cursor()
            cursor.execute("""
                SELECT COUNT(*) 
                FROM usuario 
                WHERE ID_Puesto = 1 AND oculto = 0
            """)
            count = cursor.fetchone()[0]
            cursor.close()
            conexion.close()
            return count
    except Exception as e:
        raise Exception(f"Error al contar administradores: {str(e)}")
    return 0

def insertar_usuario(datos):
    conexion = conectar_db()
    if conexion:
        try:
            cursor = conexion.cursor()
            # No incluimos el id_usuario ya que lo generará el trigger
            sql = """INSERT INTO usuario (contrasenna, nombre, correo, Direccion, ID_Puesto) 
                     VALUES (%s, %s, %s, %s, %s)"""
            valores = (
                datos['contrasenna'],
                datos['nombre'],
                datos['correo'],
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
        
        consulta = """
            SELECT ID_usuario, Nombre, ID_Puesto 
            FROM usuario 
            WHERE ID_usuario = %s 
            AND contrasenna = %s 
            AND oculto = 0
        """
        cursor.execute(consulta, (ID_usuario, contrasenna))
        resultado = cursor.fetchone()
        
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
        
        consulta = """
            SELECT ID_usuario, contrasenna, Nombre, correo, ID_Puesto 
            FROM usuario 
            WHERE ID_usuario = %s AND oculto = 0
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
    """Muestra solo los combos que no están ocultos"""
    try:
        conexion = conectar_db()
        if not conexion:
            raise Exception("No se pudo establecer conexión con la base de datos")
            
        cursor = conexion.cursor()
        
        consulta = """
        SELECT c.Nombre, p1.Nombre AS Producto1, p2.Nombre AS Producto2, c.Precio
        FROM combos c
        JOIN producto p1 ON c.Producto1_ID = p1.ID_producto
        JOIN producto p2 ON c.Producto2_ID = p2.ID_producto
        WHERE c.oculto = 0
        ORDER BY c.Nombre
        """
        
        cursor.execute(consulta)
        combos = cursor.fetchall()
        
        cursor.close()
        conexion.close()
        return combos
        
    except Exception as e:
        print(f"Error en mostrar_combos: {e}")
        return []

def ocultar_combo(nombre_combo):
    """Marca un combo como oculto en lugar de eliminarlo"""
    try:
        conexion = conectar_db()
        cursor = conexion.cursor()
        if conexion.is_connected():
            # Verifica si el combo existe
            check_query = "SELECT COUNT(*) FROM combos WHERE Nombre = %s AND oculto = 0"
            cursor.execute(check_query, (nombre_combo,))
            result = cursor.fetchone()
            if result[0] == 0:
                raise Exception(f"Combo '{nombre_combo}' no encontrado o ya está oculto.")

            # SQL para ocultar el combo
            query = "UPDATE combos SET oculto = 1 WHERE Nombre = %s"
            cursor.execute(query, (nombre_combo,))
            
            conexion.commit()

    except Error as e:
        raise Exception(f"Error al ocultar combo: {str(e)}")
    finally:
        if conexion and conexion.is_connected():
            cursor.close()
            conexion.close()

from mysql.connector import Error  # Asegúrate de importar Error correctamente


def eliminar_combo(nombre_combo):
    try:
        conexion = conectar_db()
        cursor = conexion.cursor()
        if conexion.is_connected():
            # Verifica si el combo existe antes de intentar eliminarlo
            check_query = "SELECT COUNT(*) FROM combos WHERE Nombre = %s"
            cursor.execute(check_query, (nombre_combo,))
            result = cursor.fetchone()
            if result[0] == 0:
                print(f"Combo '{nombre_combo}' no encontrado.")
                return

            # SQL para eliminar el combo
            query = "DELETE FROM combos WHERE Nombre = %s"
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
        if conexion and conexion.is_connected():
            cursor.close()
            conexion.close()

def obtener_precio_producto(nombre_producto):
    try:
        connection = conectar_db()
        cursor = connection.cursor()
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
        params = (
            datos_venta['producto'],
            datos_venta['fecha'],
            datos_venta['cantidad'],
            float(datos_venta['precio_total']),
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

def generar_gafete(datos_usuario, qr_path):
    try:
        # Cargar la imagen de plantilla
        gafete = Image.open('imagenes/plantilla_gafete.png')
        draw = ImageDraw.Draw(gafete)
        
        # Cargar fuente
        try:
            font_name = ImageFont.truetype("arial.ttf", 30)
            font_id = ImageFont.truetype("arial.ttf", 24)
        except:
            font_name = ImageFont.load_default()
            font_id = ImageFont.load_default()

        # Configurar posiciones
        NOMBRE_POS = (243, 708)  # (x, y) para el nombre
        ID_POS = (250, 783)      # (x, y) para el ID
        QR_POS = (123, 284)      # (x, y) para el QR
        QR_SIZE = (338, 338)     # Tamaño del QR

        # Agregar nombre y ID sin etiquetas
        draw.text(NOMBRE_POS, f"{datos_usuario[2]}", fill='black', font=font_name)
        draw.text(ID_POS, f"{datos_usuario[0]}", fill='black', font=font_id)

        # Agregar QR
        qr_img = Image.open(qr_path)
        qr_img = qr_img.resize(QR_SIZE)
        gafete.paste(qr_img, QR_POS)

        # Crear directorio si no existe
        gafete_dir = "./gafetes"
        if not os.path.exists(gafete_dir):
            os.makedirs(gafete_dir)

        # Guardar gafete
        gafete_path = f"{gafete_dir}/gafete_{datos_usuario[0]}.png"
        gafete.save(gafete_path)
        
        return gafete_path

    except Exception as e:
        print(f"Error al generar gafete: {e}")
        return None

def obtener_combo_por_nombre(nombre_combo):
    try:
        conexion = conectar_db() 
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT id, nombre, precio 
            FROM combos 
            WHERE nombre = %s AND oculto = 0
        """, (nombre_combo,))
        combo = cursor.fetchone()

        conexion.close()
        return combo
    except Exception as e:
        print(f"Error al obtener combo: {e}")
        return None

def cargar_datos_combo(nombre_combo):
    try:
        conexion = conectar_db()
        cursor = conexion.cursor()

        consulta = """
            SELECT c.Nombre, p1.Nombre AS Producto1, p2.Nombre AS Producto2, c.Precio
            FROM combos c
            JOIN producto p1 ON c.Producto1_ID = p1.ID_producto
            JOIN producto p2 ON c.Producto2_ID = p2.ID_producto
            WHERE c.Nombre = %s AND c.oculto = 0
        """
        
        cursor.execute(consulta, (nombre_combo,))
        combo = cursor.fetchone()
        cursor.close()
        conexion.close()
        
        return combo
        
    except Exception as e:
        print(f"Error al cargar los datos del combo: {str(e)}")
        return None

def obtener_descuentos():
    """Obtiene solo los descuentos activos con información del producto"""
    try:
        conexion = conectar_db()
        cursor = conexion.cursor()
        
        cursor.execute("""
            SELECT d.ID_descuento, d.Porcentaje, d.Producto_ID, d.Precio_final
            FROM descuentos d
            JOIN producto p ON d.Producto_ID = p.ID_producto
            WHERE d.oculto = 0
            ORDER BY d.ID_descuento
        """)
        
        descuentos = cursor.fetchall()
        cursor.close()
        conexion.close()
        return descuentos
    except Exception as e:
        print(f"Error al obtener descuentos: {e}")
        return []

def agregar_descuento(producto, descuento, precio_final):
    conexion = conectar_db()
    cursor = conexion.cursor()
    try:
        # First get the product ID
        cursor.execute("SELECT ID_producto FROM producto WHERE Nombre = %s", (producto,))
        resultado = cursor.fetchone()
        if not resultado:
            raise Exception("Producto no encontrado")
        producto_id = resultado[0]

        # Then insert the discount with the product ID
        cursor.execute("""
            INSERT INTO descuentos (Porcentaje, Producto_ID, Precio_final) 
            VALUES (%s, %s, %s)
        """, (descuento, producto_id, precio_final))
        
        conexion.commit()
    except Exception as e:
        raise Exception(f"Error al agregar descuento: {str(e)}")
    finally:
        conexion.close()

def mostrar_descuentos():
    try:
        conexion = conectar_db()
        cursor = conexion.cursor()
        cursor.execute("SELECT ID_descuento FROM descuentos")
        resultados = cursor.fetchall()
        conexion.close()

        descuentos = [fila[0] for fila in resultados]
        return descuentos
    
    except Exception as e:
        print(f"Error al obtener descuentos: {e}")
        return []

def ocultar_descuento(id_descuento):
    """Marca un descuento como oculto en lugar de eliminarlo"""
    try:
        conexion = conectar_db()
        cursor = conexion.cursor()
        cursor.execute("UPDATE descuentos SET oculto = 1 WHERE ID_descuento = %s", (id_descuento,))
        conexion.commit()
        conexion.close()
    except Exception as e:
        raise Exception(f"Error al ocultar descuento: {str(e)}")

def actualizar_combo(nombre_original, datos):
    try:
        conexion = conectar_db()
        cursor = conexion.cursor()
        
        # Obtener los IDs de los productos
        cursor.execute("SELECT ID_producto FROM producto WHERE Nombre = %s", (datos['producto1'],))
        id_producto1 = cursor.fetchone()
        
        cursor.execute("SELECT ID_producto FROM producto WHERE Nombre = %s", (datos['producto2'],))
        id_producto2 = cursor.fetchone()
        
        if not id_producto1 or not id_producto2:
            raise Exception("Uno o ambos productos no existen")
        
        # Actualizar el combo
        sql = """
            UPDATE combos 
            SET Nombre = %s, 
                Producto1_ID = %s, 
                Producto2_ID = %s, 
                Precio = %s 
            WHERE Nombre = %s
        """
        valores = (
            datos['nombre'],
            id_producto1[0],
            id_producto2[0],
            datos['precio'],
            nombre_original
        )
        
        cursor.execute(sql, valores)
        conexion.commit()
        cursor.close()
        conexion.close()
        
    except Exception as e:
        print(f"Error al actualizar combo: {e}")
        raise Exception(f"Error al actualizar combo: {str(e)}")

def ocultar_producto(nombre_producto):
    """Marca un producto como oculto en lugar de eliminarlo"""
    try:
        conexion = conectar_db()
        cursor = conexion.cursor()
        
        # SQL para ocultar el producto
        sql = "UPDATE Producto SET oculto = 1 WHERE Nombre = %s"
        cursor.execute(sql, (nombre_producto,))
        
        conexion.commit()
        cursor.close()
        conexion.close()
        
        return True
    except Exception as e:
        raise Exception(f"Error al ocultar el producto: {str(e)}")

def obtener_stock_producto(nombre_producto):
    """Obtiene el stock disponible de un producto"""
    try:
        connection = conectar_db()
        if connection:
            cursor = connection.cursor()
            cursor.execute("SELECT Cantidad FROM Producto WHERE Nombre = %s", (nombre_producto,))
            resultado = cursor.fetchone()
            return resultado[0] if resultado else 0
    except Exception as e:
        print(f"Error al obtener stock: {e}")
        return 0
    finally:
        if connection:
            connection.close()
