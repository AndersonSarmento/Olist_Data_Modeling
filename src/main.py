import pandas as pd
from db_utils import create_connection, generate_create_table, execute_query

if __name__ == "__main__":
    try:
        # Estabelecendo conexão com o banco de dados
        conexao = create_connection()

        if conexao.is_connected():
            print("Conexão bem-sucedida ao banco de dados.")
        else:
            print("Falha na conexão ao banco de dados.")
            exit()

        # Caminho do arquivo CSV
        path_customers = "/home/ander/Documentos/projetos/Olist_Data_Modeling/data/raw/olist_customers_dataset.csv"
        path_olist_geolocation = "/home/ander/Documentos/projetos/Olist_Data_Modeling/data/raw/olist_geolocation_dataset.csv"
        path_olist_order_items = "/home/ander/Documentos/projetos/Olist_Data_Modeling/data/raw/olist_order_items_dataset.csv"
        path_olist_order_payments = "/home/ander/Documentos/projetos/Olist_Data_Modeling/data/raw/olist_order_payments_dataset.csv"
        path_olist_order_reviews = "/home/ander/Documentos/projetos/Olist_Data_Modeling/data/raw/olist_order_reviews_dataset.csv"
        path_olist_orders = "/home/ander/Documentos/projetos/Olist_Data_Modeling/data/raw/olist_orders_dataset.csv"
        path_olist_products = "/home/ander/Documentos/projetos/Olist_Data_Modeling/data/raw/olist_products_dataset.csv"
        path_olist_sellers = "/home/ander/Documentos/projetos/Olist_Data_Modeling/data/raw/olist_sellers_dataset.csv"
        path_product_category_name_translation = "/home/ander/Documentos/projetos/Olist_Data_Modeling/data/raw/product_category_name_translation.csv"

        # Lendo o arquivo CSV
        df_customers = pd.read_csv(path_customers)
        
        # Gerando o comando SQL para criar a tabela
        query = generate_create_table(df_customers, "customers")
        
        # Executando o comando SQL para criar a tabela
        execute_query(conexao, query)
        print("Tabela 'customers' criada com sucesso.")
        
        # Inserindo os dados manualmente no banco de dados
        cursor = conexao.cursor()
        for _, row in df_customers.iterrows():
            sql = """
            INSERT INTO customers (customer_id, customer_unique_id, customer_zip_code_prefix, customer_city, customer_state)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(sql, tuple(row))
        
        # Confirmar as alterações no banco de dados
        conexao.commit()
        cursor.close()
        print("Dados inseridos na tabela 'customers' com sucesso.")
    
    except Exception as e:
        print(f"Erro durante a ingestão: {e}")
    
    finally:
        # Fechando a conexão
        if conexao.is_connected():
            conexao.close()
            print("Conexão com o banco de dados encerrada.")