# load required packages

from zipfile import ZipFile
import requests
import os
from bs4 import BeautifulSoup

def game_types():
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
        # abbreivated match_type stored as key
        key = temp_text.split('/')[2][:-4]

        # magical part of this cell :)
        data_url[key] = [link, match_type]

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

    return (data_url, input_list)


def file_process():

    input_list = game_types()[1]
    data_url = game_types()[0]

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

        if type_cric == 't20s':
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

        try:
            os.remove(type_cric + '.zip')
        except OSError as e:
            print('Error: %s : %s' % (type_cric + '.zip', e.strerror))
        print(type_cric.upper() + ' has been processed')


file_process()