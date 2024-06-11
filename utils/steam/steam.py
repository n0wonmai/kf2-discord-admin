from steam_web_api import Steam
from utils.toolbox import read_config

import os
import logging

log = logging.getLogger("kf2bot")

PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../config.json")

def steam_user_info(steamid: str):
    """ Get steam user info """

    log.info(f"Requested user info, STEAM_ID: {steamid}")
    steam = Steam(read_config(PATH)["steam_token"])
    user = steam.users.get_user_details(steamid)

    return user


if __name__ == "__main__":
    pass
