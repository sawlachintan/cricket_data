import multiprocessing
import json
import os
from zipfile import ZipFile
import pandas as pd
import numpy as np

def expand_wickets(row):
    if isinstance(row, list) and len(row) > 0:
        return pd.Series({
            'wickets_kind': row[0]['kind'],
            'wickets_player_out': row[0]['player_out']
        })
    else:
        return pd.Series({
            'wickets_kind': pd.NA,
            'wickets_player_out': pd.NA
        })

def process_game(match_id, counter, LEAGUE):

    with ZipFile(f"./data/temp/{LEAGUE}.zip", "r") as zip:
        with zip.open(f"{match_id}.json") as json_data:
                    all_match_data = json.loads(json_data.read().decode())
    
    temp_info_df = pd.json_normalize(all_match_data['info'], max_level=0)
    temp_info_df['dates'] = temp_info_df['dates'].apply(lambda x: x[0])
    temp_info_df = temp_info_df.rename(columns={"dates": "date"})

    if 'officials' in temp_info_df.columns:
        temp_officials_df = pd.json_normalize(temp_info_df.loc[0, 'officials'])
        temp_officials_df = temp_officials_df.T.explode(0).reset_index()
        temp_officials_df.columns = ['type', 'name']
        temp_officials_df['key'] = f"{LEAGUE}{counter:05d}"
        # officials_df = pd.concat(
        #     [officials_df, temp_officials_df], ignore_index=True)
        temp_info_df = temp_info_df.drop(columns=['officials'])
    else:
         temp_officials_df = pd.DataFrame()

    temp_playing_xi_df = pd.json_normalize(
        temp_info_df['players']).T[0].apply(pd.Series).T
    temp_playing_xi_df = pd.melt(
        temp_playing_xi_df, value_vars=temp_info_df['teams'][0])
    temp_playing_xi_df.columns = ["team", "name"]
    temp_playing_xi_df['key'] = f"{LEAGUE}{counter:05d}"

    temp_info_df = temp_info_df.drop(columns=['players'])

    temp_toss_df = pd.json_normalize(temp_info_df['toss'])
    temp_toss_df['key'] = f"{LEAGUE}{counter:05d}"
    # toss_df = pd.concat([toss_df, temp_toss_df], ignore_index=True)
    temp_info_df = temp_info_df.drop(columns=['toss'])

    temp_team_df = temp_info_df['teams'].apply(pd.Series)
    inn_teams = temp_info_df['teams'][0]
    temp_team_df.columns = ['team_1', 'team_2']
    temp_team_df['key'] = f"{LEAGUE}{counter:05d}"
    # team_df = pd.concat([team_df, temp_team_df], ignore_index=True)
    temp_info_df = temp_info_df.drop(columns=['teams'])

    if 'event' in temp_info_df.columns:
        temp_event_df = pd.json_normalize(temp_info_df['event'])
        temp_event_df['key'] = f"{LEAGUE}{counter:05d}"
        # event_df = pd.concat([event_df, temp_event_df], ignore_index=True)
        temp_info_df = temp_info_df.drop(columns=['event'])
    else:
        temp_event_df = pd.DataFrame()
            
    temp_registry_df = pd.DataFrame(
        [temp_info_df['registry'][0]['people']]).T.reset_index()
    temp_registry_df.columns = ['name', 'registry_key']
    # registry_df = pd.concat([registry_df, temp_registry_df], ignore_index=True)
    temp_info_df = temp_info_df.drop(columns=['registry'])

    temp_outcome_df = pd.json_normalize(temp_info_df['outcome'])
    temp_outcome_df['key'] = f"{LEAGUE}{counter:05d}"
    # outcome_df = pd.concat([outcome_df, temp_outcome_df], ignore_index=True)
    temp_info_df = temp_info_df.drop(columns=['outcome'])

    if 'player_of_match' in temp_info_df.columns:
        temp_info_df['player_of_match'] = temp_info_df['player_of_match'].apply(
            lambda x: x[0])
    temp_info_df['key'] = f"{LEAGUE}{counter:05d}"
    # info_df = pd.concat([info_df, temp_info_df], ignore_index=True)

    inn_counter = 0
    match_ball_by_ball_data = pd.DataFrame()
    match_batting_positions = dict()
    for inn in all_match_data['innings']:
        inn_counter += 1
        temp_innings_df = pd.json_normalize(inn)
        if 'powerplays' in temp_innings_df:
            temp_innings_df = temp_innings_df.drop(columns=['powerplays'])
        
        if 'overs' in temp_innings_df.columns:
            temp_innings_df = temp_innings_df.explode('overs')
        else:
            print(f"'overs' key missing for match_id: {match_id}, {inn}")
            continue
        overs_df = pd.json_normalize(temp_innings_df['overs'])
        all_overs_data = pd.DataFrame()
        for idx, row in overs_df.iterrows():
            one_over_data = pd.json_normalize(row['deliveries'])
            one_over_data['over'] = row['over']
            one_over_data['delivery_no'] = 1
            if 'extras.wides' in one_over_data.columns:
                one_over_data.loc[~one_over_data['extras.wides'].isna(),
                                  'delivery_no'] = 0
            if 'extras.noballs' in one_over_data.columns:
                one_over_data.loc[~one_over_data['extras.noballs'].isna(),
                                  'delivery_no'] = 0
            one_over_data['delivery_no'] = one_over_data['delivery_no'].cumsum()
            one_over_data.loc[one_over_data['delivery_no']
                              == 0, 'delivery_no'] = 1
            if 'wickets' in one_over_data.columns:
                wicket_expansion = one_over_data['wickets'].apply(
                    expand_wickets)
                one_over_data = pd.concat(
                    [one_over_data, wicket_expansion], axis=1)

                # Drop the original wickets column if needed
                one_over_data.drop(columns=['wickets'], inplace=True)

            all_overs_data = pd.concat(
                [all_overs_data,  one_over_data], ignore_index=True)
            all_overs_data['batting_team'] = temp_innings_df.iloc[0, 0]
            all_overs_data['inning_no'] = inn_counter
            combined = pd.concat(
                [all_overs_data['batter'], all_overs_data['non_striker']])

            # Drop duplicates while keeping the first occurrence to maintain order
            unique_batters = combined.sort_index().drop_duplicates()

            # Create a mapping of each batter to their batting position
            temp_batting_positions = {
                batter: position + 1 for position, batter in enumerate(unique_batters)}
            match_batting_positions.update(temp_batting_positions)
        match_ball_by_ball_data = pd.concat(
            [match_ball_by_ball_data, all_overs_data])

    match_ball_by_ball_data['bowling_team'] = match_ball_by_ball_data['batting_team']\
        .apply(lambda x: inn_teams[0] if x != inn_teams[0] else inn_teams[1])
    match_ball_by_ball_data['key'] = f"{LEAGUE}{counter:05d}"
    # final_innings_df = pd.concat(
    #     [final_innings_df, match_ball_by_ball_data], ignore_index=True)

    temp_playing_xi_df['batting_position'] = temp_playing_xi_df['name'].map(
        match_batting_positions)
    # playing_xi_df = pd.concat(
    #     [playing_xi_df, temp_playing_xi_df], ignore_index=True)
    
    return {"officials": temp_officials_df, "toss": temp_toss_df,
            "team": temp_team_df, "event": temp_event_df,
            "registry": temp_registry_df, "playing_xi": temp_playing_xi_df,
            "outcome": temp_outcome_df, "info": temp_info_df,
            "innings": match_ball_by_ball_data}


