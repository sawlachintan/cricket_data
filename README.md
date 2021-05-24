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

| Game Type             | Abbreviation | Link                     |
| --------------------- | ------------ | ------------------------ |
| Indian Premier League | IPL          | [IPL Data](./ipl_data)   |
| Pakistan Super League | PSL          | [PSL Data](./psl_data)   |
| T20 Internationals    | t20s         | [T20I Data](./t20s_data) |

### How to use the API to fetch data

1. The base url for a dataframe of any game type is "https://sawlachintan.github.io/cricket_data/"
2. If the game type required is "IPL" and the dataframe required is toss, then append "ipl_data/toss_df.csv" to the base url.

#### Note
For any issues with the files, raise an issue in the repo.

### Strucutre of the dataframes

**Meta**

| Name     | Type   | Desc                                           |
| -------- | ------ | ---------------------------------------------- |
| Key_ID   | string | A common ID to relate info across dataframes   |
| Version  | float  | version of the file from where data is fetched |
| Created  | date   | date on which the file was created             |
| Revision | float  | number of times the file was revised.          |

---

**Info**

| Name            | Type    | Desc                                             |
| --------------- | ------- | ------------------------------------------------ |
| Key_ID          | string  | A common ID to relate info across dataframes     |
| City            | string  | name of the city where the match is played       |
| Date            | date    | date of the match                                |
| Player of Match | string  | name of the player of the match                  |
| venue           | string  | name of the stadium where the match is held      |
| Neutral Venue   | boolean | if the match is played at a neutral venue or not |

**Umpires**

| Name    | Type   | Desc                                         |
| ------- | ------ | -------------------------------------------- |
| Key_ID  | string | A common ID to relate info across dataframes |
| Umpires | string | Names of the umpires for the match           |

**Outcome**

| Name          | Type    | Desc                                         |
| ------------- | ------- | -------------------------------------------- |
| Key_ID        | string  | A common ID to relate info across dataframes |
| Winner        | string  | name of the team who won the match           |
| Result Type   | string  | how the winning team won - runs or wickets   |
| Result Margin | int     | number by which the team won                 |
| Eliminator    | boolean | if the match was an eliminator match or not  |

**Teams**

| Name   | Type   | Desc                                          |
| ------ | ------ | --------------------------------------------- |
| Key_ID | string | A common ID to relate info across dataframes  |
| Teams  | string | Names of the teams participating in the match |

**Toss**

| Name          | Type   | Desc                                            |
| ------------- | ------ | ----------------------------------------------- |
| Key_ID        | string | A common ID to relate info across dataframes    |
| Toss winner   | string | Name of the team winning the toss for the match |
| Toss decision | string | Choice of team winning the toss                 |

**Innings**

| Name              | Type   | Desc                                                  |
| ----------------- | ------ | ----------------------------------------------------- |
| Key_ID            | string | A common ID to relate info across dataframes          |
| innings_no        | int    | Innings number of the particular match                |
| team              | string | name of the team batting in that innings              |
| ball              | float  | over and ball number of that innings                  |
| batsman           | string | name of the batsman facing the ball                   |
| bowler            | string | name of the bowler bowling the ball                   |
| non_striker       | string | name of the person on the other end of the pitch      |
| runs_batsman      | int    | number of runs scored by the batsman in that ball     |
| runs_extras       | int    | extra runs gotten off the delivery                    |
| runs_non_boundary | int    | runs that were more than 4 but not from a boundary    |
| runs_total        | int    | total runs scored from the delivery                   |
| wicket_fielder    | string | name of the fielder who is part of getting the wicket |
| wicket_kind       | string | manner in which batsman/non_striker lost the wicket   |
| wicket_player_out | string | name of the player who got out in that delivery       |
| extras_type       | string | name of the way in which the extra runs were rewarded |
| extras_runs       | int    | runs rewarded from the type of extras                 |
