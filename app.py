from flask import Flask, request, jsonify
from db_config import conectar
import hashlib

app = Flask(__name__)


@app.route('/login', methods=['POST'])
def login():
    dados = request.get_json()
    email = dados.get('email')
    senha = dados.get('senha')
    tipo = dados.get('tipo')

    if not email or not senha or not tipo:
        return jsonify({'status': 'erro', 'mensagem': 'Campos obrigatórios em falta'}), 400

    try:
        conn = conectar()
        cursor = conn.cursor(dictionary=True)

        # Opcional: criptografar a senha para comparar com hash (ex: hashlib)
        senha_hash = hashlib.sha256(senha.encode()).hexdigest()

        cursor.execute("""
            SELECT * FROM usuarios 
            WHERE email = %s AND senha = %s AND tipo = %s
        """, (email, senha_hash, tipo))

        usuario = cursor.fetchone()

        if usuario:
            return jsonify({'status': 'sucesso', 'mensagem': 'Login válido'})
        else:
            return jsonify({'status': 'erro', 'mensagem': 'Usuário ou senha incorretos'}), 401

    except Exception as erro:
        return jsonify({'status': 'erro', 'mensagem': str(erro)}), 500

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


if __name__ == '__main__':
    app.run(debug=True)
