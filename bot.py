import os
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")
GUILD_ID = int(os.getenv("GUILD_ID"))

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    guild = discord.Object(id=GUILD_ID)
    try:
        bot.tree.copy_global_to(guild=guild)
        await bot.tree.sync(guild=guild)
        print("chronicler-bot is online as", bot.user)
    except Exception as e:
        print(f"Error syncing commands: {e}")

# Help command
@bot.tree.command(name="help_chronicler", description="Show XP, levels, role promotions commands")
async def help_chronicler(interaction: discord.Interaction):
    embed = discord.Embed(title="📜 Chronicler Commands", color=discord.Color.green())
    embed.add_field(name="XP Tracking", value="Earn XP by sending messages.", inline=False)
    embed.add_field(name="Levels", value="Automatically promotes you to new roles when thresholds are reached.", inline=False)
    embed.add_field(name="Rank", value="Check your level and XP progress with /rank.", inline=False)
    embed.add_field(name="Leaderboard", value="View the server's top members with /leaderboard.", inline=False)
    await interaction.response.send_message(embed=embed, ephemeral=True)

bot.run(TOKEN)
