
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from db_config import conectar
from datetime import datetime

import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True) # Aplica CORS global


@app.route('/')
def home():
    return jsonify({"mensagem": "API ISPSECURITY ativa!"})


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
    
    
@app.route('/cadastrar-veiculo', methods=['POST'])
def cadastrar_veiculo():
    # Coleta dados do formulário via FormData
    matricula = request.form.get('matricula')
    proprietario = request.form.get('proprietario')
    tipo_usuario = request.form.get('tipo_usuario')
    marca = request.form.get('marca')
    modelo = request.form.get('modelo')
    estado = request.form.get('estado', 'Ativo')
    cadastrado_por = 1  # ID fictício do usuário logado

    imagem = request.files.get('imagem')

    # Validação de campos obrigatórios
    if not all([matricula, proprietario, tipo_usuario]):
        return jsonify({"status": "erro", "mensagem": "Preencha todos os campos obrigatórios."}), 400

    # Salvar imagem (se enviada)
    nome_arquivo = None
    if imagem and imagem.filename != '':
        nome_seguro = secure_filename(imagem.filename)
        caminho = os.path.join(UPLOAD_FOLDER, nome_seguro)
        imagem.save(caminho)
        nome_arquivo = nome_seguro

    # Inserção no banco de dados
    try:
        conn = conectar()
        cursor = conn.cursor()
        query = """
            INSERT INTO veiculos_cadastrado 
            (matricula, proprietario, tipo_usuario, marca, modelo, estado, imagem, cadastrado_por)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            matricula, proprietario, tipo_usuario,
            marca, modelo, estado, nome_arquivo, cadastrado_por
        ))
        conn.commit()
        return jsonify({"status": "sucesso", "mensagem": "Veículo cadastrado com sucesso!"})
    except Exception as e:
        conn.rollback()
        return jsonify({"status": "erro", "mensagem": str(e)}), 500
    finally:
        cursor.close()
        conn.close()



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

    # Acessos pendentes (se quiser usar estado NULL ou outro critério)
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


@app.route("/dashboard-seguranca", methods=["GET"])
def dados_dashboard_seguranca():
    conn = conectar()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("SELECT COUNT(*) AS total FROM veiculos_cadastrado WHERE estado = 'Ativo'")
        total_autorizados = cursor.fetchone()["total"]
#   cursor.execute("SELECT COUNT(*) FROM veiculos_cadastrado")
 #   total_veiculos = cursor.fetchone()[0]

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

@app.route('/api/historico', methods=['GET'])
def historico_acessos():
    try:
        conn = conectar()
        cursor = conn.cursor(dictionary=True)

        busca = request.args.get('busca', '').strip()

        query = """
            SELECT 
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

        for a in acessos:
            a["hora_acesso"] = str(a["hora_acesso"])

        return jsonify(acessos)

    except Exception as e:
        print("Erro ao filtrar histórico:", e)
        return jsonify({"erro": str(e)}), 500
    finally:
        cursor.close()
        conn.close()




if __name__ == '__main__':
    app.run(debug=True)





