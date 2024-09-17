from flask import request, jsonify, session
from werkzeug.security import check_password_hash
from project.models.database import get_db_connection

# Lista de e-mails com privilégios de admin e recrutadores
ADMIN_EMAILS = ['sergio@cdcia.com.br']  # Atualize com seus e-mails de administradores
RECRUTADOR_EMAILS = ['sejacf@cfcontabilidade.com']  # Atualize com seus e-mails de recrutadores

def login():
    if request.method == 'POST':
        data = request.get_json()  # Recebe os dados do front-end em JSON
        email = data.get('email')
        senha = data.get('senha')

        # Verificar se o email existe e pegar o hash da senha do banco
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM candidatos WHERE email = %s"
        cursor.execute(query, (email,))
        usuario = cursor.fetchone()
        cursor.close()
        connection.close()

        if usuario:
            if check_password_hash(usuario['senha'], senha):
                # Salvar o ID do usuário na sessão
                session['usuario_logado'] = usuario['id']  # ID do usuário
                session['usuario'] = usuario['nome']  # Nome do usuário

                # Verificar se o email é de admin ou recrutador
                if email in ADMIN_EMAILS:
                    session['is_admin'] = True
                    session['is_recrutador'] = False  # Não é recrutador
                    return jsonify({'success': True, 'role': 'admin', 'message': 'Login bem-sucedido como admin'})
                
                elif email in RECRUTADOR_EMAILS:
                    session['is_admin'] = False  # Não é administrador
                    session['is_recrutador'] = True  # É recrutador
                    return jsonify({'success': True, 'role': 'recrutador', 'message': 'Login bem-sucedido como recrutador'})
                
                else:
                    # Usuário comum
                    session['is_admin'] = False
                    session['is_recrutador'] = False
                    return jsonify({'success': True, 'role': 'usuario', 'message': 'Login bem-sucedido como usuário comum'})
            else:
                return jsonify({'success': False, 'message': 'Senha incorreta'}), 401
        else:
            return jsonify({'success': False, 'message': 'Email ou senha incorretos'}), 401

    return jsonify({'success': False, 'message': 'Método não permitido'}), 405
