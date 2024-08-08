# CS: Creating a New Statistic to Rate Pro Players

## Abstract
Counter Strike was a game with very humble roots; starting as a Half-Life mod from 2000 to the game it is today, the game has gone through many iterations and evolutions. And with it existed a professional scene, starting from CS 1.6, moving to Source briefly, staying on Global Offensive for a decade before now moving on towards CS 2. With a competitive scene, there had to be *some* metric that could appropriately measure and rank players based off their gameplay. 

Indeed, [HLTV](https://www.hltv.org/) created their own metric known as [HLTV Rating 2.0.](https://www.hltv.org/news/20695/introducing-rating-20) However, it can be noted that this statistic puts heavy bias onto players that often "bait," or have selfish playstyles. Further, AWPers get favoured more with this statistic as they tend to survive more frequently. Think of the players like BlameF or Jame - can you truly say that their rating is as accurate as some players that clearly influence winning like Niko or Device? Because of this, HLTV rating is a good measure, but not entirely the most accurate one.

I've attempted to create a statistic that attempts to remove some of these biases. Based off MLB/Baseball's WAR (Wins Above Replacement), I've coined my own statistic - SAR. Statistics Above Replacement. By using the metrics of Kills, ADR, KAST, Impact, and Team Win Rate and pitting them against a weighted average as factors that influence this statistic, we can attempt to measure just how useful - or how *useless* - some players truly are to their team's success.

## Understanding the Pieces of the Equation
Before we dive into any math, some variables need to be understood first. Here are all of the statistics I've collected from players:

### Kills
Quite possibly the most difficult variable to understand. Here's an example of an infamous kill(s):

![](https://media1.tenor.com/m/lbVPssj-JJUAAAAC/happy-envyus.gif)

In all seriousness, kills are the basis of most of these following statistics. 

### AWP%
I've coined this as the percentage of kills that come from the One-Shot Sniper Rifle in the game. Here's it in action.

![](https://media1.tenor.com/m/_Q-bZCgn24AAAAAC/coldzera.gif)

The AWP being the most expensive weapon in the game presents an interesting conundrum for teams: it is often worth it to save the gun in some rounds rather than try to go for plays that could be winnable - think like folding in a round of Poker. As a result of this, AWP players tend to play more risk averse than most other riflers.

How many kills players have with the AWP will be important in the future. Here's an example weapon spread of the greatest Global Offensive player, S1mple.

![](/pictures/s1mple.png)

### KAST
An HLTV statistic, KAST stands for percentage of rounds where a player had a Kill, Assist, Survived, or Traded. In other words, a statistic that attempts to show how useful a player is generally.

KAST is not a perfect statistic. Think about the amount of times a player can simply hide and not affect the game, or simply pick up an exit frag. Are they truly influencing winning?

As a result of this, this statistic will be used in determining a future factor, but will not be used by itself.

### Impact


