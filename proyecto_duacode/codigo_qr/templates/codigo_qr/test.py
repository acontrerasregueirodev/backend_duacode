import cv2
import pyzbar

# Iniciamos la captura de la cámara web
cap = cv2.VideoCapture(0)

while True:
    # Capturamos una imagen de la cámara web
    ret, frame = cap.read()

    # Detectamos los códigos QR en la imagen
    decoded = pyzbar.decode(frame)

    # Accedemos al primer código QR detectado
    code = decoded[0]

    # Imprimimos la información del código QR
    if code:
        print(code.data)

    # Mostramos la imagen en la pantalla
    cv2.imshow("Imagen", frame)

    # Esperamos a que se pulse una tecla
    key = cv2.waitKey(1)

    # Si se pulsa la tecla "q", salimos del bucle
    if key == ord("q"):
        break

# Liberamos la cámara web
cap.release()

# Cerramos la ventana de la imagen
cv2.destroyAllWindows()