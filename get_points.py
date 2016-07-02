import json
import os
import time

from pymongo import MongoClient

import requests


def get_points():
    client = MongoClient()

    items = client['thegame']['items']

    while True:
        try:
            response = requests.post(
                'http://thegame.nerderylabs.com/points',
                headers={
                    'apikey': os.environ['API_KEY']
                }
            )

            json_content = response.content

            content = json.loads(json_content.decode('utf8'))

            if content['Item'] is not None:
                items.insert(content['Item'])

            time.sleep(1)
        except requests.exceptions.ConnectionError:
            pass
