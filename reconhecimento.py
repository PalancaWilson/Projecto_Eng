# reconhecimento_yolo.py - Versão Melhorada para Interface Web
import torch
import easyocr
import cv2
import numpy as np
import mysql.connector
import os
import re
import base64
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from PIL import Image
import io

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Configurações do modelo
try:
    # Tentar carregar modelo customizado primeiro
    modelo_yolo = torch.hub.load('ultralytics/yolov5', 'custom',
                                path='runs/train/placas_angola_v1/weights/best.pt')
    print("Modelo customizado carregado com sucesso!")
except:
    # Fallback para modelo genérico
    modelo_yolo = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
    print("Usando modelo genérico YOLOv5")

# OCR otimizado
reader = easyocr.Reader(['pt', 'en'], gpu=torch.cuda.is_available())


def preprocessar_roi(roi):
    """Melhorar qualidade da ROI para OCR"""
    if roi is None or roi.size == 0:
        return None
        
    # Redimensionar se muito pequena
    height, width = roi.shape[:2]
    if height < 40 or width < 120:
        scale_factor = max(40 / height, 120 / width)
        new_width = int(width * scale_factor)
        new_height = int(height * scale_factor)
        roi = cv2.resize(roi, (new_width, new_height), interpolation=cv2.INTER_CUBIC)
    
    # Converter para escala de cinza
    if len(roi.shape) == 3:
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    else:
        gray = roi
    
    # Múltiplas técnicas de processamento
    processed_images = []
    
    # 1. Imagem original
    processed_images.append(roi)
    
    # 2. Threshold adaptativo
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY, 11, 2)
    processed_images.append(cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR))
    
    # 3. Equalização de histograma
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    cl1 = clahe.apply(gray)
    processed_images.append(cv2.cvtColor(cl1, cv2.COLOR_GRAY2BGR))
    
    # 4. Desfoque gaussiano + sharpening
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    sharpened = cv2.filter2D(blurred, -1, kernel)
    processed_images.append(cv2.cvtColor(sharpened, cv2.COLOR_GRAY2BGR))
    
    return processed_images


def validar_matricula_angolana(texto):
    """Validar formato de matrícula angolana"""
    # Limpar texto
    texto_limpo = re.sub(r'[^A-Z0-9]', '', texto.upper())
    
    # Padrões de matrícula angolana (ajustar conforme necessário)
    padroes = [
        r'^[A-Z]{2}[0-9]{2}[A-Z]{2}$',  # AB12CD
        r'^[A-Z]{3}[0-9]{3}$',  # ABC123
        r'^[0-9]{2}[A-Z]{2}[0-9]{2}$',  # 12AB34
        r'^[A-Z]{2}[0-9]{3}[A-Z]{2}$',  # AB123CD
        r'^[A-Z]{1}[0-9]{2}[A-Z]{2}[0-9]{2}$',  # A12BC34
    ]
    
    for padrao in padroes:
        if re.match(padrao, texto_limpo):
            return True, texto_limpo
    
    # Verificar se tem tamanho mínimo
    if 5 <= len(texto_limpo) <= 9:
        return True, texto_limpo
    
    return False, None


def detectar_veiculos_e_placas(img_cv):
    """Detectar veículos e extrair regiões de placas"""
    # Inferência com YOLO
    resultados = modelo_yolo(img_cv)
    deteccoes = resultados.xyxy[0]
    
    if len(deteccoes) == 0:
        return []
    
    # Se usando modelo customizado, todas as detecções são placas
    if 'custom' in str(modelo_yolo.model):
        placas_detectadas = []
        for * box, conf, cls in deteccoes.tolist():
            if conf > 0.3:  # Confiança mínima
                placas_detectadas.append({
                    'box': box,
                    'confidence': conf,
                    'type': 'license_plate'
                })
        return placas_detectadas
    
    # Se usando modelo genérico, filtrar veículos
    else:
        classes_veiculos = [2, 5, 7]  # car, bus, truck
        veiculos_detectados = []
        
        for * box, conf, cls in deteccoes.tolist():
            if conf > 0.5 and int(cls) in classes_veiculos:
                veiculos_detectados.append({
                    'box': box,
                    'confidence': conf,
                    'type': 'vehicle'
                })
        
        return veiculos_detectados


