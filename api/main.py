from fastapi import FastAPI
from pydantic import BaseModel

# Import'ları try-except ile kontrol edelim
try:
    from services.parsing_service import parse_address
except ImportError:
    def parse_address(address):
        return {"error": "parsing_service bulunamadı", "address": address}

try:
    from matching_service import match_address
except ImportError:
    def match_address(address):
        return {"error": "matching_service bulunamadı", "address": address}

try:
    from enrichment_service import enrich_address
except ImportError:
    def enrich_address(address):
        return {"error": "enrichment_service bulunamadı", "address": address}

app = FastAPI()

@app.get("/status")
def get_status():
    return {"status": "API çalışıyor"}

class AddressRequest(BaseModel):
    address: str

@app.post("/abi")
def parse(req: AddressRequest):
    return parse_address(req.address)

@app.post("/match")
def match(req: AddressRequest):
    return match_address(req.address)

@app.post("/enrich")
def enrich(req: AddressRequest):
    result = enrich_address(req.address)
    return result

@app.post("/resolve_address")
def resolve_address(req: AddressRequest):
    # Tam iş akışı: Parse → Match → Enrich
    parsed = parse_address(req.address)
    matched = match_address(req.address)
    enriched = enrich_address(req.address)
    
    return {
        "input_address": req.address,
        "parsed": parsed,
        "matched": matched,
        "enriched": enriched,
        "status": "completed"
    }