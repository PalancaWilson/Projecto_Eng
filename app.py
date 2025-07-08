
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from db_config import conectar
from datetime import datetime
import torch
import easyocr
import cv2
import numpy as np
import os
import re
import base64
from werkzeug.utils import secure_filename
from PIL import Image
import io


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True) # Aplica CORS global


@app.route('/')
def home():
    return jsonify({"mensagem": "API ISPSECURITY ativa!"})


# Ronta para o login 
@app.route('/login', methods=['POST', 'OPTIONS'])
@cross_origin()  # <- CORS especificamente na rota
def login():
    if request.method == 'OPTIONS':
        return '', 204  # resposta ao preflight

    dados = request.get_json()
    email = dados.get('email')
    senha = dados.get('senha')
    tipo = dados.get('tipo')

    conn =conectar()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT * FROM funcionarios WHERE email=%s AND senha=%s AND cargo=%s"
   
    cursor.execute(query, (email, senha, tipo))
    usuario = cursor.fetchone()

    cursor.close()
    conn.close()

    if usuario:
        return jsonify({"status": "sucesso", "usuario": usuario})
    else:
        return jsonify({"status": "erro", "mensagem": "Credenciais inválidas."}), 401
    
    
    # Rota para cadastr de veiculos 
@app.route('/cadastrar-veiculo', methods=['POST'])
def cadastrar_veiculo():
    matricula = request.form.get('matricula')
    proprietario = request.form.get('proprietario')
    tipo_usuario = request.form.get('tipo_usuario')
    marca = request.form.get('marca')
    modelo = request.form.get('modelo')
    estado = request.form.get('estado', 'Ativo')
    cadastrado_por = 1  # Exemplo: ID do funcionário logado

    validade = request.form.get('validade') or '2025-12-31'  # valor padrão
    horario_acesso = request.form.get('horario_acesso') or '07:00-18:00'

    imagem = request.files.get('imagem')
    nome_arquivo = None

    if not all([matricula, proprietario, tipo_usuario]):
        return jsonify({"status": "erro", "mensagem": "Preencha todos os campos obrigatórios."}), 400

    if imagem and imagem.filename != '':
        nome_seguro = secure_filename(imagem.filename)
        caminho = os.path.join(UPLOAD_FOLDER, nome_seguro)
        imagem.save(caminho)
        nome_arquivo = nome_seguro

    try:
        conn = conectar()
        cursor = conn.cursor()

        # Inserção do veículo
        query_veiculo = """
            INSERT INTO veiculos_cadastrado 
            (matricula, proprietario, tipo_usuario, marca, modelo, estado, imagem, cadastrado_por)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query_veiculo, (
            matricula, proprietario, tipo_usuario,
            marca, modelo, estado, nome_arquivo, cadastrado_por
        ))
        id_veiculo_novo = cursor.lastrowid  # recupera o ID do veículo inserido

        # Inserção na tabela permissoes_acesso
        query_permissao = """
            INSERT INTO permissoes_acesso (id_veiculo, validade, horario_acesso, id_frequentador)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query_permissao, (
            id_veiculo_novo, validade, horario_acesso, tipo_usuario
        ))

        conn.commit()
        return jsonify({"status": "sucesso", "mensagem": "Veículo e permissão cadastrados com sucesso!"})

    except Exception as e:
        conn.rollback()
        return jsonify({"status": "erro", "mensagem": str(e)}), 500

    finally:
        cursor.close()
        conn.close()

# Rota da dashbourd do administrador

@app.route('/dashboard-data', methods=['GET'])
def dashboard_data():
    conn = conectar()
    cursor = conn.cursor()

    # Total de veículos cadastrados
    cursor.execute("SELECT COUNT(*) FROM veiculos_cadastrado")
    total_veiculos = cursor.fetchone()[0]

    # Total de acessos recusados
    cursor.execute("SELECT COUNT(*) FROM acessos WHERE estado = 'Recusado'")
    recusados = cursor.fetchone()[0]

    # Acessos do dia atual
    cursor.execute("SELECT COUNT(*) FROM acessos WHERE DATE(data_acesso) = CURDATE()")
    acessos_dia = cursor.fetchone()[0]

    # Acessos pendentes 
    cursor.execute("SELECT COUNT(*) FROM veiculos_cadastrado WHERE estado IS NULL OR estado = 'Inativo'")
    pendentes = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return jsonify({
        "total_veiculos": total_veiculos,
        "recusados": recusados,
        "acessos_dia": acessos_dia,
        "pendentes": pendentes
    })


    # Rota da dashbourd do segurança
@app.route("/dashboard-seguranca", methods=["GET"])
def dados_dashboard_seguranca():
    conn = conectar()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("SELECT COUNT(*) AS total FROM veiculos_cadastrado WHERE estado = 'Ativo'")
        total_autorizados = cursor.fetchone()["total"]

        cursor.execute("SELECT COUNT(*) AS total FROM acessos WHERE estado = 'Recusado'")
        tentativas_negadas = cursor.fetchone()["total"]

        cursor.execute("SELECT COUNT(*) AS total FROM acessos WHERE data_acesso = CURDATE()")
        acessos_hoje = cursor.fetchone()["total"]

        return jsonify({
            "total_autorizados": total_autorizados,
            "tentativas_negadas": tentativas_negadas,
            "acessos_hoje": acessos_hoje
        })

    except Exception as e:
        return jsonify({"erro": str(e)}), 500
    finally:
        cursor.close()
        conn.close()


