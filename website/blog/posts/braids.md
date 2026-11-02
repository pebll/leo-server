---
date: '2026-10-31'
slug: braids
tags: []
title: braids
---

# Problem statement
So, in 2026, there are a lot of ways to communicate. WhatsApp, Signal, MS Teams, Slack, Snapchat, Insta, BeReal, Matrix, Telegram... the list is very long. Most of the stuff happens on WA, some on Signal, a little (but still important) on Telegram, and the Open Coding Stammtisch-related chats are all on Matrix. And I don't have a smartphone, only a flip phone with SMS.

While I would love to only communicate via one messenger, ideally Matrix or Signal, that's not how it works, and I have to adapt if I want to have some kind of social life.

So on my computer, I have: Whatsie (a Linux WhatsApp Web client), Signal Desktop, Telegram Desktop, and Element. This is annoying, as I need to autostart them all because otherwise I forget them and don't read messages for days (especially Signal & Telegram). Having 4 different messenger apps open on a computer is also quite annoying. Also, I have some contacts on multiple messengers, so the situation sometimes arises that I need to find something I sent or got sent, but I first need to figure out on which messenger.

Well, it works, but it's not really great.

Then Georg told me about nchat.

# nchat

nchat is short for "ncurses chat", a chat client for WhatsApp, Signal & Telegram that runs in the terminal. Genius! A unified inbox, unified client! I tried it, but quickly got overwhelmed by the terminal experience. While I love doing stuff in the terminal, using a messenger there is hard: no images, lots of shortcuts, hard to look at...
![cd60b4280107fc5c50ebc112e05c6b99.png](/blog/assets/braids/cd60b4280107fc5c50ebc112e05c6b99.png)
Also, I wanted Matrix integrated too, because going from 4 clients to 2 is very unsatisfying. At this point I want all of them in one. I researched a bit online, and found Beeper, which does exactly what nchat does but on steroids. Nice client, many more messengers available. While it had most of the features I wanted, a few things bothered me. I did not want to depend on more third-party servers for this (which actually hasn't been the case for a year now, I misread that), and our own Matrix homeserver wouldn't have been possible. And yeah, it's corporate, has a premium tier, and is closed source.

# Braids

So I set out to build it myself. I wanted nchat+:
- a nice GUI
- Matrix integration

Using Claude Code, this goes so fast. In ~2-3 days (absolutely not full time!), I've built braids. It's called that because I liked the idea of merging different chat streams into one. What I really like is the calm notification logo, which grows brighter over time:
![ceeb95b4ed4b4d6698dfc1c4dd3ba993.png](/blog/assets/braids/ceeb95b4ed4b4d6698dfc1c4dd3ba993.png)
Because that was also a thing that annoyed me with the desktop clients. The red dot would instantly catch my eye and make me click on it. This way it's much more discreet and doesn't force you to look at every new message in some random group you don't care about anyway.

Other great features:
- global search: now I can find what I want regardless of which messenger it was sent
- global media library: same as above, great to have all in one place
- forward from/to any messenger: this is great! Before, you had to copy the text from one messenger to the other, share the files again, very inconvenient.

Other than that, it works like you would expect from any messenger. And it works. It's so nice. I've been using braids for 2 days (while still adding features like voice messages & stickers & co) and it's really an improvement.

Braids is only available on Linux, but yeah, just switch to Linux if you haven't already.
Install it here: https://pebll.github.io/braids

![0e40195a7a8f2f669c747ee24979fd64.png](/blog/assets/braids/0e40195a7a8f2f669c747ee24979fd64.png)
