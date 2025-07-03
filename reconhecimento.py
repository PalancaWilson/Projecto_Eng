# backend/reconhecimento.py

import cv2
import numpy as np
import easyocr
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import mysql.connector
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Configuração da conexão com MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="mutombo21",  # coloque sua senha aqui
    database="ispsecurity"
)
cursor = conn.cursor(dictionary=True)

reader = easyocr.Reader(['pt'])


@app.route('/reconhecer-matricula', methods=['POST'])
def reconhecer_matricula():
    if 'imagem' not in request.files:
        return jsonify({"erro": "Nenhuma imagem enviada."}), 400

    imagem = request.files['imagem']
    caminho = os.path.join("uploads", imagem.filename)
    imagem.save(caminho)

    # Leitura da imagem
    img = cv2.imread(caminho)
    resultados = reader.readtext(img)

    matricula_detectada = None
    for (bbox, texto, confianca) in resultados:
        texto = texto.upper().replace(" ", "").replace("-", "").strip()
        if 6 <= len(texto) <= 10:
            matricula_detectada = texto
            break

    os.remove(caminho)

    if not matricula_detectada:
        return jsonify({"matricula": None, "mensagem": "Nenhuma matrícula detectada."}), 404

    # Verificação na base de dados
    cursor.execute("SELECT * FROM veiculos_cadastrado WHERE REPLACE(REPLACE(REPLACE(matricula, '-', ''), ' ', ''), '/', '') = %s", (matricula_detectada,))
    veiculo = cursor.fetchone()

    if veiculo:
        # Grava acesso na tabela "acessos"
        now = datetime.now()
        cursor.execute("""
            INSERT INTO acessos (id_carro, tipo_frequentador, estado, data_acesso, hora_acesso, imagem)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            veiculo['id_veiculo'],
            veiculo['tipo_usuario'],
            'Autorizado',
            now.date(),
            now.time(),
            imagem.filename
        ))
        conn.commit()
        return jsonify({"matricula": matricula_detectada, "status": "Autorizado"})
    else:
        return jsonify({"matricula": matricula_detectada, "status": "Recusado"})


if __name__ == '__main__':
    os.makedirs("uploads", exist_ok=True)
    app.run(debug=True)
