# Eltern-Image
FROM alpine:latest

# Setzen Sie des Arbeitsverzeichnis im Container
WORKDIR /app

# Kopieren des Inhalts des aktuellen Verzeichnisses in den Container im Verzeichnis /app
COPY . /app

# Installieren Sie alle benötigten Pakete, die in requirements.txt angegeben sind
RUN apk add python3 py3-pip
RUN apk add tree net-tools curl lynx vim iproute2
RUN tree

RUN python -m pip install --break-system-packages -r requirements.txt

# Definieren seiner Umgebungsvariablen
ENV NAME=World

WORKDIR src
# py server starten
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
EXPOSE 8000
