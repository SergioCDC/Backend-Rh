import os
from dotenv import load_dotenv
import mysql.connector

# Carregar variáveis de ambiente
load_dotenv()

# Conexão ao banco de dados MySQL
def get_db_connection():
    connection = mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME'),
        port=int(os.getenv('DB_PORT'))  # Adicionando o parâmetro de porta

    )
    return connection
