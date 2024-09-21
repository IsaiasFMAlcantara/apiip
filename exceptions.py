from fastapi.exceptions import RequestValidationError
from fastapi import HTTPException
from fastapi.responses import JSONResponse

# Manipulador de exceção para erros de validação de requisição
async def validation_exception_handler(request, exc: RequestValidationError):
    errors = exc.errors()
    formatted_errors = [{"loc": error["loc"], "msg": error["msg"], "type": error["type"]} for error in errors]
    # Retorna uma resposta JSON personalizada para erros de validação
    return JSONResponse(
        status_code=422,
        content={
            "mensagem": "Erro de validação nos dados fornecidos",
            "detalhes": formatted_errors
        },
    )

# Manipulador de exceção para erros HTTP personalizados
async def custom_http_exception_handler(request, exc: HTTPException):
    # Retorna uma resposta JSON personalizada com o código de status e a mensagem de erro
    return JSONResponse(
        status_code=exc.status_code,
        content={"mensagem": exc.detail["mensagem"]},
    )
