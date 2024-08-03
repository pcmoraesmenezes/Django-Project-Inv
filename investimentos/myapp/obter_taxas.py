import gspread
from google.oauth2.service_account import Credentials
import requests
from time import sleep

def obter_taxa_selic():
    url = 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.11/dados/ultimos/1?formato=json'
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        taxa_selic = float(data[0]['valor'])
        print(f"Taxa Selic obtida: {taxa_selic}")
        return taxa_selic
    else:
        raise Exception(f"Erro ao obter taxa Selic: {response.status_code}")

def obter_taxa_cdi(max_retries=10):
    url = "https://brasilapi.com.br/api/taxas/v1"
    for attempt in range(max_retries):
        response = requests.get(url)
        if response.status_code == 200:
            try:
                taxas = response.json()
                for taxa in taxas:
                    if taxa['nome'] == 'CDI':
                        taxa_cdi_anual = float(taxa['valor']) / 100  
                        taxa_cdi_diaria = (1 + taxa_cdi_anual)**(1/252) - 1
                        print(f"Taxa CDI obtida (diária): {taxa_cdi_diaria * 100}")
                        return taxa_cdi_diaria * 100  # Convertendo para percentual
            except ValueError:
                raise Exception("Erro ao parsear a resposta JSON: " + response.text)
        else:
            print(f"Erro ao obter taxa CDI (tentativa {attempt + 1} de {max_retries}): {response.status_code}")
            sleep(1)
    
    raise Exception("Erro ao obter taxa CDI após várias tentativas.")

def obter_taxas():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_file('myapp/sheet-inv-c670b38614b5.json', scopes=scope)
    client = gspread.authorize(creds)

    spreadsheet = client.open_by_key('18HWYRTr--5Hw71h9wdLFODgf3JmzaHJZHiGckq-7auw')
    worksheet = spreadsheet.get_worksheet(1)  # Acessa a segunda aba (index 1)
    return worksheet


def atualizar_sheets(worksheet):

    selic = obter_taxa_selic()
    cdi = obter_taxa_cdi()

    try:
        print(f"Atualizando taxa CDI na planilha... {cdi:.8f}")
        worksheet.update_acell('A2', f"{cdi:.8f}".replace(".", ","))  # Substituindo ponto por vírgula
    except Exception as e:
        print(f"Erro ao atualizar CDI: {e}")
        return False

    try:
        print(f"Atualizando taxa Selic na planilha... {selic:.8f}")
        worksheet.update_acell('B2', f"{selic:.8f}".replace(".", ","))  # Substituindo ponto por vírgula
    except Exception as e:
        print(f"Erro ao atualizar Selic: {e}")
        return False

    return True


def obter_valores():
    worksheet = obter_taxas()
    cdi = worksheet.acell('A2').value
    selic = worksheet.acell('B2').value
    return cdi, selic


if __name__ == "__main__":
    worksheet = obter_taxas()
    atualizar_sheets(worksheet)
    print("Taxas atualizadas com sucesso!")