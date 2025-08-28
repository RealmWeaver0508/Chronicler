import discord
from discord.ext import commands
from discord import app_commands, Embed
import os
import db

TOKEN = os.getenv("DISCORD_TOKEN_XP")
GUILD_ID = int(os.getenv("GUILD_ID"))

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree

progression_roles = {
    0: "Seed",
    10: "Awakened",
    20: "Tempered",
    35: "Harmonized",
    50: "Ascendant",
    75: "Sovereign"
}

XP_PER_MESSAGE = 5

def level_from_xp(xp: int) -> int:
    return int(xp ** 0.5)

def level_embed(member, new_level):
    embed = Embed(
        title="📜 A New Chapter Unfolds",
        description=f"{member.mention} has advanced to **Level {new_level}**!",
        color=discord.Color.gold()
    )
    embed.set_footer(text="The Chronicler records this moment in the annals of Enoch.")
    return embed

@bot.event
async def on_ready():
    print(f"✅ Chronicler active as {bot.user}")
    await tree.sync(guild=discord.Object(id=GUILD_ID))

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    xp = XP_PER_MESSAGE
    db.add_xp(message.author.id, xp)

    total_xp = db.get_user_xp(message.author.id)
    new_level = level_from_xp(total_xp)
    old_level = db.get_user_level(message.author.id)

    if new_level > old_level:
        db.set_user_level(message.author.id, new_level)
        levels_channel = discord.utils.get(message.guild.text_channels, name="levels")
        if levels_channel:
            await levels_channel.send(embed=level_embed(message.author, new_level))

        if new_level in progression_roles:
            role_name = progression_roles[new_level]
            role = discord.utils.get(message.guild.roles, name=role_name)
            if role:
                await message.author.add_roles(role)

@tree.command(name="rank", description="Show your level and XP")
async def rank(interaction: discord.Interaction):
    xp = db.get_user_xp(interaction.user.id)
    level = db.get_user_level(interaction.user.id)
    embed = Embed(title="📖 Your Chronicle", color=discord.Color.blue())
    embed.add_field(name="Level", value=level)
    embed.add_field(name="XP", value=xp)
    await interaction.response.send_message(embed=embed, ephemeral=True)

@tree.command(name="leaderboard", description="Show the top adventurers")
async def leaderboard(interaction: discord.Interaction):
    leaders = db.get_leaderboard()
    embed = Embed(title="🏅 Hall of Deeds", color=discord.Color.purple())
    for i, (user_id, xp, lvl) in enumerate(leaders, start=1):
        embed.add_field(name=f"#{i}", value=f"<@{user_id}> - Lvl {lvl} ({xp} XP)", inline=False)
    await interaction.response.send_message(embed=embed)

bot.run(TOKEN)
