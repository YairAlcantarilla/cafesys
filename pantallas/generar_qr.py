import qrcode
import os

def generar_qr_login(usuario, contraseña, nombre_archivo):
    # Crear los datos en formato "usuario:contraseña"
    datos = f"{usuario}:{contraseña}"
    
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
    ruta_qr = f"./qr_codes/{nombre_archivo}.png"
    os.makedirs("./qr_codes", exist_ok=True)
    qr_image.save(ruta_qr)
    return ruta_qr

# Ejemplo de uso
if __name__ == "__main__":
    # Generar QR para un usuario
    ruta = generar_qr_login("250101", "admin123", "admin_qr")
    print(f"QR generado en: {ruta}")