from pydantic import BaseModel, validator
from fastapi import HTTPException
from ipaddress import ip_address

# Define o modelo de requisição para o cálculo de IPv4
class IPv4Request(BaseModel):
    ip: str  # Campo para o endereço IP
    subnet: str  # Campo para a máscara de sub-rede

    # Validador para o campo de IP
    @validator('ip')
    def validate_ip(cls, v):
        try:
            ip_obj = ip_address(v)  # Converte o valor de IP para um objeto de endereço IP
            if ip_obj.version != 4:  # Verifica se é um endereço IPv4
                raise HTTPException(
                    status_code=400,
                    detail={"mensagem": "O IP deve ser um endereco IPv4 valido"}
                )
        except ValueError:
            # Lança exceção se o IP for inválido
            raise HTTPException(
                status_code=400,
                detail={"mensagem": "Endereco IP invalido"}
            )
        return v

    # Validador para o campo de sub-rede
    @validator('subnet')
    def validate_subnet(cls, v):
        try:
            subnet = int(v)  # Converte a sub-rede para inteiro
            if not (0 <= subnet <= 32):  # Verifica se está entre 0 e 32
                raise HTTPException(
                    status_code=406,
                    detail={"mensagem": "A mascara de sub-rede deve estar entre 0 e 32"}
                )
        except ValueError:
            # Lança exceção se a sub-rede for inválida
            raise HTTPException(
                status_code=406,
                detail={"mensagem": "A mascara de sub-rede deve ser um numero inteiro entre 0 e 32"}
            )
        return v



class CalcIMC(BaseModel):
    peso: float
    genero: str
    altura: float

    @validator('genero')
    def validar_genero(cls, genero):
        if genero not in ['H', 'M']:
            raise ValueError('O gênero deve ser H (Homem) ou M (Mulher).')
        return genero

    @validator('peso')
    def validar_peso(cls, peso):
        if peso <= 0:
            raise ValueError('O peso deve ser um número maior que 0.')
        return peso

    @validator('altura')
    def validar_altura(cls, altura):
        if altura <= 0:
            raise ValueError('A altura deve ser um número maior que 0.')
        return altura
