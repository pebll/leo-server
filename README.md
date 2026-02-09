# Léo's personal server

Currently running:

## Reverse proxy (caddy-service)

Runs the caddy image in docker container and routes all requests only through port 80 and 443.

## Landing page (website-service)

A very simple landing page (saying "Hi Leo")
Has its own Dockerfile installing python and uvicorn
Runs uvicorn in a docker container on Port 8000

## CardDAV Server (radicale-service)

A CardDAV server used to sync contacts served by Radicale.
The server runs a radicale image in a docker container on Port 5232

## Calavera server (calavera-server-service)

This is running the godot server for the calavera game
Has its own very simple Dockerfile just running the executable.
The server runs on port 9080
