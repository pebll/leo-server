FROM python:3.11-slim
WORKDIR /app
# Install stockfish
RUN apt-get update && apt-get install -y stockfish && rm -rf /var/lib/apt/lists/*
# Copy python dependencies
COPY ./elo-estimator/requirements.txt .
COPY ./elo-estimator/setup.py .
COPY ./elo-estimator/elo_ai ./elo_ai
# install cpu torch
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu
# install other packages from PyPi
RUN pip install --no-cache-dir -r requirements.txt && pip install gunicorn
# Copy rest
COPY ./elo-estimator/ .
WORKDIR /app/web
EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "1", "--threads", "1", "app:app"]
