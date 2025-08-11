
from fastapi import FastAPI
from pydantic import BaseModel
from services.parsing_service import parse_address
from matching_service import match_address
from services.enrichment_service import enrich_address


app = FastAPI()

@app.get("/status")
def get_status():
    return {"status": "API çalışıyor"}

class AddressRequest(BaseModel):
    address: str

@app.post("/parse")
def parse(req: AddressRequest):
    return parse_address(req.address)

@app.post("/match")
def match(req: AddressRequest):
    return match_address(req.address)

@app.post("/enrich")
def enrich(req: AddressRequest):
    result = enrich_address(req.address)
    return result