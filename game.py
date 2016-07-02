from datetime import datetime, timedelta
import json
from multiprocessing import Process
import os

from dotenv import load_dotenv
from pymongo import MongoClient
import requests

from get_points import get_points

TIME_SINCE_LAST_ITEM_USE = (datetime.now() - timedelta(weeks=1))

load_dotenv('.env')


def normalize_item(item):
    if item.get('Some'):
        new_item = item['Some']
    elif isinstance(item.get('Fields'), list):
        new_item = item['Fields'][0]
    else:
        new_item = item['Case']['Fields'][0]

    return new_item


def points(target):
    response = requests.get(
        'http://thegame.nerderylabs.com/points/{0}'.format(target)
    )

    print(response.content)


def effects(target):
    response = requests.get(
        'http://thegame.nerderylabs.com/effects/{0}'.format(target)
    )

    print(response.content)


def print_item(idx, item):
    new_item = normalize_item(item)

    print('Item #{0} Name: {1}'.format(idx, new_item['Name']))
    print('\t Description: {0}'.format(new_item['Description']))
    print('\t Rarity: {0}'.format(new_item['Rarity']))
    print('\n')


def use_item(data, idx, target=None):
    global TIME_SINCE_LAST_ITEM_USE

    new_item = normalize_item(data[idx])

    if target:
        url = 'http://thegame.nerderylabs.com/items/use/{0}?target={1}'.format(new_item['Id'], target)
    else:
        url = 'http://thegame.nerderylabs.com/items/use/{0}'.format(new_item['Id'])

    response = requests.post(
        url,
        headers={
            'apikey': os.environ['API_KEY'],
        }
    )

    if response.status_code == 200:
        response_dict = json.loads(response.content.decode('utf8'))

        for message in response_dict['Messages']:
            print(message)

        print(response_dict)
    else:
        TIME_SINCE_LAST_ITEM_USE = (datetime.now() - timedelta(weeks=1))
        print('Stale item, sorry')

    items.remove({'_id': data[idx]['_id']})


def list_items(data):
    for idx, item in enumerate(items.find()):
        print_item(idx, item)


def route_command(command, args):
    # Forgive me Guido!!
    global TIME_SINCE_LAST_ITEM_USE

    if command == 'list_items':
        list_items(list(items.find()))

    if command == 'use_item':
        if TIME_SINCE_LAST_ITEM_USE > (datetime.now() - timedelta(minutes=1, seconds=10)):
            print('Too soon to use an item!')
            return

        TIME_SINCE_LAST_ITEM_USE = datetime.now()

        try:
            use_item(list(items.find()), idx=int(args[0]), target=args[1])
        except IndexError:
            use_item(list(items.find()), idx=int(args[0]))

    if command == 'points':
        points(args[0])

    if command == 'effects':
        effects(args[0])


point_process = Process(target=get_points)
point_process.start()

client = MongoClient()

items = client['thegame']['items']

while True:
    input_string = input('Enter Command > ').split(' ')

    command = input_string[0]
    args = input_string[1:]

    route_command(command, args)
