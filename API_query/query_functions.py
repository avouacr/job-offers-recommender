import json
import os
from datetime import datetime, time

import numpy as np
import pandas as pd
import requests
import re

# Some ideas taken from :
# https://github.com/Cocorico84/employme/blob/855cfcda2c54f42b9c42dcbf4ac87cdf09248b7f/back/manager.py
# https://stackoverflow.com/questions/42213427/change-variable-after-a-specific-amount-of-time-python

path_to_API_codes_csv = "/private/access.csv"

access = pd.read_csv(path_to_API_codes_csv, header=0)
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
            data = connection_with_dates(range_str, min_date, max_date)

    return data


def create_date_range_str(i):
    """
    Creates str needed to get more results from the Pole Emploi API
    Args:
        i: "page" index (i.e. we divide all results in pages of 150 elements, the maxium the API returns)

    Returns: str (e.g. '0-149)

    """
    return str(str(min(i, 1000)) + '-' + str(min(i + 149, 1149)))


def cut_datime_range_into_frecs(min_day, max_day, num_items=10):
    """ Cuts a datetime range into a list with smaller intervalles

    Args:
        min_day (datetime):
        max_day (datetime):
        num_items (int): number of intervals

    Returns: list of datetime values

    """
    timestamp_range = np.linspace(datetime.timestamp(max_day), datetime.timestamp(min_day), num_items, dtype=np.int64)
    timestamp_range = [datetime.fromtimestamp(i) for i in timestamp_range]
    return timestamp_range


def query_results(min_day, max_day):
    """
    Queries results whose upload date is in the range

    Args:
        min_day (datetime): starting day
        max_day (datetime): end dat

    Returns: list of results (as json object)

    """
    list_of_results = []

    # As we get at maxium 150 values per query (and 1200 overall) we need to loop through the queries
    for i in list(range(0, 1150, 150)):
        date_range_str = create_date_range_str(i)
        res = connection_with_dates(date_range_str, min_day, max_day)
        list_of_results.append(res)

        try:
            # if we get less than 150 results, we stop querying
            if len(res['resultats']) < 150:
                break
        except:
            pass

    return list_of_results


def get_results_in_dates_list(dates_range, path):
    """
    Queries day by day and saves results as separate csv files in a folder (specified in the path argument).
    If a day has too many results (>1200), the range is cut by 10 and queryied again (operation repeated as much as
    needed)

    Args:
        dates_range (list of days as datime object): range to query
        path (str):

    Returns: Nothing, csv files are saved

    """

    # loop through the days
    for day in range(1, len(dates_range) - 1):

        # select day and previous day
        min_day = dates_range[day]
        max_day = dates_range[day - 1]

        list_of_results = query_results(min_day, max_day)

        try:
            # convert results to df
            list_dfs = [pd.DataFrame.from_dict(request_as_dict['resultats']) for request_as_dict in list_of_results]
        except KeyError:
            # if any has not 'results', save the error for posterior checkup
            # print("error")
            global saving_error
            saving_error = list_of_results

        # concatenate results
        dfs_date = pd.concat(list_dfs, sort=True)

        # if we did not get any results do not save anything
        if len(dfs_date.index) == 0:
            pass

        # if we got less than 1200 results, save as cv in the desired folder
        elif len(dfs_date.index) < 1200:
            csv_name = os.path.join(path, str(dates_range[day + 1]) + ".csv")
            dfs_date.to_csv(csv_name, sep=",")

        # if max reached (therefore we did not get all results), does not save csv, cuts time range and reruns code
        if len(dfs_date.index) == 1200:
            new_range = cut_datime_range_into_frecs(min_day, max_day, 10)
            get_results_in_dates_list(new_range, path)
            # TO DO: something to avoid infinite loop (i.e. if more than 1200 at the same day, hour,second ?)
            # (allthough in practice this has never happened so far)


liste_regions_et_France = ['France',
                           "Auvergne-Rhône-Alpes",
                           "Bourgogne-Franche-Comté",
                           "Bretagne",
                           "Centre-Val de Loire",
                           "Corse",
                           "Grand Est",
                           "Hauts-de-France",
                           "Île-de-France",
                           "Normandie",
                           "Nouvelle-Aquitaine",
                           "Occitanie",
                           "Pays de la Loire",
                           "Provence-Alpes-Côte d'Azur",
                           "Guadeloupe",
                           "Martinique",
                           "Guyane",
                           "La Réunion",
                           "Mayotte"]


def extract_location(dictionnary):
    if not isinstance(dictionnary, dict):
        return None

    if ('codePostal' in dictionnary):
        if len(dictionnary['codePostal']) == 5:
            try:
                as_num = dictionnary['codePostal']
                return as_num
            except ValueError:
                pass

    if 'libelle' in dictionnary:
        text = dictionnary['libelle']
        nums = re.findall('\d+', text)
        try:
            dpt = nums[0]
            if len(dpt) == 2:
                return dpt
        except IndexError:
            pass
        if text in liste_regions_et_France:
            return text
        else:
            return None
