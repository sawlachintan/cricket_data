import pandas as pd
import numpy as np


def umpire_entry(umpire_info, key: str) -> pd.DataFrame:
    '''
    Returns a dataframe that contains information of umpires in the match

        Parameters:
            umpire_info: a list of umpires in the match
            key: index of the match

        Returns:
            a dataframe of who umpired the match
    '''
    umpire_df = pd.DataFrame(columns=['key', 'umpire'])
    if umpire_info == np.nan:
        umpire_dict = {'key': key, 'umpire': np.nan}
        umpire_df = umpire_df.append(umpire_dict, ignore_index=True)
    else:
        for umpire in umpire_info:
            umpire_dict = {'key': key, 'umpire': umpire}
            umpire_df = umpire_df.append(umpire_dict, ignore_index=True)
    return umpire_df


def toss_entry(toss_info: dict, key: str) -> pd.DataFrame:
    '''
    Returns a dataframe that contains toss information of the match

    Parameters:
        toss_info: a dict of toss information
        key: index of the match

    Returns:
        a dataframe of toss information of the match

    '''
    # possibility of adding the 'uncontested' variable in the future
    toss_df = pd.DataFrame(columns=['key', 'decision', 'winner'])
    toss_dict = {
        'key': key,
        'decision': toss_info['decision'],
        'winner': toss_info['winner']}
    toss_df = toss_df.append(toss_dict, ignore_index=True)
    return toss_df


def team_entry(key: str, team_info: list) -> pd.DataFrame:
    '''
    Returns a dataframe that teams that participated in the match

    Parameters:
        team: a list of teams that participated in the match
        key: index of the match

    Returns:
        a dataframe of teams that participated in the match

    '''
    team_df = pd.DataFrame(columns=['key', 'team'])
    for team in team_info:
        team_dict = {'key': key, 'team': team}
        team_df = team_df.append(team_dict, ignore_index=True)
    return team_df


def info_entry(key: str, gen_info: dict) -> pd.DataFrame:
    '''
    Returns a dataframe that contains general information about a match

    Parameters:
        gen_info: a dict of info from the main dict
        key: index of the match

    Returns:
        a dataframe of general information of the match

    '''
    gen_df = pd.DataFrame(columns=['key', 'city', 'competition', 'date', 'gender',
                                   'match_type', 'neutral_venue', 'overs', 'player_of_match', 'venue'])
    gen_dict = {
        'key': key,
        'gender': gen_info['gender'],
        'match_type': gen_info['match_type']}
    conditional_cols = ['venue', 'city',
                        'competition', 'overs', 'neutral_venue']
    for col in conditional_cols:
        if col in gen_info.keys():
            gen_dict[col] = gen_info[col]
    gen_dict['date'] = gen_info['dates'][0]
    if 'player_of_match' in gen_info.keys():
        gen_dict['player_of_match'] = gen_info['player_of_match'][0]
    gen_df = gen_df.append(gen_dict, ignore_index=True)
    return gen_df


