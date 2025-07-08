import torch
import cv2

# Carregar modelo pré-treinado do YOLOv5
model = torch.hub.load('ultralytics/yolov5', 'custom', path='placa.pt')  # Substitua 'best.pt' por seu modelo


def detectar_placa(caminho_imagem):
    img = cv2.imread(caminho_imagem)
    results = model(img)
    boxes = results.xyxy[0].tolist()  # Lista de [x1, y1, x2, y2, confianca, classe]
    
    if boxes:
        x1, y1, x2, y2, conf, cls = boxes[0]
        recorte = img[int(y1):int(y2), int(x1):int(x2)]
        return recorte
    return None
