# Quantifying UFC Fighters Rankings

*Stats are accurate up to and including August 24th 2024
Written by Juno Thiensirisak
## Introduction

The current method of ranking UFC fighter is based on votes from media members and has been that way since rankings were first released in [2013](https://www.sportsnet.ca/mma/ufc/ufc-fighter-rankings-february-2013/). There has been a lot of skepticism surrounding the rankings with some fans doing their own investigation and finding out that the “media” consists of inactive X (Twitter) [users](https://www.reddit.com/r/MMA/comments/hfyyxj/just_who_exactly_are_the_ufc_ranking_panelists/?utm_source=share&utm_medium=ios_app&utm_name=iossmf) with double digit followers as well as [websites](https://www.reddit.com/r/MMA/comments/t6s6fk/the_ufc_rankings_panel_consists_of_some_unknown/?utm_source=share&utm_medium=ios_app&utm_name=iossmf) that seldom post about MMA related news.

Newly signed fighters start off unranked and after winning enough fights, may become ranked in the top 15 of their division and possibly the pound for pound rankings. However it is unclear how many fights they would need to win, or against which caliber of opponents they need to defeat in order to become ranked. Furthermore, losing fights while being ranked can decrease your ranking by an arbitrary amount or even demote fighters to unranked. To become the champion of the weight division, you must beat the reigning champion. The fighters who get a chance to dethrone the champion are typically (but not always) higher ranked, coming off a recent win, and are exciting fighters.

Its not a reach to say that the UFC indirectly or even directly creates the ranking themselves. We can see glaring examples of favoritism with big names like Jon Jones being ranked #3 pound for pound despite only fighting twice in the past 4 years.

![Jon Jones two most recent fights](https://raw.githubusercontent.com/nthiens/UFCDataAnalysis/main/jon%20jones.PNG)

There are several motivating factors on why it would be in the UFC’s favor to control the rankings.

-   It is can be used as a tool to artificially inflate the ranking of the fighter because the fighter is deemed more profitable and marketable (see Conor McGregor)
-   Ranked fighters typically fight within their rankings (and ideally up the rankings) so altering the rankings can provide favorable matchups for the UFC

The unmeritocratic practices used by UFC can negatively affect a fighter’s career by denying them opportunities to become ranked, work their way up to rankings, and potentially earning a title shot. This also has implications on how much money they can make over their UFC career and their athletic legacy.

## Solution
Other MMA organizations follow the same ranking system as UFC with some being more transparent regarding how much direct influence they have over rankings. The only major organization that strays away from this biased model is PFL (Professional Fighters League). The PFL adopts a [regular season](https://www.sportingnews.com/ca/mma/news/pfl-format-explained-mma-league-season-points-playoff-system/tznjnf0zkmwhb3nhgmahafkk) where fighters earn 3 points for a win, 1 point for a draw, and 0 points for a loss. A finish in round 1 grants 3 points to the winner, a finish in round 2 rewards 2 points, and a finish in round 3 gives the winner 1 point. Eventually, the fighters with the most points fight each other in playoffs until one winner remains and wins $1,000,000. The playoffs are a good idea, however the scoring system leading up to it is not. It fails to factor in the skill level of fighters which means that a fighter who is lucky enough to face easy competition at the start has a higher chance of making the playoffs.

The best option for ranking fighters would be an Elo rating system. This is already used in chess, but can be applied to any zero sum game. To summarize, all players start with a ranking. When a player wins against another player, the number of points "earned" depends on the difference in ranking. If the winner started off with a significantly lower ranking than the opponent, then they will gain a lot of points. If the winner started off with a significantly higher ranking than their opponent, they will only gain a little bit of points. The same applies to "losing" points as it depends on the difference in points. The upside to this is that winners cannot artificially inflate their rankings by beating easy opponents because eventually they will not earn much points from beating them. To be the best, you must consistently beat those similar in skill or better than you.

**Formula for calculating Elo:**

Initialize rating for all fighters to be 1500, represented by R
Expected score for fighter A and B: $E_A=\dfrac{1}{1+10^\frac{R_B-R_A}{400}}$ and $E_A=\dfrac{1}{1+10^\frac{R_A-R_B}{400}}$ 


The new rating is for the winner is $R'=R+K(1-E)$, loser is $R'=R+K(0-E)$ and draw is $R'=R+K(0.5-E)$

Note that k is called the K-Factor. A high K factor means the ratings will change more drastically, if all other factors are kept equal. A K-Factor of 30 is used in the code.
```
k <- 30
  winner_expected_score <- 1/(1+10^((loser_old_elo - winner_old_elo)/400))
  loser_expected_score <- 1/(1+10^((winner_old_elo - loser_old_elo)/400))
  
  if (draw == FALSE) {
    winner_new_elo <- winner_old_elo + k * (1 - winner_expected_score)
    winner_new_elo <- winner_new_elo$elo[1]
    loser_new_elo <- loser_old_elo + k * (0 - loser_expected_score)
    loser_new_elo <- loser_new_elo$elo[1]
  } else {
    winner_new_elo <- winner_old_elo + k * (0.5 - winner_expected_score)
    winner_new_elo <- winner_new_elo$elo[1]
    loser_new_elo <- loser_old_elo + k * (0.5 - loser_expected_score)
    loser_new_elo <- loser_new_elo$elo[1]
  }
```
Using [data I scraped](https://github.com/nthiens/UFCWebScraper) from www.ufcstats.com, I was able to extract all the fight information and outcomes then applied the formula.

The full R code can be found [here](https://github.com/nthiens/UFCDataAnalysis/blob/main/elo.R). Make sure to import events.csv, fighters.csv, and fights_overview.csv.

To get in depth Elo information use the function
*get_elo_specific(start_date, end_date, min_weight, max_weight, elo_data, criteria, max_rank)*.
- start_date and end_date specifies the date range for the Elo ranking, for example **as.Date("2024-08-24")**.
- min_weight and max_weight specifies the weight range for fighters, for example **135**.
- elo_data contains comprehensive elo data. Use **all_elo**.
- criteria is either **"latest"** or **"peak"** which specifies whether to use most recent elo or highest elo given the date range.
- max_rank shows the number of fighters shown. Maximum is **20**.
## Results
![Real rankings vs Elo rankings](https://raw.githubusercontent.com/nthiens/UFCDataAnalysis/main/rankings.png)

Note that I have omitted the rankings for featherweight and below. This is because featherweights and lower weight classes are shared between men and women and there is no data from the UFC website to differentiate between fighter's gender. The date range used was 2023-08-25 to 2024-08-24.

## Limitations

To become the "best" of the division, you need to become the champion by beating the current champion and you retain this title by beating challengers. The champions in each division do not necessarily have the highest Elo rating as seen in the middleweight division and higher. The same case applies to interim champs (when the champion cannot fight due to injuries, an interim fight and thus interim champion is crowned).

Another issue arises when a fighter fights in more than one weight class. In fighters.csv, the information regarding the fighter's weight only shows one weight even if they have competed in multiple weight classes. This means that their Elo rating can only be applied to one weight class. In reality, fighters can be ranking in more than one weight class. Max Holloway is ranked at both featherweight and lightweight on UFC's website but in fighters.csv he is only shown as a featherweight (145 lbs).

There are several factors Elo fails to account for. For one, Elo fails to account for fighter inactivity. If a fighter does not fight in a long time, then their rating should decrease, especially since they might have ring rust. A more substantial issue however, would be the initial rating of 1500 given to all fighters at the start of their UFC career. This is absolutely not indicative of real life as fighters that get signed to the UFC are of varying skill levels. A rough estimate of a fighters starting Elo score can be calculated by using the combined record of the fighter's opponents prior to signing with the UFC. The K-Factor should also be adjusted during important fights such as main/co-main fights and championship fights. Since these fights are high level, have longer rounds, and are more important, they should have a higher K-Factor. The last thing to note is the competitiveness of a fight. Fights that do not end by knockout or submission are scored via decision. If it is a split decision or the scorecards are very close, the K-Factor should be reduced accordingly.
