import datetime
import re
from time import sleep, time
import json
import pandas as pd
from selenium.webdriver.common.keys import Keys
import random

from database.db import SQLiteDB

from driver import WebDriverManager

# from log.config_log import ApplicationLogger

# logger = ApplicationLogger()

with open('componentes.json', 'r') as file:
    WHATSAPP_COMPONENTS = json.load(file)

def format_datetime_for_csv(dt):
    return dt.strftime("%d/%m/%Y %H:%M") if pd.notnull(dt) else ""


def escolher_numero(row):
    colunas_telefone = ["TELEFONE_COMUNICACAO", "TELEFONE1", "TELEFONE2"]
    regex_numeros = re.compile(r"\D")
    for coluna in colunas_telefone:
        telefone = row[coluna]
        if pd.notnull(telefone) and str(telefone).strip() != "":
            telefone_limpo = re.sub(regex_numeros, "", str(telefone))
            return telefone_limpo
    return None


if __name__ == "__main__":
    df = pd.read_csv("OCORRENCIAS.csv", sep=";", dtype=object)
    # df = df[df['TELEFONE'] != 83999999999]
    df_ocorr = df.copy()
    df_ocorr["NUM_OCORRENCIA"] = df["ANO_OCORRENCIA"] + "-" + df["NUM_OCORRENCIA"]
    
    df_ocorr["TELEFONE1"] = (
        df_ocorr["TELEFONE1"]
        .astype(float)
        .astype("Int64")
    )
    df_ocorr["TELEFONE1"] = df_ocorr["TELEFONE1"].astype('str')
    df_ocorr["TELEFONE2"] = (
        df_ocorr["TELEFONE2"]
        .astype(float)
        .astype("Int64")
    )
    df_ocorr["TELEFONE2"] = df_ocorr["TELEFONE2"].astype('str')
    
    df_ocorr["TELEFONE_ESCOLHIDO"] = df_ocorr.apply(escolher_numero, axis=1)
    # df_ocorr["DH_INICIAL"] = pd.to_datetime(df["DH_INICIAL"], format="%d/%m/%Y %H:%M").dt.strftime("%d/%m")
    
    # Adição das Ocorrências no banco de dados
    db = SQLiteDB("databaseCOI.db")
    db.connect()
    db.create_tables()
    for index, row in df_ocorr.iterrows():
        columns = list(df_ocorr.columns)
        values = list(row)
        db.execute_insert("ocorrencias", columns, values)

    df_envio, colunas_envio = db.execute_query(
        "SELECT oc.* FROM ocorrencias oc left join envio on envio.num_ocorrencia = oc.num_ocorrencia where envio.num_ocorrencia is null"
    )


    df_envio = pd.DataFrame(df_envio, columns=colunas_envio)
    df_envio["data_hora"] = pd.to_datetime(
        df_envio["DH_INICIAL"],
        dayfirst=True,
        format="%d/%m/%Y %H:%M:%S",
        errors="coerce",
    )
    df_envio["data_atual"] = pd.Timestamp.now()
    df_envio["data_atual"] = pd.to_datetime(
        df_envio["data_atual"],
        dayfirst=True,
        format="%d/%m/%Y %H:%M",
        errors="coerce",
    )
    df_envio["ATRASO"] = (
        df_envio["data_atual"] - df_envio["data_hora"]
    ) / pd.Timedelta(hours=1)

    print(df_envio)
    # Inicia o Webdriver
    service = WebDriverManager()
    try:
        # Verifica se conseguimos acessar o site do whatsapp
        service.driver.get("https://web.whatsapp.com")
    except Exception as e:
        print(f"Erro ao abrir o site do https://web.whatsapp.com/: {str(e)}")
        # logger.log_error(f"Erro ao abrir o site do https://web.whatsapp.com/: {str(e)}")
        # logger.log_error("Fechando driver")

    for index, row in df_envio.iterrows():
        start_time = time()
        sleep((random.uniform(1, 10)))
        search_box = service.search_component(*WHATSAPP_COMPONENTS["search_box"])
        mensagem = (
            f"ENERGISA: Olá! Acompanharemos a solicitação de {row.DESCRICAO_SERVICO} para o cliente {row.NOMECSD} por esse meio.\n"
            "ATENÇÃO! Este contato destina-se apenas para o retorno da sua comunicação conosco. A Energisa não solicita informações pessoais ou realiza cobranças por este meio. Lembre-se de verificar o disjuntor que fica no seu medidor de energia! \n A sua energia já está normal?\n"
            f"Podemos considerar a sua solicitação de número {row.NUM_OCORRENCIA}, referente à {row.DESCRICAO_SERVICO}, para a Unidade Consumidora 5/{row.CDC_CLIENTE} registrada em nome do cliente {row.NOMECSD}, como resolvida e a energia normalizada?\n"
          )
        # mensagem = ""

        if search_box:
            print(
                "Componente search_box encontrado. Acessando pagina do contato"
            )

        else:
            print("Fechando driver")
            service.close_driver()

        sleep(1.5)

        nova_conversa = service.search_component(*WHATSAPP_COMPONENTS["nova_conversa"])
        nova_conversa.click()

        pesquisa_contato = service.search_component(
            *WHATSAPP_COMPONENTS["pesquisa_contato"]
        )
        pesquisa_contato.send_keys({row.TELEFONE_ESCOLHIDO})
        sleep(1.5)
        pesquisa_contato.send_keys(Keys.ENTER)
        sleep(1.5)

        message_box = service.fail_box_f(*WHATSAPP_COMPONENTS["message_box"])

        if not message_box:
            df_envio.loc[index, "SIT_WHATSAPP"] = "0"
            print("Componente message_box não encontrado")
            end_time = time()
            tempo = end_time - start_time
            df_envio.loc[index, "TEMP_ENVIO"] = tempo
            
            data_atual = datetime.datetime.now()
            data_formatada = data_atual.strftime("%d/%m/%Y")

            df_envio.loc[index, "DATA_ENVIO"] = data_formatada
            # Adicionado 23/07/2024, pois antes não era possível salvar os casos em que nao se encontrava o número do cliente.
            columns = df_envio[
            [
                "NUM_OCORRENCIA",
                "TELEFONE_ESCOLHIDO",
                "DATA_ENVIO",
                "SIT_WHATSAPP",
                "TEMP_ENVIO",
                "ATRASO"
            ]
            ].columns
            
            values = [
                df_envio.loc[index, "NUM_OCORRENCIA"],
                df_envio.loc[index, "TELEFONE_ESCOLHIDO"],
                df_envio.loc[index, "DATA_ENVIO"],
                df_envio.loc[index, "SIT_WHATSAPP"],
                df_envio.loc[index, "TEMP_ENVIO"],
                df_envio.loc[index, "ATRASO"]
            ]
            db.execute_insert("envio", columns, values)
        
            try:
                pesquisa_contato.send_keys(Keys.ESCAPE)
            except Exception:
                try:
                    message_box.send_keys(Keys.ESCAPE)
                except Exception:
                    continue
            continue

        df_envio.loc[index, "SIT_WHATSAPP"] = "1"

        service.send_keys(message_box, mensagem)


        message_box = service.fail_box_f(*WHATSAPP_COMPONENTS["message_box"])
        # print("encontrado")
        message_box.send_keys(Keys.ESCAPE)

        end_time = time()
        tempo = end_time - start_time
        data_atual = datetime.datetime.now()
        data_formatada = data_atual.strftime("%d/%m/%Y")

        df_envio.loc[index, "TEMP_ENVIO"] = tempo
        df_envio.loc[index, "DATA_ENVIO"] = data_formatada
        columns = df_envio[
            [
                "NUM_OCORRENCIA",
                "TELEFONE_ESCOLHIDO",
                "DATA_ENVIO",
                "SIT_WHATSAPP",
                "TEMP_ENVIO",
                "ATRASO"
            ]
        ].columns
        
        values = [
            df_envio.loc[index, "NUM_OCORRENCIA"],
            df_envio.loc[index, "TELEFONE_ESCOLHIDO"],

            df_envio.loc[index, "DATA_ENVIO"],
            df_envio.loc[index, "SIT_WHATSAPP"],
            df_envio.loc[index, "TEMP_ENVIO"],
            df_envio.loc[index, "ATRASO"]
        ]
        db.execute_insert("envio", columns, values)