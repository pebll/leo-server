---
title: Radicale
date: "2026-06-15"
tags: [self-hosting, thunderbird, docker]
slug: radicale
---

## The Problem

I use Thunderbird, I love it. The one problem I faced often is that my contacts are not synchronized, so on each device, I need to find the email address by looking in sent emails or so even if I already saved the contact on another device.

Since Thunderbird is an independent client, and IMAP/SMTP only transports email, there is no straightforward way to synchronize your contacts as it would be with for example Google or Outlook.

## The Solution

You need to actually host your own server that holds this contact information.

**What is Radicale:** A very simple Python server to synchronize CardDAV (contacts) and CalDAV (calendar) information across clients and back them up.

## How To

### Prerequisites

You need a server reachable through the internet: in my case I use my bwcloud VM and my léo.com domain name.

The easiest way is to attach the server through Docker, so having a reverse proxy already set up is very useful (I use Caddy).

### Radicale

A nice guy already made a Radicale Docker image, ready for import: [tomsquest/docker-radicale](https://github.com/tomsquest/docker-radicale).

So the process is very easy:

1. Add the Radicale image in your Docker Compose (see how I did it at [pebll/leo-server](https://github.com/pebll/leo-server)).
2. Create the necessary folder structure and config (see my repo also — I use password-encrypted authentication).
3. You will need to add a user and a password encrypted with bcrypt. To generate such a thing you will first need the Apache utils package (`apt install apache2-utils` or similar).
4. Then just use:

   ```bash
   htpasswd -c -B /radicale/config/users your_username
   ```

   and enter your desired password twice. This will generate the password file.

   - `-c` means create new (omit if adding a second user)
   - `-B` means using the bcrypt algorithm — it won't work without it
5. Make a new DNS record for your desired domain name (in my case `radicale.léo.com`).
6. In the Caddyfile, add a route to the Radicale container:

   ```caddy
   radicale.léo.com {
     reverse_proxy radicale-service:5232
   }
   ```

7. This should be everything. Now you can visit your website in the browser, connect with user and password, and upload your CardDAV file (create new or upload an existing one by downloading from your Thunderbird client).
8. Then just go into Thunderbird → Address Books → create new → CardDAV, enter URL, user and password — and here you go!

## The Result

All my clients are now synced and I am very happy!
