import pytz
import requests
from bs4 import BeautifulSoup
from zipfile import ZipFile
from datetime import datetime
import os
from pandas import read_csv, DataFrame

def game_types() -> dict:
    '''
    Returns a dict of the abbreviation codes of T20 leagues provided in the README

        Returns:
            a dict of the abbreviation codes of T20 leagues provided in the README
    '''

    # url of the source
    main_url = 'https://cricsheet.org/matches/'

    # requesting website for data with BS4
    page = requests.get(main_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    tag_dl = soup.find_all('dl')

    # storing required links and their wrapped text in a dictionary called data_url
    data_url = dict()
    match_type = [match.text for match in tag_dl[0].find_all('dt')]
    count = 0
    for i in tag_dl[0].find_all('dd'):
        # print(type(i) == "<class 'bs4.element.Tag'>")
        # print(isinstance(type(i), bs4.element.Tag))
        # print(i.find_all('a')[1]['href'].split('/')[2][:-4])
        key = i.find_all('a')[1]['href'].split('/')[2][:-4]
        link = 'https://cricsheet.org' + i.find_all('a')[1]['href']
        data_url[key] = [link, match_type[count]]
        count += 1

    # printing the dictionary for reference
    # for key in data_url:
        # print(key,':',data_url[key][1], data_url[key][0])

    with open('./README.md', 'r') as f:
        readme = f.readlines()

    readme = readme[readme.index('### Game types available <br>\n'):]
    readme = readme[4:]

    table = list()
    for x in readme:
        if x[0] != '|':
            break
        table.append(x)

    table = [x.split('| ') for x in table]

    input_list = [table[x][2].strip().lower() for x in range(0, len(table))]

    # print(data_url)

    output_dict = {}
    for input in input_list:
        output_dict[input] = data_url[input][0]

    return output_dict

def file_process():
    games_dict = game_types()

    for game in games_dict:

        r = requests.get(games_dict[game])

        zip_file = f'./{game}.zip'

        with open(zip_file, 'wb') as zip:
            zip.write(r.content)
        
        with ZipFile(zip_file, 'r') as zipObj:
            listofFileNames = zipObj.namelist()
            for filename in listofFileNames:
                if filename.endswith('.yaml'):
                    zipObj.extract(filename, f'./{game}_files')
                if filename.endswith('.txt'):
                    zipObj.extract(filename, './')
        
        files_list = list()

        if game == 't20s':
            with open('./README.txt', 'a') as file_obj:
                file_obj.write('\n')
                file_obj.write(
                    '2019-05-05 - international - T20 - female - 1182643 - Kenya vs Namibia')
        
        with open('./README.txt', 'r') as readme:
            for line in readme:
                if line[0] == '2':
                    readme_list = line.split('-')
                    readme_list = [x.strip(' ') for x in readme_list]
                    readme_list = [x.strip('\n') for x in readme_list]
                    files_list.append(str(readme_list[6]))
        
        count = 1
        for i in range(len(files_list)-1, -1, -1):
            for filename in enumerate(os.listdir(f'./{game}_files')):
                new_name = filename[1][:-5]
                if files_list[i] == new_name:
                    file_count = str(format(count, '04d'))
                    dst = f'./{game}_files/{game}{file_count}.yaml'
                    src = f'./{game}_files/{filename[1]}'

                    os.rename(src, dst)

            count += 1
        
        with open('./logs.txt','a') as f:
            now = datetime.now(pytz.utc)
            dt_string = now.strftime("%b %d, %Y %H:%M:%S UTC")
            f.write(f'{dt_string} | {len(files_list)} files of {game.upper()} processed\n')
            if game == 'wtc':
                final_line = '-'*20
                f.write(f'{final_line}\n')

        try:
            os.remove(f'{game}.zip')
        except OSError as e:
            print(f'Error: {game}.zip : {e.strerror}')

def load_df(file_types: dict, game: str) -> dict:
    dict_data_df = dict()

    for file_type in file_types.keys():
        if not f'{file_type}_df.csv' in os.listdir(f'{game}_data'):
            dict_data_df[file_type] = DataFrame(
                columns=file_types[file_type])
        else:
            dict_data_df[file_type] = read_csv(
                f'./{game}_data/{file_type}_df.csv')

    return dict_data_df
