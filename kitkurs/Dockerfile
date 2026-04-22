FROM python:3.11-alpine
WORKDIR /app

COPY ./kitkurs/web_visu/ ./web_visu/
COPY ./kitkurs/start.sh .

RUN chmod +x start.sh

EXPOSE 7777

CMD ["sh", "start.sh"]