# Rota dos veículos que acessaram a instituição nas ultimas 24 horas
@app.route("/ultimos-acessos", methods=["GET"])
def ultimos_acessos():
    conn = conectar()
    cursor = conn.cursor(dictionary=True)

    try:
        query = """
            SELECT 
                TIME_FORMAT(a.hora_acesso, '%H:%i') AS hora,
                v.matricula,
                a.estado
            FROM acessos a
            JOIN veiculos_cadastrado v ON a.id_carro = v.id_veiculo
            ORDER BY a.data_acesso DESC, a.hora_acesso DESC
            LIMIT 10
        """
        cursor.execute(query)
        resultados = cursor.fetchall()
        return jsonify(resultados)
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
    finally:
        cursor.close()
        conn.close()


# rota para o gráfico de acessos por hora
@app.route("/grafico-acessos", methods=["GET"])
def grafico_acessos():
    conn = conectar()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT HOUR(hora_acesso) AS hora, COUNT(*) AS total
            FROM acessos
            WHERE data_acesso = CURDATE()
            GROUP BY HOUR(hora_acesso)
            ORDER BY hora
        """)
        dados = cursor.fetchall()
        return jsonify(dados)
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# Rota para cadastrar frequentadores
@app.route("/frequentadores", methods=["GET"])
def listar_frequentadores():
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id_frequentador, nome, tipo FROM frequentadores")
    frequentadores = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(frequentadores)


UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Rota dos historico de acessos
@app.route('/api/historico', methods=['GET'])
def historico_acessos():
    try:
        conn = conectar()
        cursor = conn.cursor(dictionary=True)

        busca = request.args.get('busca', '').strip()

        query = """
            SELECT 
                a.id_acesso,  -- Adicione isso
                a.data_acesso,
                a.hora_acesso,
                f.tipo AS tipo_usuario,
                v.matricula,
                a.estado
            FROM acessos a
            JOIN veiculos_cadastrado v ON a.id_carro = v.id_veiculo
            JOIN frequentadores f ON a.tipo_frequentador = f.id_frequentador
        """

        if busca:
            query += " WHERE v.matricula LIKE %s"
            cursor.execute(query + " ORDER BY a.data_acesso DESC, a.hora_acesso DESC", [f"%{busca}%"])
        else:
            query += " ORDER BY a.data_acesso DESC, a.hora_acesso DESC"
            cursor.execute(query)

        acessos = cursor.fetchall()

        # Conversão da hora, se necessário
        for a in acessos:
            a["hora_acesso"] = str(a["hora_acesso"])

        return jsonify(acessos)

    except Exception as e:
        print("Erro ao filtrar histórico:", e)
        return jsonify({"erro": str(e)}), 500
    finally:
        cursor.close()
        conn.close()


@app.route('/api/acessos', methods=['POST'])
def inserir_acesso():
    try:
        dados = request.get_json()
        id_carro = dados.get('id_carro')
        tipo_frequentador = dados.get('tipo_frequentador')
        estado = dados.get('estado', 'Autorizado')  # ✅ valor válido
        imagem = dados.get('imagem')  # Pode ser opcional

        if not id_carro or not tipo_frequentador:
            return jsonify({"status": "erro", "mensagem": "Campos obrigatórios faltando."}), 400

        conn = conectar()
        cursor = conn.cursor()

        query = """
            INSERT INTO acessos (id_carro, tipo_frequentador, data_acesso, hora_acesso, estado, imagem)
            VALUES (%s, %s, CURDATE(), CURTIME(), %s, %s)
        """
        cursor.execute(query, (id_carro, tipo_frequentador, estado, imagem))
        conn.commit()

        return jsonify({"status": "sucesso", "mensagem": "Acesso inserido com sucesso!"})

    except Exception as e:
        print("Erro ao inserir acesso:", e)
        return jsonify({"status": "erro", "mensagem": str(e)}), 500
    finally:
        cursor.close()
        conn.close()


@app.route('/api/acessos/<int:id_acesso>', methods=['DELETE'])
def remover_acesso(id_acesso):
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM acessos WHERE id_acesso = %s", (id_acesso,))
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({"status": "erro", "mensagem": "Acesso não encontrado."}), 404

        return jsonify({"status": "sucesso", "mensagem": "Acesso removido com sucesso!"})

    except Exception as e:
        print("Erro ao remover acesso:", e)
        return jsonify({"status": "erro", "mensagem": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# ROTAS CRUD para permissões de veículos

# Ler permissões
@app.route('/api/permissoes', methods=['GET'])
def listar_permissoes():
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT 
            p.id_permissao,
            p.validade,
            p.horario_acesso,
            f.tipo AS tipo_usuario,
            f.nome AS nome_frequentador,
            v.matricula,
            v.proprietario
        FROM permissoes_acesso p
        JOIN veiculos_cadastrado v ON p.id_veiculo = v.id_veiculo
        JOIN frequentadores f ON p.id_frequentador = f.id_frequentador
    """)
    dados = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(dados)


@app.route('/api/permissoes/<int:id>', methods=['PUT'])
def atualizar_permissao(id):
    try:
        dados = request.get_json()
        validade = dados.get('validade')
        horario = dados.get('horario_acesso')
        id_frequentador = dados.get('id_frequentador')  # Atualiza corretamente

        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE permissoes_acesso
            SET validade=%s, horario_acesso=%s, id_frequentador=%s
            WHERE id_permissao=%s
        """, (validade, horario, id_frequentador, id))
        conn.commit()
        return jsonify({"status": "sucesso", "mensagem": "Permissão atualizada."})
    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# Rotas para o reconhecimento de placas


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


if __name__ == '__main__':
    app.run(debug=True)




