from scraper import game_types, file_process
import pandas as pd
import os
import yaml
import numpy as np
import shutil


def meta_func(temp_info, type_cric, i):

    meta_dict = temp_info['meta']
    meta_dict['key_id'] = type_cric + str(format(i, '04d'))

    return meta_dict


# reference meta_df
meta_columns = ['key_id', 'data_version', 'created', 'revision']

input_list = game_types()[1]
data_url = game_types()[0]

# type_cric = 'ipl'
file_process()

for type_cric in input_list:
    current_meta = pd.read_csv(
        'https://sawlachintan.github.io/cricket_data/' + type_cric + '_data/meta_df.csv')
    print(current_meta.head())

    files_list = os.listdir(type_cric + '_files')
    meta_df = pd.DataFrame(columns=meta_columns)

    for i in range(1, len(files_list)+1):

        path = './' + type_cric + '_files/' + \
            type_cric + str(format(i, '04d')) + '.yaml'

        key_id = type_cric + str(format(i, '04d'))

        with open(path) as f:
            cric_dict = yaml.load(f)

        # import functions for their particular usage
        meta_df = meta_df.append(
            meta_func(cric_dict, type_cric, i), ignore_index=True)

    print(meta_df.head())
    # code for comparing the dataframes
    theory = meta_df[['data_version', 'revision']]
    prac = current_meta[['data_version', 'revision']]
    print(theory.shape, prac.shape)
    # theory['data_match'] = np.where((theory['data_version'] == prac['data_version']) | (theory['revision'] == prac['revision']),'True', 'False')

    print('--------------------')
    print(theory.shape)
    print('--------------------')
    try:
        shutil.rmtree(type_cric + '_files')
    except OSError as e:
        print('Error: %s : %s' % (type_cric + '_files', e.strerror))
try:
    os.remove('README.txt')
except OSError as e:
    print('Error: %s : %s' % ('README.txt', e.strerror))
