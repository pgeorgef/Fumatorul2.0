import discord
import json
from discord.ext import commands
from discord.ext.commands import Bot
from discord.voice_client import VoiceClient
from gtts import gTTS
import random
import ffmpeg
from time import sleep
from discord.errors import ClientException


def read_token():
    """Function to read the discord token
    Returns the token
    """
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
    try:  # checks if the user that send the command is in a voice channel
        channel = author.voice.channel
        current_members = []
        for member in channel.members:
            current_members.append(member.name)

        tts = gTTS(random.choice(current_members))
        tts.save('random.mp3')
        name_sound = ffmpeg.input('random.mp3')
        clip_sound = ffmpeg.input('clip.mp3')
        ffmpeg.concat(name_sound, clip_sound, v=0, a=1).output(
            'out.mp3').run(overwrite_output=True)

        vc = await channel.connect()
        vc.play(discord.FFmpegPCMAudio(source='out.mp3'))
        while vc.is_playing():
            sleep(.1)
        print(current_members)
        await ctx.voice_client.disconnect()
    except AttributeError:
        await ctx.send(f"{author.mention} is an idiot")
    except ClientException:  # handle the case when someone is spamming the bot command
        await ctx.send(f"{author.mention} stop spamming")

bot.run(token)
