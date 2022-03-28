# cricket_data

This repository will act as a backend for the cricket data processed from [Cricsheet](https://wwww.cricsheet.org)

### General format of each game type

Each game type has a folder with 11 files in it. These files contain ball by ball data, meta information about the game and meta information about the file itself.
The 11 files are: <br>

1. **Bowl out Dataframe** - information about who participated in the Bowl out if it occurred for a match - _bowl_out_cf.csv_
2. **Dates dataframe** - date or dates of when each match was played - _dates_df.csv_
3. **Info Dataframe** - information about where and when each match occurs. It also contains the player of the match - _info_df.csv_
4. **Innings Dataframe** - ball by ball information on each match - _innings_df.csv_
5. **Meta Dataframe** - meta information about the file containing match details - _meta_df.csv_
6. **Outcome Dataframe** - information about which team won the match and by what margin - _outcome_df.csv_
7. **Player of match Dataframe** - information about the player or players of the match. There have been matches where there were more than 1 player of the match - _pom_df.csv_
8. **Supersub Dataframe** - information about who participates in the supersub format. - _supersub_df.csv_
9. **Team Dataframe** - information about which teams are participating in the match - _team_df.csv_
10. **Toss Dataframe** - information about which team won the toss and whether they chose to bat or field - _toss_df.csv_
11. **Umpires Dataframe** - information about who were on field umpires in each match - _umpires_df.csv_

### Game types available <br>

| Game Type                    | Abbreviation | Link                     |
| ---------------------------- | ------------ | ------------------------ |
| Afghanistan Premier League   | apl          | [APL Data](./apl_data)   |
| Big Bash League              | bbl          | [BBL Data](./bbl_data)   |
| Bangladesh Premier League    | bpl          | [BPL Data](./bpl_data)   |
| Caribbean Premier League     | cpl          | [CPL Data](./cpl_data)   |
| Indian Premier League        | IPL          | [IPL Data](./ipl_data)   |
| Lanka Premier League         | lpl          | [LPL Data](./lpl_data)   |
| Mzansi Super League          | msl          | [MSL Data](./msl_data)   |
| Natwest T20 Blast            | ntb          | [NTB Data](./ntb_data)   |
| Pakistan Super League        | PSL          | [PSL Data](./psl_data)   |
| T20 Internationals           | t20s         | [T20I Data](./t20s_data) |
| Women's Big Bash             | wbb          | [WBB Data](./wbb_data)   |
| Women's Cricket Super League | wsl          | [WSL Data](./wsl_data)   |
| Women's T20 Challenge        | wtc          | [WTC Data](./wtc_data)   |

### How to use the API to fetch data

1. The base url for a dataframe of any game type is "https://sawlachintan.github.io/cricket_data/"
2. If the game type required is "IPL" and the dataframe required is toss, then append "ipl_data/toss_df.csv" to the base url.

#### Note

For any issues with the files, raise an issue in the repo.

### Strucutre of the dataframes

**Meta**

| Name         | Type   | Desc                                           |
| ------------ | ------ | ---------------------------------------------- |
| key          | string | A common ID to relate info across dataframes   |
| data_version | float  | version of the file from where data is fetched |
| created      | date   | date on which the file was created             |
| revision     | int    | number of times the file was revised.          |

---

**Info**

| Name            | Type    | Desc                                             |
| --------------- | ------- | ------------------------------------------------ |
| key             | string  | A common ID to relate info across dataframes     |
| city            | string  | name of the city where the match is played       |
| competition     | string  | name of the competition                          |
| date            | date    | date of the match                                |
| gender          | string  | gender of the players in the match               |
| match_type      | string  | format of the game                               |
| player_of_match | string  | name of the first player of the match            |
| venue           | string  | name of the stadium where the match is held      |
| neutral_venue   | boolean | if the match is played at a neutral venue or not |

---

**Dates**

| Name | Type   | Desc                                         |
| ---- | ------ | -------------------------------------------- |
| key  | string | A common ID to relate info across dataframes |
| date | date   | dates of when the matches were held          |

---

**Player of Match**

| Name            | Type   | Desc                                         |
| --------------- | ------ | -------------------------------------------- |
| key             | string | A common ID to relate info across dataframes |
| player_of_match | string | name of the players of match                 |

---

**Umpires**

| Name   | Type   | Desc                                         |
| ------ | ------ | -------------------------------------------- |
| key    | string | A common ID to relate info across dataframes |
| umpire | string | Names of the umpires for the match           |

---

**Outcome**

| Name       | Type    | Desc                                                 |
| ---------- | ------- | ---------------------------------------------------- |
| key        | string  | A common ID to relate info across dataframes         |
| by_innings | int     | number of innings the match was won by               |
| by_type    | string  | how the winning team won - runs or wickets           |
| by_margin  | string  | number by which the team won                         |
| bowl_out   | string  | name of the team who won the bowl_out                |
| eliminator | boolean | if the match was an eliminator match or not          |
| method     | string  | different method of winning D/L or 1st innings score |
| result     | string  | draw, no result, or tie when no team won the match   |
| winner     | string  | name of the team who won the match                   |

---

**Teams**

| Name | Type   | Desc                                          |
| ---- | ------ | --------------------------------------------- |
| key  | string | A common ID to relate info across dataframes  |
| team | string | Names of the teams participating in the match |

---

**Toss**

| Name     | Type   | Desc                                            |
| -------- | ------ | ----------------------------------------------- |
| key      | string | A common ID to relate info across dataframes    |
| decision | string | Choice of team winning the toss                 |
| winner   | string | Name of the team winning the toss for the match |

---

**Innings**

| Name              | Type   | Desc                                                  |
| ----------------- | ------ | ----------------------------------------------------- |
| key               | string | A common ID to relate info across dataframes          |
| inning_no         | int    | Innings number of the particular match                |
| delivery_no       | float  | ball and over number of the innings                   |
| batting_team      | string | name of the team batting in that innings              |
| batter            | string | name of the batsman facing the ball                   |
| bowler            | string | name of the bowler bowling the ball                   |
| non_striker       | string | name of the person on the other end of the pitch      |
| runs_batter       | int    | number of runs scored by the batsman in that ball     |
| runs_extras       | int    | extra runs gotten off the delivery                    |
| runs_non_boundary | int    | runs that were more than 4 but not from a boundary    |
| runs_total        | int    | total runs scored from the delivery                   |
| wicket_fielder    | string | name of the fielder who is part of getting the wicket |
| wicket_kind       | string | manner in which batsman/non_striker lost the wicket   |
| wicket_player_out | string | name of the player who got out in that delivery       |
| extras_type       | string | name of the way in which the extra runs were rewarded |
| extras_run        | int    | runs rewarded from the type of extras                 |
| over              | int    | over number of the innings                            |
| n_ball            | int    | ball of the over                                      |
