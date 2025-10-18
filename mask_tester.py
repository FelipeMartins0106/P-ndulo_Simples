import cv2
import numpy as np

video_path = 'Pêndulo.mp4' 

cor_min = np.array([0, 0, 0])
cor_max = np.array([179, 80, 80])

cap = cv2.VideoCapture(video_path)
ret, frame = cap.read()
cap.release()

if ret:
    # Redimensiona para caber na tela
    scale_percent = 50
    width = int(frame.shape[1] * scale_percent / 100)
    height = int(frame.shape[0] * scale_percent / 100)
    frame_resized = cv2.resize(frame, (width, height), interpolation=cv2.INTER_AREA)

    # Aplica a máscara
    hsv = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2HSV)
    mascara = cv2.inRange(hsv, cor_min, cor_max)

    # Mostra os resultados
    cv2.imshow('Original Redimensionado', frame_resized)
    cv2.imshow('Mascara Resultante', mascara)

    print("Pressione 'q' para fechar.")
    while True:
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()
else:
    print("Erro ao ler o vídeo.")