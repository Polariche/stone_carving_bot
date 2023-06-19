import aiohttp
from aiohttp import web
import asyncio
import pandas as pd

from query import *
from collections import deque
import re
import time

# ------------------------------------------ using api -----------------------------------------------

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

async def queue_loop(app):
    Query.loop = asyncio.get_running_loop()

    while True:
        if len(app.queue) > 0:
            query = app.queue.pop()
            await fetch(query)

            h = query.response_headers
            app.limits = {'reset': int(h['x-ratelimit-reset']), 
                            'remaining': int(h['x-ratelimit-remaining'])}

            print(app.limits)

        if app.limits['remaining'] <= 0:
            await asyncio.sleep(max(app.limits['reset'] - time.time(), 0))

        else:
            await asyncio.sleep(0.01)
            

# --------------------------------------------- data stuff -------------------------------------------
# TODO : move this to a data file
materials = {"찬란한 명예의 돌파석": 66110224, "최상급 오레하 융화 재료": 6861011, "정제된 파괴강석": 66102005, "정제된 수호강석": 66102105}
material_names = tuple(map(str, materials.keys()))

# ---------------------------------------------- web ---------------------------------------------------

app = web.Application()
routes = web.RouteTableDef()

async def execute(queries):
    app.queue.extend(queries)
    query_results = await asyncio.gather(*[q.result for q in queries])

    return web.json_response(query_results)

@routes.get('/stone/{id1}/{id2}')
async def search_stone_price(request):
    id1 = request.match_info.get('id1')
    id2 = request.match_info.get('id2')

    return await execute([StoneQuery(id1, id2)])

@routes.get('/material/{name}')
async def search_materials_price(request):
    name = request.match_info.get('name')

    return await execute([MarketItemsQuery(materials[name])])

@routes.get('/gem/{level}/{name}')
async def search_materials_price(request):
    level = request.match_info.get('level')
    name = request.match_info.get('name')

    p = re.compile('[멸홍]')
    m = p.finditer(name)
    gemtypes = {a[0] for a in m}

    if len(gemtypes) == 0:
        gemtypes = {'멸', '홍'}

    return await execute([GemQuery(level, gemtype) for gemtype in gemtypes])

app.add_routes(routes)

async def main():

    runner = aiohttp.web.AppRunner(app)
    await runner.setup()
    site = aiohttp.web.TCPSite(runner)    
    await site.start()

    # wait forever
    app.ql = queue_loop(app)
    app.queue = deque()
    app.limits = {'reset': -1, 'remaining': 100}
    await app.ql


if __name__ == '__main__':
    asyncio.run(main())
    