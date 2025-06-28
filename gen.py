import requests
import json
import time
import asyncio
import aiohttp
from config import API_KEY,SECRET_KEY


async def generate(prompt):
    url='https://api-key.fusionbrain.ai/'
    AUTH_HEADERS = {
        'X-Key': f'Key {API_KEY}',
        'X-Secret': f'Secret {SECRET_KEY}',
    }
    params = {
        "type": "GENERATE",
        "numImages": 1,
        "width": 1024,
        "height": 1024,
        "generateParams": {
            "query": f"{prompt}"
        }
    }

    files = {
        'model_id': (None, 4),
        'params': (None, json.dumps(params), 'application/json')
    }
    response = requests.post(url + 'key/api/v1/text2image/run', headers=AUTH_HEADERS, files=files)
    data = response.json()
    attempts=0
    while attempts < 40:
        response = requests.get(url + 'key/api/v1/text2image/status/' + data['uuid'], headers=AUTH_HEADERS)
        data = response.json()
        if data['status'] == 'DONE':
            return data['images']

        attempts += 1
        await asyncio.sleep(3)

# async def main():
#     images = await generate('Кот')
#     print(images)
#
# asyncio.run(main())
