import asyncio
from twikit import Client

USERNAME = 'autoaibot14299'
EMAIL = 'don.linglok@gmail.com'
PASSWORD = 'B*xLbj8XkeAX*Ds'

# Initialize client
client = Client('en-US')

import os
import re
from PIL import Image
import random
import string
from random import randint
from time import sleep

image_folder = "E:\\stable-diffusion-output\\Read\\2024_new\\2024-07-28_new"
search_extensions = ".png"

async def main():
    await client.login(
        auth_info_1=USERNAME,
        auth_info_2=EMAIL,
        password=PASSWORD
    )
    
    i = 0
    for root, dirs, files in os.walk(image_folder):
        if(dirs == []):
            for file in files:
                if i < 100:
                    # Upload media files and obtain media_ids
                    media_ids = [
                    ]

                    file_name = os.path.splitext(file)[0].replace(search_extensions, "")
                    file_extension = os.path.splitext(file)[1]
                    if file_extension == search_extensions:
                        media_ids.append(await client.upload_media(
                            root+"\\"+file_name+search_extensions,
                            wait_for_completion=True))

                        digits = "".join( [random.choice(string.digits) for i in range(8)] )
                        chars = "".join( [random.choice(string.ascii_letters) for i in range(15)] )

                        # Create a tweet with the provided text and attached media
                        await client.create_tweet(
                            text=digits + chars,
                            media_ids=media_ids
                        )
                        i=i+1
                        sleep(round(random.uniform(5.0, 60.0), 10))

asyncio.run(main())
