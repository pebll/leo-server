---
title: "Global Game Jam 2026 - Calavera"
date: "2026-02-14"
tags: [gamedev, networking]
slug: global-game-jam-2026-calavera
---

The Global Game Jam is a game jam with a special twist. It is global in the sense that everyone in the world participates in the same jam, with the same theme. But this usually also means that the jam is completely online, and the feeling of a "hackathon" is kind of lost. The GGJ has the unique feature that it organizes local events all around the world — also in Karlsruhe, where we even had two!

Our team of three — Jan, Léo and Georg — chose to participate in the event organized by the Godot Stammtisch, a nice group of people that love gamedev and Godot. The jam started on Friday the 30th at 18h, and there we got the theme of this year's jam: **Mask**. We started brainstorming lots of ideas.

One idea: a game set in a dystopian world in the style of *1984*, where security cameras of an autocratic government track the population constantly. People have gotten used to wearing masks of all kinds and colors to confuse the cameras and escape automatic face recognition. A secret rebel agency needs to perform missions to weaken the government — but beware, the cameras can still track and remember your mask! Your goal as a secret agent is to switch and edit your mask to confuse the cameras and not get caught in your illegal actions.

Another idea: a medieval Venetian masked ball. People dancing happily, but hidden among the dancers are assassins and kings. Backstabbing vibes. Never knowing if your dancing neighbour is just an innocent noblewoman or a disguised mercenary plotting to murder you. Played on a simple grid, you would play against another human, but each would not know where the other's characters are.

This is the idea we went for in the end, since it is very simple, and we already had a simple grid + character movement system set up. Moreover, it required multiplayer — a thing that makes each game developer wake sweaty after a nightmare about it. So it was time to demystify this theory and try to implement the simplest version of multiplayer there can be: just send moves across, no need to worry about timing, performance, etc.

So up we went, and that first evening we did not make it too far. Come the next day, the meat of the project. Léo started to take care of multiplayer, Jan of implementing logic, and Georg went wild and started designing the dancers.

What do these three have to say about their experience?

**Léo:** Actually, Godot already has a very simple and intuitive high-level multiplayer system. I first used some public repo of a simple matchmaking example, made for peer-to-peer multiplayer. That was indeed much simpler, because this would cut entirely the need for a server. It took some time to figure out what data to send and how to synchronize turns and movements, but in the end it worked pretty well after a day of work.

**Jan:** never answered the call :_(

**Georg:** There was not a lot of time! But the pizza was nice and had slices of delicious things on it. I learned there is an onion technique for animation and apparently I used it (?).

At the end of the day, basic multiplayer existed and raw first logic existed, and first games were playable — although it was not yet very fun.

The third and last day was mainly: implement the last logic features, implement the art that Georg so well made the day before, implement sounds and music, menu and polish. This was a lot and we worked hard until the end. We got the artwork to work; the visuals got a final sketchy overhaul to not look like default grey blocks. Logic side, we actually managed to implement all the features we had defined the first day. The code became a hugeee pile of spaghetti which never ever would be maintainable — but since we just accepted the fact, it was still very easy to hack in some features, and it also was quite fun. Georg and Jan implemented some very cool homemade background music, and Jan implemented cool sounds for all the effects. What came out of the last day was a finished game. Notice the *finished*. That is very unusual for gamedev projects, and that's why game jams are so cool.

Only sad problem we realised when pushing the web version to itch: the peer-to-peer code did not work inside the browser… firewalls and what do I know. So since we didn't have any singleplayer, the only way to play was to download the Win or Linux version and have a friend who did the same.

So one week later, I set out on a mission: make it playable over the world wide web. I set up my own server to host the Calavera game server. It took a few days but went pretty smooth.

Here's what I've written after finishing it:

> It works! It works!
>
> We made this game for the Global Game Jam 2026 (GGJ) last week (3 people in 48 hours). The theme was "mask", not too hard to guess. We used Godot for the first time for 2 of our devs, and for the first time also integrated multiplayer! During the jam, we implemented peer-to-peer LAN multiplayer, since this was much simpler and did not require a server. It worked very well in the editor.
>
> But then, 20 mins left, we upload our project to the web and have a sudden realization. It does not work in the browser… since the browser has proxies and what do I know that blocked our LAN communication :(
>
> During the last week, I wanted one thing: make it playable! So I migrated the project to use instead server-client multiplayer via a websocket. I set up my personal website (léo.com) which I wanted to do for a long time, and hosted the server for the game there. And it works!! Here is the result!
>
> To the development of the game itself: it was very much fun, we did not do much else except work on this project for the whole 48 hours and we are very happy with the results. The code grew messier minute by minute in the hours approaching the deadline, and the commit messages more random than ever, but we managed to implement all the features we had defined on the first day. Also we managed to implement the whole art style only in the last day, which came out quite nice.

So yes. It was a very very cool experience where we all learned a lot!
