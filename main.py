from fastapi import FastAPI
from pydantic import BaseModel
from ipv4 import calculate_ipv4
from ipv4binary import calculate_ipv4_binary

class IPv4Request(BaseModel):
    ip: str
    subnet: str

app = FastAPI()

@app.post("/calculate_ipv4")
def func_calcular_ipv4(request: IPv4Request):
    return calculate_ipv4(ip=request.ip, subnet=request.subnet)

@app.post("/calculate_ipv4_binary")
def func_calcular_ipv4_binary(request: IPv4Request):
    return calculate_ipv4_binary(ip=request.ip, subnet=request.subnet)
