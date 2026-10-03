---
date: '2026-10-03'
slug: wg-gefunden
tags:
- project
- software
title: WG Gefunden!
---

# Finding a WG is hard

I never had to move out and find a WG. For that I am lucky. Yet for many of my acquaintances, who had to find a new place, I could hear that it is really not that easy. In Karlsruhe, it's difficult, but manageable. In some other cities, it's a nightmare...

For example Munich. My brother who is moving there for his master's did search for a long time and while running out of time and options he had to settle for a very expensive and weird Zweck-WG. Arriving there on October 1st was a shock, totally dirty, broken, and with walls so thin that you can hear your roomie talk in his room.

<div style="display: flex; gap: 1em; justify-content: center; flex-wrap: wrap;">
<img src="/blog/assets/wg-gefunden/signal-2026-10-01-20-52-19-618_002.jpg" alt="signal-2026-10-01-20-52-19-618_002.jpg" width="225" height="300">
<img src="/blog/assets/wg-gefunden/signal-2026-10-01-20-52-19-618_005.jpg" alt="signal-2026-10-01-20-52-19-618_005.jpg" width="225" height="300">
</div>

This is horrible. It was clear that he could not live there and would need to find a new WG. So, in this need, I thought that there would be probably a way to improve the WG search experience. That's how I came up with the idea of "WG Gefunden!"

# WG Gefunden!

We are in an era where we can basically build any website (or anything) with very little time, knowledge, and energy (except the one needed to run the data centers...): The era of vibe-coding. 

The idea was the following: an automatic smart scraper that evaluates all the offers and notifies you when good offers are found. This would help a lot because you don't need to go onto WG Gesucht every hour yourself to check for new offers. Also, you don't lose your time with non-fitting offers where you discover in the description that it's only for women or that this is actually a Verbindung.

For the evaluation, I use two scores: 
- A base score, computed with some parameters of the offer (cost, distance, size, recency...) that is customizable
- An AI score, computed by an LLM that reads your profile and the offer description and flags incompatibilities and outputs a score.

With these, we can define "good" and "fantastic" offers, and send emails notifying when such offers are found. 

That's it. With that, a simple dashboard and options page, and we are good to go. And it works really well, and all of this was programmed in approx. 1.5 days with the use of Claude Code. That's very impressive. 

The instance is running on my homeserver and served at wgg.léo.com

Below is a screenshot of the dashboard running for a search in Karlsruhe:

![Screenshot_2026-10-03_17-50-44.png](/blog/assets/wg-gefunden/Screenshot_2026-10-03_17-50-44.png)

# Analytics

While developing this, I tested it with two accounts, one for Karlsruhe and one for Munich. The difference is impressive. When I first set up the Karlsruhe search, almost ALL offers were tagged as "Fantastic". By Munich standards. The below charts (with same parameters for both cities) really highlight those differences:
![Screenshot_2026-10-03_17-54-13.png](/blog/assets/wg-gefunden/Screenshot_2026-10-03_17-54-13.png)
![Screenshot_2026-10-03_17-54-53.png](/blog/assets/wg-gefunden/Screenshot_2026-10-03_17-54-53.png)

Guess which one is which city...

In the "Score" and "AI Score" charts we can see the quality of the offers differ immensely. The lowest score a Karlsruhe WG obtains is obtained only by 3 offers in Munich. The average AI score in Karlsruhe is around 7.5 while in Munich it's more like 5. Rent is also an interesting chart, we can see that in Munich it's a very beautiful bell curve that has 750€ as its mean rent, ufff! In Karlsruhe, this is much more "Gleichverteilt", and here again, the most expensive offer of 650€ is in the lower 10% of Munich's prices. Finally, we can see that in Karlsruhe, every WG is super close to the University, accessible by bike, but in Munich, the distances from the Uni are much greater, which makes it more important to live close to good ÖPNV connections, since bike is not always so nice here. 

Overall, I hope this can help find a better WG quicker, and it was definitely a fun project to work on!
