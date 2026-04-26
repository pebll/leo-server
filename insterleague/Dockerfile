FROM node:18-alpine

WORKDIR /app

COPY ./insterfreestyle-league/package*.json ./
RUN npm install --production

COPY ./insterfreestyle-league/ ./


EXPOSE 3000

CMD ["node", "server.js"]
