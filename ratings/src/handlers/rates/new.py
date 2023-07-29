from json import loads
from aiohttp import ClientSession

from ...config import base_url, headers


async def request():
    async with ClientSession() as session:
        async with session.get(f'{base_url}/new', headers=headers) as response:
            resp = await response.text()
        return loads(resp)