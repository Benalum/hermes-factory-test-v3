from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class CalculationRequest(BaseModel):
    a: float
    b: float

class CalculationResponse(BaseModel):
    result: float

@app.post("/add", response_model=CalculationResponse)
async def add(req: CalculationRequest):
    return CalculationResponse(result=req.a + req.b)

@app.post("/subtract", response_model=CalculationResponse)
async def subtract(req: CalculationRequest):
    return CalculationResponse(result=req.a - req.b)

@app.post("/multiply", response_model=CalculationResponse)
async def multiply(req: CalculationRequest):
    return CalculationResponse(result=req.a * req.b)

@app.post("/divide", response_model=CalculationResponse)
async def divide(req: CalculationRequest):
    if req.b == 0:
        raise HTTPException(status_code=400, detail="Division by zero")
    return CalculationResponse(result=req.a / req.b)
