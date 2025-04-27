import os
import discord
import requests
# from dotenv import load_dotenv
from discord.ext import commands
from discord import app_commands

# load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
STEAM_API_KEY = os.getenv("STEAM_API_KEY")
GUILD_ID = os.getenv("GUILD_ID")

if not DISCORD_TOKEN or not STEAM_API_KEY or not GUILD_ID:
    raise ValueError("env variables missing")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    try:
        bot.tree.clear_commands(guild=discord.Object(id=GUILD_ID))
        bot.tree.add_command(steamgame, guild=discord.Object(id=GUILD_ID))
        await bot.tree.sync(guild=discord.Object(id=GUILD_ID))
        print(f"ready to go")
    except Exception as e:
        print(f"error: {e}")

# slash command to get game info
@app_commands.command(name="steamgame", description="Look up a Steam game")
@app_commands.describe(game_name="Name of game")
async def steamgame(interaction: discord.Interaction, game_name: str):
    await interaction.response.defer()

    # search Steam store
    search_url = f"https://store.steampowered.com/api/storesearch/?term={game_name}&cc=us&l=en"
    search_resp = requests.get(search_url).json()

    if not search_resp.get("items"):
        await interaction.followup.send("No results found.")
        return

    game = search_resp["items"][0]
    name = game["name"]
    link = game.get("url", f"https://store.steampowered.com/app/{game['id']}")

    # price handling
    if game.get("is_free"):
        price = "Free"
    elif game.get("price"):
        final_price = game["price"].get("final", 0)
        currency = game["price"].get("currency", "USD")
        price = f"{currency} ${final_price / 100:.2f}"
    else:
        price = "Price not available"

    # desc
    desc_resp = requests.get(f"https://store.steampowered.com/api/appdetails?appids={game['id']}").json()
    desc_data = desc_resp[str(game['id'])].get("data", {})
    short_desc = desc_data.get("short_description", "No description available.")

    # embed output
    embed = discord.Embed(title=name, url=link, description=short_desc)
    embed.add_field(name="Price", value=price, inline=False)

    await interaction.followup.send(embed=embed)

# add command to tree
bot.tree.add_command(steamgame, guild=discord.Object(id=GUILD_ID))

bot.run(DISCORD_TOKEN)