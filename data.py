# load required packages

import yaml
import zipfile
from zipfile import ZipFile
import requests
import os
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

# url of the source
main_url = 'https://cricsheet.org/'

# requesting website for data with BS4
page = requests.get(main_url)
soup = BeautifulSoup(page.content, 'html.parser')
tag_dt = soup.find_all('dt')

# storing required links and their wrapped text in a dictionary called data_url
data_url = dict()
for tag in tag_dt:
    temp_text = tag.a['href']
    match_type = tag.a.contents[0]
    link = main_url + temp_text  # link of the match types
    key = temp_text.split('/')[2][:-4]  # abbreivated match_type stored as key

    # magical part of this cell :)
    data_url[key] = [link, match_type]

# printing the dictionary for reference
# for key in data_url:
    # print(key,':',data_url[key][1], data_url[key][0])

# there is a change in this part. The main goal is to read from the markdown. For now, it will be manually done

with open('./README.md', 'r') as f:
    readme = f.readlines()

readme = readme[readme.index('### Game types available <br>\n'):]
readme = readme[4:]

table = list()
for x in readme:
    if x[0] == '|':
        table.append(x)

table = [x.split('| ') for x in table]

input_list = [table[x][2].strip().lower() for x in range(0, len(table))]
print(input_list)

# functions to process dictionary


def meta_func(temp_info, type_cric, i):

    meta_dict = temp_info['meta']
    meta_dict['key_id'] = type_cric + str(format(i, '04d'))

    return meta_dict


def toss_func(temp_info, type_cric, i):
    '''
    Returns a dictionary of information on info of the match

        Parameters:
            temp_info: a dictionary containing raw information of the match
            type_cric: type of cricket format

        Returns:
            a dictionary of information on info of the match
    '''

    toss_dict = temp_info['toss']
    toss_dict['key_id'] = type_cric + str(format(i, '04d'))

    return toss_dict


def info_func(temp_info, type_cric, i):
    '''
    Returns a dictionary of information on info of the match

        Parameters:
            temp_info: a dictionary containing raw information of the match
            type_cric: type of cricket format

        Returns:
            a dictionary of information on info of the match
    '''

    # initialising variable
    info_dict = dict()

    # storing necessary information from the variable into the info dictionary
    info_dict['key_id'] = type_cric + str(format(i, '04d'))

    if 'city' in temp_info.keys():
        info_dict['city'] = temp_info['city']
    else:
        info_dict['city'] = np.nan

    if 'competition' in temp_info.keys():
        info_dict['competition'] = temp_info['competition']
    else:
        info_dict['competition'] = np.nan

    if 'dates' in temp_info.keys():
        info_dict['date'] = temp_info['dates'][0]
    else:
        info_dict['date'] = np.nan

    if 'gender' in temp_info.keys():
        info_dict['gender'] = temp_info['gender']
    else:
        info_dict['gender'] = np.nan

    if 'match_type' in temp_info.keys():
        info_dict['match_type'] = temp_info['match_type']
    else:
        info_dict['match_type'] = np.nan

    if 'match_type_number' in temp_info.keys():
        info_dict['match_type_number'] = temp_info['match_type_number']
    else:
        info_dict['match_type_number'] = np.nan

    if 'neutral_venue' in temp_info.keys():
        info_dict['neutral_venue'] = 1
    else:
        info_dict['neutral_venue'] = np.nan

    if 'overs' in temp_info.keys():
        info_dict['overs'] = temp_info['overs']
    else:
        info_dict['overs'] = np.nan

    if 'player_of_match' in temp_info.keys():
        info_dict['player_of_match'] = temp_info['player_of_match'][0]
    else:
        info_dict['player_of_match'] = np.nan

    if 'venue' in temp_info.keys():
        info_dict['venue'] = temp_info['venue']
        if temp_info['venue'] == 'Dubai International Cricket Stadium':
            info_dict['city'] = 'Dubai'
        if temp_info['venue'] == 'Sharjah Cricket Stadium':
            info_dict['city'] = 'Sharjah'
    else:
        info_dict['venue'] = np.nan

    # return dictionary
    return info_dict


