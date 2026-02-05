# Léo's personal server

Currently running:

- A very simple landing page (saying "Hi Leo")
- A CardDAV server used to sync contacts served by Radicale

## Landing Page

TODO

## CardDAV Server

The server runs on Port 5232

### Setup steps ran on server:

- Install Radicale
`sudo apt install radicale`
- Setup config
`cp ~/leo-server/CardDAV/config /etc/radicale/config`
- Create a new user (enter password twice)
`sudo htpasswd -B -c /etc/radicale/users pebll`
