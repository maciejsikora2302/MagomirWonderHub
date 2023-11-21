import requests
import json
from pprint import pprint

import os
import datetime

def get_today_timestamp():
    return datetime.datetime.now().strftime('%Y-%m-%d')

def get_timestamp():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def is_timestamp_equal_today(timestamp: datetime):
    today_timestamp = get_today_timestamp()
    return timestamp == today_timestamp

def is_timestamp_older_than_one_minute(timestamp: datetime):
    today_timestamp = datetime.datetime.strptime(get_timestamp(), '%Y-%m-%d %H:%M:%S')
    time_difference = today_timestamp - timestamp
    one_minute = datetime.timedelta(minutes=1)

    return time_difference > one_minute
    

BASE_LINK = "https://api.guildwars2.com/v2/"
with open('../secrets/secrets.json', 'r') as f:
    API_KEY = json.load(f)['gw2_api_key']
HEADERS = {'Authorization': 'Bearer ' + API_KEY}

def process_daily(raw_data):
    fractals = raw_data['fractals']
    pve = raw_data['pve']
    pvp = raw_data['pvp']
    special = raw_data['special']
    wvw = raw_data['wvw']

    filtered_ids = list(filter(lambda x: x['level']['max'] == 80, 
                               fractals + pve + pvp + special + wvw))
    filtered_ids = list(map(lambda x: x['id'], filtered_ids))
    filtered_ids = list(map(str, filtered_ids))
    filtered_ids = ','.join(filtered_ids)
    # pprint(filtered_ids)
    infos = get_info_about_achi(filtered_ids)
    # pprint(infos)

    names = list(
        map(lambda x: x['name'], infos))
    names_with_id = list(
        map(lambda x: (x['name'], x['id']), infos))
    #remove from list if name contains 'Tier 1' 'Tier 2' 'Tier 3', but leave 'Tier 4'
    names = list(filter(lambda x: 'Tier 1' not in x and 'Tier 2' not in x and 'Tier 3' not in x, names))
    #apply the same filter to names_with_id
    names_with_id = list(filter(lambda x: 'Tier 1' not in x[0] and 'Tier 2' not in x[0] and 'Tier 3' not in x[0], names_with_id))


    fractal_icon = 'static/gw2_icons/Daily_Fractals.png'
    # pve_icon = 'static/gw2_icons/Daily_Achievement.png'
    pve_icon = 'static/gw2_icons/green_icon4.png'
    pvp_icon = 'static/gw2_icons/Daily_PvP_Achievement.png'
    # pvp_icon = 'static/gw2_icons/gold_icon.png'
    special_icon = 'static/gw2_icons/unknown_small.png'
    wvw_icon = pve_icon
    alt_text = 'No icon'

    def get_list_of_ids(array):
        return list(map(lambda x: x['id'], array))

    fractal_content = []
    pve_content = []
    pvp_content = []
    special_content = []
    wvw_content = []
    other_content = []

    easy_daily = [
        "Mystic Forger",
        "Big Spender",
        "Vista Viewer",
        "Reward Earner"
    ]

    mid_daily = [
        "Caravan Disruptor",
        "Veteran Creature Slayer",
        "Jumping Puzzle",
        "Miner",
        "Luberer",
        "Forager",
    ]

    names_with_type = []
    for name in names_with_id:
        name_id = name[1]
        normal_name = name[0]

        if name_id in get_list_of_ids(fractals):
            content = {'name': normal_name, 'icon': special_icon}
            fractal_content.append(content)
        elif name_id in get_list_of_ids(pve):
            content = {'name': normal_name, 'icon': pve_icon, 'id': name_id}
            if "Mystic Forger" in normal_name:
                content = {'name': normal_name.upper(), 'icon': fractal_icon}
            pve_content.append(content)
        elif name_id in get_list_of_ids(pvp):
            content = {'name': normal_name, 'icon': pvp_icon}
            pvp_content.append(content)
        elif name_id in get_list_of_ids(special):
            content = {'name': normal_name, 'icon': special_icon}
            special_content.append(content)
        elif name_id in get_list_of_ids(wvw):
            content = {'name': normal_name, 'icon': wvw_icon}
            wvw_content.append(content)
        else:
            content = {'name': normal_name, 'icon': special_icon}
            other_content.append(content)

    #sort each type of content by name
    fractal_content = sorted(fractal_content, key=lambda x: x['name'])
    pve_content = sorted(pve_content, key=lambda x: x['name'])
    pvp_content = sorted(pvp_content, key=lambda x: x['name'])
    special_content = sorted(special_content, key=lambda x: x['name'])
    wvw_content = sorted(wvw_content, key=lambda x: x['name'])
    other_content = sorted(other_content, key=lambda x: x['name'])

    names_with_type = fractal_content + pve_content + pvp_content + special_content + wvw_content + other_content
    
    for content in names_with_type:
        for daily in easy_daily:
            if daily.lower() in content['name'].lower():
                content['icon'] = 'static/gw2_icons/gold_icon.png'
        for daily in mid_daily:
            if daily.lower() in content['name'].lower():
                content['icon'] = 'static/gw2_icons/silver_icon.png'

    for content in names_with_type:
        content['name'] = content['name'].replace('—', ' — ')
        content['name'] = content['name'].replace('Daily', '')

    return names_with_type

