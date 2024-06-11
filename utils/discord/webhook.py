from discord import Webhook
from utils.toolbox import read_config

import os
import aiohttp
import logging

log = logging.getLogger("kf2bot")

PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../config.json")

async def on_message(
        url: str = read_config(PATH)["webhook_url"],
        message: str = "",
        name: str = "",
        avatar: str = ""
    ):
    """ Send webhook """
    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url(url, session=session)
        await webhook.send(content=message, username=name, avatar_url=avatar)


if __name__ == "__main__":
    pass
    