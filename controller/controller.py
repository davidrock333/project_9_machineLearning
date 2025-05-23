import requests as request  # installed from request
import pandas as pd  # installed from pandas
import os
import yaml  # installed from PyYAML
from bs4 import BeautifulSoup as bs  # installed from bs4
import logging as log  # control error from logs


def __exception__(exception, where: str = ''):
    '''
        Read the exception and 
        return a dict to describe the error
    '''
    return {"type": type(exception),
            "notes": exception.args,
            "error": exception,
            "from": where}


def __charge_table_lxml__(URL):
    '''
        Send a get request
        If status is 200 return text 
        If status is not 200 return string with 
            the status code 
    '''
    try:
        req = request.get(URL)
        if req.status_code == 200:
            soup = bs(req.text, 'lxml')
            return soup
        else:
            return 'Error,status code return {}'.format(req.status_code)
    except Exception as e:
        return __exception__(e, 'charge_table_lxml')


def __charge_variables__():
    '''
        Read the file config,yml 
        return all variables defined as a array
    '''
    log.debug('Reading variables')
    ENV = os.environ.get("ENV")
    try:
        with open('config.yml', 'r') as file:
            data = yaml.safe_load(file)
        if ENV == None:
            log.debug('Running in test mood')
            return data["test"]
        elif ENV == "pro":
            log.info('Running in production mood')
            return data[ENV]
    except Exception as e:
        log.warning(__exception__(e, 'charge_variables'))


def charge_file(url):
    '''
        url: type String Not null
        Getting url and return a dataframe from csv file 
        using pandas.read_csv
    '''
    try:
        return pd.read_csv(url)
    except Exception as e:
        return __exception__(e, 'charge_file')


def get_variable(arg):
    try:
        log.info('Running in test mood')
        data = __charge_variables__()
        return data[arg]
    except Exception as e:
        log.warning(__exception__(e, 'get_variable'))


def check_duplicates(dataframe):
    '''
        Check in the dataframe if exist duplicates returning string  
    '''
    value = [f'Values duplicated {value}' if dataframe.duplicated(
    ).sum() != 0 else 'Duplicates not found']
    return value


def charge_table(request, attrs: dict):
    '''
        Charge table from the request, the URL is setting from YML to avoid using from 
    '''
    URL = get_variable(request)
    try:
        content = []
        soup = __charge_table_lxml__(URL)
        table = soup.find('table', attrs=attrs)
        data_columns = table.find('thead').find_all('th')
        columns = [column.text for column in data_columns]

        for row in table.find_all('tr'):
            content.append(
                [element.text for element in row.find_all('td') if element.text != ""])
        content.pop(0)
        return pd.DataFrame(data=content, columns=columns)
    except Exception as e:
        return __exception__(e, 'charge_table')