def get_gw2_daily():
    daily_data_path = 'data/daily.json'

    if check_if_data_is_up_to_date(daily_data_path):
        print("Daily data is up to date.")
        raw_data = load_data(daily_data_path)
    else:
        print("Daily data is not up to date. Getting new data.")
        response = requests.get(BASE_LINK + "achievements/daily", headers=HEADERS)
        raw_data = response.json()
        save_data_with_timestamp(raw_data, daily_data_path)


    return process_daily(raw_data)


def get_gw2_tomorrow():

    daily_data_path = 'data/tomorrow.json'

    if check_if_data_is_up_to_date(daily_data_path):
        print("Tomorrow data is up to date.")
        raw_data = load_data(daily_data_path)
    else:
        print("Tomorrow data is not up to date. Getting new data.")
        response = requests.get(BASE_LINK + "achievements/daily/tomorrow", headers=HEADERS)
        raw_data = response.json()
        save_data_with_timestamp(raw_data, daily_data_path)

    return process_daily(raw_data)
    

def get_gw2_compleated_check(ids):
    data_path = 'data/achi_check.json'

    if check_if_data_is_older_than_one_minute(data_path):
        print("Compleated achi is up to date.")
        raw_data = load_data(data_path)
    else:
        print("Compleated achi is not up to date. Getting new data.")
        response = requests.get(BASE_LINK + f"account/achievements?id={ids[0]}", headers=HEADERS)
        raw_data = response.json()
        save_data_with_timestamp(raw_data, data_path, get_time_function = get_timestamp)

    
    return raw_data


def get_info_about_achi(ids: list[str]):
    response = requests.get(BASE_LINK + f"achievements?ids={ids}", headers=HEADERS)
    raw_data = response.json()
    return raw_data

def save_data_with_timestamp(data, file_path, get_time_function: callable = get_today_timestamp):
    timestamp = get_time_function()
    to_save = {
        'timestamp': timestamp,
        'data': data
    }
    with open(file_path, 'w') as f:
        json.dump(to_save, f)

def check_if_data_is_up_to_date(file_path):

    #if path doesnt exists, return false
    if not os.path.exists(file_path):
        return False

    with open(file_path, 'r') as f:
        data = json.load(f)
        timestamp = data['timestamp']
    return is_timestamp_equal_today(timestamp)

def check_if_data_is_older_than_one_minute(file_path):
    #if path doesnt exists, return false
    if not os.path.exists(file_path):
        return False

    with open(file_path, 'r') as f:
        data = json.load(f)
        timestamp = data['timestamp']
    return is_timestamp_equal_today(timestamp)

