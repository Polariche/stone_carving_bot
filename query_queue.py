import aiohttp
from aiohttp import web
import asyncio
import pandas as pd

from query import *

with open("tokens/smilegate.token", "r") as f:
    key = f.readlines()[0]

headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
            'authorization': f'bearer {key}'
            }

async def fetch(query):
    async with aiohttp.ClientSession(headers=headers) as session:
        return await query.fetch(session)

async def make_stone_query(request):
    id1 = request.match_info.get('id1', None)
    id2 = request.match_info.get('id2', None)

    query = StoneQuery(id1, id2)
    query_result = await fetch(query)

    return web.json_response(query_result)

if __name__ == '__main__':
    app = web.Application()
    app.add_routes([web.get('/stone/{id1}/{id2}', make_stone_query)])

    web.run_app(app)