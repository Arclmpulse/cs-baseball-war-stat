# CS: Creating a New Statistic to Rate Pro Players

## Abstract
Counter Strike was a game with very humble roots; starting as a Half-Life mod from 2000 to the game it is today, the game has gone through many iterations and evolutions. And with it existed a professional scene, starting from CS 1.6, moving to Source briefly, staying on Global Offensive for a decade before now moving on towards CS 2. With a competitive scene, there had to be *some* metric that could appropriately measure and rank players based off their gameplay. 

Indeed, [HLTV](https://www.hltv.org/) created their own metric known as [HLTV Rating 2.0.](https://www.hltv.org/news/20695/introducing-rating-20) However, it can be noted that this statistic puts heavy bias onto players that often "bait," or have selfish playstyles. Further, AWPers get favoured more with this statistic as they tend to survive more frequently. Think of the players like BlameF or Jame - can you truly say that their rating is as accurate as some players that clearly influence winning like Niko or Device? Because of this, HLTV rating is a good measure, but not entirely the most accurate one.

I've attempted to create a statistic that attempts to remove some of these biases. Based off MLB/Baseball's WAR (Wins Above Replacement), I've coined my own statistic - RAR. Rounds Above Replacement. By using the metrics of Kills, ADR, KAST, Impact, and Team Win Rate and pitting them against a weighted average as factors that influence this statistic, we can attempt to measure just how useful - or how *useless* - some players truly are to their team's success.

## 1.0: Understanding the Pieces of the Equation
Before we dive into any math, some variables need to be understood first. I've tried to make this readable such that you don't really need to understand anything about Counter Strike to read this, but some of these following topics are necessary to know. Here are all of the statistics I've collected from players:

### 1.1 Kills
Quite possibly the most difficult variable to understand. Here's an example of an infamous kill(s):

![](/pictures/happy.gif)

In all seriousness, **kills** are the basis of most of these following statistics. An example of a post-match statistic from an infamous set:

![](/pictures/postmatch.png)

Here, we can see that the **K** in **K-D** refers to kills across the entire set. There are several ways to quantify this, with **KPR** (Kills Per Round) being quite common, and is the one that will mostly be referenced through this.

### 1.2 ADR
Referencing back to the previous figure, **ADR** stands for **Average Damage per Round** - essentially, a raw metric for how many of a player's bullets are landing on their opponents. A lot of stats are based on ADR, and is sometimes more useful of a statistic than measuring raw kills, as softening up enemies can make kills for teammates easier. This will be important for later.

### 1.3 KAST
An HLTV statistic, **KAST** stands for the **percentage of rounds where a player had a Kill, Assist, Survived, or Traded.** In other words, a statistic that attempts to show how useful a player was in a map, generally speaking. If you're never involved in any action, this statistic can definitely call you out on it.

**KAST** is not a perfect statistic, however. Think about the amount of times a player can simply bait for a kill and not really affect the game, save the **AWP** or simply pick up an exit frag. Are they truly influencing winning rounds?

As a result of this, this statistic will be used in determining a future factor, but will not be used by itself as an important metric.

### 1.4 Impact
An HLTV statistic. In essence, **Impact** measures the impact made from kills per round. Here was a round that was particularly impactful:

![](/pictures/niko-fail-simple.gif)

I kid, of course. The following equation can be roughly used to measure **Impact:**

```math
{Impact} = 2.13({KPR}) + 0.42({APR}) - 0.4
```

Where **KPR** stands for *Kills per Round*, and **APR** is *Assists per Round*.

This statistic is useful in a raw sense - Impact gives you a good sense of how useful a player is from round to round. Though again, this does not always tell the whole story of how useful the kills were - were those exit frags on a lost round?  Because of this, this statistic will be used as a factor in the future.

### 1.5 HLTV Rating
Another HLTV statistic. Though this will not be used in any calculations due to the complexity of its equation, it will still be referenced periodically as a baseline or a benchmark to reference my own statistic against.

HLTV rating is HLTV's own "all in one" statistic. By combining **KAST**, **KPR**, **DPR** (Deaths per round), **Impact** and **ADR**, a standardized *player rating* can be created. The following shows off the reverse engineered equation for **HLTV Rating:**

```math
\text{Rating 2.0} = 0.0073({KAST}) + 0.3591({KPR}) - 0.5329({DPR}) + 0.2372({Impact}) + 0.0032({ADR}) + 0.1587

```

HLTV rating has it's own issues. Again, HLTV rating tends to bias towards AWPers due to the presence of KAST and the heavy negative bias against high DPR. Conversely, this stat is generally biased against entry fraggers and site anchors as the players who are often dying, but giving their lives to either stall out site executes or creating space for the star riflers on CT or T sides respectively. As such, while it is a good stat to generally see who is a good player and who is not, it is not perfect.

### 1.6 AWP%
I've coined this as the percentage of kills that come from the One-Shot Sniper Rifle in the game. Here's an infamous play with it in action:

![](/pictures/coldzera.gif)

The **AWP** being the most expensive weapon in the game presents an interesting conundrum for teams: it is often worth it to save the gun in some rounds rather than try to go for plays that could be winnable - think like folding in a round of Poker. Cut your losses early, try again in another round. Jame and Virtus Pro/AVANGAR/Outsiders were teams notorious for stretching this idea to the limit, playing a very unique and efficient brand of Counter Strike, though boring at times. As a result of this, **AWP** players tend to play more risk averse than most other riflers. This is pretty influential for some future stats, such as **KAST** or **Rating**, where simply being an AWP player can inflate stats.

How many kills players have with the **AWP** will be important in the future. Here's an example weapon spread of the greatest Global Offensive player, S1mple.

![](/pictures/s1mple.png)

By attempting to standardize rifle kills to AWP players, we can try to measure players' impact on a more even footing.

### 1.7 IGL
It is no secret that taking on the **IGL** (In Game Leader) role drops players' stats, and for good reason - they have to focus on midround calls, look at radar half the time, and coordinate plays with their teammates. As such, being an IGL will often drop fragging output. And to make matters worse, most teams will usually put the IGL in bad spots to sacrifice certain parts of the map, in favour of giving their stars areas where they can be set-up easier. Being a hard entry and/or a site anchor are two roles that IGLs often get stuck with. Karrigan is a notorious example of this, being a hard entry on most of his T sides with Faze. Yet this is pretty unfair - why should a player's value only be measured by the amount of frags they're getting? As such, being an IGL or not will be another factor.


### 1.8 Win Rate
A self explanatory statistic, **win rate** just refers to the team's results in the recent past. A player's team's win rate will be another factor in determining how useful they are to the team.

- - - 

## 2.0 Creating Variables and the Equation
Now that these statistics have been defined, the pieces of the equation to calculate this new "all in one" statistic can now be determined. Due to HLTV's strict policies against scraping data on their website, this data has been manually collected. Normally, an API would've been used for ease and to automate this, but as this is more of a proof on concept/personal side project, the following data that was manually scraped from the site was found to be sufficient:

<details>
<summary><b>Player Data (ACCURATE AS OF 04/08/2024, BIG EVENTS 2024 ONLY)</b></summary>

|Player    |Total Kills|Rounds Won|Total Rounds|Maps Played|ADR |Rating|Impact|KAST |AWP%  |IGL|Rank|Win|Loss|KPR  |
|----------|-----------|----------|------------|-----------|----|------|------|-----|------|---|----|---|----|-----|
|chopper   |514        |536       |917         |44         |63.2|0.99  |0.92  |0.747|0.19% |1  |2   |33 |11  |0.561|
|donk      |830        |536       |917         |44         |94.8|1.37  |1.57  |0.761|1.45% |0  |2   |33 |11  |0.905|
|sh1ro     |689        |536       |917         |44         |75.3|1.24  |1.12  |0.785|38.75%|0  |2   |33 |11  |0.751|
|zont1x    |619        |536       |917         |44         |77.1|1.13  |1.09  |0.756|0.16% |0  |2   |33 |11  |0.675|
|magixx    |566        |536       |917         |44         |68.2|1.08  |0.96  |0.773|2.83% |0  |2   |33 |11  |0.617|
|Brollan   |829        |706       |1210        |57         |79.4|1.13  |1.19  |0.735|0.12% |0  |3   |38 |19  |0.685|
|Jimpphat  |899        |706       |1210        |57         |78  |1.19  |1.14  |0.769|0.11% |0  |3   |38 |19  |0.743|
|xertioN   |908        |706       |1210        |57         |82.3|1.19  |1.37  |0.732|0.33% |0  |3   |38 |19  |0.75 |
|torzsi    |884        |706       |1210        |57         |73.6|1.14  |1.09  |0.726|40.61%|0  |3   |38 |19  |0.731|
|siuhy     |726        |706       |1210        |57         |67.8|0.97  |0.9   |0.702|0.14% |1  |3   |38 |19  |0.6  |
|Zywoo     |1115       |707       |1325        |60         |86.6|1.32  |1.42  |0.765|29.51%|0  |4   |36 |24  |0.842|
|Spinx     |930        |707       |1325        |60         |77.2|1.12  |1.06  |0.74 |0.75% |0  |4   |36 |24  |0.702|
|FlameZ    |905        |707       |1325        |60         |74.4|1.11  |1.2   |0.749|0.22% |0  |4   |36 |24  |0.683|
|mezii     |800        |707       |1325        |60         |68.7|1.02  |0.96  |0.734|0.00% |0  |4   |36 |24  |0.604|
|apEX      |763        |707       |1325        |60         |69.8|0.98  |0.94  |0.722|0.26% |1  |4   |36 |24  |0.576|
|m0nesy    |1587       |999       |1966        |88         |81.5|1.26  |1.33  |0.748|42.97%|0  |5   |55 |36  |0.807|
|NiKo      |1491       |1028      |2024        |91         |81.7|1.18  |1.3   |0.73 |1.41% |0  |5   |55 |36  |0.737|
|hunter    |1305       |1028      |2024        |91         |72  |1.04  |0.97  |0.721|0.46% |0  |5   |55 |36  |0.645|
|Hooxi     |755        |731       |1440        |65         |60.6|0.88  |0.86  |0.699|0.93% |1  |5   |55 |36  |0.524|
|nexa      |1085       |913       |1797        |81         |66.1|0.98  |0.81  |0.72 |0.18% |0  |5   |55 |36  |0.604|
|karrigan  |1011       |940       |1788        |82         |65.2|0.9   |0.96  |0.668|1.29% |1  |6   |48 |34  |0.565|
|broky     |1350       |940       |1788        |82         |75.6|1.17  |1.11  |0.76 |35.85%|0  |6   |48 |34  |0.755|
|ropz      |1237       |940       |1788        |82         |73.5|1.08  |0.98  |0.733|1.78% |0  |6   |48 |34  |0.692|
|frozen    |1276       |940       |1788        |82         |80.2|1.14  |1.14  |0.735|0.86% |0  |6   |48 |34  |0.714|
|rain      |1156       |940       |1788        |82         |75.1|1.04  |1.1   |0.702|0.00% |0  |6   |48 |34  |0.647|
|AleksiB   |982        |712       |1873        |87         |62.4|0.92  |0.79  |0.698|1.02% |1  |1   |38 |27  |0.524|
|w0nderful |1372       |712       |1873        |87         |74.2|1.15  |1.08  |0.738|28.86%|0  |1   |38 |27  |0.733|
|jL        |1341       |712       |1873        |87         |79.5|1.14  |1.17  |0.727|0.60% |0  |1   |38 |27  |0.716|
|b1t       |1341       |712       |1873        |87         |75.6|1.11  |1.12  |0.722|0.45% |0  |1   |38 |27  |0.716|
|iM        |1247       |712       |1873        |87         |74.6|1.01  |1.09  |0.666|0.40% |0  |1   |38 |27  |0.666|
|ELIGE     |589        |360       |782         |36         |81.4|1.16  |1.3   |0.738|2.55% |0  |11  |16 |20  |0.753|
|hallzerk  |549        |360       |782         |36         |73.1|1.09  |1.08  |0.71 |32.60%|0  |11  |16 |20  |0.702|
|Grim      |526        |360       |782         |36         |73.9|1.03  |1.01  |0.702|0.38% |0  |11  |16 |20  |0.673|
|JT        |479        |360       |782         |36         |70.4|0.96  |0.97  |0.698|0.00% |1  |11  |16 |20  |0.613|
|floppy    |428        |360       |782         |36         |66.4|0.94  |0.84  |0.712|0.70% |0  |11  |16 |20  |0.547|
|Nertz     |737        |514       |1033        |46         |78.5|1.11  |1.19  |0.697|1.63% |0  |9   |23 |23  |0.713|
|TeSeS     |745        |514       |1033        |46         |80.6|1.14  |1.18  |0.734|0.54% |0  |9   |23 |23  |0.721|
|sjuush    |657        |514       |1033        |46         |73.1|1.03  |0.98  |0.718|0.76% |0  |9   |23 |23  |0.636|
|kyxsan    |616        |514       |1033        |46         |67.3|0.96  |0.92  |0.695|0.65% |1  |9   |23 |23  |0.596|
|nicoodoz  |665        |514       |1033        |46         |66  |1.02  |1     |0.705|28.27%|0  |9   |23 |23  |0.644|
|snappi    |338        |332       |679         |32         |59  |0.82  |0.73  |0.666|0.00% |1  |13  |15 |17  |0.498|
|dupreeh   |276        |179       |366         |17         |82.3|1.16  |1.3   |0.713|0.00% |0  |13  |4  |13  |0.754|
|Maden     |484        |332       |679         |32         |77.3|1.1   |1.13  |0.726|1.03% |0  |13  |15 |17  |0.713|
|SunPayus  |446        |332       |679         |32         |68.1|1.08  |1.08  |0.725|41.03%|0  |13  |15 |17  |0.657|
|Magisk    |414        |332       |679         |32         |72.2|1.03  |0.92  |0.744|0.00% |0  |13  |15 |17  |0.61 |
|electronic|876        |629       |1271        |59         |79.3|1.08  |1.11  |0.712|0.00% |0  |7   |25 |34  |0.689|
|Jame      |832        |618       |1249        |58         |68.4|1.12  |1.04  |0.738|54.45%|1  |7   |29 |29  |0.666|
|FL1T      |814        |618       |1249        |58         |79  |1.11  |1.16  |0.728|0.49% |0  |7   |29 |29  |0.652|
|norbert   |761        |618       |1249        |58         |68.9|0.99  |1.02  |0.691|0.92% |0  |7   |29 |29  |0.609|
|fame      |754        |618       |1249        |58         |63.6|0.99  |0.98  |0.714|0.40% |0  |7   |29 |29  |0.604|
|Ax1le     |269        |193       |382         |18         |80.3|1.15  |1.23  |0.751|1.49% |0  |30  |7  |11  |0.704|
|Boombl4   |240        |193       |382         |18         |68.2|1.01  |1.01  |0.73 |20.00%|1  |30  |7  |11  |0.628|
|Perfecto  |238        |193       |382         |18         |64.4|1.03  |0.84  |0.754|2.52% |0  |30  |7  |11  |0.623|
|Hobbit    |252        |193       |382         |18         |73.9|1.05  |1.03  |0.733|1.59% |0  |30  |7  |11  |0.66 |
|Twistzz   |539        |360       |724         |31         |80.8|1.18  |1.22  |0.735|1.11% |0  |14  |15 |16  |0.744|
|NAF       |508        |360       |724         |31         |77.7|1.14  |1.04  |0.757|2.56% |0  |14  |15 |16  |0.702|
|YEKINDAR  |462        |360       |724         |31         |73.7|1.05  |1.25  |0.682|0.22% |0  |14  |15 |16  |0.638|
|cadiaN    |441        |360       |724         |31         |66.1|1.03  |0.88  |0.739|50.34%|1  |14  |15 |16  |0.609|
|skullz    |542        |445       |904         |39         |65.9|0.96  |0.9   |0.7  |0.37% |0  |14  |15 |16  |0.6  |
|KSCERATO  |504        |329       |694         |32         |82.2|1.19  |1.25  |0.726|0.00% |0  |15  |14 |18  |0.726|
|yuurih    |450        |329       |694         |32         |78.5|1.04  |1.03  |0.703|0.89% |0  |15  |14 |18  |0.648|
|FalleN    |445        |329       |694         |32         |63.6|1     |1     |0.676|46.74%|1  |15  |14 |18  |0.641|
|chelo     |384        |329       |694         |32         |62.6|0.9   |0.95  |0.659|7.03% |0  |15  |14 |18  |0.553|
|MAJ3R     |356        |313       |637         |29         |65.2|0.96  |0.9   |0.694|3.37% |1  |16  |13 |16  |0.559|
|XANTARES  |447        |313       |637         |29         |82.3|1.19  |1.31  |0.749|0.89% |0  |16  |13 |16  |0.702|
|woxic     |426        |313       |637         |29         |70  |1.06  |0.94  |0.738|44.84%|0  |16  |13 |16  |0.669|
|Wicadia   |430        |313       |637         |29         |72.9|1.05  |1.12  |0.697|0.47% |0  |16  |13 |16  |0.675|
|Calyx     |379        |313       |637         |29         |64.4|0.96  |0.84  |0.714|0.26% |0  |16  |13 |16  |0.595|
|bLitz     |303        |227       |450         |20         |80.1|1.06  |1.1   |0.711|1.32% |1  |10  |8  |12  |0.673|
|Senzu     |312        |227       |450         |20         |74.7|1.09  |1.24  |0.704|4.81% |0  |10  |8  |12  |0.693|
|Techno    |303        |227       |450         |20         |75  |1.05  |1.13  |0.676|0.99% |0  |10  |8  |12  |0.673|
|910       |291        |227       |450         |20         |63.9|1     |0.92  |0.682|47.77%|0  |10  |8  |12  |0.647|
|mzinho    |272        |227       |450         |20         |68.1|0.96  |0.95  |0.676|0.37% |0  |10  |8  |12  |0.604|
|slaxz     |373        |271       |549         |24         |69.5|1.08  |1.05  |0.716|52.55%|0  |27  |9  |15  |0.679|
|s1n       |359        |271       |549         |24         |75.4|1.1   |1.1   |0.734|0.84% |1  |27  |9  |15  |0.654|
|Swisher   |342        |271       |549         |24         |71.2|1.01  |1.02  |0.699|0.88% |0  |27  |9  |15  |0.623|
|reck      |334        |271       |549         |24         |67.9|0.96  |0.89  |0.705|0.00% |0  |27  |9  |15  |0.608|
|malbsMD   |511        |339       |683         |30         |81.7|1.17  |1.36  |0.726|0.00% |0  |27  |9  |11  |0.748|
|device    |392        |297       |513         |25         |81.5|1.29  |1.23  |0.776|40.31%|1  |8   |17 |8   |0.764|
|stavn     |377        |297       |513         |25         |84.5|1.23  |1.31  |0.756|2.65% |0  |8   |17 |8   |0.735|
|jabbi     |386        |297       |513         |25         |73.6|1.16  |1.14  |0.758|0.52% |0  |8   |17 |8   |0.752|
|staehr    |332        |297       |513         |25         |74.6|1.11  |1.17  |0.741|0.90% |0  |8   |17 |8   |0.647|
|br0       |392        |297       |513         |25         |68.5|1.04  |0.97  |0.75 |0.26% |0  |8   |17 |8   |0.764|
|tabseN    |293        |221       |448         |21         |75.3|1.04  |1.01  |0.723|0.68% |1  |24  |11 |10  |0.654|
|Krimbo    |313        |221       |448         |21         |78.7|1.15  |1.13  |0.743|1.92% |0  |24  |11 |10  |0.699|
|JDC       |318        |221       |448         |21         |78.5|1.11  |1.19  |0.728|0.00% |0  |24  |11 |10  |0.71 |
|syrsoN    |276        |221       |448         |21         |63.5|0.95  |0.88  |0.679|56.52%|0  |24  |11 |10  |0.616|
|prosus    |261        |221       |448         |21         |65.9|0.93  |0.98  |0.71 |0.00% |0  |24  |11 |10  |0.583|
|gla1ve    |213        |198       |412         |21         |59.6|0.86  |0.79  |0.684|0.00% |1  |25  |9  |12  |0.517|
|Goofy     |263        |198       |412         |21         |71.4|1.06  |1.08  |0.723|0.00% |0  |25  |9  |12  |0.638|
|Kylar     |273        |198       |412         |21         |70.7|1.05  |1.15  |0.699|0.37% |0  |25  |9  |12  |0.663|
|hades     |331        |198       |412         |21         |81.4|1.26  |1.27  |0.75 |45.92%|0  |25  |9  |12  |0.803|
|dycha     |248        |198       |412         |21         |73.7|0.99  |1.03  |0.682|0.00% |0  |25  |9  |12  |0.602|
|alistair  |398        |330       |698         |31         |58.4|0.91  |0.81  |0.683|46.73%|0  |20  |13 |18  |0.57 |
|INS       |517        |330       |698         |31         |87.4|1.14  |1.24  |0.709|0.97% |0  |20  |13 |18  |0.741|
|vexite    |452        |330       |698         |31         |71.5|0.98  |1.02  |0.678|0.22% |0  |20  |13 |18  |0.648|
|dexter    |439        |330       |698         |31         |71.8|0.94  |1.1   |0.642|0.68% |1  |20  |13 |18  |0.629|
|liazz     |395        |330       |698         |31         |65.7|0.9   |0.75  |0.689|0.51% |0  |20  |13 |18  |0.566|
|r1nkle    |204        |143       |300         |13         |67.5|1.06  |1.13  |0.7  |56.37%|0  |17  |5  |8   |0.68 |
|maxster   |213        |143       |300         |13         |75.8|1.1   |1.06  |0.727|0.47% |0  |17  |5  |8   |0.71 |
|alex      |217        |143       |300         |13         |75.5|1.13  |1.13  |0.74 |0.00% |1  |17  |5  |8   |0.723|
|zorte     |184        |133       |275         |13         |69.7|1.05  |1.12  |0.676|36.96%|0  |21  |7  |6   |0.669|
|magnojez  |199        |133       |275         |13         |79.5|1.11  |1.14  |0.727|0.00% |0  |21  |7  |6   |0.724|
|kairon    |174        |133       |275         |13         |72.7|1.01  |0.93  |0.72 |0.57% |0  |21  |7  |6   |0.633|
|s1ren     |166        |133       |275         |13         |63.2|0.94  |0.87  |0.68 |0.00% |0  |21  |7  |6   |0.604|
|nafany    |149        |133       |275         |13         |61.9|0.89  |0.96  |0.669|0.00% |1  |21  |7  |6   |0.542|
|KRIMZ     |151        |100       |240         |10         |72.7|1.05  |1.05  |0.683|1.32% |0  |22  |3  |7   |0.629|
|bodyy     |132        |100       |240         |10         |68.1|0.94  |0.93  |0.679|0.76% |1  |22  |3  |7   |0.55 |
|afro      |148        |100       |240         |10         |64.1|0.95  |0.88  |0.667|45.27%|0  |22  |3  |7   |0.617|
|matys     |146        |100       |240         |10         |68.5|0.88  |0.94  |0.621|0.68% |0  |22  |3  |7   |0.608|
|Snax      |358        |297       |597         |28         |69.3|0.97  |0.93  |0.695|0.84% |1  |29  |9  |9   |0.6  |
|isak      |238        |191       |370         |18         |70.8|1.02  |0.99  |0.7  |0.42% |0  |29  |9  |9   |0.643|
|volt      |240        |191       |370         |18         |72.1|1.03  |0.94  |0.73 |0.00% |0  |29  |9  |9   |0.649|

</details>

From this data, we can create all of the variables necessary to determine RAR.

Something to be noted: although a shift could've been achieved in this statistic by adding and not multiplying by a factor, I firmly believe that players who are positive should be rewarded for staying above average, while poor players should be more heavily penalized for this. As such, this statistic, and the rest will follow this methodology.

### 2.1 wKAA (Weighted Kills Above Average)
The first factor that will be determined calculates how much higher a player's KPR is above the average. This is done to see who is fragging out, and who is struggling to find kills amongst the players. The following equation can be used to determine this statistic:

```math
{wKAA} = \frac{{KPR} - {Avg KPR}} {Avg KPR} * 4.3333
```

Where **KPR** is **Kills Per Round.** This stat will be balanced around 1.5 being the highest score one can attain - the 4.3333 was used as a factor to elevate this.

We can see who leads the charts in this statistic below:

<details>
<summary><b>wKAA of Players</b></summary>

|Player      |wKAAFactor  |
|------------|------------|
|donk        |1.641506963 |
|Zywoo       |1.217874987 |
|m0nesy      |0.982523889 |
|hades       |0.95562662  |
|device      |0.693378254 |
|br0         |0.693378254 |
|broky       |0.6328594   |
|dupreeh     |0.626135083 |
|ELIGE       |0.619410766 |
|jabbi       |0.612686449 |
|sh1ro       |0.605962132 |
|xertioN     |0.599237815 |
|malbsMD     |0.585789181 |
|Twistzz     |0.558891912 |
|Jimpphat    |0.552167595 |
|INS         |0.538718961 |
|NiKo        |0.511821693 |
|stavn       |0.498373058 |
|w0nderful   |0.484924424 |
|torzsi      |0.47147579  |
|KSCERATO    |0.437854205 |
|magnojez    |0.42440557  |
|alex        |0.417681253 |
|TeSeS       |0.404232619 |
|jL          |0.370611034 |
|b1t         |0.370611034 |
|frozen      |0.3571624   |
|Nertz       |0.350438082 |
|Maden       |0.350438082 |
|JDC         |0.330265131 |
|maxster     |0.330265131 |
|Ax1le       |0.289919229 |
|Spinx       |0.276470595 |
|XANTARES    |0.276470595 |
|NAF         |0.276470595 |
|hallzerk    |0.276470595 |
|Krimbo      |0.256297643 |
|Senzu       |0.215951741 |
|ropz        |0.209227424 |
|electronic  |0.189054472 |
|Brollan     |0.162157204 |
|FlameZ      |0.14870857  |
|r1nkle      |0.128535619 |
|slaxz       |0.121811302 |
|zont1x      |0.094914033 |
|Wicadia     |0.094914033 |
|Grim        |0.081465399 |
|bLitz       |0.081465399 |
|Techno      |0.081465399 |
|zorte       |0.054568131 |
|woxic       |0.054568131 |
|iM          |0.034395179 |
|Jame        |0.034395179 |
|Kylar       |0.014222228 |
|Hobbit      |-0.005950723|
|SunPayus    |-0.026123674|
|tabseN      |-0.046296626|
|s1n         |-0.046296626|
|FL1T        |-0.05974526 |
|volt        |-0.079918211|
|yuurih      |-0.086642528|
|vexite      |-0.086642528|
|rain        |-0.093366845|
|staehr      |-0.093366845|
|910         |-0.093366845|
|hunter      |-0.106815479|
|nicoodoz    |-0.113539796|
|isak        |-0.120264114|
|FalleN      |-0.133712748|
|YEKINDAR    |-0.153885699|
|Goofy       |-0.153885699|
|sjuush      |-0.167334333|
|kairon      |-0.187507284|
|dexter      |-0.214404553|
|KRIMZ       |-0.214404553|
|Boombl4     |-0.22112887 |
|Swisher     |-0.254750455|
|Perfecto    |-0.254750455|
|magixx      |-0.295096358|
|afro        |-0.295096358|
|syrsoN      |-0.301820675|
|JT          |-0.321993626|
|Magisk      |-0.342166577|
|norbert     |-0.348890894|
|cadiaN      |-0.348890894|
|reck        |-0.355615212|
|matys       |-0.355615212|
|nexa        |-0.38251248 |
|mezii       |-0.38251248 |
|fame        |-0.38251248 |
|mzinho      |-0.38251248 |
|s1ren       |-0.38251248 |
|dycha       |-0.395961114|
|siuhy       |-0.409409748|
|skullz      |-0.409409748|
|Snax        |-0.409409748|
|kyxsan      |-0.436307017|
|Calyx       |-0.443031334|
|prosus      |-0.523723139|
|apEX        |-0.570793358|
|alistair    |-0.611139261|
|liazz       |-0.638036529|
|karrigan    |-0.644760846|
|chopper     |-0.671658115|
|MAJ3R       |-0.685106749|
|chelo       |-0.725452651|
|bodyy       |-0.745625603|
|floppy      |-0.765798554|
|nafany      |-0.799420139|
|Hooxi       |-0.920457847|
|AleksiB     |-0.920457847|
|gla1ve      |-0.967528066|
|snappi      |-1.095290091|
</details>

Unsuprisingly, **Donk** leads the charts with a staggering **1.64.** Not far behind him is **Zywoo** at **1.22.** 

Some nice surprises include **Hades, Br0 and Malbs** - the former having a perception of being a mediocre tier 1 AWPer, **Br0** being a roleplayer on Astralis, and the latter having played for a Tier 2 team with M80. 

Some bad surprises include **Rain and Sjuush** - **Rain** in particular has had decent success throughout the year so to see him with a negative score was quite shocking. 

**Hunter, Mezii and Perfecto** have both had inconsistent performances throughout the year despite their big names, so to see them not fragging well is not a big surprise. 

And expectedly, IGLs mostly take the very bottom of this stat, with infamously bad fraggers like **Hooxi and Snappi** highlighting the worst fraggers currently. **AleksiB** being so low too was a bit of a surprise given some of his star roles and reputation for his fragging ability as an IGL, though it's nothing too out of the ordinary.

### 2.2 wAAA (Weighted ADR Above Average)
This next factor uses a similar methodology to **2.1 wKAA**, but instead uses ADR to see which players are doing the most damage round by round. The following equation can be used to see this:

```math
{wAAA} = \frac{{ADR} - {Avg ADR}} {12.6666}
```
Where **ADR** is **Average Damage per Round.** 

This statistic was given a slightly higher weight than **wKAA** at 1.75. **ADR** is often more of a useful metric with how involved players are in action, since a lot of the players going for openers will be the ones that are *more useful*. I believe players who are going for gunfights a lot, and succeeding in softening up or removing weapons is more important than just securing kills, and as such was given a slightly higher weight.

The following shows the table of **wAAA** below:

<details>
<summary><b>wAAA of Players</b></summary>

|Player      |wAAAFactor  |
|------------|------------|
|donk        |1.747833025 |
|INS         |1.163591749 |
|Zywoo       |1.10043053  |
|stavn       |0.93463233  |
|xertioN     |0.760938978 |
|dupreeh     |0.760938978 |
|XANTARES    |0.760938978 |
|KSCERATO    |0.753043826 |
|NiKo        |0.713568064 |
|malbsMD     |0.713568064 |
|m0nesy      |0.697777759 |
|device      |0.697777759 |
|ELIGE       |0.689882607 |
|hades       |0.689882607 |
|Twistzz     |0.642511693 |
|TeSeS       |0.626721388 |
|Ax1le       |0.603035931 |
|frozen      |0.595140778 |
|bLitz       |0.587245626 |
|jL          |0.539874712 |
|magnojez    |0.539874712 |
|Brollan     |0.531979559 |
|electronic  |0.524084407 |
|FL1T        |0.50039895  |
|Krimbo      |0.476713493 |
|Nertz       |0.460923188 |
|yuurih      |0.460923188 |
|JDC         |0.460923188 |
|Jimpphat    |0.421447426 |
|NAF         |0.397761969 |
|Maden       |0.366181359 |
|Spinx       |0.358286207 |
|zont1x      |0.350391055 |
|maxster     |0.247754074 |
|broky       |0.231963769 |
|b1t         |0.231963769 |
|alex        |0.224068617 |
|s1n         |0.216173464 |
|sh1ro       |0.208278312 |
|tabseN      |0.208278312 |
|rain        |0.192488007 |
|Techno      |0.184592855 |
|Senzu       |0.160907398 |
|iM          |0.153012245 |
|staehr      |0.153012245 |
|FlameZ      |0.13722194  |
|w0nderful   |0.121431636 |
|Grim        |0.097746179 |
|Hobbit      |0.097746179 |
|YEKINDAR    |0.081955874 |
|dycha       |0.081955874 |
|torzsi      |0.074060721 |
|jabbi       |0.074060721 |
|ropz        |0.066165569 |
|hallzerk    |0.03458496  |
|sjuush      |0.03458496  |
|Wicadia     |0.018794655 |
|kairon      |0.00300435  |
|KRIMZ       |0.00300435  |
|Magisk      |-0.036471412|
|volt        |-0.044366564|
|hunter      |-0.052261717|
|dexter      |-0.068052021|
|vexite      |-0.091737478|
|Goofy       |-0.099632631|
|Swisher     |-0.115422936|
|isak        |-0.147003545|
|Kylar       |-0.154898698|
|JT          |-0.178584155|
|woxic       |-0.210164764|
|apEX        |-0.225955069|
|zorte       |-0.233850221|
|slaxz       |-0.249640526|
|Snax        |-0.265430831|
|norbert     |-0.29701144 |
|mezii       |-0.312801745|
|br0         |-0.32859205 |
|matys       |-0.32859205 |
|Jame        |-0.336487202|
|magixx      |-0.352277507|
|Boombl4     |-0.352277507|
|SunPayus    |-0.360172659|
|mzinho      |-0.360172659|
|bodyy       |-0.360172659|
|reck        |-0.375962964|
|siuhy       |-0.383858116|
|r1nkle      |-0.407543574|
|kyxsan      |-0.423333878|
|floppy      |-0.49439025 |
|nexa        |-0.518075707|
|cadiaN      |-0.518075707|
|nicoodoz    |-0.525970859|
|skullz      |-0.533866012|
|prosus      |-0.533866012|
|liazz       |-0.549656316|
|karrigan    |-0.589132078|
|MAJ3R       |-0.589132078|
|Perfecto    |-0.652293297|
|Calyx       |-0.652293297|
|afro        |-0.675978754|
|910         |-0.691769059|
|fame        |-0.715454516|
|FalleN      |-0.715454516|
|syrsoN      |-0.723349669|
|chopper     |-0.747035126|
|s1ren       |-0.747035126|
|chelo       |-0.79440604 |
|AleksiB     |-0.810196345|
|nafany      |-0.849672107|
|Hooxi       |-0.952309088|
|gla1ve      |-1.031260611|
|snappi      |-1.078631526|
|alistair    |-1.12600244 |
|            |            |

</details>

Again, **Donk** tops the charts with a monumental **1.75.** Shockingly, **INS** slots in at #2 here - for someone who plays on a team (**Flyquest**) that is not good, his numbers are even more impressive in that regard. 

Some other positive surprises include **Ax1le** being up there in spite of his poor year so far, **blitz** being an IGL yet having a very positive score, and **magnojez** playing for another relatively poor team, yet performing well in this metric.

Some negative surprises include **Ropz** barely treading above water in this metric, **r1nkle** despite having a pretty good individual year on NIP performing fairly poorly here, and **br0** having such low ADR numbers despite his high KPR.

Unsurprisingly, mostly IGLs are at the bottom again. **Alistair** and **Syrson** being two of the worst AWPs in Tier 1/ Tier 1.5 being this low is no surprise either; if you aren't hitting your shots with the sniper, your ADR is going to suffer immensely.

### 2.3 kAWP (KAST/AWP% Adjustment Factor)
I've mentioned this already, but saving the AWP is valid strategy in a lost round - you can bring it into the next one, and try your luck at a tricky set piece again or force the enemy T-side to respect the angles the AWP could be holding.

The problem is when AWP players get passive. They want to survive, they want to save, they don't go for 50/50, 55/45 or even 60/40 plays that could flip heads. Yes you save the most expensive gun in the game, but was it really worth it if you could've just won your team the round in the first place?

Sometimes the answer is yes, and Jame's teams like Virtus Pro/Outsiders/AVANGAR made this their entire identity. Which is fine, since all players on the team were looking to save the AWP if it went down. But for AWPers, I believe baiting/passive AWPs are not usually winning players, and as such I've created a factor to penalize this playstyle.

**kAWP** is **KAST/AWP% Adjustment Factor.** What this metric does is take a player's relative to the average **KAST** rating as well as the amount of share of kills they have with the AWP, and compound them together. This was done in order to firstly see which player's are AWPers for one, and which players are more likely to save with the KAST rating. Non AWPers are nearly guaranteed to not get penalized at all by this factor, as most non AWP players have sub 1% AWP rates, and as such the amount they will get subtracted from is minimal.

Obviously this isn't a perfect way to measure it. A player like Zywoo would be the anthesis of this: he's a winning player with a high KAST rating and is an AWPer. The best AWPer, in fact. But because there was no access to player's saving data, this had to suffice instead.

The equation below shows this off:

```math
{kAWP} = ({KAST} - {Avg KAST}) * {AWP\%} * 9.7000
```
Where KAST is % of rounds where a player got a kill, assist, survived or was traded, and AWP% refers to amount of kills done with the AWP. 9.7 was chosen as  the factor to round the kAWP stat to approximately 0.25.

The following shows off the list. Only AWPers were shown in the table below, though other players do have kAWP scores, most of them were below 1E-2 and as such were irrelevant.

<details>
<summary><b>kAWP of AWPers</b></summary>

|Player   |kAWPFactor |
|---------|-----------|
|sh1ro    |0.259220697|
|device   |0.23446579 |
|broky    |0.152884704|
|hades    |0.151286488|
|Zywoo    |0.140159704|
|m0nesy   |0.133231337|
|Jame     |0.116009339|
|cadiaN   |0.112135691|
|woxic    |0.095534596|
|w0nderful|0.061488145|
|torzsi   |0.03925226 |
|SunPayus |0.035678308|
|Boombl4  |0.027091327|
|slaxz    |-1.86E-05  |
|hallzerk |-0.019085136|
|nicoodoz |-0.030261159|
|r1nkle   |-0.087679794|
|zorte    |-0.143531707|
|alistair |-0.149743183|
|910      |-0.157709484|
|FalleN   |-0.181511688|
|syrsoN   |-0.203044349|
|afro     |-0.21532375|

</details>

This seems to check out at first glance. **sh1ro** while a great player, is sometimes criticized by the community for being too passive and *baity.* 

On the flipside, **Boombl4** was an AWP that was *part-time* since his team (**C9**) had no AWP, and he was also often entrying in sites when there was no AWP in play, which likely lowered his KAST. 

Some surprises are that **Jame** is only middle of the pack here, but that is likely due to his relatively poor individual performance this year. **Device** is another name that feels off - while he is more of a passive AWPer, he's not someone who struggles or gets criticized for not finding impact in rounds.

Players like **Monesy** and **Zywoo** being more middle of the pack here are also unsurprising, as both are more willing to scrap and go for clutches where they might fall flat on their face. 

### 2.4 iAWP (Impact/AWP% Adjustment Factor)
Because it does feel a bit unfair that AWPers are the only position that have a penalizing stat, I've created another metric that rewards AWPers who find impact in rounds: coined **iAWP.** **Impact/AWP% Adjustment Factor**, this is calculated in an identical way to **2.3 kAWP,** but uses **HLTV Impact** to calculate this.

```math
{iAWP} = ({Impact} - {Avg Impact}) * {AWP\%} * 6.7500
```

<details>
<summary><b>iAWP of AWPers</b></summary>

|Player   |iAWPFactor |
|---------|-----------|
|m0nesy   |0.743212307|
|Zywoo    |0.678613263|
|hades    |0.619740644|
|device   |0.441909426|
|r1nkle   |0.260963458|
|sh1ro    |0.154850586|
|zorte    |0.147697488|
|broky    |0.120556888|
|torzsi   |0.08512482 |
|SunPayus |0.060019675|
|Senzu    |0.055777261|
|hallzerk |0.047688068|
|w0nderful|0.047119192|
|slaxz    |-0.022973065|
|Jame     |-0.058288499|
|Boombl4  |-0.059409717|
|nicoodoz |-0.101879874|
|FalleN   |-0.168442352|
|woxic    |-0.331986205|
|910      |-0.414187676|
|afro     |-0.507194932|
|cadiaN   |-0.563998076|
|syrsoN   |-0.633237411|
|alistair |-0.730721021|

</details>