def conectar():
    """Conectar ao banco de dados"""
    try:
        return mysql.connector.connect(
            host='localhost',
            user='root',
            password='mutombo21',
            database='ispsecurity'
        )
    except mysql.connector.Error as err:
        print(f"Erro de conexão: {err}")
        return None


@app.route("/reconhecer-matricula", methods=["POST"])
def reconhecer_matricula():
    """Endpoint principal para reconhecimento"""
    try:
        # Verificar se dados foram enviados
        if 'imagem' not in request.files and 'image_data' not in request.form:
            return jsonify({"erro": "Nenhuma imagem enviada"}), 400

        # Processar imagem do arquivo ou base64
        if 'imagem' in request.files:
            imagem = request.files['imagem']
            nome_arquivo = secure_filename(imagem.filename)
            caminho = os.path.join(UPLOAD_FOLDER, nome_arquivo)
            imagem.save(caminho)
            img_cv = cv2.imread(caminho)
        else:
            # Processar base64 da câmera
            image_data = request.form['image_data']
            image_data = image_data.split(',')[1]  # Remover header data:image/jpeg;base64,
            
            # Decodificar base64
            image_bytes = base64.b64decode(image_data)
            image = Image.open(io.BytesIO(image_bytes))
            img_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            
            # Salvar imagem para log
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nome_arquivo = f"camera_{timestamp}.jpg"
            caminho = os.path.join(UPLOAD_FOLDER, nome_arquivo)
            cv2.imwrite(caminho, img_cv)

        if img_cv is None:
            return jsonify({"erro": "Erro ao processar imagem"}), 400

        # Detectar veículos/placas
        deteccoes = detectar_veiculos_e_placas(img_cv)
        
        if not deteccoes:
            return jsonify({
                "matricula": None,
                "status": "Nenhum veículo detectado",
                "imagem": nome_arquivo
            }), 404

        # Processar cada detecção
        melhor_resultado = None
        melhor_confianca = 0
        
        for deteccao in deteccoes:
            x1, y1, x2, y2 = map(int, deteccao['box'])
            conf_deteccao = deteccao['confidence']
            
            # Expandir região para capturar melhor a placa
            h, w = img_cv.shape[:2]
            margin = 15
            
            # Para veículos, focar na parte inferior onde ficam as placas
            if deteccao['type'] == 'vehicle':
                # Ajustar região para parte inferior do veículo
                altura_veiculo = y2 - y1
                y1 = y1 + int(altura_veiculo * 0.6)  # Focar nos 40% inferiores
                
            x1 = max(0, x1 - margin)
            y1 = max(0, y1 - margin)
            x2 = min(w, x2 + margin)
            y2 = min(h, y2 + margin)
            
            roi = img_cv[y1:y2, x1:x2]
            
            if roi.size == 0:
                continue
            
            # Processar ROI com múltiplas técnicas
            processed_rois = preprocessar_roi(roi)
            
            if not processed_rois:
                continue
            
            # Aplicar OCR em cada versão processada
            for processed_roi in processed_rois:
                try:
                    resultado_ocr = reader.readtext(processed_roi, detail=1)
                    
                    for (bbox, texto, confianca_ocr) in resultado_ocr:
                        if confianca_ocr < 0.5:  # Filtrar textos com baixa confiança
                            continue
                        
                        # Validar formato da matrícula
                        valida, matricula_limpa = validar_matricula_angolana(texto)
                        
                        if valida:
                            # Calcular confiança total
                            confianca_total = (conf_deteccao + confianca_ocr) / 2
                            
                            if confianca_total > melhor_confianca:
                                melhor_confianca = confianca_total
                                melhor_resultado = {
                                    'matricula': matricula_limpa,
                                    'confianca': confianca_total,
                                    'bbox': [x1, y1, x2, y2]
                                }
                                
                except Exception as e:
                    print(f"Erro no OCR: {e}")
                    continue
        
        # Verificar se encontrou alguma matrícula
        if not melhor_resultado:
            return jsonify({
                "matricula": None,
                "status": "Nenhuma matrícula válida detectada",
                "imagem": nome_arquivo
            }), 404
        
        # Verificar no banco de dados
        conexao = conectar()
        if not conexao:
            return jsonify({"erro": "Erro de conexão com banco de dados"}), 500
        
        try:
            cursor = conexao.cursor(dictionary=True)
            cursor.execute("""
                SELECT * FROM veiculos_cadastrado 
                WHERE REPLACE(REPLACE(REPLACE(matricula, '-', ''), ' ', ''), '/', '') = %s
            """, (melhor_resultado['matricula'],))
            veiculo = cursor.fetchone()

            if veiculo:
                # Registrar acesso autorizado
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
                    nome_arquivo
                ))
                conexao.commit()
                
                return jsonify({
                    "matricula": melhor_resultado['matricula'],
                    "status": "Autorizado",
                    "tipo_usuario": veiculo['tipo_usuario'],
                    "confianca": float(melhor_resultado['confianca']),
                    "imagem": nome_arquivo,
                    "proprietario": veiculo.get('proprietario', 'N/A')
                })
            else:
                # Registrar acesso negado
                now = datetime.now()
                cursor.execute("""
                    INSERT INTO acessos (id_carro, tipo_frequentador, estado, data_acesso, hora_acesso, imagem, matricula_detectada)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (
                    None,
                    'Desconhecido',
                    'Recusado',
                    now.date(),
                    now.time(),
                    nome_arquivo,
                    melhor_resultado['matricula']
                ))
                conexao.commit()
                
                return jsonify({
                    "matricula": melhor_resultado['matricula'],
                    "status": "Recusado",
                    "confianca": float(melhor_resultado['confianca']),
                    "imagem": nome_arquivo,
                    "motivo": "Veículo não cadastrado"
                })
                
        except Exception as e:
            return jsonify({"erro": f"Erro no banco de dados: {str(e)}"}), 500
        finally:
            if cursor:
                cursor.close()
            if conexao:
                conexao.close()

    except Exception as e:
        return jsonify({"erro": f"Erro no processamento: {str(e)}"}), 500


@app.route("/status", methods=["GET"])
def status():
    """Endpoint para verificar status do sistema"""
    return jsonify({
        "status": "online",
        "modelo": "YOLOv5 + EasyOCR",
        "gpu_disponivel": torch.cuda.is_available(),
        "timestamp": datetime.now().isoformat()
    })


@app.route("/historico-acessos", methods=["GET"])
def historico_acessos():
    """Endpoint para obter histórico de acessos"""
    try:
        conexao = conectar()
        if not conexao:
            return jsonify({"erro": "Erro de conexão"}), 500
        
        cursor = conexao.cursor(dictionary=True)
        cursor.execute("""
            SELECT a.*, v.proprietario, v.matricula as matricula_cadastrada
            FROM acessos a
            LEFT JOIN veiculos_cadastrado v ON a.id_carro = v.id_veiculo
            ORDER BY a.data_acesso DESC, a.hora_acesso DESC
            LIMIT 50
        """)
        acessos = cursor.fetchall()
        
        # Converter datetime para string
        for acesso in acessos:
            if acesso['data_acesso']:
                acesso['data_acesso'] = acesso['data_acesso'].strftime('%Y-%m-%d')
            if acesso['hora_acesso']:
                acesso['hora_acesso'] = str(acesso['hora_acesso'])
        
        return jsonify(acessos)
    
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if conexao:
            conexao.close()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
