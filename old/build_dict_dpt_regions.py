
import json

with open('data/corresp_regions_dpt.txt', 'r') as f:
    test = f.read().splitlines()

dic_corresp = {}
for x in test:
    str_split = x.split(', ')
    region = str_split[0]
    dpt_list = str_split[1:]
    for dpt in dpt_list:
        dic_corresp[dpt] = region

with open('data/dict_dpt_region.json', 'w') as fp:
    json.dump(dic_corresp, fp)

# with open('data/dict_dpt_region.json', 'r') as fp:
#     data = json.load(fp)