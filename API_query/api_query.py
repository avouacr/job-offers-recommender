import ast
import glob
import os
import re
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import query_functions

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



if __name__ == "__main__":

    # create directory where offers are stored
    path = 'test'
    os.makedirs(path)

    # query from a # of days back until today
    num_days_lookback = 3

    # create the day range
    dates_range = [(datetime.utcnow() - timedelta(days=i)) for i in
                   np.linspace(0, num_days_lookback, num_days_lookback)]

    # query results
    query_functions.get_results_in_dates_list(dates_range, path)

    # get all files from folder
    all_files = glob.glob(path + "/*.csv")

    result_list = []

    # for each file, append them to list, and remove from directory
    for filename in all_files:
        df = pd.read_csv(filename, index_col=None, header=0)
        result_list.append(df)
        os.remove(filename)

    # concatenate
    frame = pd.concat(result_list, axis=0, ignore_index=True, sort=True)

    # remove duplicates (actually not needed, but still good to be sure everything is ok)
    frame = frame.astype(str).drop_duplicates()

    # TO DO: remove id duplicate

    # Get zipcode, or at least the departement
    frame["lieuTravail"] =  frame["lieuTravail"].apply(ast.literal_eval)
    frame["localisation"] = frame["lieuTravail"].apply(extract_location)
    frame = frame.dropna(subset=['localisation'])

    # save single file
    frame.to_csv(os.path.join(path, "all_offers.csv"), sep=",")
