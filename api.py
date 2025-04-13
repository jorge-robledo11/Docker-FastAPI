from fastapi import FastAPI
from autogluon.tabular import TabularPredictor
import pandas as pd
import uvicorn
from typing import Optional
from pydantic import BaseModel
import asyncio

app = FastAPI()

# Carga el predictor al iniciar la aplicación
MODEL_PATH = 'runs/'
predictor = TabularPredictor.load(MODEL_PATH)

class DataPoint(BaseModel):
    state: str
    city: str
    local_pickup: bool
    free_shipping: bool
    shipping_mode: str
    listing_type: str
    buying_mode: str
    attribute_group_id: Optional[str] = None
    attribute_group: Optional[str] = None
    attribute_id: Optional[str] = None
    status: str
    accepts_mercadopago: bool
    currency: str
    automatic_relist: bool
    stock_quantity: int
    available_quantity: int
    total_amount: float
    date_difference_hr: float
    time_difference_hr: float

@app.post('/predict')
async def predict_endpoint(datapoint: DataPoint):
    # Ejecuta la predicción en un thread para que no bloquee el event loop
    data_df = pd.DataFrame([datapoint.model_dump()])
    
    # Usa asyncio.to_thread para correr la inferencia de forma asíncrona
    prediction = await asyncio.to_thread(predictor.predict, data_df)
    # Como predictor.predict devuelve un DataFrame, extraemos la predicción
    return {'prediction': prediction.iloc[0]}

if __name__ == '__main__':
    uvicorn.run(
        app=app, 
        host='0.0.0.0', 
        port=5000
    )
