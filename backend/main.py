from fastapi import FastAPI
from qiskit import QuantumCircuit

app = FastAPI()

@app.get("/nft")
async def get_nft_info():
    return {"message": "Información sobre NFTs cuánticos"}

@app.get("/blockchain")
async def get_blockchain_info():
    return {"message": "Información sobre blockchain cuántica"}

# Integración futura de AI cuántica inteligente
@app.get("/quantum-ai")
async def quantum_ai_integration():
    return {"message": "Soporte para AI cuántica inteligente"}