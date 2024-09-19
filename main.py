import os
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, validator
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from ipaddress import ip_address
from ipv4 import calculate_ipv4

app = FastAPI()

origins = [
    "http://localhost:8000",
    "https://calcip-bn6s2x.flutterflow.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)

class IPv4Request(BaseModel):
    ip: str
    subnet: str

    @validator('ip')
    def validate_ip(cls, v):
        try:
            ip_obj = ip_address(v)
            if ip_obj.version != 4:
                raise HTTPException(
                    status_code=400,  # Erro específico para o IP
                    detail={
                        "mensagem": "O IP deve ser um endereço IPv4 válido"
                    }
                )
        except ValueError:
            raise HTTPException(
                status_code=400,  # Erro de IP inválido
                detail={
                    "mensagem": "Endereço IP inválido"
                }
            )
        return v

    @validator('subnet')
    def validate_subnet(cls, v):
        try:
            subnet = int(v)
            if not (0 <= subnet <= 32):
                raise HTTPException(
                    status_code=406,  # Erro específico para a máscara de sub-rede
                    detail={
                        "mensagem": "A máscara de sub-rede deve estar entre 0 e 32"
                    }
                )
        except ValueError:
            raise HTTPException(
                status_code=406,  # Erro específico para a máscara de sub-rede
                detail={
                    "mensagem": "A máscara de sub-rede deve ser um número inteiro entre 0 e 32"
                }
            )
        return v

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    errors = exc.errors()
    formatted_errors = [{"loc": error["loc"], "msg": error["msg"], "type": error["type"]} for error in errors]
    return JSONResponse(
        status_code=422,
        content={
            "mensagem": "Erro de validação nos dados fornecidos",
            "detalhes": formatted_errors
        },
    )

@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "mensagem": exc.detail["mensagem"]
        },
    )

@app.post("/calcular_ipv4")
def func_calcular_ipv4(request: IPv4Request):
    try:
        result = calculate_ipv4(ip=request.ip, subnet=request.subnet)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,  # Retorna 500 para erro interno do servidor
            detail={
                "mensagem": "Erro interno do servidor",
                "detalhes": str(e)
            }
        )
    return {
        "mensagem": "Calculo realizado com sucesso",
        "resultado": result
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