def outcome_func(temp_info, type_cric, i):
    '''
    Returns a dictionary of information on outcome of the match

        Parameters:
            temp_info: a dictionary containing raw information of the match
            type_cric: type of cricket format

        Returns:
            a dictionary of information on outcome of the match
    '''

    # initialising variable
    outcome_dict = dict()

    # storing necessary information from the variable into the output dictionary
    outcome_dict['key_id'] = type_cric + str(format(i, '04d'))

    temp_info = temp_info['outcome']

    if 'by' in temp_info.keys():
        if 'innings' in temp_info['by'].keys():
            outcome_dict['by_innings'] = temp_info['by']['innings']
        else:
            outcome_dict['by_innings'] = np.nan

        if 'runs' in temp_info['by'].keys():
            outcome_dict['by_type'] = 'runs'
            outcome_dict['by_margin'] = temp_info['by']['runs']
        elif 'wickets' in temp_info['by'].keys():
            outcome_dict['by_type'] = 'wickets'
            outcome_dict['by_margin'] = temp_info['by']['wickets']
        else:
            outcome_dict['by_type'] = np.nan
            outcome_dict['by_margin'] = np.nan
    else:
        outcome_dict['by_innings'] = np.nan
        outcome_dict['by_type'] = np.nan
        outcome_dict['by_margin'] = np.nan

    if 'bowl_out' in temp_info.keys():
        outcome_dict['bowl_out'] = temp_info['bowl_out']
    else:
        outcome_dict['bowl_out'] = np.nan

    if 'eliminator' in temp_info.keys():
        outcome_dict['eliminator'] = temp_info['eliminator']
    else:
        outcome_dict['eliminator'] = np.nan

    if 'method' in temp_info.keys():
        outcome_dict['method'] = temp_info['method']
    else:
        outcome_dict['method'] = np.nan

    if 'result' in temp_info.keys():
        outcome_dict['result'] = temp_info['result']
    else:
        outcome_dict['result'] = np.nan

    if 'winner' in temp_info.keys():
        outcome_dict['winner'] = temp_info['winner']
    else:
        outcome_dict['winner'] = np.nan

    # return dictionary
    return outcome_dict