def load_data(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
        data = data['data']
    return data

if __name__ == "__main__":
    for _ in get_gw2_daily():
        print(_)
    # get_gw2_tomorrow()
    # get_gw2_compleated_check(['1981', '500', '1954', '1953'])



'''
Example of infos about achi
[{'description': 'Climb that ladder!',
  'flags': ['Pvp', 'Daily'],
  'icon': 'https://render.guildwars2.com/file/FE01AF14D91F52A1EF2B22FE0A552B9EE2E4C3F6/511340.png',
  'id': 3450,
  'locked_text': '',
  'name': 'Daily PvP Tournament Participator',
  'requirement': 'Participate in a PvP Tournament',
  'rewards': [{'count': 1, 'id': 68120, 'type': 'Item'}],
  'tiers': [{'count': 1, 'points': 0}],
  'type': 'Default'},
 {'description': '',
  'flags': ['Daily'],
  'icon': 'https://render.guildwars2.com/file/339192F5581BB3F771CF359BAB2C90537BD560CB/1228225.png',
  'id': 4210,
  'locked_text': '',
  'name': 'Daily Tier 3 Deepstone',
  'requirement': 'Complete Deepstone at fractal scale 51 or higher.',
  'rewards': [{'count': 1, 'id': 78613, 'type': 'Item'}],
  'tiers': [{'count': 1, 'points': 0}],
  'type': 'Default'},
 {'description': '',
  'flags': ['Daily'],
  'icon': 'https://render.guildwars2.com/file/A442B13E7B0D4A2F7136702FA858EA0C9F0CE4B3/1228223.png',
  'id': 2976,
  'locked_text': '',
  'name': 'Daily Tier 1 Molten Furnace',
  'requirement': 'Complete Molten Furnace at fractal scale 1 or higher.',
  'rewards': [{'count': 1, 'id': 78200, 'type': 'Item'}],
  'tiers': [{'count': 1, 'points': 0}],
  'type': 'Default'},
'''

'''
Example of raw data:

{'fractals': [{'id': 2245,
               'level': {'max': 80, 'min': 1},     
               'required_access': ['GuildWars2',   
                                   'HeartOfThorns',
                                   'PathOfFire']}, 
              {'id': 2266,
               'level': {'max': 80, 'min': 1},     
               'required_access': ['GuildWars2',   
                                   'HeartOfThorns',
                                   'PathOfFire']}, 
              {'id': 3238,
               'level': {'max': 80, 'min': 1},     
               'required_access': ['GuildWars2',   
                                   'HeartOfThorns',
                                   'PathOfFire']}, 
              {'id': 4244,
               'level': {'max': 80, 'min': 1},     
               'required_access': ['GuildWars2',
                                   'HeartOfThorns',
                                   'PathOfFire']},
              {'id': 4218,
               'level': {'max': 80, 'min': 1},
               'required_access': ['GuildWars2',
                                   'HeartOfThorns',
                                   'PathOfFire']},
              {'id': 4210,
               'level': {'max': 80, 'min': 1},
               'required_access': ['GuildWars2',
                                   'HeartOfThorns',
                                   'PathOfFire']},
              {'id': 4224,
               'level': {'max': 80, 'min': 1},
               'required_access': ['GuildWars2',
                                   'HeartOfThorns',
                                   'PathOfFire']},
              {'id': 4551,
               'level': {'max': 80, 'min': 1},
               'required_access': ['GuildWars2',
                                   'HeartOfThorns',
                                   'PathOfFire']},
              {'id': 4496,
               'level': {'max': 80, 'min': 1},
               'required_access': ['GuildWars2',
                                   'HeartOfThorns',
                                   'PathOfFire']},
              {'id': 4526,
               'level': {'max': 80, 'min': 1},
               'required_access': ['GuildWars2',
                                   'HeartOfThorns',
                                   'PathOfFire']},
              {'id': 4494,
               'level': {'max': 80, 'min': 1},
               'required_access': ['GuildWars2',
                                   'HeartOfThorns',
                                   'PathOfFire']},
              {'id': 2976,
               'level': {'max': 80, 'min': 1},
               'required_access': ['GuildWars2',
                                   'HeartOfThorns',
                                   'PathOfFire']},
              {'id': 2955,
               'level': {'max': 80, 'min': 1},
               'required_access': ['GuildWars2',
                                   'HeartOfThorns',
                                   'PathOfFire']},
              {'id': 2944,
               'level': {'max': 80, 'min': 1},
               'required_access': ['GuildWars2',
                                   'HeartOfThorns',
                                   'PathOfFire']},
              {'id': 2903,
               'level': {'max': 80, 'min': 1},
               'required_access': ['GuildWars2',
                                   'HeartOfThorns',
                                   'PathOfFire']}],
 'pve': [{'id': 1968,
          'level': {'max': 80, 'min': 1},
          'required_access': ['GuildWars2', 'HeartOfThorns', 'PathOfFire']},
         {'id': 1939,
          'level': {'max': 80, 'min': 11},
          'required_access': ['GuildWars2', 'HeartOfThorns', 'PathOfFire']},
         {'id': 1946,
          'level': {'max': 80, 'min': 40},
          'required_access': ['GuildWars2', 'HeartOfThorns', 'PathOfFire']},
         {'id': 1964,
          'level': {'max': 39, 'min': 11},
          'required_access': ['GuildWars2', 'HeartOfThorns', 'PathOfFire']},
         {'id': 2905,
          'level': {'max': 80, 'min': 80},
          'required_access': ['GuildWars2', 'HeartOfThorns', 'PathOfFire']},
         {'id': 1933,
          'level': {'max': 80, 'min': 80},
          'required_access': ['GuildWars2', 'HeartOfThorns', 'PathOfFire']},
         {'id': 1933,
          'level': {'max': 79, 'min': 31},
          'required_access': ['GuildWars2', 'HeartOfThorns', 'PathOfFire']}],
 'pvp': [{'id': 1856,
          'level': {'max': 80, 'min': 1},
          'required_access': ['GuildWars2', 'HeartOfThorns', 'PathOfFire']},
         {'id': 1861,
          'level': {'max': 80, 'min': 11},
          'required_access': ['GuildWars2', 'HeartOfThorns', 'PathOfFire']},
         {'id': 3450,
          'level': {'max': 80, 'min': 11},
          'required_access': ['GuildWars2', 'HeartOfThorns', 'PathOfFire']},
         {'id': 3449,
          'level': {'max': 80, 'min': 31},
          'required_access': ['GuildWars2', 'HeartOfThorns', 'PathOfFire']}],
 'special': [],
 'wvw': [{'id': 437,
          'level': {'max': 80, 'min': 1},
          'required_access': ['GuildWars2', 'HeartOfThorns', 'PathOfFire']},
         {'id': 1852,
          'level': {'max': 80, 'min': 11},
          'required_access': ['GuildWars2', 'HeartOfThorns', 'PathOfFire']},
         {'id': 1843,
          'level': {'max': 80, 'min': 11},
          'required_access': ['GuildWars2', 'HeartOfThorns', 'PathOfFire']},
         {'id': 1845,
          'level': {'max': 80, 'min': 31},
          'required_access': ['GuildWars2', 'HeartOfThorns', 'PathOfFire']}]}
'''