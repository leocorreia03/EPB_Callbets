import os
import sqlite3
from sqlite3 import Error

CURRENT_DIRECTORY = os.path.abspath(os.path.dirname(__file__))
TABLES_PATH = os.path.join(CURRENT_DIRECTORY, "tables")


class SQLiteDB:
    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = None

    def connect(self):
        try:
            self.conn = sqlite3.connect(self.db_file)
            print("Conexão com base de dados SQLite efetuada com sucesso.")
        except Error as e:
            print(f"Erro ao conectar com base de dados SQLite : {e}.")

    def disconnect(self):
        if self.conn:
            self.conn.close()
            print("Conexão com base de dados SQLite fechada com sucesso.")
        else:
            print("Erro ao desconectar com base de dados SQLite.")

    def create_tables(self):
        for table in os.listdir(TABLES_PATH):
            table = os.path.join(TABLES_PATH, table)
            table_name = os.path.basename(table)
            print(table_name)
            try:
                with open(table, "r") as script_file:
                    script = script_file.read()
                    cursor = self.conn.cursor()
                    cursor.executescript(script)
                    self.conn.commit()
                    print(f"Tabela {table_name} criada com sucesso.")
            except Error as e:
                print(f"Erro ao criar a tabela: {e}.")

    def execute_query(self, query, data=None):
        try:
            cursor = self.conn.cursor()
            if data:
                cursor.execute(query, data)
            else:
                cursor.execute(query)
            self.conn.commit()
            col_names = [desc[0] for desc in cursor.description]
            print("Query executada com sucesso")
            return cursor.fetchall(), col_names
        except Error as e:
            print(f"Error executando query: {e}")
            return None

    def execute_script_file(self, file_path):
        try:
            with open(file_path, "r") as script_file:
                script = script_file.read()
                cursor = self.conn.cursor()
                cursor.executescript(script)
                self.conn.commit()
                print("Script executado com sucesso")
        except Error as e:
            print(f"Erro ao executar o script: {e}")

    def execute_insert(self, table, columns, values, conflict_action="IGNORE"):
        try:
            cursor = self.conn.cursor()
            placeholders = ", ".join(["?" for _ in values])
            query = f"INSERT OR {conflict_action} INTO {table} ({', '.join(columns)}) VALUES ({placeholders})"
            cursor.execute(query, values)
            self.conn.commit()
            print("Inserção concluída com sucesso")
        except Error as e:
            print(f"Erro ao inserir: {e}")


if __name__ == "__main__":
    import pandas as pd

    df = pd.read_csv("OCORRENCIAS.csv", sep=";", dtype=object)
    df_ocorr = df.copy()
    df_ocorr["NUM_OCORRENCIA"] = df["ANO_OCORRENCIA"] + "-" + df["NUM_OCORRENCIA"]

    db = SQLiteDB("databaseCOI.db")
    db.connect()
    db.create_tables()
    for index, row in df_ocorr.iterrows():
        columns = list(df_ocorr.columns)
        values = list(row)
        db.execute_insert("ocorrencias", columns, values)

    df_envio, colunas_envio = db.execute_query(
        "SELECT oc.*, envio.num_ocorrencia FROM ocorrencias oc left join envio on envio.num_ocorrencia = oc.num_ocorrencia where envio.num_ocorrencia is null"
    )

    ## SIMULAR PREENCHIMENTO DA TABELA ENVIO
    ## PEGAR NUMERO DA OCORRENCIA, NOME, TELEFONE ESCOLHIDO, ESCOLHER ALEATORIAMENTE ENTRE 3, SE O TELEFONE EXISTE OU NÃO(SE EXISTE A MENSAGEM FOI ENVIADA).

    df_envio = pd.DataFrame(df_envio, columns=colunas_envio)
    df_envio = df_envio[["NUM_OCORRENCIA", "TELEFONE_OCORRENCIA"]]
    df_envio["SIT_WHATSAPP"] = 1
    df_envio["TEMP_ENVIO"] = 45
    df_envio["DATA_ENVIO"] = "08/05/2024 06:01:08"
    for index, row in df_envio.iterrows():
        columns = list(df_envio.columns)
        values = list(row)
        db.execute_insert("envio", columns, values)

    ## SIMULAR PREENCHIMENTO DA TABELA SITUACAO
    df_situacao, colunas_situacao = db.execute_query(
        "SELECT  * FROM envio where envio.SIT_WHATSAPP = 1"
    )  # Verificar regra para pegar apenas os envios do dia
    print(df_situacao)
    df_situacao = pd.DataFrame(df_situacao, columns=colunas_situacao)
    df_situacao = df_situacao[["NUM_OCORRENCIA"]]
    df_situacao["COD_ATENDIMENTO"] = 2  # 0,1,2,3
    df_situacao["ENQUETE_1"] = 1
    df_situacao["ENQUETE_2"] = 0
    df_situacao["ENQUETE_3"] = 1
    df_situacao["DESTINO_PRINT"] = "path"
    for index, row in df_situacao.iterrows():
        columns = list(df_situacao.columns)
        values = list(row)
        db.execute_insert("situacao", columns, values)

    db.disconnect()