def innings_entry(key_id: str, innings_list: list) -> pd.DataFrame:
    '''
    Returns a dataframe that contains winner and margin information about a match

    Parameters:
        outcome_info: a dict of info from the main dict
        key: index of the match

    Returns:
        a dataframe of winner and margin information of the match

    '''
    innings_df = pd.DataFrame(columns=['key', 'inning_no', 'batting_team', 'delivery_no', 'batter', 'bowler', 'non_striker',
                              'runs_batter', 'runs_extras', 'runs_non_boundary', 'runs_total', 'wicket_fielder', 'wicket_kind', 'wicket_player_out', 'extras_type'])
    for inning in innings_list:
        for key, value in inning.items():
            if 'super over' in key.lower():
                inning_no += 1
            else:
                inning_no = int(key[0])

            batting_team = value['team']
            for a_ball in value['deliveries']:
                ball_data_dict = {}
                delivery_no = list(a_ball.keys())[0]

                ball_data_dict['key'] = key_id
                ball_data_dict['inning_no'] = inning_no
                ball_data_dict['batting_team'] = batting_team
                ball_data_dict['delivery_no'] = delivery_no

                # print(delivery_no, type(delivery_no))
                # print(a_ball, type(a_ball))
                delivery_data = a_ball[delivery_no]

                ball_data_dict['non_striker'] = delivery_data['non_striker']
                ball_data_dict['bowler'] = delivery_data['bowler']

                runs_data = delivery_data['runs']

                try:
                    ball_data_dict['batter'] = delivery_data['batsman']
                    ball_data_dict['runs_batter'] = runs_data['batsman']
                except KeyError:
                    try:
                        ball_data_dict['batter'] = delivery_data['batter']
                        ball_data_dict['runs_batter'] = runs_data['batter']
                        print('reference is batter now')
                    except KeyError:
                        ball_data_dict['batter'] = np.nan
                        ball_data_dict['runs_batter'] = np.nan
                        print('Lookup reference for batter')

                ball_data_dict['runs_extras'] = runs_data['extras']
                ball_data_dict['runs_total'] = runs_data['total']

                ball_data_dict['runs_non_boundary'] = runs_data['non_boundary'] if 'non_boundary' in runs_data.keys(
                ) else 0

                del runs_data

                if 'extras' in delivery_data.keys():
                    extras_data = delivery_data['extras']
                    ball_data_dict['extras_type'] = list(extras_data.keys())[0]
                    ball_data_dict['extras_run'] = extras_data[ball_data_dict['extras_type']]

                    del extras_data

                else:
                    ball_data_dict['extras_type'] = np.nan
                    ball_data_dict['extras_run'] = np.nan

                if 'wicket' in delivery_data.keys():
                    wicket_data = delivery_data['wicket']

                    if type(wicket_data) == list:
                        ball_data_dict['wicket_fielder'] = wicket_data[0]['fielders'][0] if 'fielders' in wicket_data[0].keys(
                        ) else np.nan
                        ball_data_dict['wicket_kind'] = wicket_data[0]['kind']
                        ball_data_dict['wicket_player_out'] = wicket_data[0]['player_out']
                        innings_df = innings_df.append(
                            ball_data_dict, ignore_index=True)
                        ball_data_dict['wicket_fielder'] = wicket_data[1]['fielders'][0] if 'fielders' in wicket_data[1].keys(
                        ) else np.nan
                        ball_data_dict['wicket_kind'] = wicket_data[1]['kind']
                        ball_data_dict['wicket_player_out'] = wicket_data[1]['player_out']
                    else:
                        ball_data_dict['wicket_fielder'] = wicket_data['fielders'][0] if 'fielders' in wicket_data.keys(
                        ) else np.nan
                        ball_data_dict['wicket_kind'] = wicket_data['kind']
                        ball_data_dict['wicket_player_out'] = wicket_data['player_out']

                    del wicket_data

                else:
                    ball_data_dict['wicket_fielder'] = np.nan
                    ball_data_dict['wicket_kind'] = np.nan
                    ball_data_dict['wicket_player_out'] = np.nan

                innings_df = innings_df.append(
                    ball_data_dict, ignore_index=True)
                del ball_data_dict

    over_series = pd.Series(dtype='object')
    ball_series = pd.Series(dtype='object')

    # print(list(innings_df.inning_no.unique()))

    for inn in list(innings_df.inning_no.unique()):
        # print(inn)
        temp_df = innings_df[innings_df.inning_no ==
                             inn][['delivery_no', 'extras_type']]

        temp_df['new_ball'] = temp_df['delivery_no'].copy(deep=True)
        temp_df['new_ball'] = temp_df['new_ball'].astype('str')
        ball_split = temp_df['new_ball'].str.split('.', n=1, expand=True)
        temp_df['over'] = ball_split[0]
        temp_df['n_ball'] = ball_split[1]

        overs = sorted(set(temp_df[(temp_df.extras_type == 'wides') | (
            temp_df.extras_type == 'noballs')]['over']))

        for over in overs:
            temp = temp_df[temp_df.over == str(over)].copy(deep=True)
            for ball in range(temp.shape[0]):
                temp.iloc[ball, temp_df.columns.get_loc('n_ball')] = ball + 1
            temp_df.loc[temp_df.delivery_no.isin(
                temp.delivery_no), 'n_ball'] = temp.n_ball

            for ball in range(temp.shape[0] - 1):
                if temp.iloc[ball, temp_df.columns.get_loc('extras_type')] == 'wides' or temp.iloc[ball, temp_df.columns.get_loc('extras_type')] == 'noballs':
                    for a_ball in range(ball + 1, temp.shape[0]):
                        temp.iloc[a_ball, temp_df.columns.get_loc('n_ball')] = str(
                            int(temp.iloc[a_ball, temp_df.columns.get_loc('n_ball')]) - 1)
                    temp_df.loc[temp_df.delivery_no.isin(
                        temp.delivery_no), 'n_ball'] = temp.n_ball
        del overs
        # print(temp_df)
        over_series = over_series.append(temp_df.over, ignore_index=True)
        ball_series = ball_series.append(temp_df.n_ball, ignore_index=True)
        del temp_df

    innings_df['over'] = over_series
    innings_df['ball'] = ball_series
    # innings_df = innings_df.drop(columns=['ball'])
    # print(innings_df)
    # print(over_series, type(over_series))
    # print(ball_series, type(ball_series))
    del over_series
    del ball_series

    innings_df['over'] = innings_df['over'].astype('float').astype('Int64')
    innings_df['ball'] = innings_df['ball'].astype('float').astype('Int64')
    innings_df['inning_no'] = innings_df['inning_no'].astype('Int64')
    innings_df['runs_batter'] = innings_df['runs_batter'].astype('Int64')
    innings_df['runs_extras'] = innings_df['runs_extras'].astype('Int64')
    innings_df['runs_total'] = innings_df['runs_total'].astype('Int64')

    return innings_df


