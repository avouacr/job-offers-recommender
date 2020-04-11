import os
from datetime import datetime, time, timedelta

import pandas as pd
import requests
import json
import numpy as np

# Ideas taken from :
# https://github.com/Cocorico84/employme/blob/855cfcda2c54f42b9c42dcbf4ac87cdf09248b7f/back/manager.py
# https://stackoverflow.com/questions/42213427/change-variable-after-a-specific-amount-of-time-python

# TO DO: use environment variables
# TO DO: separer classes, fonction sur differents scripts
access = pd.read_csv("/home/jaime/projet_info_3A/private/access.csv", header=0)
id_api = access["Identifiant"][0]
key_api = access["Clé secrète"][0]

client_id = id_api
client_secret = key_api
access_tokens = {}
cached_packages = None
scope = 'api_offresdemploiv2'
url = "https://api.emploi-store.fr/partenaire"


class TimedValue:
    """
    Elements of this class return True only if less that 4.5 seconds have passed since initialization
    This is important as the Pole Emploi API token only lasts 5 seconds (TO DO: check that)
    """

    def __init__(self):
        self._started_at = datetime.fromtimestamp(0)  # to do False if not started

        pass

    def start(self):
        self._started_at = datetime.utcnow()

    def __call__(self):
        time_passed = datetime.utcnow() - self._started_at
        if time_passed.total_seconds() < 4.5:
            return True
        return False


value = TimedValue()


def set_global_TOKEN():
    """
    Needed to set and update when needed the global variable TOKEN (Pole Emploi API token)
    Returns: Does not return, sets global var TOKEN.

    """
    global TOKEN
    if value() == False:
        url_token = 'https://entreprise.pole-emploi.fr/connexion/oauth2/access_token'
        r = requests.post(url_token, headers={'Content-Type': 'application/x-www-form-urlencoded'},
                          params={'realm': '/partenaire'},
                          data={'grant_type': 'client_credentials', 'client_id': id_api,
                                'client_secret': key_api,
                                'scope': f'application_{id_api} api_offresdemploiv2 o2dsoffre'})
        data = r.json()
        TOKEN = data['access_token']
        value.start()


def connection_with_dates(range_str, min_date, max_date):
    """
    Returns job offers posted between two dates

    Args:
        range_str (str): range of results (e.g. 0-149), maximum is 150 per query, total max is 1200 (TO DO: recheck)
        min_date (datetime): beginning date
        max_date (datetime): end date

    Returns:

    """
    str_min_date = min_date.strftime("%Y-%m-%dT%H:%M:%SZ")
    str_max_date = max_date.strftime("%Y-%m-%dT%H:%M:%SZ")

    set_global_TOKEN()
    url_offers = f'{url}/offresdemploi/v2/offres/search'
    r = requests.get(url=url_offers,
                     params={'range': range_str, 'minCreationDate': str_min_date, 'maxCreationDate': str_max_date},
                     # {'motsCles': 'informatique'} ,# params={'rantge=':range_str}, #,  params={'motsCles': 'informatique'}
                     headers={'Authorization': f'Bearer {TOKEN}'})
    #     print(r)
    try:
        data = r.json()
    except json.decoder.JSONDecodeError:

        try:
            time.sleep(float(
                r.headers['Retry-After']) + 0.1)  # to avoid <Response [429]>, too many requests (if JSONDecodeError).
        except:
            print("###")
            print(str_min_date, str_max_date)
            print(r)
            print(r.headers)
        #             data = connection_with_dates(range_str,min_date,max_date) # to comment ?

        data = connection_with_dates(range_str, min_date, max_date)

    return data


#%%

all_dfs=[]

#%%
path='test'
os.makedirs(path)


# path="/home/jaime/projet_info_3A/private/day_by_day/"

#%%

num_days_lookback = 365*2
dates_range = [(datetime.utcnow()-timedelta(days=i)-timedelta(days=423)) for i in np.linspace(0,num_days_lookback,num_days_lookback)]

#%%

datetime.utcnow()-timedelta(days=423)


def create_date_range_str(i):
    return str(str(min(i, 1000)) + '-' + str(min(i + 149, 1149)))


# %%

def cut_datime_range_into_frecs(min_day, max_day, num_items):
    # mettre num items au lieu de 10 dans la ligne au dessous
    timestamp_range = np.linspace(datetime.timestamp(max_day), datetime.timestamp(min_day), 10, dtype=np.int64)
    timestamp_range = [datetime.fromtimestamp(i) for i in timestamp_range]
    return timestamp_range


# %%

def query_results(min_day, max_day):
    list_of_results = []

    for i in list(range(0, 1150, 150)):
        date_range_str = create_date_range_str(i)
        res = connection_with_dates(date_range_str, min_day, max_day)
        list_of_results.append(res)

        try:
            if len(res['resultats']) < 150:
                break
        except:
            pass

    return list_of_results


# %%

def get_results_in_dates_list(dates_range):
    for day in range(1, len(dates_range) - 1):
        # IMPORTANT: check if range(1,len(dates_range)-1) or range(1,len(dates_range))

        min_day = dates_range[day]
        max_day = dates_range[day - 1]

        # do it more efficient (function and if condition on results)
        #         list_of_results = [connection_with_dates(create_date_range_str(i),min_day,max_day)
        #                            for i in list(range(0,1150,150))]

        list_of_results = query_results(min_day, max_day)

        try:
            list_dfs = [pd.DataFrame.from_dict(request_as_dict['resultats']) for request_as_dict in list_of_results]
        except KeyError:
            print("AAAAAAA")
            print("KEY ERROR, CHECK GLOBAL VAR saving_error")
            global saving_error
            saving_error = list_of_results

        dfs_date = pd.concat(list_dfs, sort=True)

        if len(dfs_date.index) == 0:
            pass

        elif len(dfs_date.index) < 1200:
            csv_name = os.path.join(path, str(dates_range[day + 1]) + ".csv")
            dfs_date.to_csv(csv_name, sep=",")
            # return ?

        if len(dfs_date.index) == 1200:
            print("start missing part of the day")
            # does not save csv, cuts time range and reruns code
            new_range = cut_datime_range_into_frecs(min_day, max_day, 5)
            get_results_in_dates_list(new_range)
            # do something to avoid infinite loop (i.e. if more than 1200 at the same day, hour,second ?)
            print("end missing part of the day: SOLVED")


# %%

get_results_in_dates_list(dates_range)
