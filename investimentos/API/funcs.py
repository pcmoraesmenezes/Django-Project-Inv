import os
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from time import sleep
from taxas import cdi, selic

def inicializar():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_file('sheet-inv-c670b38614b5.json', scopes=scope)
    client = gspread.authorize(creds)
    spreadsheet = client.open_by_key('18HWYRTr--5Hw71h9wdLFODgf3JmzaHJZHiGckq-7auw')
    worksheet = spreadsheet.sheet1
    return worksheet

def atualizar_tempo_de_aplicacao(df):
    data_inicial = df['Data']
    data_atual = pd.to_datetime('today')
    tempo_de_aplicacao = data_atual - pd.to_datetime(data_inicial, dayfirst=True)
    df['Tempo de Aplicação'] = tempo_de_aplicacao.dt.days - 1
    aux = df['Tempo de Aplicação'].astype(int)
    print(f'Tipo: {type(aux)}')
    return aux

def calcular_taxa_de_retorno(taxa_retorno):    
    if 'Selic' in taxa_retorno:
        taxa_valor = float(taxa_retorno.split('+')[1].replace('%', '').strip()) / 100
        return selic + taxa_valor
    elif 'CDI' in taxa_retorno:
        taxa_valor = float(taxa_retorno.replace('% CDI', '').strip()) / 100
        return cdi * taxa_valor
    else:
        return None

def calcular_valor_atual(df):
    aux = df.copy()
    aux['Taxa Efetiva'] = aux['Taxa de Retorno'].apply(calcular_taxa_de_retorno)
    aux['Valor'] = aux['Valor'].astype(float)  
    aux['Imposto'] = aux['Imposto'].astype(float)  
    aux['Tempo de Aplicacao'] = atualizar_tempo_de_aplicacao(aux).astype(int)

    def calcular_valor(row):
        valor_investido = row['Valor']
        taxa_efetiva_anual = row['Taxa Efetiva']
        imposto = row['Imposto']
        dias = row['Tempo de Aplicacao']

        if 'CDI' in row['Taxa de Retorno']:
            taxa_cdi_diaria = (1 + cdi) ** (1 / 252) - 1
            taxa_efetiva_diaria = taxa_cdi_diaria * (taxa_efetiva_anual / cdi)
        else:
            taxa_selic_diaria = (1 + selic) ** (1 / 252) - 1
            taxa_adicional_diaria = (taxa_efetiva_anual - selic) / 252
            taxa_efetiva_diaria = (1 + taxa_selic_diaria) * (1 + taxa_adicional_diaria) - 1

        rendimento_bruto = valor_investido * (1 + taxa_efetiva_diaria) ** dias

        imposto_renda = imposto * (rendimento_bruto - valor_investido)

        valor_liquido = rendimento_bruto - imposto_renda

        return valor_liquido

    aux['Valor Atual'] = aux.apply(calcular_valor, axis=1)
    return aux['Valor Atual']

def atualizar_sheets(worksheet, df, max_retries=10):
    aux = df.copy()
    aux['Valor'] = pd.to_numeric(aux['Valor'], errors='coerce')
    aux['Tempo de Aplicacao'] = atualizar_tempo_de_aplicacao(df)
    aux['Valor Atual'] = calcular_valor_atual(df)
    aux['Ganhos'] = aux['Valor Atual'] - aux['Valor']

    tempo_de_aplicacao = aux['Tempo de Aplicacao']
    valor_atual = aux['Valor Atual']
    ganhos = aux['Ganhos']

    print(tempo_de_aplicacao, valor_atual, ganhos)    
    
    cell_range_tempo = f'G2:G{len(df) + 1}'
    cell_list_tempo = worksheet.range(cell_range_tempo)
    for i, cell in enumerate(cell_list_tempo):
        cell.value = int(tempo_de_aplicacao.iloc[i])

    cell_range_valor = f'H2:H{len(df) + 1}'
    cell_list_valor = worksheet.range(cell_range_valor)
    for i, cell in enumerate(cell_list_valor):
        cell.value = float(valor_atual.iloc[i])

    cell_range_ganhos = f'I2:I{len(df) + 1}'
    cell_list_ganhos = worksheet.range(cell_range_ganhos)
    for i, cell in enumerate(cell_list_ganhos):
        cell.value = float(ganhos.iloc[i])

    def try_update_cells(cell_list):
        for attempt in range(max_retries):
            try:
                worksheet.update_cells(cell_list)
                return True 
            except Exception as e:
                print(f"Erro ao atualizar células na tentativa {attempt + 1}: {e}")
                if attempt < max_retries - 1:
                    sleep(2)
        return False

    if not try_update_cells(cell_list_tempo):
        print("Falha ao atualizar Tempo de Aplicação após várias tentativas.")
    if not try_update_cells(cell_list_valor):
        print("Falha ao atualizar Valor Atual após várias tentativas.")
    if not try_update_cells(cell_list_ganhos):
        print("Falha ao atualizar Ganhos após várias tentativas.")


def view_data_from_sheet():
    worksheet = inicializar()
    data = worksheet.get_all_values()
    df = pd.DataFrame(data[1:], columns=data[0])
    return df

def update_data_from_sheet():
    worksheet = inicializar()
    data = worksheet.get_all_values()
    df = pd.DataFrame(data[1:], columns=data[0])
    atualizar_sheets(worksheet, df)
    return df

update_data_from_sheet()