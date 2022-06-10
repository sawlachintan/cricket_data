from file_functions import *
import os
import yaml
import shutil
from dataframe_functions import *
from datetime import datetime
import pytz


def main():
    # download zip files and rename yaml files
    file_process()

    file_types = {'meta': ['key', 'data_version', 'created', 'revision'],
                  'toss': ['key', 'toss_winner', 'toss_decision'],
                  'team': ['key', 'team'],
                  'umpires': ['key', 'umpire'],
                  'info': ['key', 'city', 'competition', 'date', 'gender',
                           'match_type', 'neutral_venue', 'overs', 'player_of_match', 'venue'],
                  'dates': ['key', 'date'],
                  'outcome': ['key', 'by_innings', 'by_type', 'by_margin', 'bowl_out',
                              'eliminator', 'method', 'result', 'winner'],
                  'pom': ['key', 'player_of_match'],
                  'bowl_out': ['key', 'bowler', 'outcome'],
                  'supersub': ['key', 'team', 'player'],
                  'innings': ['key', 'inning_no', 'batting_team', 'delivery_no', 'batter', 'bowler', 'non_striker',
                              'runs_batter', 'runs_extras', 'runs_non_boundary', 'runs_total', 'wicket_fielder', 'wicket_kind', 'wicket_player_out', 'extras_type']}

    for game in game_types().keys():
        start_time = datetime.now(pytz.utc)
        files_list = os.listdir(f'{game}_files')

        if not os.path.exists(f'{game}_data'):
            os.makedirs(f'{game}_data')

        dict_data_df = load_df(file_types, game)

        meta_df = dict_data_df['meta']
        toss_df = dict_data_df['toss']
        team_df = dict_data_df['team']
        umpires_df = dict_data_df['umpires']
        info_df = dict_data_df['info']
        dates_df = dict_data_df['dates']
        outcome_df = dict_data_df['outcome']
        pom_df = dict_data_df['pom']
        bowl_out_df = dict_data_df['bowl_out']
        supersub_df = dict_data_df['supersub']
        innings_df = dict_data_df['innings']

        for file_num in range(1, len(files_list) + 1):
            formatted_file_num = str(format(file_num, '04d'))
            key = f'{game}{formatted_file_num}'

            del formatted_file_num

            path = f'./{game}_files/{key}.yaml'
            with open(path) as f:
                cric_dict = yaml.safe_load(f)

            del path

            cric_meta = cric_dict['meta']
            cric_meta['key'] = key
            if key not in list(meta_df.key):
                meta_df = meta_df.append(cric_meta, ignore_index=True)

            cric_info = cric_dict['info']

            if 'umpires' in cric_info.keys() and key not in list(umpires_df.key):
                umpires_df = umpires_df.append(umpire_entry(
                    umpire_info=cric_info['umpires'], key=key), ignore_index=True)
            if key not in list(team_df.key):
                team_df = team_df.append(team_entry(
                    team_info=cric_info['teams'], key=key), ignore_index=True)
            if key not in list(toss_df.key):
                toss_df = toss_df.append(toss_entry(
                    toss_info=cric_info['toss'], key=key), ignore_index=True)
            if key not in list(outcome_df.key):
                outcome_df = outcome_df.append(outcome_entry(
                    key=key, outcome_info=cric_info['outcome']), ignore_index=True)
            if key not in list(dates_df.key):
                dates_df = dates_df.append(date_entry(
                    key=key, dates=cric_info['dates']), ignore_index=True)

            if 'player_of_match' in cric_info.keys() and key not in list(pom_df.key):
                pom_df = pom_df.append(
                    pom_entry(key=key, pom_list=cric_info['player_of_match']), ignore_index=True)

            if key not in list(info_df.key):
                info_df = info_df.append(
                    info_entry(key=key, gen_info=cric_info))

            if 'bowl_out' in cric_info.keys() and key not in list(bowl_out_df.key):
                bowl_out_df = bowl_out_df.append(bowl_out_entry(
                    key, cric_info['bowl_out']), ignore_index=True)

            if 'supersubs' in cric_info.keys() and key not in list(supersub_df.key):
                supersub_df = supersub_df.append(supersub_entry(
                    key=key, supersub_info=cric_info['supersubs']), ignore_index=True)

            if key not in list(innings_df.key):
                innings_df = innings_df.append(
                    innings_entry(key_id=key, innings_list=cric_dict['innings']))

            del cric_info
            del cric_dict
            del key

        toss_df['winner'] = toss_df.winner.replace(
            'Rising Pune Supergiant', 'Rising Pune Supergiants')
        toss_df['winner'] = toss_df.winner.replace(
            'Delhi Daredevils', 'Delhi Capitals')
        toss_df['winner'] = toss_df.winner.replace(
            'Pune Warriors', 'Pune Warriors India')
        toss_df['winner'] = toss_df.winner.replace(
            'Kings XI Punjab', 'Punjab Kings')

        team_df['team'] = team_df.team.replace(
            'Rising Pune Supergiant', 'Rising Pune Supergiants')
        team_df['team'] = team_df.team.replace(
            'Delhi Daredevils', 'Delhi Capitals')
        team_df['team'] = team_df.team.replace(
            'Pune Warriors', 'Pune Warriors India')
        team_df['team'] = team_df.team.replace(
            'Kings XI Punjab', 'Punjab Kings')

        outcome_df['winner'] = outcome_df.winner.replace(
            'Rising Pune Supergiant', 'Rising Pune Supergiants')
        outcome_df['winner'] = outcome_df.winner.replace(
            'Delhi Daredevils', 'Delhi Capitals')
        outcome_df['winner'] = outcome_df.winner.replace(
            'Pune Warriors', 'Pune Warriors India')
        outcome_df['winner'] = outcome_df.winner.replace(
            'Kings XI Punjab', 'Punjab Kings')

        innings_df['batting_team'] = innings_df.batting_team.replace(
            'Rising Pune Supergiant', 'Rising Pune Supergiants')
        innings_df['batting_team'] = innings_df.batting_team.replace(
            'Delhi Daredevils', 'Delhi Capitals')
        innings_df['batting_team'] = innings_df.batting_team.replace(
            'Pune Warriors', 'Pune Warriors India')
        innings_df['batting_team'] = innings_df.batting_team.replace(
            'Kings XI Punjab', 'Punjab Kings')

        meta_df.to_csv(f'./{game}_data/meta_df.csv', index=False)
        umpires_df.to_csv(f'./{game}_data/umpires_df.csv', index=False)
        team_df.to_csv(f'./{game}_data/team_df.csv', index=False)
        toss_df.to_csv(f'./{game}_data/toss_df.csv', index=False)
        outcome_df.to_csv(f'./{game}_data/outcome_df.csv', index=False)
        dates_df.to_csv(f'./{game}_data/dates_df.csv', index=False)
        pom_df.to_csv(f'./{game}_data/pom_df.csv', index=False)
        info_df.to_csv(f'./{game}_data/info_df.csv', index=False)
        innings_df.to_csv(f'./{game}_data/innings_df.csv', index=False)

        del meta_df
        del umpires_df
        del team_df
        del toss_df
        del outcome_df
        del dates_df
        del pom_df
        del info_df
        del innings_df
        del files_list
        del dict_data_df

        shutil.rmtree(f'{game}_files')

        final_time = datetime.now(pytz.utc)
        time_taken = final_time - start_time

        print(f'{game}: {time_taken}')


if __name__ == "__main__":
    main()
