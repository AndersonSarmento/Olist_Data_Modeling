import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Estabelecendo conexão com o banco de dados
def create_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),       # Endereço do servidor
        user=os.getenv("DB_USER"),       # Usuário do banco de dados
        password=os.getenv("DB_PASSWORD"),  # Senha do banco de dados
        database=os.getenv("DB_NAME")    # Nome do banco de dados
    )  # Fechar o parêntese da função

 #Função para executar comandos SQL sem retorno
def execute_query(conexao, comando):
    cursor = conexao.cursor()
    try:
        cursor.execute(comando)
        conexao.commit()
    except Error as e:
        print(f"Erro ao executar o comando: {e}")
    finally:
        cursor.close()
# Função para buscar todos os resultados de uma consulta

def query_fetch_all(conexao, comando):
    cursor = conexao.cursor()
    try:
        cursor.execute(comando)
        return cursor.fetchall()
    except Error as e:
        print(f"Erro ao buscar resultados: {e}")
        return []
    finally:
        cursor.close()

# Função para buscar apenas um resultado de uma consulta
def query_fetch_one(conexao, comando):
    cursor = conexao.cursor()
    try:
        cursor.execute(comando)
        return cursor.fetchone()
    except Error as e:
        print(f"Erro ao buscar resultado: {e}")
        return None
    finally:
        cursor.close()

def generate_create_table(df, table_name):
    sql_types = {
        "object": "VARCHAR(255)",
        "int64": "INT",
        "float64": "FLOAT",
        "datetime64[ns]": "DATETIME",
        "bool": "BOOLEAN"
    }
    
    columns = []
    for col_name, col_type in df.dtypes.items():
        sql_type = sql_types.get(str(col_type), "VARCHAR(255)")
        columns.append(f"{col_name} {sql_type}")
    
    columns_sql = ",\n    ".join(columns)
    create_table_sql = f"CREATE TABLE IF NOT EXISTS {table_name} (\n    {columns_sql}\n);"
    return create_table_sql