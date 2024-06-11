from discord.ui import View
from utils.webadmin.webadmin import get_players

import discord

class UserMenu(View) :
    """ Bot UI """
    def __init__(self):
        super().__init__()
        self.member = None

    @discord.ui.button(label='Show players', style=discord.ButtonStyle.blurple, disabled=False)
    async def action_show_players(self, interaction: discord.Interaction, button: discord.ui.Button):
        """ Show players """

        players = await get_players()

        if len(players[0]) > 0:
            await interaction.response.send_message("Players online: " + "".join(players[1]))
        else:
            await interaction.response.send_message("There are no players")
        await interaction.response.edit_message(view=self)


if __name__ == "__main__":
    pass
