from bs4 import BeautifulSoup
from utils.toolbox import read_config
from utils.session_request import SessionRequest
from utils.discord.webhook import on_message
from utils.discord.color import colorize_message
from utils.steam.steam import steam_user_info

import os
import logging
import requests

log = logging.getLogger("kf2bot")

PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../config.json")

async def login() -> requests.Session:
    """ Login to webadmin """

    data = read_config(PATH)

    global host
    host = f"http://{data['host_ip']}:{data['port']}"

    payload = {
        "password_hash": None,
        "remember": 2678400,
        "username": data["username"],
        "password": data["password"]
    }

    session = requests.Session()
    login = SessionRequest(f"{host}/ServerAdmin/", "GET")
    await login.request(session)

    soup = BeautifulSoup(login.response.text, "lxml")
    token = soup.find("input", {"name":"token"}).get('value')
    payload["token"] = token

    obj = SessionRequest(f"{host}/ServerAdmin/", "POST")
    await obj.request(session, payload)

    responce_data = obj.response.text

    return session, responce_data


async def server_info() -> dict:
    """ Get current server info """

    _, html = await login()
    soup = BeautifulSoup(html, "lxml")

    game = soup.find_all("dl", class_="gs_details")[0].text.strip().split("\n")
    rules = soup.find_all(id="currentRules")[0].text.strip().split("\n")

    return {
        "map": game[1],
        "players": game[3],
        "wave": game[4],
        "difficulty": rules[3]
    }


async def get_players() -> list:
    """ Get online players """

    session, _ = await login()
    obj = SessionRequest(f"{host}/ServerAdmin/current/players", "GET")
    await obj.request(session)

    soup = BeautifulSoup(obj.response.text, "lxml")
    table = soup.find_all("tr")

    player_info = {}
    player_names = []

    if len(table) > 1:
        for player in table[1:]:
            # Check if theres no players
            if "There are no players" in player.text:
                break
            else:
                p = player.text.strip().split("\n")[0] # Vanilla
                player_names.append(colorize_message(p))
                id = player.text.strip().split("\n")[4] # Vanilla
                player_info[p] = id

    return [player_info, player_names]


async def hook_message() -> None:
    """ Hook in-game message and relay it to discord """

    session, _ = await login()
    obj = SessionRequest(f"{host}/ServerAdmin/current/chat", "GET")
    await obj.request(session)

    soup = BeautifulSoup(obj.response.text, "lxml")
    chat_messages = soup.find_all("div", class_="chatmessage")
    notice_messages = soup.find_all("div", class_="chatnotice")

    if chat_messages:
        log.debug("Player message found!")
        chat_info = []
        for msg in chat_messages:
            name = msg.findChildren("span", class_="username", recursive=False)[0].text
            message = msg.findChildren("span", class_="message", recursive=False)[0].text
            chat_info.append({name: message})

        player_info = await get_players()

        for playername, playerid in player_info[0].items():
            for num, item in enumerate(chat_info):
                if playername in item:  
                    steam_info = steam_user_info(playerid)
                    await on_message(
                        message=item[playername],
                        name=steam_info["player"]["personaname"],
                        avatar=steam_info["player"]["avatarmedium"]
                    )
                    chat_info.pop(num)
                    break

    if notice_messages:
        log.debug("Server notice found!")
        data = read_config(PATH)
        for msg in notice_messages:
            notice = msg.findChildren("span", class_="message", recursive=False)[0].text

            # Exclude kick messages
            if not "*VOTEKICK*" in notice:
                if "*ADMIN*:" in notice:
                    notice = notice.replace("*ADMIN*:", "")
                await on_message(
                    message=notice,
                    name=data["botname"],
                    avatar=data["avatar_url"]
                )
                break


async def relay():
    """ Relay loop """
    while True:
        await hook_message()


if __name__ == "__main__":
    pass
