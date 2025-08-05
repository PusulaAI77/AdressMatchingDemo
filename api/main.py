
from fastapi import FastAPI
from pydantic import BaseModel
from services.parsing_service import parse_address

app = FastAPI()

@app.get("/status")
def get_status():
    return {"status": "API çalışıyor"}

class AddressRequest(BaseModel):
    address: str

@app.post("/parse")
def parse(req: AddressRequest):
    return parse_address(req.address)
