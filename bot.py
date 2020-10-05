import io
import os
import queue
import random
import shutil
from asyncio import queues

import discord
import requests
import youtube_dl
from PIL import Image, ImageFont, ImageDraw
from discord.ext import commands
from discord.utils import get
from dotenv import load_dotenv
import json

import meta

load_dotenv()
TOKEN = os.getenv("TOKEN")
bot = commands.Bot(command_prefix="!")
os.chdir(r"C:\Users\Minor\Downloads\Programs\Programs\Programming\Discbot")
bot.remove_command('help')
client = discord.Client()
queues = {}


@bot.event
async def on_ready():
    print("Зареган как: " + bot.user.name + "\n")


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
async def clear(ctx, amount=250):
    await ctx.channel.purge(limit=amount)
    await ctx.send("Успешно очистил " + str(amount) + " сообщений.")
    print('Cleared ' + str(amount))


@bot.event
async def on_member_join(member):
    channel = bot.get_channel(703592757733752856)
    role = discord.utils.get(member.guild.roles, id=718100764136046732)
    await member.add_roles(role)
    await channel.send(f'Пользователь {member.name} присоединился')



@bot.command(name="play")
async def play(ctx, url: str):
    def check_queue():
        Queue_infile = os.path.isdir("./Queue")
        if Queue_infile is True:
            if Queue_infile is True:
                DIR = os.path.abspath(os.path.realpath("Queue"))
                length = len(os.listdir(DIR))
                still_q = length - 1
            try:
                first_file = os.listdir(DIR)[0]
            except:
                print("No more queued song(s)\n")
                queues.clear()
                return
            main_location = os.path.dirname(os.path.realpath(__file__))
            song_path = os.path.abspath(os.path.realpath("Queue") + "\\" + first_file)
            if length != 0:
                print("Song done, playing next queued\n")
                print(f"Songs still in queue: {still_q}")
                song_there = os.path.isfile("song.mp3")
                if song_there:
                    os.remove("song.mp3")
                shutil.move(song_path, main_location)
                for file in os.listdir("./"):
                    if file.endswith(".mp3"):
                        os.rename(file, 'song.mp3')

                voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: check_queue())
                voice.source = discord.PCMVolumeTransformer(voice.source)
                voice.source.volume = 0.07

            else:
                queue.clear()
                return

        else:
            queue.clear()
            print("No songs were queued before the ending of the last song\n")

    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
            queue.clear()
            print("Removed old song file")
    except PermissionError:
        print("Trying to delete song file, but it's being played")
        await ctx.send("ERROR: Music playing")
        return

    Queue_infile = os.path.isdir("./Queue")
    try:
        Queue_folder = "./Queue"
        if Queue_infile is True:
            print("Removed old Queue Folder")
            shutil.rmtree(Queue_folder)
    except:
        print("No old Queue folder")

    await ctx.send("Getting everything ready now")

    voice = get(bot.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("Downloading audio now\n")
        ydl.download([url])

    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            name = file
            print(f"Renamed File: {file}\n")
            os.rename(file, "song.mp3")

    voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: check_queue())
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.07

    nname = name.rsplit("-", 2)
    await ctx.send(f"Playing: {nname[0]}")
    print("playing\n")


@bot.command(name="next")
async def next(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_playing():
        print("Playin ne    xt song")
        voice.stop()
        await ctx.send("Next song")
    else:
        print("No music playing next song")
        await ctx.send("No music playing failed")


@bot.command(name="stop")
async def stop(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)

    queues.clear()
    queue_infile = os.path.isdir("./Queue")
    if queue_infile is True:
        shutil.rmtree("./Queue")

    if voice and voice.is_playing():
        print("Music stopped")
        voice.stop()
        await ctx.send("Прекращение воспроизведения музыки удалось")
    else:
        print("No music playing failed to stop")
        await ctx.send("Прекращение воспроизведения музыки не удалось")


@bot.command(name="queue")
async def queue(ctx, url: str):
    Queue_infile = os.path.isdir("./Queue")
    if Queue_infile is False:
        os.mkdir("Queue")
    DIR = os.path.abspath(os.path.realpath("Queue"))
    q_num = len(os.listdir(DIR))
    q_num += 1
    add_queue = True
    while add_queue:
        if q_num in queues:
            q_num += 1
        else:
            add_queue = False
            queues[q_num] = q_num

    queue_path = os.path.abspath(os.path.realpath("Queue") + f"\song{q_num}.%(ext)s")

    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'outtmpl': queue_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("Downloading audio now\n")
        ydl.download([url])
    await ctx.send("Добавляю песню " + str(q_num) + " в очередь")

    print("Song added to queue\n")


@bot.command(name="resume")
async def resume(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_paused():
        print("Resumed music")
        voice.resume()
        await ctx.send("Музыка продолжает играть")
    else:
        print("Music is not paused")
        await ctx.send("Музыка уже играет")


@bot.command(name="pause")
async def pause(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_playing():
        print("Music paused")
        voice.pause()
        await ctx.send("Музыка остановлена")
    else:
        print("Music not playing failed pause")
        await ctx.send("Я не смог остановить музыку")


@bot.command(name="leave")
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
        print(f"The bot has left {channel}")
        await ctx.send(f"Вышел из {channel}")
    else:
        print("Bot was told to leave voice channel, but was not in one")
        await ctx.send("Бот пытался выйти из канала, но не смог")


@bot.command(name="join")
async def join(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice is not None:
        return await voice.move_to(channel)
    await channel.connect()
    print(f"The bot has connected to {channel}\n")
    await ctx.send(f"Я присоединился к {channel}.")


@bot.command(name="info")
async def info(ctx):
    img = Image.new("RGBA", (400, 200), "#36393f")
    url = str(ctx.author.avatar_url)[:-10]
    response = requests.get(url, stream=True)
    response = Image.open(io.BytesIO(response.content))
    response = response.convert("RGBA")
    response = response.resize((100, 100), Image.ANTIALIAS)
    img.paste(response, (15, 15, 115, 115))
    idraw = ImageDraw.Draw(img)
    name = ctx.author.name  # Minor
    tag = ctx.author.discriminator  # 6473
    headline = ImageFont.truetype("arial.ttf", size=20)
    utxt = ImageFont.truetype("arial.ttf", size=14)
    idraw.text((145, 15), f'{name}#{tag}', font=headline)
    idraw.text((145, 50), f'ID: {ctx.author.id}', font=utxt)
    img.save("info.png")
    await ctx.send(file=discord.File(fp="info.png"))


@bot.command(name="volume")
@commands.has_role("creator")
async def volume(ctx, volume: int):
    if ctx.voice_client is None:
        return await ctx.send("Музыка не играет, что редактировать?")
    print(volume / 100)

    ctx.voice_client.source.volume = volume / 100
    await ctx.send(f"Звук изменен до {volume}")


@bot.command(name="help")
async def help(ctx):
    img = Image.open('help.png')
    await ctx.send(file=discord.File(fp="help.png"))


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="помощь"))


if __name__ == "__main__":
    bot.run(TOKEN)
