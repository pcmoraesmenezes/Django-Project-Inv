from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import APIKeyHeader
from obter_taxas import atualizar_planilha_cdi_selic, obter_taxas_selic_cdi_planilha
from funcs import view_data_from_sheet, update_data_from_sheet
from dotenv import load_dotenv
import os

load_dotenv()
chave = os.getenv('API_KEY')

app = FastAPI()

api_key_header = APIKeyHeader(name="api_key")

def validar_chave(api_key: str = Depends(api_key_header)):
    if api_key != chave:
        raise HTTPException(status_code=403, detail="Chave de API inválida")

@app.post("/atualizar_taxas")
async def atualizar_taxas(api_key: str = Depends(validar_chave)):
    """
    Essa função atualiza a planilha da taxa CDI e Selic.
    """
    worksheet = obter_taxas_selic_cdi_planilha()
    try:
        atualizar_planilha_cdi_selic(worksheet)
        return {"message": "Planilha atualizada com sucesso!"}
    except Exception as e:
        return {"message": f"Erro ao atualizar planilha: {e}"}
    

@app.get("/api/visualizar_dados_investimentos")
async def visualizar_dados_investimentos(api_key: str = Depends(validar_chave)):
    """
    Essa função retorna os dados da planilha de investimentos.
    """
    try:
        df = view_data_from_sheet()
        return {"message": "Dados obtidos com sucesso!", "data": df.to_dict()}
    except Exception as e:
        return {"message": f"Erro ao obter dados da planilha: {e}"}
    

@app.post("/api/atualizar_dados_investimentos")
async def atualizar_dados_investimentos(api_key: str = Depends(validar_chave)):
    """
    Essa função atualiza os dados da planilha de investimentos.
    """
    try:
        df = update_data_from_sheet()
        return {"message": "Dados atualizados com sucesso!", "data": df.to_dict()}
    except Exception as e:
        return {"message": f"Erro ao atualizar dados da planilha: {e}"}
