FROM python:3.11-alpine
WORKDIR /app

COPY ./kitkurs/web_visu/ ./web_visu/
COPY ./kitkurs/start.sh .

RUN chmod +x start.sh

EXPOSE 7777

CMD ["python3", "-m", "http.server", "7777", "-d", "web_visu"]
