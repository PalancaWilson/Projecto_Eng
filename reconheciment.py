import easyocr
import numpy as np

reader = easyocr.Reader(['pt'])


def reconhecer_texto(imagem_cv2):
    resultados = reader.readtext(imagem_cv2)
    for _, texto, confianca in resultados:
        if 6 <= len(texto.replace("-", "").replace(" ", "")) <= 10:
            return texto
    return None
