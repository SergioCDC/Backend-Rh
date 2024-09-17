from flask import Flask, request, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from project.models.database import (inserir_vaga, listar_vagas, inserir_candidato, verificar_candidato, obter_vaga, 
                                atualizar_vaga, deletar_vaga_db, inserir_candidatura, verificar_cpf_existente, 
                                verificar_candidatura_existente, atualizar_candidatura)
from project.controllers.inscricao import processar_inscricao
from project.controllers.login import login as login_controller
from config.config import get_db_connection




def register_routes(app):
    # Página inicial (index)
    @app.route('/', methods=['GET'])
    def index():
        vagas = listar_vagas()  # Obtenha as vagas do banco de dados
        return jsonify(vagas)  # Retorne os dados das vagas como JSON


    @app.route('/cadastro', methods=['POST'])
    def cadastro():
        if request.method == 'POST':
            try:
                data = request.get_json()  # Recebe os dados em JSON do front-end
                candidato_id = processar_inscricao(data)  # Processa a inscrição com os dados recebidos
                
                # Armazenar o ID do candidato na sessão
                session['usuario_logado'] = candidato_id
                session['candidato_nome'] = data.get('nome')  # Armazena o nome para exibição
                
                return jsonify({'success': True, 'message': 'Cadastro realizado com sucesso!'})
            except ValueError as e:
                return jsonify({'success': False, 'message': str(e)}), 400


    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'GET':
            return jsonify({'message': 'Por favor, utilize o método POST para logar.', 'success': False})
        return login_controller()

    # Recrutador
    @app.route('/recrutador', methods=['GET'])
    def recrutador():
        if not session.get('is_admin') and not session.get('is_recrutador'):
            return jsonify({'success': False, 'message': 'Acesso negado!'}), 403
        else:
            vagas = listar_vagas()
            return jsonify(vagas)  # Retorne a lista de vagas em JSON para o recrutador


    @app.route('/recrutador/processar', methods=['POST'])
    def processar_vaga():
        if 'is_recrutador' not in session or not session['is_recrutador']:
            return jsonify({'success': False, 'message': 'Acesso negado. Usuário não autorizado.'}), 403

        data = request.get_json()  # Recebe os dados do front-end em JSON
        titulo = data.get('titulo')
        descricao = data.get('descricao')
        requisitos = data.get('requisitos')

        # Inserir a vaga no banco de dados
        inserir_vaga(titulo, descricao, requisitos)
        return jsonify({'success': True, 'message': 'Vaga criada com sucesso!'})

    @app.route('/recrutador/deletar/<int:vaga_id>', methods=['POST'])
    def deletar_vaga(vaga_id):
        try:
            deletar_vaga_db(vaga_id)
            return jsonify({'success': True, 'message': 'Vaga deletada com sucesso!'})
        except Exception as e:
            print(f"Erro ao deletar vaga: {e}")
            return jsonify({'success': False, 'message': 'Erro ao deletar a vaga.'}), 500


    @app.route('/recrutador/editar/<int:vaga_id>', methods=['POST'])
    def editar_vaga(vaga_id):
        try:
            data = request.get_json()
            titulo = data.get('titulo')
            descricao = data.get('descricao')
            requisitos = data.get('requisitos')
            
            atualizar_vaga(vaga_id, titulo, descricao, requisitos)
            return jsonify({'success': True, 'message': 'Vaga atualizada com sucesso!'})
        except Exception as e:
            print(f"Erro ao editar vaga: {e}")
            return jsonify({'success': False, 'message': 'Erro ao editar a vaga.'}), 500


    @app.route('/vagas_logado', methods=['GET'])
    def vagas_logado():
        # Verifica se o usuário está logado
        if 'usuario_logado' not in session:
            return jsonify({'success': False, 'message': 'Usuário não está logado'}), 403
        
        # Se o usuário estiver logado, retornar a lista de vagas
        vagas = listar_vagas()  # Obtenha as vagas do banco de dados
        return jsonify(vagas)  # Retorna as vagas em formato JSON



    @app.route('/inscricao/<int:vaga_id>', methods=['POST'])
    def inscrever(vaga_id):
        print(f"Vaga ID: {vaga_id}")
        print(f"Usuário logado na sessão: {session.get('usuario_logado')}")

        # Verifica se a sessão contém o usuário logado corretamente
        if 'usuario_logado' not in session or session.get('usuario_logado') is None:
            return jsonify({'error': 'Usuário não logado.'}), 403

        candidato_id = session.get('usuario_logado')

        # Verifica se o candidato já se inscreveu para essa vaga
        if verificar_candidatura_existente(candidato_id, vaga_id):
            return jsonify({'error': 'Você já se inscreveu para esta vaga.'}), 400

        # Processa a inscrição
        try:
            inserir_candidatura(candidato_id, vaga_id)
            return jsonify({'success': 'Inscrição realizada com sucesso!'}), 200
        except Exception as e:
            print(f"Erro ao processar inscrição: {e}")
            return jsonify({'error': 'Erro ao processar inscrição.'}), 500


    @app.route('/admin/candidaturas', methods=['GET', 'POST'])
    def admin_candidaturas():
        # Verifica se o usuário logado é um administrador
        if not session.get('is_admin'):
            return jsonify({'success': False, 'message': 'Acesso negado. Você não tem permissão.'}), 403
        
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        if request.method == 'POST':
            # Operação de exclusão ou edição
            data = request.get_json()

            if data.get('action') == 'deletar':
                # Deletar candidatura
                candidatura_id = data.get('id')
                query = "DELETE FROM candidaturas WHERE id = %s"
                cursor.execute(query, (candidatura_id,))
                connection.commit()
                return jsonify({'success': True, 'message': 'Candidatura deletada com sucesso!'})

            elif data.get('action') == 'editar':
                # Editar dados do candidato
                candidato_id = data.get('candidato_id')
                nome = data.get('nome')
                email = data.get('email')
                cpf = data.get('cpf')
                curso = data.get('curso')

                # Atualizar a tabela `candidatos`
                query = """
                UPDATE candidatos
                SET nome = %s, email = %s, cpf = %s, curso = %s
                WHERE id = %s
                """
                cursor.execute(query, (nome, email, cpf, curso, candidato_id))
                connection.commit()
                return jsonify({'success': True, 'message': 'Candidato atualizado com sucesso!'})

        # Listar candidaturas
        query = """
        SELECT 
            candidaturas.id,
            candidatos.id AS candidato_id,
            candidatos.nome AS nome_candidato,
            candidatos.email AS email_candidato,
            candidatos.cpf,
            candidatos.curso,
            vagas.titulo AS titulo_vaga,
            candidaturas.data_candidatura
        FROM candidaturas
        JOIN candidatos ON candidaturas.candidato_id = candidatos.id
        JOIN vagas ON candidaturas.vaga_id = vagas.id
        """
        cursor.execute(query)
        candidaturas = cursor.fetchall()

        cursor.close()
        connection.close()

        return jsonify(candidaturas)  # Retorna as candidaturas como JSON

    

    @app.route('/candidaturas', methods=['GET'])
    def pesquisa_candidaturas():
        # Verifica se o usuário logado é administrador ou recrutador
        if not session.get('is_admin') and not session.get('is_recrutador'):
            return jsonify({'success': False, 'message': 'Acesso negado. Você não tem permissão.'}), 403

        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        # Consulta para listar candidaturas
        query_candidaturas = """
        SELECT 
            candidaturas.id,
            candidatos.id AS candidato_id,
            candidatos.nome AS nome_candidato,
            candidatos.email AS email_candidato,
            candidatos.cpf,
            candidatos.curso,
            vagas.titulo AS titulo_vaga,
            candidaturas.data_candidatura
        FROM candidaturas
        JOIN candidatos ON candidaturas.candidato_id = candidatos.id
        JOIN vagas ON candidaturas.vaga_id = vagas.id
        """
        cursor.execute(query_candidaturas)
        candidaturas = cursor.fetchall()

        cursor.close()
        connection.close()

        return jsonify(candidaturas)  # Retorna as candidaturas como JSON

    
    @app.route('/logout', methods=['POST'])
    def logout():
        # Limpa a sessão do usuário
        session.clear()
        return jsonify({'success': True, 'message': 'Você foi deslogado com sucesso!'})

    

