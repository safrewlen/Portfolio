import pandas as pd
import numpy as np
import re
from collections import Counter


def load_data(path):
    data = pd.read_csv(path, sep=',')
    pd.set_option('display.max_columns', 999)
    data['Posting Date'] = data['Posting Date'].astype('datetime64[D]')
    data['Mean Salary'] = data['Salary Range From'] + (data['Salary Range To'] - data['Salary Range From']) / 2
    return data


def select_non_numeric_columns(df):
    str_columns = []
    for column in df.columns:
        if(df[column].dtype == object):
            str_columns.append(column)
    return str_columns


# excces chars like \t, $, @ and so on
def remove_char(col_val):
    col_val = re.sub(r'[^a-zA-Z0-9 &?!.,-]', '', str(col_val))
    return col_val


def load_purified_data(path):
    data = load_data(path)
    str_columns = select_non_numeric_columns(data)
    for col in data[str_columns]:
        data[col] = data[col].apply(remove_char)
        data[col] = data[col].str.lower()
    data = data.replace('nan', np.NaN)
    return data


def top_words(col):
    text_rm_symbols = []
    flat_list = []
    top_words = []

    text_list = col.tolist() 
    text_list_nan_rm = [x for x in text_list if str(x) != 'nan']
    
    for text in text_list_nan_rm:
        text = re.sub(r'[^a-zA-Z0-9 ]', '', text)
        text_rm_symbols.append(text)
        
    for word in text_rm_symbols:
        flat_list = flat_list + word.split(' ')
        
    flat_list = list(filter(None, flat_list))
    top_stats = Counter(flat_list).most_common()
    for tup in top_stats:
        top_words.append(tup[0])
    return top_words