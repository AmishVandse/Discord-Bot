import requests, json
import datetime
from discord.ext import commands, tasks
import discord
from dataclasses import dataclass



dataclass
class Session:
    is_active: bool = False
    start_time: int = 0

bot_token = "Insert Bot Token"  
channel_id = 1160375592865255565
max_study_time = 45


bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
session = Session()


@bot.event
async def on_ready():
    channel = bot.get_channel(channel_id)
    await channel.send("Hello! Study bot is ready!")


@tasks.loop(minutes = max_study_time, count=2)
async def break_time():
    if break_time.current_loop == 0:
        return
     
    channel = bot.get_channel(channel_id)
    await channel.send(f"TAKE A BREAK, you have been studying for {max_study_time} minutes.")

@bot.command()
async def add(ctx, *arr):
    result = 0
    for i in arr:
        result += int(i)
    await ctx.send(f"Result: {result}")
@bot.command()

async def multiply(ctx, *arr):
    result = 1
    for i in arr:
        result *= int(i)
    await ctx.send(f"Result: {result}")

@bot.command()
async def divide(ctx, a, b):
    try:
        result = int(a) / int(b)
        await ctx.send(f"Result: {result}")
    except ZeroDivisionError:
        await ctx.send("Cannot divide by zero.")

@bot.command()
async def subtract(ctx, a, b):
    result = int(a) - int(b)
    await ctx.send(f"Result: {result}")


@bot.command()
async def start(ctx, *arr):
    if session.is_active:
        await ctx.send("A session is already active!")
        return

    session.is_active = True
    session.start_time = ctx.message.created_at.timestamp()
    human_readable_time = ctx.message.created_at.strftime("%H:%M:%S")
    break_time.start()
    await ctx.send(f"Study session started as {human_readable_time}")

@bot.command()
async def end(ctx):
    if not session.is_active:
        await ctx.send("Session not active")

    session.is_active = False
    end_time = ctx.message.created_at.timestamp()
    duration = end_time- session.start_time
    human_readable_duration = str(datetime.timedelta(seconds=duration))
    break_time.stop()
    await ctx.send(f"Session ended after {human_readable_duration} seconds")


bot.run(bot_token)
