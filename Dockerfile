# ============================
# Stage 1: Builder
# ============================
FROM python:3.12.9-slim-bookworm as builder

# Instala dependencias de sistema necesarias (por ejemplo, libgomp1 para LightGBM)
RUN apt-get update && apt-get install -y libgomp1 && apt-get clean

WORKDIR /app

# Instala Poetry globalmente
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir poetry

# Copia solo los archivos de configuración de Poetry para aprovechar la caché
COPY pyproject.toml poetry.lock /app/

# Configura Poetry para no crear virtualenv y exporta las dependencias a requirements.txt
RUN poetry config virtualenvs.create false \
    && poetry export --without-hashes -f requirements.txt -o requirements.txt

# ============================
# Stage 2: Final image
# ============================
FROM python:3.12.9-slim-bookworm

# Instala también las dependencias de sistema necesarias (libgomp1)
RUN apt-get update && apt-get install -y libgomp1 && apt-get clean

WORKDIR /app

# Copia el archivo con las dependencias generado en el builder
COPY --from=builder /app/requirements.txt /app/

# Instala las dependencias en la imagen final
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copia el resto del código y assets (servidor.py, cliente.py, runs/, data/, etc.)
COPY . /app/

# Expone el puerto 5000 para la API
EXPOSE 5000

# Comando para arrancar el servidor y luego ejecutar el cliente (para pruebas)
CMD ["sh", "-c", "uvicorn servidor:app --host 0.0.0.0 --port 5000 & python cliente.py"]
