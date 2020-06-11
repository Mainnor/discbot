import os
import random

import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord.utils import get
import youtube_dl
from dotenv import load_dotenv

import meta

load_dotenv()
TOKEN = os.getenv("TOKEN")
bot = commands.Bot(command_prefix="!")


@bot.command(name="split")
@commands.has_role("creator")
async def split_users(ctx, users_per_team, base_channel, team_a_channel, team_b_channel):
    guild = ctx.guild

    base = discord.utils.get(guild.voice_channels, name=base_channel)
    if not base:
        await ctx.send(meta.NO_BASE_CHANNEL_MSG)
        return

    team_a = discord.utils.get(guild.voice_channels, name=team_a_channel)
    if not team_a:
        await ctx.send(meta.NO_TEAM_A_CHANNEL_MSG)
        return

    team_b = discord.utils.get(guild.voice_channels, name=team_b_channel)
    if not team_b:
        await ctx.send(meta.NO_TEAM_B_CHANNEL_MSG)
        return

    users = base.members
    users_per_team = int(users_per_team)

    if len(users) < users_per_team:
        await ctx.send(meta.TEAM_GT_USERS_MSG)
        return

    team_a_membs = random.sample(users, users_per_team)
    team_b_membs = list(set(users) - set(team_a_membs))

    for user_a in team_a_membs:
        await user_a.move_to(team_a)

    for user_b in team_b_membs:
        await user_b.move_to(team_b)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.MissingRole):
        await ctx.send(meta.MISSING_ROLE_MSG)


@bot.command(name="clear")
@commands.has_role("creator")
async def clear(ctx, amount=20):
    await ctx.channel.purge(limit=amount)
    await ctx.send("Успешно очистил " + str(amount) + " сообщений.")


@bot.event
async def on_member_join(member):
    channel = bot.get_channel(703592757733752856)
    role = discord.utils.get(member.guild.roles, id=718100764136046732)
    await member.add_roles(role)
    await channel.send(f'Пользователь {member.name} присоединился')


@bot.command(name="play")
@commands.has_role("everyone")
async def play(ctx, url: str):
    global name
    if_song = os.path.isfile('song.mp3')

    try:
        if if_song:
            os.remove('song.mp3')
            print('[log] Старая песня удалена')
    except PermissionError:
        print('[log] Я не смог удалить песню')

    await ctx.send('Ожидайте лютый кач')

    voice = get(discord.client.voice_clients, guild=ctx.guild)
    ydl_opt = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExctractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192'
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opt) as ydl:
        print('[log] Гружу музыку')
        ydl.download([url])

    for file in os.listdir('./'):
        if file.endswith('.mp3'):
            name = file
            os.rename(file, 'song.mp3')

        voice.play(discord.FFmpegPCMAudio('song.mp3'),
                   after=lambda e: print(f'[log] {name}, Музыка все, выбирай новую'))
        voice.src = discord.PCMVolumeTransformer(voice.src)
        voice.src.volume = 0.07
        song_name = name.rsplit('_', 2)
        await ctx.send(f'Сейчас играет: {song_name[0]}')



if __name__ == "__main__":
    bot.run(TOKEN)
