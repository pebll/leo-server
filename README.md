# Léo's personal server

Currently running:

- A very simple landing page (saying "Hi Leo")
- A CardDAV server used to sync contacts served by Radicale

## Landing Page

TODO

## CardDAV Server

The server runs on Port 5232

User: pebll
Password: lel

### Setup steps ran on server:

- Install Radicale and Apache2 (for password)
`sudo apt update`
`sudo apt install radicale apache2-utils`
- Setup config
`cp ~/leo-server/CardDAV/config /etc/radicale/config`
- Create a new user (enter password twice)
`sudo htpasswd -B -c /etc/radicale/users pebll`
- Create storage folder and grant rights
`sudo mkdir -p /var/lib/radicale/collections`
`sudo chown -R radicale:radicale /var/lib/radicale/collections`
- Restart radicale
`sudo systemctl restart radicale`

