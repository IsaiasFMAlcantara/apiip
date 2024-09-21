import os
import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import IPv4Request, CalcIMC  # Importa o modelo de requisição
from services import calculate_ipv4,calcular_imc  # Importa a lógica de cálculo de IPv4
from exceptions import validation_exception_handler, custom_http_exception_handler  # Manipuladores de exceção

# Inicializa a aplicação FastAPI
app = FastAPI()

# Define as origens permitidas para o CORS (Cross-Origin Resource Sharing)
origins = [
    "http://localhost:8000",  # Permite chamadas do localhost
    "https://calcip-bn6s2x.flutterflow.app",  # Permite chamadas do aplicativo FlutterFlow
    "https://teste-53pnl4.flutterflow.app"
]

# Configura o middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Permite apenas as origens definidas
    allow_credentials=True,  # Permite o uso de cookies e credenciais
    allow_methods=["POST"],  # Permite apenas o método POST
    allow_headers=["*"],  # Permite todos os cabeçalhos
)

# Define manipuladores de exceção personalizados para a aplicação
app.exception_handler(RequestValidationError)(validation_exception_handler)
app.exception_handler(HTTPException)(custom_http_exception_handler)

# Endpoint para calcular o IPv4
@app.post("/calcular_ipv4")
def func_calcular_ipv4(request: IPv4Request):
    # Tenta executar a função de cálculo do IPv4
    try:
        result = calculate_ipv4(ip=request.ip, subnet=request.subnet)
    except HTTPException as e:
        raise e  # Lança exceções específicas para erros de IP e máscara
    except Exception as e:
        # Trata erros internos do servidor
        raise HTTPException(
            status_code=500,
            detail={
                "mensagem": "Erro interno do servidor, tente novamente mais tarde",
                "detalhes": str(e)
            }
        )
    # Retorna a mensagem de sucesso e o resultado do cálculo
    return {"mensagem": "Calculo realizado com sucesso", "resultado": result}

@app.post("/calcular_imc")
def func_calcular_imc(request: CalcIMC):

    try:
        resultado = calcular_imc(genero=request.genero,peso=request.peso,altura=request.altura)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "mensagem": "Erro interno do servidor, tente novamente mais tarde",
                "detalhes": str(e)
            }
        )
    return {
        'mensagem':'Calculo realizado com sucesso',
        'resultado':resultado
    }

# Inicializa o servidor Uvicorn, usando o valor da variável PORT ou 8000 por padrão
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