if __name__ == "__main__":
    LEAGUES = ["ipl", "bbl", "sma", "sat",
           "mlc", "cpl", "psl", "ntb", "lpl", "bpl", "t20s","ilt"]

    for league in LEAGUES:
        officials_df = pd.DataFrame()
        toss_df = pd.DataFrame()
        team_df = pd.DataFrame()
        event_df = pd.DataFrame()
        registry_df = pd.DataFrame()
        playing_xi_df = pd.DataFrame()
        outcome_df = pd.DataFrame()
        info_df = pd.DataFrame()
        final_innings_df = pd.DataFrame()
        LEAGUE = league
        data = pd.read_csv(f"./data/util/{LEAGUE}.csv", parse_dates=['date'])

        num_cores = multiprocessing.cpu_count()
        with multiprocessing.Pool(num_cores) as pool:
            func_args = data['cricsheet_id'].to_frame()
            func_args['counter'] = func_args.index + 1
            func_args['match_type'] = league
            func_args = func_args.to_numpy().tolist()
            result = pool.starmap(process_game,func_args)
        
        officials_df = pd.concat([x['officials'] for x in result])
        toss_df = pd.concat([x['toss'] for x in result])
        team_df = pd.concat([x['team'] for x in result])
        event_df = pd.concat([x['event'] for x in result])
        registry_df = pd.concat([x['registry'] for x in result])
        playing_xi_df = pd.concat([x['playing_xi'] for x in result])
        outcome_df = pd.concat([x['outcome'] for x in result])
        info_df = pd.concat([x['info'] for x in result])
        final_innings_df = pd.concat([x['innings'] for x in result])

        os.makedirs(f"./data/bronze/{LEAGUE}", exist_ok=True)

        info_df.to_csv(f"./data/bronze/{LEAGUE}/info_df.csv",index=False)
        info_df['season'] = info_df['season'].astype(str)
        if 'missing' in info_df.columns:
            info_df = info_df.drop(columns=['missing'])
        info_df.to_parquet(f"./data/bronze/{LEAGUE}/info_df.parquet",index=False)

        playing_xi_df.columns = [str(x) for x in playing_xi_df.columns]
        playing_xi_df.to_csv(f"./data/bronze/{LEAGUE}/playing_xi_df.csv",index=False)
        playing_xi_df.to_parquet(f"./data/bronze/{LEAGUE}/playing_xi_df.parquet",index=False)

        registry_df = registry_df.drop_duplicates(ignore_index=True).sort_values('name',ignore_index=True)
        registry_df.to_csv(f"./data/bronze/{LEAGUE}/registry_df.csv",index=False)
        registry_df.to_parquet(f"./data/bronze/{LEAGUE}/registry_df.parquet",index=False)

        outcome_df.to_csv(f"./data/bronze/{LEAGUE}/outcome_df.csv",index=False)
        outcome_df.to_parquet(f"./data/bronze/{LEAGUE}/outcome_df.parquet",index=False)

        officials_df.to_csv(f"./data/bronze/{LEAGUE}/officials_df.csv",index=False)
        officials_df.to_parquet(f"./data/bronze/{LEAGUE}/officials_df.parquet",index=False)

        toss_df.to_csv(f"./data/bronze/{LEAGUE}/toss_df.csv",index=False)
        toss_df.to_parquet(f"./data/bronze/{LEAGUE}/toss_df.parquet",index=False)

        team_df.to_csv(f"./data/bronze/{LEAGUE}/team_df.csv",index=False)
        team_df.to_parquet(f"./data/bronze/{LEAGUE}/team_df.parquet",index=False)

        if 'group' in event_df.columns:
            event_df['group'] = event_df['group'].astype(str)
        if 'stage' in event_df.columns:
            event_df['stage'] = event_df['stage'].astype(str)
        event_df.to_csv(f"./data/bronze/{LEAGUE}/event_df.csv",index=False)
        event_df.to_parquet(f"./data/bronze/{LEAGUE}/event_df.parquet",index=False)

        final_innings_df.columns = [x.replace(".","_") for x in final_innings_df.columns]
        def melt_extras(x):
            if not pd.isna(x['extras_noballs']):
                return "noballs"
            elif not pd.isna(x['extras_wides']):
                return "wides"
            elif not pd.isna(x['extras_legbyes']):
                return "legbyes"
            elif not pd.isna(x['extras_byes']):
                return "byes"
            elif not pd.isna(x['extras_penalty']):
                return "penalty"
            else:
                return pd.NA
        final_innings_df['extras_type'] = pd.NA
        extras_mask = final_innings_df['runs_extras'] > 0
        final_innings_df.loc[extras_mask,['extras_type']] = final_innings_df.loc[extras_mask,].apply(melt_extras, axis=1)
        final_innings_df = final_innings_df.rename({"runs_extras":"extras_run"})
        extras_cols = ['extras_noballs', 'extras_wides', 'extras_legbyes','extras_byes','extras_penalty']
        for col in extras_cols:
            if col in final_innings_df.columns:
                final_innings_df = final_innings_df.drop(columns=[col])

        final_innings_df = final_innings_df.replace(np.nan,pd.NA)
        final_innings_df.to_csv(f"./data/bronze/{LEAGUE}/innings_df.csv", index=False)
        final_innings_df.to_parquet(f"./data/bronze/{LEAGUE}/innings_df.parquet",index=False)

        # Check if the file exists and remove it
        if os.path.isfile(f"./data/temp/{LEAGUE}.zip"):
            os.remove(f"./data/temp/{LEAGUE}.zip")
            print(f"File ./data/temp/{LEAGUE}.zip has been removed.")
        else:
            print(f"./data/temp/{LEAGUE}.zip does not exist.")