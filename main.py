import discord
import json
from discord.ext import commands
from discord.ext.commands import Bot
from discord.voice_client import VoiceClient


def read_token():
    '''
    Function to read the discord token
    Returns the token
    '''
    with open('config.json', 'r') as config_file:
        token = json.load(config_file)['token']
    return token


token = read_token()
bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected')


@bot.command(name='fumatorul')
async def say_fumatorul(ctx):
    author = ctx.message.author
    channel = author.voice.channel
    if channel != None:
        print(channel)
    else:
        await ctx.send(f"{author.display_name} is an idiot")


bot.run(token)
