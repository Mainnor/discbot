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
load_dotenv()
TOKEN = os.getenv("TOKEN")
TOKEN = os.getenv("TOKEN")
bot = commands.Bot(command_prefix="!")
client = discord.Client()

if __name__ == "__main__":
    bot.run(TOKEN)
