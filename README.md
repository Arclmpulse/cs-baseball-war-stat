# CS: Creating a New Statistic to Rate Pro Players

## Abstract
Counter Strike was a game with very humble roots; starting as a Half-Life mod from 2000 to the game it is today, the game has gone through many iterations and evolutions. And with it existed a professional scene, starting from CS 1.6, moving to Source briefly, staying on Global Offensive for a decade before now moving on towards CS 2. With a competitive scene, there had to be *some* metric that could appropriately measure and rank players based off their gameplay. 

Indeed, [HLTV](https://www.hltv.org/) created their own metric known as [HLTV Rating 2.0.](https://www.hltv.org/news/20695/introducing-rating-20) However, it can be noted that this statistic puts heavy bias onto players that often "bait," or have selfish playstyles. Further, AWPers get favoured more with this statistic as they tend to survive more frequently. Think of the players like BlameF or Jame - can you truly say that their rating is as accurate as some players that clearly influence winning like Niko or Device? Because of this, HLTV rating is a good measure, but not entirely the most accurate one.

I've attempted to create a statistic that attempts to remove some of these biases. Based off MLB/Baseball's WAR (Wins Above Replacement), I've coined my own statistic - SAR. Statistics Above Replacement. By using the metrics of Kills, ADR, KAST, Impact, and Team Win Rate and pitting them against a weighted average as factors that influence this statistic, we can attempt to measure just how useful - or how *useless* - some players truly are to their team's success.

## 1.0: Understanding the Pieces of the Equation
Before we dive into any math, some variables need to be understood first. Here are all of the statistics I've collected from players:

### 1.1 Kills
Quite possibly the most difficult variable to understand. Here's an example of an infamous kill(s):

![](/pictures/happy.gif)

In all seriousness, **kills** are the basis of most of these following statistics. 

### 1.2 ADR
**ADR** stands for **Average Damage per Round** - essentially, a raw metric for how many of a player's bullets are landing on their opponents. A lot of stats are based on ADR, and is sometimes more useful of a statistic than measuring raw kills, as softening up enemies can make kills for teammates easier.

### 1.3 AWP%
I've coined this as the percentage of kills that come from the One-Shot Sniper Rifle in the game. Here's it in action.

![](/pictures/coldzera.gif)

The **AWP** being the most expensive weapon in the game presents an interesting conundrum for teams: it is often worth it to save the gun in some rounds rather than try to go for plays that could be winnable - think like folding in a round of Poker. As a result of this, **AWP** players tend to play more risk averse than most other riflers.

How many kills players have with the **AWP** will be important in the future. Here's an example weapon spread of the greatest Global Offensive player, S1mple.

![](/pictures/s1mple.png)

### 1.4 KAST
An HLTV statistic, **KAST** stands for the **percentage of rounds where a player had a Kill, Assist, Survived, or Traded.** In other words, a statistic that attempts to show how useful a player is generally.

**KAST** is not a perfect statistic. Think about the amount of times a player can simply hide and not affect the game, or simply pick up an exit frag. Are they truly influencing winning?

As a result of this, this statistic will be used in determining a future factor, but will not be used by itself.

### 1.5 Impact
Another HLTV statistic, though this one is a bit more complex. In essence, **Impact** measures the impact made from kills per round. 

The following equation can be roughly used to measure **Impact:**

```math
\text{Impact} = 2.13(\text{KPR}) + 0.42(\text{APR}) - 0.4
```

Where **KPR** stands for *Kills per Round*, and **APR** is *Assists per Round*.

This statistic is useful in a raw sense - Impact gives you a good sense of how useful a player is from round to round. Though again, this does not always tell the whole story of how useful the kills were - were those exit frags on a lost round?  Because of this, this statistic will be used as a factor in the future.

### 1.6 HLTV Rating
Though this will not be used in any calculations due to the complexity of the equation, it will still be referenced periodically.

HLTV rating is HLTV's own "all in one" statistic. By combining **KAST**, **KPR**, **DPR** (Deaths per round), **Impact** and **ADR**, a standardized *player rating* can be created. 

```math
\text{Rating 2.0} = 0.0073(\text{KAST}) + 0.3591(\text{KPR}) - 0.5329(\text{DPR}) + 0.2372(\text{Impact}) + 0.0032(\text{ADR}) + 0.1587

```

HLTV rating has it's own issues. Again, HLTV rating tends to bias towards AWPers due to the presence of KAST and the heavy negative bias against high DPR. Conversely, this stat is generally biased against entry fraggers and site anchors. 

### 1.7 IGL
It is no secret that taking on the **IGL** (In Game Leader) role drops players' stats, and for good reason - they have to focus on midround calls, look at radar half the time, and coordinate with their teammates. As such, being an IGL will often drop fragging output. Yet this is pretty unfair - why should a player's value only be measured by the amount of frags they're getting? As such, being an IGL or not will be another factor.


### 1.8 Win Rate
A self explanatory statistic, **win rate** just refers to the team's results in the recent past. A player's team's win rate will be another factor in determining how useful they are to the team.

- - - 

## 2.0 Creating Variables and the Equation
