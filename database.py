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

def get_notas_fiscais():
    query = "SELECT * FROM notas_fiscais ORDER BY data DESC;"
    return fetch_data(query)

def get_jovens_missao():
    query = "SELECT * FROM jovens_missao ORDER BY data_prevista ASC;"
    return fetch_data(query)

def get_rapazes():
    query = "SELECT * FROM rapazes ORDER BY nome ASC;"
    return fetch_data(query)

def get_mocas():
    query = "SELECT * FROM mocas ORDER BY nome ASC;"
    return fetch_data(query)
