from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from utils.webadmin.webadmin import relay
from utils.discord.bot import bot_run

import os
import asyncio
import logging

log = logging.getLogger("kf2bot")
logname = str(datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))
logpath = os.path.abspath("logs")

if os.path.isdir(logpath) is False:
    os.mkdir(logpath)

logging.basicConfig(
    level=logging.INFO,
    filename=f"logs/{logname}.log",
    filemode="w",
    format="%(asctime)s %(levelname)s %(message)s"
)

async def start():
    """ Main function """

    loop = asyncio.get_running_loop()
    with ThreadPoolExecutor() as pool:
        task1 = asyncio.create_task(relay())
        task2 = loop.run_in_executor(pool, bot_run)

        await task1
        await task2


if __name__ == "__main__":

    log.debug("Starting KF2 discord admin bot ...")

    # Start bot and relay
    asyncio.run(start())
