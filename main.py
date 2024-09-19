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
                raise ValueError('IP must be an IPv4 address')
        except ValueError:
            raise ValueError('Invalid IP address')
        return v

    @validator('subnet')
    def validate_subnet(cls, v):
        try:
            subnet = int(v)
            if not (0 <= subnet <= 32):
                raise ValueError('Subnet must be between 0 and 32')
        except ValueError:
            raise ValueError('Subnet must be an integer between 0 and 32')
        return v

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    errors = exc.errors()
    formatted_errors = [{"loc": error["loc"], "msg": error["msg"], "type": error["type"]} for error in errors]
    return JSONResponse(
        status_code=422,
        content={"detail": formatted_errors},
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error"},
    )

@app.post("/calculate_ipv4")
def func_calcular_ipv4(request: IPv4Request):
    try:
        result = calculate_ipv4(ip=request.ip, subnet=request.subnet)
    except ValueError as e:
        raise HTTPException(status_code=400, detail={"msg": str(e)})
    except Exception as e:
        raise HTTPException(status_code=500, detail={"msg": "Internal Server Error"})
    return result

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
