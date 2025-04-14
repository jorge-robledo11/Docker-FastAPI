import os
import pandas as pd
import numpy as np
import asyncio
import aiohttp

# Lee el host del servidor desde la variable de entorno, con "server" como valor por defecto
SERVER_HOST = os.getenv("SERVER_HOST", "server")
url = f"http://{SERVER_HOST}:5000/predict"

data = pd.read_parquet('data/test_data.parquet')
np.random.seed(77)
size = 100
rows = np.random.randint(0, data.shape[0], size=size)
datapoints = data.iloc[rows, 1:].to_dict(orient='records')

async def send_request(session, data):
    delay = np.random.uniform(0.5, 3)
    await asyncio.sleep(delay)
    try:
        async with session.post(url, json=data, timeout=10) as response:
            return await response.json()
    except Exception as e:
        return {"error": str(e)}

async def main():
    async with aiohttp.ClientSession() as session:
        tasks = [send_request(session, peticion) for peticion in datapoints]
        responses = await asyncio.gather(*tasks)
        for res in responses:
            print("Respuesta solicitud:", res)

if __name__ == "__main__":
    asyncio.run(main())
