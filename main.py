from pathlib import Path
import os

import discord
from discord import Colour, Embed
from discord_slash import SlashCommand
from discord_slash.model import SlashCommandOptionType as option_type
from discord_slash.utils.manage_commands import create_option
import yaml
from yaml import CLoader

config_path = Path(os.path.dirname(__file__)) / 'config.yml'
if config_path.exists():
    with open(config_path) as f:
        config = yaml.load(f, Loader=CLoader)
else:
    raise SystemExit('Missing config file!')

GUILD_IDS = config['guild_ids']
BOT_TOKEN = config['BOT_TOKEN']

client = discord.Client(intents=discord.Intents.all())
slash = SlashCommand(client, sync_commands=True)


@client.event
async def on_ready():
    print('Ready!')


@slash.slash(name="ping", guild_ids=GUILD_IDS)
async def ping(ctx):
    await ctx.send(f"Pong! ({client.latency*1000}ms)")


user_kwargs = {
    'name': 'user',
    'description': 'Get info about user',
    'options': [
        create_option(
            name='user',
            description='The user to get information on',
            option_type=option_type.USER,
            required=False
        )
    ]
}
@slash.slash(**user_kwargs, guild_ids=GUILD_IDS)
async def user_info(ctx, user=None):
    if user is None:
        user = ctx.author

    on_server = bool(ctx.guild.get_member(user.id))
    name = str(user)
    if on_server and user.nick:
        name = f"{user.nick} ({name})"

    embed = Embed(colour=Colour.blurple(), title=name)
    embed.add_field(name='User Information',
                    value=(f'Created: {user.created_at:%m/%d/%y %H:%M UTC}'),
                    inline=False)
    embed.set_thumbnail(url=str(user.avatar_url))
    embed.colour = user.top_role.colour if on_server else Colour.blurple()
    await ctx.send(embed=embed)


client.run(BOT_TOKEN)
