import os
import random
import html
import discord
import requests
from discord.ui import View, Select
from discord import SelectOption
from discord.ext import commands
from discord import app_commands
#from dotenv import load_dotenv

#load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
STEAM_API_KEY = os.getenv("STEAM_API_KEY")
GUILD_ID = os.getenv("GUILD_ID")

if not DISCORD_TOKEN or not STEAM_API_KEY or not GUILD_ID:
    raise ValueError("env variables missing")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# for games i own
UNPLAYED_GAMES = [
    "Alba: A Wildlife Adventure",
    "Assassin's Creed Odyssey",
    "Batman",
    "Celeste",
    "Cyberpunk 2077",
    "Dark Souls II",
    "ELDEN RING",
    "L.A. Noire",
    "Lies of P",
    "Need for Speed",
    "NieR:Automata",
    "Nioh",
    "Persona",
    "Portal",
    "Red Dead Redemption",
    "Spiritfarer",
    "The Witcher",
    "The Witness"
]


@bot.event
async def on_ready():
    try:
        guild=discord.Object(id=GUILD_ID)

        # clear existing commands
        bot.tree.clear_commands(guild=discord.Object(id=GUILD_ID))

        # add slash commands to tree
        commands = [steamgame, randomgame]

        for cmd in commands:
            bot.tree.add_command(cmd, guild=guild)

        # sync
        await bot.tree.sync(guild=discord.Object(id=GUILD_ID))

        print("ready to go")
    except Exception as e:
        print(f"error: {e}")

class GameSelectView(View):
    def __init__(self, games):
        super().__init__(timeout=30)
        options = [
            SelectOption(label=game["name"], value=str(game["id"])) for game in games[:10]
        ]
        self.add_item(GameSelect(options, games))

class GameSelect(Select):
    def __init__(self, options, games):
        super().__init__(placeholder="Choose...", options=options)
        self.games = {str(game["id"]): game for game in games}

    async def callback(self, interaction: discord.Interaction):
        selected_game = self.games[self.values[0]]
        appid = selected_game["id"]
        detail_resp = requests.get(f"https://store.steampowered.com/api/appdetails?appids={appid}", timeout=10).json()
        detail_data = detail_resp[str(appid)]["data"]

        description = html.unescape(detail_data.get("short_description", "No description available."))
        header_image = detail_data.get("header_image", None)
        name = selected_game["name"]
        link = selected_game.get("url", f"https://store.steampowered.com/app/{selected_game['id']}")

        # release date
        release_info = detail_data.get("release_date", {})
        release_date = release_info.get("date", "Unknown")

        # price handling
        if selected_game.get("price"):
            final_price = selected_game["price"].get("final", 0)
            currency = selected_game["price"].get("currency", "USD")
            price = f"{currency} ${final_price / 100:.2f}"
        else:
            price = "Free"

        embed = discord.Embed(
            title=name,
            url=link,
            description=description,
            color=discord.Color.blue()
        )
        embed.add_field(name="Price", value=price, inline=True)
        embed.add_field(name="Release Date", value=release_date, inline=True)

        if header_image:
            embed.set_image(url=header_image)

        embed.set_footer(text="Powered by Steam")

        await interaction.response.edit_message(content=None, embed=embed, view=None)

# slash command to get game info
@app_commands.command(name="steamgame", description="Look up a Steam game")
@app_commands.describe(game_name="Name of game")
async def steamgame(interaction: discord.Interaction, game_name: str):
    await interaction.response.defer(ephemeral=True)

    # search Steam store
    search_url = f"https://store.steampowered.com/api/storesearch/?term={game_name}&cc=us&l=en"
    search_resp = requests.get(search_url, timeout=5).json()
    games = search_resp.get("items", [])

    if not games:
        await interaction.followup.send("No results found.")
        return

    await interaction.followup.send(
        content="Choose the correct game from the dropdown:",
        view=GameSelectView(games)
    )

# slash command to get a random game
@app_commands.command(name="randomgame", description="Pick a random game from your unplayed games")
async def randomgame(interaction: discord.Interaction):
    await interaction.response.defer()

    game_name = random.choice(UNPLAYED_GAMES)

    try:
        # search game by name
        search_url = f"https://store.steampowered.com/api/storesearch/?term={game_name}&cc=us&l=en"
        search_resp = requests.get(search_url, timeout=10).json()
        if not search_resp.get("items"):
            raise Exception(f"Game not found: {game_name}")

        game = search_resp["items"][0]
        appid = game["id"]

        # details
        detail_url = f"https://store.steampowered.com/api/appdetails?appids={appid}&cc=us&l=en"
        detail_resp = requests.get(detail_url, timeout=10).json()
        detail_data = detail_resp[str(appid)]["data"]
        description = html.unescape(detail_data.get("short_description", "No description available.")),

        embed = discord.Embed(
            title=detail_data["name"],
            url=f"https://store.steampowered.com/app/{appid}/",
            description=description
            color=0x470109
        )
        embed.set_thumbnail(url=detail_data.get("header_image", ""))
        embed.add_field(
            name="Genres",
            value=", ".join([g["description"] for g in detail_data.get("genres", [])]) or "N/A",
            inline=True
        )

        await interaction.followup.send(embed=embed)

    except Exception as e:
        await interaction.followup.send(f"Error: {e}")

bot.run(DISCORD_TOKEN)
