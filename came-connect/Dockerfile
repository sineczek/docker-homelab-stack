FROM python:3.8-slim

# Ustaw katalog roboczy
WORKDIR /app

# Skopiuj wszystkie pliki repo
COPY . /app

# Zainstaluj pip, pakiety systemowe i Python dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential \
       python3-pip \
       ca-certificates \
       apt-transport-https \
       curl \
    && rm -rf /var/lib/apt/lists/* \
    \
    # Zaktualizuj pip i zainstaluj wymagane pakiety Pythona
    && pip3 install --upgrade pip --default-timeout=100 \
    && pip3 install --default-timeout=100 \
       requests \
       httpx \
       uvicorn[standard] \
       pydantic \
       websockets \
       web.py

# Otwórz port, na którym bridge wystawia REST API
EXPOSE 8080

# Uruchom bridge
CMD ["python3", "main.py", "0.0.0.0", "8080"]
