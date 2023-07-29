from io import BytesIO
from aiohttp import ClientSession
from ....config import headers

async def download(url, image_id):
    try:
        async with ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status != 200:
                    print(f"Error: {response.status}")
                else:
                    img_data = await response.read()
                    if img_data:
                        img_io = BytesIO(img_data)
                        img_io.name = f"{image_id}.webp"
                    else:
                        raise FileNotFoundError("No image data received.")
    except Exception as e: 
        print(f'Error fetching image: {e}')
    return img_io
