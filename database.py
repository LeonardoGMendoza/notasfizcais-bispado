import os
import psycopg2
from psycopg2.extras import RealDictCursor
import pandas as pd
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "bispado_db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")

def get_connection():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        return conn
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

def fetch_data(query, params=None):
    conn = get_connection()
    if conn is None:
        return pd.DataFrame()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, params)
            rows = cur.fetchall()
            df = pd.DataFrame(rows)
            return df
    except Exception as e:
        print(f"Erro ao buscar dados: {e}")
        return pd.DataFrame()
    finally:
        conn.close()

def execute_query(query, params=None):
    """Executa INSERT/UPDATE/DELETE e retorna True se bem-sucedido."""
    conn = get_connection()
    if conn is None:
        return False
    try:
        with conn.cursor() as cur:
            cur.execute(query, params)
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        print(f"Erro ao executar query: {e}")
        return False
    finally:
        conn.close()

def get_notas_fiscais():
    query = "SELECT * FROM notas_fiscais ORDER BY data DESC;"
    return fetch_data(query)

def get_jovens_missao():
    query = "SELECT * FROM jovens_missao ORDER BY data_prevista ASC;"
    return fetch_data(query)

def inserir_missionario(nome, idade, status_processo, data_prevista):
    query = """
        INSERT INTO jovens_missao (nome, idade, status_processo, data_prevista)
        VALUES (%s, %s, %s, %s);
    """
    return execute_query(query, (nome, idade, status_processo, data_prevista))

def deletar_missionario(id_missao):
    query = "DELETE FROM jovens_missao WHERE id = %s;"
    return execute_query(query, (id_missao,))

def atualizar_status_missionario(id_missao, novo_status):
    query = "UPDATE jovens_missao SET status_processo = %s WHERE id = %s;"
    return execute_query(query, (novo_status, id_missao))

def get_rapazes():
    query = "SELECT * FROM rapazes ORDER BY nome ASC;"
    return fetch_data(query)

def get_mocas():
    query = "SELECT * FROM mocas ORDER BY nome ASC;"
    return fetch_data(query)
