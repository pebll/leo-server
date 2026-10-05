FROM python:3.11-alpine
WORKDIR /app

COPY ./kitkurs/web_visu/ ./web_visu/
COPY ./kitkurs/server.py .

EXPOSE 7777

# Serves the static app plus the account API; accounts live in /app/data (volume)
CMD ["python3", "server.py", "7777", "--db", "/app/data/kitkurs.db"]
