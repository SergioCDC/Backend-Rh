from config.config import get_db_connection

def inserir_candidato(nome, cpf, email, telefone, endereco, instituicao, curso, semestre, objetivo, qualificacao, senha_hash):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        query = """
        INSERT INTO candidatos (nome, cpf, email, telefone, endereco_completo, instituicao, curso, semestre, objetivo, qualificacao, senha)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (nome, cpf, email, telefone, endereco, instituicao, curso, semestre, objetivo, qualificacao, senha_hash))
        connection.commit()
        candidato_id = cursor.lastrowid
        cursor.close()
        connection.close()

        print(f"Candidato inserido com sucesso, ID: {candidato_id}")
        return candidato_id
    except Exception as e:
        print(f"Erro ao inserir candidato: {e}")
        return None

        
def inserir_vaga(titulo, descricao, requisitos):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # Print para ver se os dados estão corretos antes de inserir
        print(f"Dados recebidos: Título: {titulo}, Descrição: {descricao}, Requisitos: {requisitos}")

        query = """
        INSERT INTO vagas (titulo, descricao, requisitos)
        VALUES (%s, %s, %s)
        """
        cursor.execute(query, (titulo, descricao, requisitos))
        connection.commit()

        cursor.close()
        connection.close()
        print("Vaga inserida com sucesso.")
    except Exception as e:
        print(f"Erro ao inserir vaga: {e}")




def inserir_candidatura(candidato_id, vaga_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
    INSERT INTO candidaturas (candidato_id, vaga_id)
    VALUES (%s, %s)
    """
    cursor.execute(query, (candidato_id, vaga_id))
    connection.commit()

    cursor.close()
    connection.close()

def verificar_candidato(email):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
    SELECT * FROM candidatos WHERE email = %s
    """
    cursor.execute(query, (email,))
    candidato = cursor.fetchone()

    cursor.close()
    connection.close()

    return candidato


def verificar_cpf_existente(cpf):
    connection = get_db_connection()
    cursor = connection.cursor()

    query = "SELECT * FROM candidatos WHERE cpf = %s"
    cursor.execute(query, (cpf,))
    candidato = cursor.fetchone()

    cursor.close()
    connection.close()

    return candidato is not None


def listar_vagas():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    query = "SELECT * FROM vagas"
    cursor.execute(query)
    vagas = cursor.fetchall()

    cursor.close()
    connection.close()

    return vagas



def deletar_vaga_db(vaga_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    query = "DELETE FROM vagas WHERE id = %s"
    cursor.execute(query, (vaga_id,))
    connection.commit()

    cursor.close()
    connection.close()


def atualizar_vaga(vaga_id, titulo, descricao, requisitos):
    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
    UPDATE vagas
    SET titulo = %s, descricao = %s, requisitos = %s
    WHERE id = %s
    """
    cursor.execute(query, (titulo, descricao, requisitos, vaga_id))
    connection.commit()

    cursor.close()
    connection.close()

def atualizar_vaga(vaga_id, titulo, descricao, requisitos):
    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
    UPDATE vagas
    SET titulo = %s, descricao = %s, requisitos = %s
    WHERE id = %s
    """
    cursor.execute(query, (titulo, descricao, requisitos, vaga_id))
    connection.commit()

    cursor.close()
    connection.close()

def obter_vaga(vaga_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    query = "SELECT * FROM vagas WHERE id = %s"
    cursor.execute(query, (vaga_id,))
    vaga = cursor.fetchone()

    cursor.close()
    connection.close()

    return vaga

def verificar_candidatura_existente(candidato_id, vaga_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    query = "SELECT * FROM candidaturas WHERE candidato_id = %s AND vaga_id = %s"
    cursor.execute(query, (candidato_id, vaga_id))
    candidatura = cursor.fetchone()

    cursor.close()
    connection.close()

    return candidatura is not None

def inserir_candidatura(candidato_id, vaga_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        query = "INSERT INTO candidaturas (candidato_id, vaga_id, data_candidatura) VALUES (%s, %s, NOW())"
        cursor.execute(query, (candidato_id, vaga_id))
        connection.commit()

        cursor.close()
        connection.close()
    except Exception as e:
        print(f"Erro ao inserir candidatura: {e}")
        raise

def atualizar_candidatura(candidatura_id, nome, email, cpf, curso, vaga):
    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
    UPDATE candidaturas
    SET nome = %s, email = %s, cpf = %s, curso = %s, vaga = %s
    WHERE id = %s
    """
    cursor.execute(query, (nome, email, cpf, curso, vaga, candidatura_id))
    connection.commit()

    cursor.close()
    connection.close()

