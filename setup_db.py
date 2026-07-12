import psycopg2
from database import get_connection

def create_tables():
    conn = get_connection()
    if conn is None:
        print("Erro: Não foi possível conectar ao banco de dados para criar as tabelas.")
        return

    commands = (
        """
        CREATE TABLE IF NOT EXISTS notas_fiscais (
            id SERIAL PRIMARY KEY,
            data DATE NOT NULL,
            valor NUMERIC(10, 2) NOT NULL,
            categoria VARCHAR(255) NOT NULL,
            descricao TEXT,
            url_imagem VARCHAR(500)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS jovens_missao (
            id SERIAL PRIMARY KEY,
            nome VARCHAR(255) NOT NULL,
            idade INTEGER,
            status_processo VARCHAR(255),
            data_prevista DATE
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS rapazes (
            id SERIAL PRIMARY KEY,
            nome VARCHAR(255) NOT NULL,
            idade INTEGER,
            frequencia_sacramental INTEGER,
            observacoes TEXT
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS mocas (
            id SERIAL PRIMARY KEY,
            nome VARCHAR(255) NOT NULL,
            idade INTEGER,
            frequencia_sacramental INTEGER,
            observacoes TEXT
        )
        """
    )

    try:
        with conn.cursor() as cur:
            for command in commands:
                cur.execute(command)
        conn.commit()
        print("Tabelas criadas com sucesso (ou já existiam).")
    except Exception as e:
        print(f"Erro ao criar tabelas: {e}")
    finally:
        conn.close()

if __name__ == '__main__':
    create_tables()
