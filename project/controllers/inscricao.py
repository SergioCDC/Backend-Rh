from project.models.database import inserir_candidato, verificar_cpf_existente
from werkzeug.security import generate_password_hash

def processar_inscricao(form_data):
    nome = form_data.get('nome')
    cpf = form_data.get('cpf')
    email = form_data.get('email')
    telefone = form_data.get('telefone')
    endereco = form_data.get('endereco')
    instituicao = form_data.get('instituicao')
    curso = form_data.get('curso')
    semestre = form_data.get('semestre')
    objetivo = form_data.get('objetivo')
    qualificacao = form_data.get('qualificacao')
    senha = form_data.get('senha')

    # Verifique os dados recebidos do formulário
    print(f"Dados recebidos: {form_data}")

    # Verificar se o CPF já existe
    if verificar_cpf_existente(cpf):
        raise ValueError("Este CPF já está cadastrado.")

    # Criptografar a senha antes de armazená-la
    senha_hash = generate_password_hash(senha)

    # Tentar inserir o candidato no banco de dados
    try:
        candidato_id = inserir_candidato(nome, cpf, email, telefone, endereco, instituicao, curso, semestre, objetivo, qualificacao, senha_hash)
        if not candidato_id:
            raise ValueError("Erro ao inserir o candidato.")
    except Exception as e:
        print(f"Erro ao processar inscrição: {e}")
        raise ValueError(f"Erro ao inserir no banco de dados: {e}")

    # Retorna o ID do candidato ou mensagem de sucesso
    print(f"Candidato inserido com sucesso com ID: {candidato_id}")
    return candidato_id