type_cric = 'ipl'
for type_cric in input_list:
    r = requests.get(data_url[type_cric][0])

    with open('./'+type_cric+'.zip', 'wb') as zip:
        zip.write(r.content)

    with ZipFile('./'+type_cric+'.zip', 'r') as zipObj:
        listofFileNames = zipObj.namelist()
        for filename in listofFileNames:
            if filename.endswith('.yaml'):
                zipObj.extract(filename, './' + type_cric + '_files')
            if filename.endswith('.txt'):
                zipObj.extract(filename, './')

    files_list = list()

    with open('./README.txt', 'r') as readme:
        for line in readme:
            if line[0] == '2':
                readme_list = line.split('-')
                readme_list = [x.strip(' ') for x in readme_list]
                readme_list = [x.strip('\n') for x in readme_list]
                files_list.append(str(readme_list[6]))

    # instead of printing this, log it in a txt file with the time it was processed on
    print(len(files_list))

    count = 1
    for i in range(len(files_list)-1, -1, -1):
        for filename in enumerate(os.listdir('./' + type_cric + '_files')):
            new_name = filename[1][:-5]
            if files_list[i] == new_name:
                dst = './' + type_cric + '_files/' + type_cric + \
                    str(format(count, '04d')) + '.yaml'
                src = './' + type_cric + '_files/' + filename[1]

                os.rename(src, dst)

        count += 1

    # code to delete the zip file and readme

    # dataframe initialization

    # columns
    meta_columns = ['key_id', 'data_version', 'created', 'revision']
    toss_columns = ['key_id', 'toss_winner', 'toss_decision']
    team_columns = ['key_id', 'team']
    umpires_columns = ['key_id', 'umpires']
    info_columns = ['key_id', 'city', 'competition', 'date', 'gender', 'match_type',
                    'match_type_number', 'neutral_venue', 'overs', 'player_of_match',
                    'venue']
    dates_columns = ['key_id', 'date']
    outcome_columns = ['key_id', 'by_innings', 'by_type', 'by_margin', 'bowl_out',
                    'eliminator', 'method', 'result', 'winner']
    pom_columns = ['key_id', 'player_of_match']
    bowl_out_columns = ['key_id', 'bowler', 'outcome']
    supersub_columns = ['key_id', 'team', 'player']

    innings_columns = ['key_id', 'innings_no', 'team', 'ball', 'batsman', 'bowler',
                    'non_striker', 'runs_batsman', 'runs_extras', 'runs_non_boundary',
                    'runs_total', 'wicket_fielder', 'wicket_kind', 'wicket_player_out',
                    'extras_type', 'extras_run']

    # checking if path exists or not
    if not os.path.exists(type_cric + '_data'):
        os.makedirs(type_cric+'_data')

    # initializing meta_df
    if not 'meta_df.csv' in os.listdir(type_cric+'_data'):
        meta_df = pd.DataFrame(columns=meta_columns)
    else:
        meta_df = pd.read_csv('./'+type_cric+'_data/meta_df.csv')

    # initializing toss_df
    if not 'toss_df.csv' in os.listdir(type_cric+'_data'):
        toss_df = pd.DataFrame(columns=toss_columns)
    else:
        toss_df = pd.read_csv('./'+type_cric+'_data/toss_df.csv')

    # initializing team_df
    if not 'team_df.csv' in os.listdir(type_cric+'_data'):
        team_df = pd.DataFrame(columns=team_columns)
    else:
        team_df = pd.read_csv('./'+type_cric+'_data/team_df.csv')

    # initializing umpires_df
    if not 'umpires_df.csv' in os.listdir(type_cric+'_data'):
        umpires_df = pd.DataFrame(columns=umpires_columns)
    else:
        umpires_df = pd.read_csv('./'+type_cric+'_data/umpires_df.csv')

    # initializing info_df
    if not 'info_df.csv' in os.listdir(type_cric+'_data'):
        info_df = pd.DataFrame(columns=info_columns)
    else:
        info_df = pd.read_csv('./'+type_cric+'_data/info_df.csv')

    # initializing meta_df
    if not 'dates_df.csv' in os.listdir(type_cric+'_data'):
        dates_df = pd.DataFrame(columns=dates_columns)
    else:
        dates_df = pd.read_csv('./'+type_cric+'_data/dates_df.csv')

    # initializing meta_df
    if not 'outcome_df.csv' in os.listdir(type_cric+'_data'):
        outcome_df = pd.DataFrame(columns=outcome_columns)
    else:
        outcome_df = pd.read_csv('./'+type_cric+'_data/outcome_df.csv')

    # initializing pom_df
    if not 'pom_df.csv' in os.listdir(type_cric+'_data'):
        pom_df = pd.DataFrame(columns=pom_columns)
    else:
        pom_df = pd.read_csv('./'+type_cric+'_data/pom_df.csv')

    # initializing bowl_out_df
    if not 'bowl_out_df.csv' in os.listdir(type_cric+'_data'):
        bowl_out_df = pd.DataFrame(columns=bowl_out_columns)
    else:
        bowl_out_df = pd.read_csv('./'+type_cric+'_data/bowl_out_df.csv')

    # initializing supersub_df
    if not 'supersub_df.csv' in os.listdir(type_cric+'_data'):
        supersub_df = pd.DataFrame(columns=supersub_columns)
    else:
        supersub_df = pd.read_csv('./'+type_cric+'_data/supersub_df.csv')

    # initializing innings_df
    if not 'innings_df.csv' in os.listdir(type_cric+'_data'):
        innings_df = pd.DataFrame(columns=innings_columns)
    else:
        innings_df = pd.read_csv('./'+type_cric+'_data/innings_df.csv')

    # log a random info dictionary in a txt file
    # it is printed in the terminal for now
    with open('./ipl_files/ipl0845.yaml') as f:
        cric_dict = yaml.load(f)
    temp_info = cric_dict['info']
    print(temp_info)

    for i in range(1, len(files_list)+1):

        path = './' + type_cric + '_files/' + \
            type_cric + str(format(i, '04d')) + '.yaml'

        key_id = type_cric + str(format(i, '04d'))

        if key_id in list(info_df['key_id']):
            continue
        else:
            print(i, 'lol')

        with open(path) as f:
            cric_dict = yaml.load(f)
        meta_info = cric_dict['meta']

        temp_info = cric_dict['info']

        # import functions for their particular usage
        meta_df = meta_df.append(
            meta_func(cric_dict, type_cric, i), ignore_index=True)

        outcome_df = outcome_df.append(outcome_func(
            temp_info, type_cric, i), ignore_index=True)
        info_df = info_df.append(
            info_func(temp_info, type_cric, i), ignore_index=True)
        toss_df = toss_df.append(
            toss_func(temp_info, type_cric, i), ignore_index=True)

        if 'dates' in temp_info.keys():
            for date in temp_info['dates']:
                date_dict = dict()
                date_dict['key_id'] = type_cric + str(format(i, '04d'))
                date_dict['date'] = date
                dates_df = dates_df.append(date_dict, ignore_index=True)
                date_dict = None
        else:
            date_dict = {'key_id': type_cric +
                         str(format(i, '04d')), 'date': np.nan}
            dates_df = dates_df.append(date_dict, ignore_index=True)
            date_dict = None

        if 'player_of_match' in temp_info.keys():
            for player in temp_info['player_of_match']:
                pom_dict = dict()
                pom_dict['key_id'] = type_cric + str(format(i, '04d'))
                pom_dict['player_of_match'] = player
                pom_df = pom_df.append(pom_dict, ignore_index=True)
                pom_dict = None
            else:
                pom_dict = {'key_id': type_cric +
                            str(format(i, '04d')), 'player_of_match': np.nan}
                pom_df = pom_df.append(pom_dict, ignore_index=True)
                pom_dict = None

        if 'supersubs' in temp_info.keys():
            supersub_dict = dict()
            for key in temp_info['supersubs']:
                supersub_dict['key_id'] = type_cric + str(format(i, '04d'))
                supersub_dict['team'] = key
                supersub_dict['player'] = temp_info['supersubs'][key]
                supersub_df = supersub_df.append(supersub_dict, ignore_index=True)
                supersub_dict = None
        else:
            supersub_dict = {'key_id': type_cric +
                             str(format(i, '04d')), 'team': np.nan, 'player': np.nan}
            supersub_df = supersub_df.append(supersub_dict, ignore_index=True)
            supersub_dict = np.nan

        if 'bowl_out' in temp_info.keys():
            bo_dict = dict()
            for x in temp_info['bowl_out']:
                x['key_id'] = type_cric + str(format(i, '04d'))
                bowl_out_df = bowl_out_df.append(x, ignore_index=True)
                x = None
        else:
            bo_dict = {'key_id': type_cric +
                       str(format(i, '04d')), 'bowler': np.nan, 'outcome': np.nan}
            bowl_out_df = bowl_out_df.append(bo_dict, ignore_index=True)
            bo_dict = None

        # teams function
        if 'teams' in temp_info.keys():
            for team in temp_info['teams']:
                team_dict = dict()
                team_dict['key_id'] = type_cric + str(format(i, '04d'))
                team_dict['teams'] = team
                team_df = team_df.append(team_dict, ignore_index=True)
                team_dict = None
        else:
            team_dict = {'key_id': type_cric +
                         str(format(i, '04d')), 'teams': np.nan}
            team_df = team_df.append(team_dict, ignore_index=True)
            team_dict = None

        # umpire function
        if 'umpires' in temp_info.keys():
            for umpire in temp_info['umpires']:
                umpire_dict = dict()
                umpire_dict['key_id'] = type_cric + str(format(i, '04d'))
                umpire_dict['umpires'] = umpire
                umpires_df = umpires_df.append(umpire_dict, ignore_index=True)
                umpire_dict = None
        else:
            umpire_dict = {'key_id': type_cric +
                           str(format(i, '04d')), 'umpires': np.nan}
            umpires_df = umpires_df.append(umpire_dict, ignore_index=True)
            umpire_dict = None

        print(i)

    if 'Unnamed: 0' in list(meta_df.columns):
        meta_df = meta_df.drop(columns='Unnamed: 0')

    if 'Unnamed: 0' in list(toss_df.columns):
        toss_df = toss_df.drop(columns='Unnamed: 0')

    if 'Unnamed: 0' in list(team_df.columns):
        team_df = team_df.drop(columns='Unnamed: 0')

    if 'Unnamed: 0' in list(umpires_df.columns):
        umpires_df = umpires_df.drop(columns='Unnamed: 0')

    if 'Unnamed: 0' in list(info_df.columns):
        info_df = info_df.drop(columns='Unnamed: 0')

    if 'Unnamed: 0' in list(dates_df.columns):
        dates_df = dates_df.drop(columns='Unnamed: 0')

    if 'Unnamed: 0' in list(outcome_df.columns):
        outcome_df = outcome_df.drop(columns='Unnamed: 0')

    if 'Unnamed: 0' in list(pom_df.columns):
        pom_df = pom_df.drop(columns='Unnamed: 0')

    if 'Unnamed: 0' in list(bowl_out_df.columns):
        bowl_out_df = bowl_out_df.drop(columns='Unnamed: 0')

    if 'Unnamed: 0' in list(supersub_df.columns):
        supersub_df = supersub_df.drop(columns='Unnamed: 0')

    # # removing unnecessary columns

    for x in meta_columns:
        if x in meta_df.columns:
            if meta_df[x].isnull().all():
                meta_df = meta_df.drop(columns=[x])
    for x in toss_columns:
        if x in toss_df.columns:
            if toss_df[x].isnull().all():
                toss_df = toss_df.drop(columns=[x])

    for x in team_columns:
        if x in team_df.columns:
            if team_df[x].isnull().all():
                team_df = team_df.drop(columns=[x])

    for x in umpires_columns:
        if x in umpires_df.columns:
            if umpires_df[x].isnull().all():
                umpires_df = umpires_df.drop(columns=[x])

    for x in info_columns:
        if x in info_df.columns:
            if info_df[x].isnull().all():
                info_df = info_df.drop(columns=[x])

    for x in dates_columns:
        if x in dates_df.columns:
            if dates_df[x].isnull().all():
                dates_df = dates_df.drop(columns=[x])

    for x in outcome_columns:
        if x in outcome_df.columns:
            if outcome_df[x].isnull().all():
                outcome_df = outcome_df.drop(columns=[x])

    for x in pom_columns:
        if x in pom_df.columns:
            if pom_df[x].isnull().all():
                pom_df = pom_df.drop(columns=[x])

    for x in bowl_out_columns:
        if x in bowl_out_df.columns:
            if bowl_out_df[x].isnull().all():
                bowl_out_df = bowl_out_df.drop(columns=[x])

    for x in supersub_columns:
        if x in supersub_df.columns:
            if supersub_df[x].isnull().all():
                supersub_df = supersub_df.drop(columns=[x])

    toss_df['winner'] = toss_df.winner.replace(
        'Rising Pune Supergiant', 'Rising Pune Supergiants')
    toss_df['winner'] = toss_df.winner.replace(
        'Delhi Daredevils', 'Delhi Capitals')
    toss_df['winner'] = toss_df.winner.replace(
        'Pune Warriors', 'Pune Warriors India')
    toss_df['winner'] = toss_df.winner.replace('Kings XI Punjab', 'Punjab Kings')

    team_df['teams'] = team_df.teams.replace(
        'Rising Pune Supergiant', 'Rising Pune Supergiants')
    team_df['teams'] = team_df.teams.replace('Delhi Daredevils', 'Delhi Capitals')
    team_df['teams'] = team_df.teams.replace(
        'Pune Warriors', 'Pune Warriors India')
    team_df['teams'] = team_df.teams.replace('Kings XI Punjab', 'Punjab Kings')

    outcome_df['winner'] = outcome_df.winner.replace('Rising Pune Supergiant', 'Rising Pune Supergiants')
    outcome_df['winner'] = outcome_df.winner.replace('Delhi Daredevils', 'Delhi Capitals')
    outcome_df['winner'] = outcome_df.winner.replace('Pune Warriors', 'Pune Warriors India')
    outcome_df['winner'] = outcome_df.winner.replace('Kings XI Punjab', 'Punjab Kings')

    data_path = './' + type_cric + '_data/'


    meta_df.to_csv(data_path + 'meta_df.csv', index=False)
    toss_df.to_csv(data_path + 'toss_df.csv', index=False)
    team_df.to_csv(data_path + 'team_df.csv', index=False)
    umpires_df.to_csv(data_path + 'umpires_df.csv', index=False)
    info_df.to_csv(data_path + 'info_df.csv', index=False)
    dates_df.to_csv(data_path + 'dates_df.csv', index=False)
    outcome_df.to_csv(data_path + 'outcome_df.csv', index=False)
    pom_df.to_csv(data_path + 'pom_df.csv', index=False)
    bowl_out_df.to_csv(data_path + 'bowl_out_df.csv', index=False)
    supersub_df.to_csv(data_path + 'supersub_df.csv', index=False)

    #code for innings

    for i in range(1, len(files_list)+1):
        path = './' + type_cric + '_files/' + type_cric + str(format(i,'04d')) + '.yaml'
        key_id = type_cric + str(format(i,'04d'))
        if key_id in list(innings_df['key_id']):
            continue
        else:
            print(i,'lol')
        
        with open(path) as f:
            cric_dict = yaml.load(f)
        temp_info = cric_dict['innings']
        #loop over list
        for x in temp_info:
            # print(x)
            #loop over dictionary
            for y in x:
                if 'super over' in y.lower():
                    innings_no += 1
                else:
                    innings_no = int(y[0])
                # print(innings_no)
                # print(x[y])
                team_name = x[y]['team']
                # print(team_name)
                all_deliveries = x[y]['deliveries']
                for z in all_deliveries:
                    delivery_no = list(z.keys())[0]
                    non_striker = z[delivery_no]['non_striker']
                    bowler = z[delivery_no]['bowler']
                    batsman = z[delivery_no]['batsman']
                    runs_batsman = z[delivery_no]['runs']['batsman']
                    runs_extras = z[delivery_no]['runs']['extras']
                    if 'non_boundary' in z[delivery_no]['runs'].keys():
                        runs_non_boundary = z[delivery_no]['runs']['non_boundary']
                    else:
                        runs_non_boundary = 0
                    runs_total = z[delivery_no]['runs']['total']

                    # This is not the accurate way, only the first wicket has to be taken, 
                    # coz of the one instance where 2 wickets took place in the same ball
                    if 'wicket' in z[delivery_no].keys():
                        # print(z[delivery_no]['wicket'])
                        if 'fielders' in z[delivery_no]['wicket'].keys():
                            wicket_fielder = z[delivery_no]['wicket']['fielders'][0]
                        else:
                            wicket_fielder = np.nan
                        wicket_kind = z[delivery_no]['wicket']['kind']
                        wicket_player_out = z[delivery_no]['wicket']['player_out']
                    else:
                        wicket_fielder = np.nan
                        wicket_kind = np.nan
                        wicket_player_out = np.nan

                    if 'extras' in z[delivery_no].keys():
                        extras_type = list(z[delivery_no]['extras'].keys())[0]
                        extras_runs = z[delivery_no]['extras'][extras_type]
                    else:
                        extras_type = np.nan
                        extras_runs = np.nan

                    innings_dict = dict()
                    innings_dict['key_id'] = type_cric + str(format(i,'04d'))
                    innings_dict['innings_no'] = innings_no
                    innings_dict['team'] = team_name
                    innings_dict['ball'] = delivery_no
                    innings_dict['batsman'] = batsman
                    innings_dict['bowler'] = bowler
                    innings_dict['non_striker'] = non_striker
                    innings_dict['runs_batsman'] = runs_batsman
                    innings_dict['runs_extras'] = runs_extras
                    innings_dict['runs_non_boundary'] = runs_non_boundary
                    innings_dict['runs_total'] = runs_total
                    
                    innings_dict['wicket_fielder'] = wicket_fielder
                    innings_dict['wicket_kind'] = wicket_kind
                    innings_dict['wicket_player_out'] = wicket_player_out
                    innings_dict['extras_type'] = extras_type
                    innings_dict['extras_runs'] = extras_runs
                    # print(z[delivery_no])

                    # for x in innings_dict:
                    #     print(x,':',innings_dict[x])
                    innings_df = innings_df.append(innings_dict, ignore_index=True)
                    
                    innings_dict = None
        print(i)
        innings_no = None

    innings_df['team'] = innings_df.team.replace('Rising Pune Supergiant','Rising Pune Supergiants')
    innings_df['team'] = innings_df.team.replace('Delhi Daredevils','Delhi Capitals')
    innings_df['team'] = innings_df.team.replace('Pune Warriors','Pune Warriors India')
    innings_df['team'] = innings_df.team.replace('Kings XI Punjab','Punjab Kings')

    if 'Unnamed: 0' in list(innings_df.columns):
        innings_df = innings_df.drop(columns='Unnamed: 0')

    for x in innings_columns:
        if x in innings_df.columns:
            if innings_df[x].isnull().all():
                innings_df = innings_df.drop(columns=[x])

    innings_df.to_csv(data_path + 'innings_df.csv', index=False)