def outcome_entry(key: str, outcome_info: dict) -> pd.DataFrame:
    '''
    Returns a dataframe that contains winner and margin information about a match

    Parameters:
        outcome_info: a dict of info from the main dict
        key: index of the match

    Returns:
        a dataframe of winner and margin information of the match

    '''
    outcome_df = pd.DataFrame(columns=[
                              'key', 'by_innings', 'by_type', 'by_margin', 'eliminator', 'bowl_out', 'method', 'result', 'winner'])
    outcome_dict = {'key': key}
    if 'by' in outcome_info.keys():
        if 'runs' in outcome_info['by'].keys():
            outcome_dict['by_type'] = 'runs'
            outcome_dict['by_margin'] = outcome_info['by']['runs']
        if 'wickets' in outcome_info['by'].keys():
            outcome_dict['by_type'] = 'wickets'
            outcome_dict['by_margin'] = outcome_info['by']['wickets']

        outcome_dict['by_innings'] = outcome_info['by']['innings'] if 'innings' in outcome_info['by'].keys(
        ) else np.nan
    else:
        outcome_dict['by_type'] = np.nan
        outcome_dict['by_margin'] = np.nan

    uncertain_columns = ['winner', 'eliminator',
                         'result', 'method', 'bowl_out']

    for a_col in uncertain_columns:
        outcome_dict[a_col] = outcome_info[a_col] if a_col in outcome_info.keys(
        ) else np.nan

    outcome_df = outcome_df.append(outcome_dict, ignore_index=True)
    return outcome_df


def date_entry(key: str, dates: list) -> pd.DataFrame:
    dates_df = pd.DataFrame(columns=['key', 'date'])
    for date in dates:
        date_dict = dict()
        date_dict['key'] = key
        date_dict['date'] = date
        dates_df = dates_df.append(date_dict, ignore_index=True)
    return dates_df


def pom_entry(key: str, pom_list: list) -> pd.DataFrame:

    pom_df = pd.DataFrame(columns=['key', 'player_of_match'])
    for pom in pom_list:
        pom_dict = dict()
        pom_dict['key'] = key
        pom_dict['player_of_match'] = pom
        pom_df = pom_df.append(pom_dict, ignore_index=True)
    return pom_df

# super sub


def supersub_entry(key: str, supersub_info: dict) -> pd.DataFrame:
    supersub_dict = dict()
    supersub_df = pd.DataFrame(columns=['key', 'team', 'player'])
    for team in supersub_info:
        supersub_dict['key'] = key
        supersub_dict['team'] = team
        supersub_dict['player'] = supersub_info[team]
        supersub_df = supersub_df.append(supersub_dict, ignore_index=True)
    return supersub_df


# bowl_out
def bowl_out_entry(key: str, bowl_out_info: dict) -> pd.DataFrame:
    bo_df = pd.DataFrame(columns=['key', 'bowler', 'outcome'])
    for bo_dict in bowl_out_info:
        bo_dict['key'] = key
        bo_df = bo_df.append(bo_dict, ignore_index=True)
    return bo_df


def player_entry(key: str, players: dict, registry: dict) -> pd.DataFrame:
    player_df = pd.DataFrame(columns=['key', 'team', 'player', 'reg_no'])
    player_dict = dict()
    for team in players:
        for player in players[team]:
            player_dict = dict()
            player_dict['key'] = key
            player_dict['team'] = team
            player_dict['player'] = player
            player_dict['reg_no'] = registry['people'][player]
            player_df = player_df.append(player_dict, ignore_index=True)
            player_dict = None

    return player_df
