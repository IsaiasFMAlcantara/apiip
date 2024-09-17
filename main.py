import os
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from ipv4 import calculate_ipv4
from ipv4binary import calculate_ipv4_binary

app = FastAPI()

class IPv4Request(BaseModel):
    ip: str
    subnet: str

@app.post("/calculate_ipv4")
def func_calcular_ipv4(request: IPv4Request):
    return calculate_ipv4(ip=request.ip, subnet=request.subnet)

@app.post("/calculate_ipv4_binary")
def func_calcular_ipv4_binary(request: IPv4Request):
    return calculate_ipv4_binary(ip=request.ip, subnet=request.subnet)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
