import pandas as pd
import numpy as np
import asyncio
import aiohttp

# Carga el dataset desde data/test_data.parquet
data = pd.read_parquet('data/test_data.parquet')

np.random.seed(77)
size = 100
rows = np.random.randint(0, data.shape[0], size=size)
datapoints = data.iloc[rows, 1:].to_dict(orient='records')

# URL del endpoint predict de la API
url = "http://127.0.0.1:5000/predict"

async def send_request(session, data):
    # Simula un retraso aleatorio entre 0.5 y 3 segundos
    delay = np.random.uniform(0.5, 3)
    await asyncio.sleep(delay)
    
    try:
        # Establece un timeout (10 segundos) para la solicitud
        async with session.post(url, json=data, timeout=10) as response:
            return await response.json()
    except Exception as e:
        return {"error": str(e)}

async def main():
    async with aiohttp.ClientSession() as session:
        # Crea tareas asíncronas para enviar todas las solicitudes concurrentemente
        tasks = [send_request(session, datapoint) for datapoint in datapoints]
        responses = await asyncio.gather(*tasks)
        for res in responses:
            print("Respuesta solicitud:", res)

if __name__ == "__main__":
    # Ejecuta la corrutina principal usando asyncio.run
    asyncio.run(main())
