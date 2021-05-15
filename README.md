# cricket_data

This repository will act as a backend for the cricket data processed from [Cricsheet](https://wwww.cricsheet.org)

### General format of each game type

Each game type has a folder with 6 files in it. These files contain ball by ball data, meta information about the game and meta information about the file itself.
The 6 files are: <br>

1. **Meta Dataframe** - meta information about the file containing match details
2. **Toss Dataframe** - information about which team won the toss and whether they chose to bat or field
3. **Team Dataframe** - information about which teams are participating in the match
4. **Info Dataframe** - information about where and when each match occurs. It also contains which team won the match and by what margin
5. **Innings Dataframe** - ball by ball information on each match
6. **Umpires Dataframe** - information about who were on field umpires in each match <br>

### Game types available <br>

| Game Type | Abbreviation | Link |
| --- | --- | --- |
| Indian Premier League | IPL | xyz |
| Pakistan Super League | PSL | klm |
