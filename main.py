import discord 
from discord.ext import commands
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time 
import requests
import urllib
import json
from random import randint
from discord.ext.commands import has_permissions, MissingPermissions
import asyncio
import random
import datetime
import discord
import os
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType
from discord.ext import commands, tasks
from discord.voice_client import VoiceClient
import youtube_dl
import urllib
import re
import datetime
from time import sleep
import ast
import re
import discord
from discord import User
import time
import random
import asyncio
import base64
from discord.ext import commands
from discord.ext.tasks import loop
from discord.ext.commands import Bot
import psutil
bot = commands.Bot('+', shard_count = 1, case_insensitive = True, intents = discord.Intents().all())
from discord.voice_client import VoiceClient
import youtube_dl
import urllib
import re
import datetime
from time import sleep
import ast
import re
import discord
from discord import User
import time
import random
import asyncio
import base64
from discord.ext import commands
from discord.ext.tasks import loop
from discord.ext.commands import Bot
import psutil
global loops
loops = {}
global nowPlaying
nowPlaying = {}
global nullTime
nullTime = time.time() # это в самом начале
allowed_people = ["479959100327723009"]
token = "ODAwMjk1MjU1OTE2MTUwODE2.YAQDCQ.uz4o4gtHtK29nro000Gh4ldWuTs"
bot.remove_command('help')
def get_status(ctx,ip):
    url = f'https://mc.api.srvcontrol.xyz/server/status?ip={ip}'
    with urllib.request.urlopen(url) as data:
        status = json.loads(data.read().decode())
        if status['online'] == True and not status['error']:
            online = status['players']['now']
            max = status['players']['max']
            status['players']['now']
            core = status['server']['name']
            motd = status['motd']
            cc = ['§1','§2','§3','§4','§5','§6','§7','§8','§9','§0','§a','§b','§c','§d','§e','§f','§m','§n','§l','§k','§r']
            for i in cc:
                motd = motd.replace(i,'')
                core = core.replace(i,'')
            emb = discord.Embed(title=f'Информация о сервере {ip}',description=f'```{motd}```',color=0xff689a)
            emb.add_field(name='Игроков онлайн', value=f'{online}/{max}', inline=True)
            emb.add_field(name='Ядро', value=core, inline=True)
            emb.set_thumbnail(url=f'https://eu.mc-api.net/v3/server/favicon/{ip}')
            return emb
        else:
            emb = discord.Embed(description=':x: Не удалось установить соединение с сервером.',color=0xff689a)
            return emb
@bot.event
async def on_command_error(ctx, error):
    id = ctx.message.author.id
    channel = bot.get_channel(858076323930439760)
    if isinstance(error, commands.errors.MemberNotFound):
        await ctx.send("**Пользователь не найден! :x:**") 
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('**Вы не правильно написали команду! :x:**')
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("**У вас нет прав! :angry:**")
        print(error)
    if isinstance(error, commands.errors.CommandInvokeError):
        await channel.send(f"**У пользователя ошибка.**"+"|""**Пользовалель:**"+"<@"+str(id)+">")
        await ctx.send("**Ошибка (проверьте права бота)! :x:**")
        print(error)
    if isinstance(error, commands.errors.BotMissingPermissions):
        await ctx.send("**У меня нету прав! :disappointed_relieved:**")
        print(error)
    if isinstance(error, commands.CommandOnCooldown):
        cooldown = round(error.retry_after)
        emb = discord.Embed(description=f':x: Вы сможете использовать эту команду через {cooldown} секунд.',color=0xdd2e44)
        await ctx.send(embed = emb,delete_after=2)
   
@bot.command()
@commands.cooldown(1, 30, commands.BucketType.user)
async def info(ctx,ip):
    def check(reaction,user):
        if reaction.message.id == lastmsg.id and reaction.emoji == '📌':
            return reaction
        else:
            return False
    if ctx.message.author.bot:
        return
    await ctx.message.delete()
    async with ctx.typing():
        emb = get_status(ctx,ip)
    lastmsg = await ctx.send(embed = emb)
    await lastmsg.add_reaction('📌')
    try:
        await asyncio.sleep(1)
        reaction = await bot.wait_for('reaction_add', timeout=30.0, check=check)
    except asyncio.TimeoutError as error:
        pass
        return
    emb = discord.Embed(description = '<a:purpleverify:853287470942257152> Закреплено! Каждые 5 минут информация о сервере будет обновляться.',color=0xff689a)
    msg = await ctx.send(embed = emb)
    await asyncio.sleep(5)
    await msg.delete()
    while True:
        emb = get_status(ctx,ip)
        await asyncio.sleep(360)
        try:
            await lastmsg.edit(embed = emb)
        except:
            break
@bot.command()
async def prioq(ctx):
    r = requests.get(f'https://api.2b2t.dev/prioq')
    embed = discord.Embed(title="2B2T", description="Приорететная очередь",color=0xff689a)
    embed.add_field(name="Очередь", value=r.json()[1], )
    embed.add_field(name="Время ожидания", value=r.json()[2], )
    await ctx.channel.send(embed=embed)
@bot.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def join(ctx, channel: discord.VoiceChannel = None):
    if ctx.message.author.bot:
        return
    if await is_overloaded(ctx):
        return
    e = False
    if ctx.author.voice:
        if channel == None:
            channel = ctx.author.voice.channel
        else:
            pass
        voice = discord.utils.get(ctx.bot.voice_clients, guild = ctx.guild)
        emb = discord.Embed(description = '<a:purpleverify:853287470942257152> Подключился к каналу.', color = 0xff689a)
        if voice:
            vc = ctx.message.guild.voice_client
            try:
                await vc.move_to(channel)
            except:
                emb = discord.Embed(description = ':x: Не удалось подключиться к голосовому каналу.', color = 0xff689a)
                e == True
        else:
            try:
                await channel.connect(timeout = 5, reconnect = True)
            except:
                emb = discord.Embed(description = ':x: Не удалось подключиться к голосовому каналу.', color = 0xff689a)
                e == True
    else:
        emb = discord.Embed(description = ':x: зайдите в голосовой канал.', color = 0xff689a)
        e = True
    m = await ctx.send(embed = emb)
    if e == True:
        await asyncio.sleep(3)
        await m.delete()
    while True:
        await asyncio.sleep(30)
        if not is_connected(ctx):
            break
        members = channel.members
        memids = []
        for member in members:
            if not member.bot:
                memids.append(member.id)
        if len(memids) == 0:
            voice = get_voice(ctx)
            await voice.disconnect()
            break
@bot.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def leave(ctx):
    if ctx.message.author.bot:
        return
    global loops
    if is_connected(ctx):
        vc = ctx.message.guild.voice_client
        if loops.get(ctx.guild.id) == True:
            loops[ctx.guild.id] = False
        await vc.disconnect()
        emb = discord.Embed(description = '<a:purpleverify:853287470942257152>  Отключен от голосового канала.', color = 0xff689a)
        await ctx.send(embed = emb)
    else:
        emb = discord.Embed(description = ':x: Я не подключен к голосовому каналу на этом сервере.', color = 0xff689a)
        await ctx.send(embed = emb, delete_after = 2)

@bot.command()
@commands.cooldown(1, 25, commands.BucketType.user)
async def radio(ctx, url = ''):
    if ctx.message.author.bot:
        return
    global loops, nowPlaying
    if await is_overloaded(ctx):
        return
    if not url:
        emb = discord.Embed(description = ':x: Используйте: `+radio <url>`\nСтанции: https://espradio.ru/stream_list', color = 0xff689a)
        await ctx.send(embed = emb)
        return
    if not ctx.author.voice:
        emb = discord.Embed(description = ':x: Вы должны находиться в голосовом канале для вызова этой команды.', color = 0xff689a)
        await ctx.send(embed = emb, delete_after = 3)
        return
    voice = get_voice(ctx)
    if nowPlaying.get(ctx.guild.id) != url:
        nowPlaying[ctx.guild.id] = url
    if ctx.message.author.voice:
        channel = ctx.author.voice.channel
        if is_connected(ctx):
            player = voice
            try:
                voice.stop()
            except:
                pass
        else:
            try:
                player = await channel.connect(timeout = 5, reconnect = True) 
            except:
                emb = discord.Embed(description = ':x: Не удалось подключиться к голосовому каналу.', color = 0xff689a)
                await ctx.send(embed = emb, delete_after = 2)
                return
    player.play(FFmpegPCMAudio(url))
    emb = discord.Embed(description = f'<a:purpleverify:853287470942257152>  Воспроизвожу:\n```{url}```', color = 0xff689a)
    await ctx.send(embed = emb)
    while True:
        await asyncio.sleep(30)
        if not is_connected(ctx):
            break
        members = channel.members
        memids = []
        for member in members:
            if not member.bot:
                memids.append(member.id)
        if len(memids) == 0:
            voice = get_voice(ctx)
            await voice.disconnect()
            break
@bot.command(aliases=['p'])
@commands.cooldown(1, 20, commands.BucketType.user)
async def play(ctx, *, query = ''):
    if ctx.message.author.bot:
        return
    if await is_overloaded(ctx):
        return
    global loops, nowPlaying
    if not query:
        emb = discord.Embed(description = '❌ Используйте: `+play <query>`', color = 0xdd2e44)
        m = await ctx.send(embed = emb, delete_after = 2)
        return
    if not ctx.author.voice:
        emb = discord.Embed(description = '❌ Вы должны находиться в голосовом канале для вызова этой команды.', color = 0xdd2e44)
        await ctx.send(embed = emb, delete_after = 2)
        return
    channel = ctx.author.voice.channel
    voice = get_voice(ctx)
    emb = discord.Embed(description = f'<a:purpleverify:853287470942257152> Выполняется поиск на YouTube:\n```{query}```', color = 0x000000)
    lastmsg = await ctx.send(embed = emb)
    query_string = urllib.parse.urlencode({'search_query': query})
    htm_content = urllib.request.urlopen('http://www.youtube.com/results?' + query_string)
    try:
        search_results = re.findall(r'/watch\?v=(.{11})', htm_content.read().decode())
        url = f'https://youtu.be/{search_results[0]}'
    except:
        pass
        await lastmsg.delete()
        emb = discord.Embed(description = '❌ По вашему запросу ничего не найдено.', color = 0xdd2e44)
        await ctx.send(embed = emb, delete_after = 2)
        return
    if is_connected(ctx) and voice.is_playing():
        try:
            voice.stop()
        except:
            pass
    await lastmsg.add_reaction('✅')
    if get_voice(ctx) != None:
        player = get_voice(ctx)
    else:
        try:
            player = await channel.connect(timeout = 5, reconnect = True)
        except:
            await lastmsg.delete()
            emb = discord.Embed(description = '❌ Не удалось подключиться к голосовому каналу.', color = 0xdd2e44)
            await ctx.send(embed = emb, delete_after = 2)
            return
    async with ctx.typing():
        ydl_opts = {'format': 'worstaudio'}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            URL = info['formats'][0]['url']
            title = info.get('title', None)
            duration = info.get('duration', None)
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 10', 'options': '-vn'}
        d = duration
        if nowPlaying.get(ctx.guild.id) == None or nowPlaying.get(ctx.guild.id) != url:
            nowPlaying[ctx.guild.id] = url
        duration = datetime.timedelta(seconds = duration)
    await lastmsg.delete()
    emb = discord.Embed(description = f'<a:purpleverify:853287470942257152> Воспроизведение:\n```{title} ({duration})```\nСсылка на видео: {url}', color = 0x000000)
    i = 1
    while loops.get(ctx.guild.id) == True or i == 1:
        if nowPlaying.get(ctx.guild.id) != url:
            break
        voice = get_voice(ctx)
        try:
            if voice.is_playing():
                voice.stop()
        except:
            pass
        player.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
        if i == 1:
            await ctx.send(embed = emb)
        i = 0
        await asyncio.sleep(d+1)
        if nowPlaying.get(ctx.guild.id) != url:
            break
        if not is_connected(ctx):
            break
        members = channel.members
        memids = []
        for member in members:
            if not member.bot:
                memids.append(member.id)
        if len(memids) == 0:
            voice = get_voice(ctx)
            await voice.disconnect()
            break
        player.stop()

@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def pause(ctx):
    if ctx.message.author.bot:
        return
    if not ctx.author.voice:
        emb = discord.Embed(description = ':x: Вы должны находиться в голосовом канале для вызова этой команды.', color = 0xff689a)
        await ctx.send(embed = emb, delete_after = 2)
        return
    voice = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
        emb = discord.Embed(color = 0xff689a, description = '<a:purpleverify:853287470942257152> Воспроизведение приостановлено.')
        await ctx.send(embed = emb)
    else:
        emb = discord.Embed(color = 0xff689a, description = ':x: Сейчас ничего не играет.')
        await ctx.send(embed = emb, delete_after = 2)

@bot.command(aliases = ['re'])
@commands.cooldown(1, 5, commands.BucketType.user)
async def resume(ctx):
    if ctx.message.author.bot:
        return
    if not ctx.author.voice:
        emb = discord.Embed(description = ':x: Вы должны находиться в голосовом канале для вызова этой команды.', color = 0xff689a)
        await ctx.send(embed = emb,delete_after = 2)
        return
    voice = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
    if await is_overloaded(ctx) and voice:
        voice.stop()
        return
    if voice.is_paused():
        voice.resume()
        emb = discord.Embed(color = 0xff689a, description = '<a:purpleverify:853287470942257152>  Воспроизведение продолжено.')
        await ctx.send(embed = emb)
    else:
        emb = discord.Embed(color = 0xff689a, description = ':x: Воспроизведение не было приостановлено.')
        await ctx.send(embed = emb, delete_after = 2)

@bot.command(aliases = ['youtube'])
@commands.cooldown(1, 20, commands.BucketType.user)
async def yt(ctx, *, query=''):
    if ctx.message.author.bot:
        return
    if await is_overloaded(ctx):
        return
    if not query:
        emb = discord.Embed(description = ':x: Использование: `+yt <query>`', color = 0xff689a)
        await ctx.send(embed = emb,delete_after = 2)
        return
    emb = discord.Embed(description=f'<a:purpleverify:853287470942257152>  Выполняется поиск на YouTube:\n```{query}```', color = 0xff689a)
    lastmsg = await ctx.send(embed = emb)
    query_string = urllib.parse.urlencode({'search_query': query})
    async with ctx.typing():
        htm_content = urllib.request.urlopen('http://www.youtube.com/results?' + query_string)
        search_results = re.findall(r'/watch\?v=(.{11})', htm_content.read().decode())
    try:
        msg = description=f'`1.` https://youtu.be/{search_results[0]}\n`2.` https://youtu.be/{search_results[1]}\n`3.` https://youtu.be/{search_results[2]}'
        await lastmsg.delete()
        await ctx.send(msg)
    except:
        await lastmsg.delete()
        emb = discord.Embed(description=':x: По вашему запросу ничего не найдено.', color = 0xff689a)
        await ctx.send(embed = emb, delete_after = 2)

@bot.command(aliases = ['s','skip'])
@commands.cooldown(1, 5, commands.BucketType.user)
async def stop(ctx):
    if ctx.message.author.bot:
        return
    if not ctx.author.voice:
        emb = discord.Embed(description = ':x: Вы должны находиться в голосовом канале для вызова этой команды.', color = 0xff689a)
        await ctx.send(embed = emb, delete_after = 2)
        return
    voice = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
    if is_connected(ctx) and voice.is_playing():
        voice.stop()
        global loops, nowPlaying
        if loops.get(ctx.guild.id) == True and nowPlaying.get(ctx.guild.id) != None:
            nowPlaying[ctx.guild.id] = None
        emb = discord.Embed(description = f'<a:purpleverify:853287470942257152>  Воспроизведение остановлено.', color = 0xff689a)
        await ctx.send(embed = emb)
    else:
        emb = discord.Embed(description = ':x: Сейчас ничего не играет.', color = 0xff689a)
        await ctx.send(embed = emb, delete_after = 2)

@bot.command(aliases = ['loop','l'])
@commands.cooldown(1, 5, commands.BucketType.user)
async def repeat(ctx):
    if ctx.message.author.bot:
        return
    global loops
    if not ctx.author.voice:
        emb = discord.Embed(description = ':x: Вы должны находиться в голосовом канале для вызова этой команды.', color = 0xff689a)
        await ctx.send(embed = emb, delete_after = 2)
        return
    key = ctx.guild.id
    loops[key] = loops.get(key)
    if loops[key] == None:
        loops[key] = False
    if loops[key] == False:
        loops[key] = True
        emb = discord.Embed(description = '<a:purpleverify:853287470942257152>  Воспроизведение зациклено.', color = 0xff689a)
        await ctx.send(embed = emb)
        return
    if loops[key] == True:
        loops[key] = False
        emb = discord.Embed(description = '<a:purpleverify:853287470942257152>  Стандартный режим воспроизведения.', color = 0xff689a)
        await ctx.send(embed = emb)

async def is_overloaded(ctx):
    if psutil.cpu_percent() >= 89 or psutil.virtual_memory().percent >= 89:
        emb = discord.Embed(description = ':x: Эта команда недоступна, так как бот в данный момент перегружен.', color = 0xff689a)
        await ctx.send(embed = emb, delete_after = 4)
        return True
    else:
        return False

def get_voice(ctx):
    voice = discord.utils.get(ctx.bot.voice_clients, guild = ctx.guild)
    return voice

def is_connected(ctx):
    voice_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
    return voice_client and voice_client.is_connected()
@bot.event
async def on_ready():
    print("Bot is ready")
@bot.command(pass_context=True)
@commands.cooldown(1, 20,commands.BucketType.user)
async def bal(ctx):
    await open_account(ctx.author)
    user = ctx.author

    users = await get_bank_data()

    wallet_amt = users[str(user.id)]["wallet"]

    bank_amt = users[str(user.id)]["bank"]

    embed = discord.Embed(title=f"Баланс {ctx.author.name}",color=0xff689a)

    embed.add_field(name= "Наличные", value= wallet_amt,inline = False)
    embed.add_field(name= "Банк", value= bank_amt,inline = False)

    await ctx.send(embed = embed)
@bot.command(pass_context=True)
@commands.cooldown(1, 600, commands.BucketType.user)
async def work(ctx):
    await open_account(ctx.author)
    user = ctx.author

    users = await get_bank_data()

    


    earnings = random.randrange(20)
    await ctx.send(embed = discord.Embed(title = f'** {ctx.author.name},вы хорошо поработали и получили {earnings} монет(ы)!**',color=0xff689a))

    users[str(user.id)]["wallet"] += earnings

    with open("mainbank.json", "w") as f:
        json.dump(users,f)

@bot.command(pass_context=True)
@commands.cooldown(1, 18000, commands.BucketType.user)
async def daily(ctx):
    await open_account(ctx.author)
    user = ctx.author

    users = await get_bank_data()

    


    earnings = random.randrange(101)
    await ctx.send(embed = discord.Embed(title = f'** {ctx.author.name}, вы получили {earnings} монет(ы)!**',color=0xff689a))

    users[str(user.id)]["wallet"] += earnings

    with open("mainbank.json", "w") as f:
        json.dump(users,f)

@bot.command(pass_context=True)
@commands.cooldown(1, 20, commands.BucketType.user)
async def withdraw(ctx,amount = None):
    await open_account(ctx.author)
    if amount == None:
        await ctx.send("**Пожалуйста, введите сумму**")
        return
    await ctx.message.delete()
    bal = await update_bank(ctx.author)

    amount = int(amount)

    if amount>bal[1]:
        await ctx.send("**У тебя нет столько денег!**")
        return
    if amount<0:
        await ctx.send("**Сумма должна быть положительной!**")
        return

    await update_bank(ctx.author,amount)
    await update_bank(ctx.author,-1*amount,"bank")

    await ctx.send(f"**Вы вывели {amount} монет(ы)!**")

@bot.command(pass_context=True)
@commands.cooldown(1, 20, commands.BucketType.user)
async def dep(ctx,amount = None):
    await open_account(ctx.author)
    if amount == None:
        await ctx.send("**Пожалуйста, введите сумму**")
        return
    bal = await update_bank(ctx.author)

    amount = int(amount)

    if amount>bal[0]:
        await ctx.send("**У тебя нет столько денег!**")
        return
    if amount<0:
        await ctx.send("**Сумма должна быть положительной!**")
        return

    await update_bank(ctx.author,-1*amount)
    await update_bank(ctx.author,amount,"bank")

    await ctx.send(f"**Вы вклали {amount} монет(ы)!**")
@bot.command(pass_context=True)
@commands.cooldown(1, 18000, commands.BucketType.user)
async def rob(ctx,member: discord.Member):
    await open_account(ctx.author)
    await open_account(member)
    bal = await update_bank(member)

    

    if bal[0]<100:
        await ctx.send("У него нету денег.")
        return

    earnings = random.randrange(0, bal[0])
  

    await update_bank(ctx.author,earnings)
    await update_bank(member,-1*earnings)

    await ctx.send(f"Ты ограбил и получил {earnings} монет!")


@bot.command(pass_context=True)
@commands.cooldown(1, 20, commands.BucketType.user)
async def slots(ctx, amount = None):
    await open_account(ctx.author)
    if amount == None:
        await ctx.send("Пожалуйста, введите сумму!")
        return
    bal = await update_bank(ctx.author)

    amount = int(amount)

    if amount>bal[0]:
        await ctx.send("У тебя нет столько денег!")
        return
    if amount<0:
        await ctx.send("Сумма должна быть положительной!")
        return

    final = []
    for i in range(3):
        a = random.choice([":coin:", ":four_leaf_clover:", ":money_with_wings:"])

        final.append(a)

    await ctx.send(str(final))

    if final[0] == final[1] or final[0] == final[2] or final[2] == final[1]:
         await update_bank(ctx.author,2*amount)
         await ctx.send("**Ты выиграл!**")

    else:
        await update_bank(ctx.author,-1*amount)
        await ctx.send("**Ты проиграл!**")


async def open_account(user):

    users = await get_bank_data()
    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["wallet"] = 0
        users[str(user.id)]["bank"] = 0

    with open("mainbank.json", "w") as f:
        json.dump(users,f)
    return True


async def get_bank_data():
    with open("mainbank.json", "r") as f:
        users = json.load(f)

    return users



async def update_bank(user, change=0,mode = 'wallet'):

    users = await get_bank_data()

    users[str(user.id)][mode] += change

    with open("mainbank.json", "w") as f:
        json.dump(users,f)

    bal = users[str(user.id)]["wallet"],users[str(user.id)]["bank"]


    return bal
global loops
loops = {}
global nowPlaying
nowPlaying = {}
global nullTime
nullTime = time.time() # это в самом начале
allowed_people = ["479959100327723009"]
token = "ODAwMjk1MjU1OTE2MTUwODE2.YAQDCQ.uz4o4gtHtK29nro000Gh4ldWuTs"
bot.remove_command('help')
async def is_overloaded(ctx):
    if ctx.author.id == 811976103673593856:
        return False
    if psutil.cpu_percent() >= 89 or psutil.virtual_memory().percent >= 89:
        emb = discord.Embed(description = ':x: Эта команда недоступна, так как бот в данный момент перегружен.', color = 0xdd2e44)
        await ctx.send(embed = emb, delete_after = 4)
        return True
    else:
        return False
@bot.event
async def on_command_error(ctx, error):
    id = ctx.message.author.id
    channel = bot.get_channel(858076323930439760)
    if isinstance(error, commands.errors.MemberNotFound):
        await ctx.send("**Пользователь не найден! :x:**") 
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('**Вы не правильно написали команду! :x:**')
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("**У вас нет прав! :angry:**")
        print(error)
    if isinstance(error, commands.errors.CommandInvokeError):
        await channel.send(f"**У пользователя ошибка.**"+"|""**Пользовалель:**"+"<@"+str(id)+">")
        await ctx.send("**Ошибка (проверьте права бота)! :x:**")
        print(error)
    if isinstance(error, commands.errors.BotMissingPermissions):
        await ctx.send("**У меня нету прав! :disappointed_relieved:**")
        print(error)
    if isinstance(error, commands.CommandOnCooldown):
        cooldown = round(error.retry_after)
        emb = discord.Embed(description=f':x: Вы сможете использовать эту команду через {cooldown} секунд.',color=0xdd2e44)
        await ctx.send(embed = emb,delete_after=2)
#-------------------------
@bot.event
async def on_ready():
    print("Bot is ready")
    DiscordComponents(bot)
    channel = bot.get_channel(858076323930439760)
    await channel.send("Я онлайн.")
    servers=list(bot.guilds)
    sleep(3)
    await channel.send(f'Я на {str(len(servers))} servers')
    while True:
        s = f'+help | [{len(bot.guilds)}]'
        await bot.change_presence(activity=discord.Streaming(name = s, url = "https://www.youtube.com/watch?v=EuJ4FFwcVVY"))
        await asyncio.sleep(360)
        print(f'[HerokuAntiSleep] {time.time()}')
@bot.command(sort_commands='2b2t')
async def stats(ctx, player):
    r = requests.get(f'https://api.2b2t.dev/stats?username={player}')
    embed = discord.Embed(title="2B2T", description="Статы",color=0xff689a)
    embed.set_image(url=f'https://minecraftskinstealer.com/api/v1/skin/render/fullbody/{player}/700')
    embed.add_field(name="ID", value=r.json()[0]['id'], )
    embed.add_field(name="Ник", value=r.json()[0]['username'], )
    embed.add_field(name="Uuid", value=r.json()[0]['uuid'], )
    embed.add_field(name="Убийства", value=r.json()[0]['kills'], )
    embed.add_field(name="Смерти", value=r.json()[0]['deaths'], )
    embed.add_field(name="Заходы", value=r.json()[0]['joins'], inline=True)
    embed.add_field(name="Выходы", value=r.json()[0]['leaves'], inline=True)
    embed.add_field(name="Уровень прав", value=r.json()[0]['adminlevel'], inline=True)
    await ctx.channel.send(embed=embed)

@bot.command()
async def seen(ctx, player):
    r = requests.get(f'https://api.2b2t.dev/seen?username={player}')
    embed = discord.Embed(title="2B2T",color=0xff689a)
    embed.set_image(url=f'https://minecraftskinstealer.com/api/v1/skin/render/fullbody/{player}/700')
    embed.add_field(name="Последний онлайн", value=r.json()[0]['seen'], )
    await ctx.channel.send(embed=embed)
    
@bot.command()
async def q(ctx):
    r = requests.get(f'https://2b2t.io/api/queue')
    embed = discord.Embed(title="2B2T",color=0xff689a)
    embed.add_field(name="Очередь", value=r.json()[0][1], )
    await ctx.channel.send(embed=embed)
#---
#moderadion
@bot.command()
@commands.has_permissions(kick_members=True)
@commands.cooldown(1, 10, commands.BucketType.user)
async def kick(ctx,member:discord.Member):
    if ctx.message.author.bot:
        return
    await ctx.message.delete()
    emb = discord.Embed(description='<a:purpleverify:853287470942257152> '+member.mention+' кикнут.',color=0xff689a)
    await member.kick()
    await ctx.send(embed = emb)

@bot.command()
@commands.has_permissions(ban_members=True)
@commands.cooldown(1, 10, commands.BucketType.user)
async def ban(ctx,member:discord.Member):
    if ctx.message.author.bot:
        return
    await ctx.message.delete()
    emb = discord.Embed(description='<a:purpleverify:853287470942257152> '+member.mention+' забанен.',color=0xff689a)
    await member.ban()
    await ctx.send(embed = emb)

@bot.command()
@commands.has_permissions(ban_members = True)
@commands.cooldown(1, 10, commands.BucketType.user)
async def unban(ctx, *, member):
    if ctx.message.author.bot:
        return
    banned_users = await ctx.guild.bans()
    try:
        member_name, member_discriminator = member.split('#')
    except:
        emb = discord.Embed(description = ':x: Некорректный аргумент.\nПример использования: `+unban User#0000`', color = 0xff689a)
        await ctx.send(embed = emb, delete_after = 2)
        return
    for ban_entry in banned_users:
        user = ban_entry.user
    try:
        await ctx.guild.unban(user)
    except commands.errors.BotMissingPermissions:
        await permerror(ctx)
        return
    except:
        emb = discord.Embed(description = ':x: Этот пользователь не был забанен.', color = 0xff689a)
        await ctx.send(embed = emb, delete_after = 2)
        return
    emb = discord.Embed(description = f'<a:purpleverify:853287470942257152> {user} разбанен.', color  = 0xff689a)
    await ctx.send(embed = emb)
@bot.command(aliases=['purge'])
@commands.has_permissions(manage_messages = True)
@commands.cooldown(1, 30, commands.BucketType.user)
async def clear(ctx, amount):
    if await is_overloaded(ctx):
        return
    try:
        amount = int(amount)
        if amount < 0:
            emb = discord.Embed(description = f':x: Некорректный аргумент.', color = 0xff689a)
            await ctx.send(embed = emb, delete_after = 2)
    except:
        emb = discord.Embed(description = f':x: Заданный аргумент не является числом.', color = 0xff689a)
        await ctx.send(embed = emb, delete_after = 2)
    else:
        try:
            deleted = await ctx.message.channel.purge(limit = amount + 1)
        except:
            await permerror(ctx)
            return
        emb = discord.Embed(description = f'<a:purpleverify:853287470942257152> Удалено `{len(deleted)-1}` сообщений.', color = 0xff689a)
@bot.command()
@commands.cooldown(1, 5,commands.BucketType.user)
async def servers(ctx):
    servers=list(bot.guilds)
    embed = discord.Embed(title=f'Я на {str(len(servers))} servers',description='\n'.join(server.name for server in servers),color=0xff689a)
    embed.set_footer(text="Yrda")
    await ctx.send(embed=embed)
#--------------
@bot.command()
@commands.cooldown(1, 5,commands.BucketType.user)
async def slowmode(ctx, seconds):
    await ctx.channel.edit(slowmode_delay=seconds)
    await ctx.send(f"Установлена заддержка медленного режима в этом канале на {seconds} секунд(ы)!")
@bot.command()
@commands.cooldown(1, 5,commands.BucketType.user)
async def google(ctx,arg1, *, arg2="."):
    embed=discord.Embed(color=0xff689a)
    embed.set_footer(text="Yrda")
    embed.set_image(url = "https://image.thum.io/get/auth/11091-RandomBot/nomention/https://google.com/search?q="+str(re.sub(' ', '+', arg1))+"+"+str(re.sub(' ', '+', arg2)))
    await ctx.send(embed=embed)
#help
@bot.command()
async def help(ctx):
    await ctx.send(
        embed=discord.Embed(title="Выберите категорию!",description="Если вы нашли ошибку сообщите серверу поддержки.",delete_after=5,color=0xff689a),
        components=[
            Button(style=ButtonStyle.red, label="Фан", emoji="🎉"),
            Button(style=ButtonStyle.green, label="Майнкрафт", emoji="🟩"),
            Button(style=ButtonStyle.blue, label="Модерация", emoji="🛡️"),
            Button(style=ButtonStyle.red, label="Музыка", emoji="🎵"),
            Button(style=ButtonStyle.green, label="Экономика", emoji="💰"),
        ]
    )
    response = await bot.wait_for("button_click")
    if response.channel == ctx.channel:
        if response.component.label == "Фан":
            embed=discord.Embed(title="Фан команды",color=0xff689a)
            embed.add_field(name="Страница 1", value="`+sniper <user>` - снайпер\n`+stonks <user>` - стонкс\n`+gun <user>` - пистолет к аватару\n`+rainbow <user>` - разноцветный аватар\n`+glitch <user>` - глич аватара\n`+trigger <user>` - триггер у аватара\n`+qr <text>` - переработка текста в QR код\n`+rip <user>` - гроб с аватаром пользователя\n`+trash <user>` - мем с мусором\n`+photo <user>` - фото в рамке\n`+hearts <user>` - добавляет сердечки к аватару\n`+wasted <user>` - wasted как у GTA\n`+covid <country>` - статистика ковида в стране (писать по английски)\n`+twitter <text>` - твит от Трампа (только на английском)\n`+popit` - попит\n`+table <user>` - пользователь опрокидывает стол\n`+google <text>` - картинка как при поиске в гугле (только англ.)", inline=False)
            await ctx.send(embed=embed)
        if response.component.label == "Майнкрафт":
            embed=discord.Embed(title="Майнкрафт команды",color=0xff689a)
            embed.add_field(name= 'Страница 2',value='`+skin <name>` - скин игрока\n`+info <ip>` - инфо о сервере\n`+q` - очередь на сервере 2b2t\n`+prioq` - приорететная очередь на сервере 2b2t\n`+seen <player>` - последний онлайн игрока на сервере 2b2t\n`+stats <player>` - инфо об игроке на сервере 2b2t\n`+checkq` - при очереди ниже 200 бот пингует вас.',inline=False)
            await ctx.send(embed=embed)
        if response.component.label == "Модерация":
            embed=discord.Embed(title="Команды модерации",color=0xff689a)
            embed.add_field(name= 'Страница 3',value='`+kick <member>` - кикнуть пользователя\n`+ban <member>` - забанить пользователя\n`+unban <member>` - разбанить пользователя\n`+mute <member> [minutes]` - замутить пользователя\n`+unmute <member>` - размутить пользователя\n`+avatar <user>` - аватар пользователя\n`+clear <amount>` - удалить последние X сообщений в текущем канале\n`+slowmode <time>` - задержка в канале\n`+userinfo <member>` - инфо о пользователе\n**Другое**\n`+servers` - сервера на которых есть бот\n`+invite` - пригласить бота\n`+support` - сервер поддержки\n`+status` - статус бота на данный момент',inline=False)
            await ctx.send(embed=embed)
        if response.component.label == "Музыка":
            embed=discord.Embed(title="Команды музыки",color=0xff689a)
            embed.add_field(name= 'Страница 4',value='`+play <query>` - воспроизвести музыку с YouTube\n`+yt <query>` - найти видео на YouTube\n`+radio <stream>` - проигрывать радио в голосовом канале\n`+stop` - остановить воспроизведение\n`+pause` - приостановить воспроизведение\n`+resume` - продолжить воспроизведение\n`+loop` - повторение музыки',inline=False)
            await ctx.send(embed=embed)
        if response.component.label == "Экономика":
            embed=discord.Embed(title="Команды экономики",color=0xff689a)
            embed.add_field(name= 'Страница 5',value='`+daily` - ежедневные деньги\n`+bal` - баланс\n`+rob <user>` - украсть у пользователя деньги\n`+slots <amount>` - казино',inline=False)
            await ctx.send(embed=embed)
@bot.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def stonks(ctx,member:discord.Member=None):
    if ctx.message.author.bot:
        return
    if not member:
        member = ctx.message.author
    await ctx.message.delete()
    embed=discord.Embed(title="Stonks",color=0xff689a)
    embed.set_footer(text="Yrda")
    avatar = str(member.avatar_url) [:-10]+'?size=512&width=512&height=512'
    embed.set_image(url = f'https://vacefron.nl/api/stonks?user='+str(avatar))
    await ctx.send(embed=embed)
@bot.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def avatar(ctx,member:discord.Member=None):
    if ctx.message.author.bot:
        return
    if not member:
        member = ctx.message.author
    emb = discord.Embed(title=f'Аватар {member}',color=0xff689a)
    avatar = str(member.avatar_url)[:-10]+'?size=512&width=512&height=512'
    emb.set_image(url = avatar)
    await ctx.send(embed = emb)
@bot.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def gun(ctx,member:discord.Member=None):
    if ctx.message.author.bot:
        return
        await ctx.message.delete()
    if not member:
        member = ctx.message.author
    embed=discord.Embed(title="Gun",color=0xff689a)
    embed.set_footer(text="Yrda")
    avatar = str(member.avatar_url) [:-10]+'?size=512&width=512&height=512'
    embed.set_image(url = f'https://api.devs-hub.xyz/gun?image='+str(avatar))
    await ctx.send(embed=embed)
@bot.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def rainbow(ctx,member:discord.Member=None):
    if ctx.message.author.bot:
        return
        await ctx.message.delete()
    if not member:
        member = ctx.message.author
    embed=discord.Embed(title="Rainbow",color=0x28ff33)
    embed.set_footer(text="Yrda")
    avatar = str(member.avatar_url) [:-10]+'?size=512&width=512&height=512'
    embed.set_image(url = f'https://api.devs-hub.xyz/rainbow?image='+str(avatar))
    await ctx.send(embed=embed)
@bot.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def glitch(ctx,member:discord.Member=None):
    if ctx.message.author.bot:
        return
        await ctx.message.delete()
    if not member:
        member = ctx.message.author
    embed=discord.Embed(title="GliTcH",color=0xff689a)
    embed.set_footer(text="Yrda")
    avatar = str(member.avatar_url) [:-10]+'?size=512&width=512&height=512'
    embed.set_image(url = f'https://api.devs-hub.xyz/glitch?image='+str(avatar))
    await ctx.send(embed=embed)
@bot.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def trigger(ctx,member:discord.Member=None):
    if ctx.message.author.bot:
        return
        await ctx.message.delete()
    if not member:
        member = ctx.message.author
    embed=discord.Embed(title="Triggered",color=0xff689a)
    embed.set_footer(text="Yrda")
    avatar = str(member.avatar_url) [:-10]+'?size=512&width=512&height=512'
    embed.set_image(url = f'https://api.devs-hub.xyz/trigger?image='+str(avatar))
    await ctx.send(embed=embed)
@bot.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def qr(ctx,arg1, *, arg2="."):
    if ctx.message.author.bot:
        return
    embed=discord.Embed(title=arg1+" "+str(arg2),color=0xff689a)
    embed.set_footer(text="Yrda")
    embed.set_image(url = f'https://api.qrserver.com/v1/create-qr-code/?size=120x120&data='+str(arg1.replace(' ','+'))+str(arg2.replace(' ','+')))
    await ctx.send(embed=embed)
@bot.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def rip(ctx,member:discord.Member=None):
    if ctx.message.author.bot:
        return
        await ctx.message.delete()
    if not member:
        member = ctx.message.author
    embed=discord.Embed(title="Покойся с миром",color=0xff689a)
    embed.set_footer(text="Yrda")
    avatar = str(member.avatar_url) [:-10]+'?size=512&width=512&height=512'
    embed.set_image(url = f'https://vacefron.nl/api/grave?user='+str(avatar))
    await ctx.send(embed=embed)
@bot.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def trash(ctx,member:discord.Member=None):
    if ctx.message.author.bot:
        return
        await ctx.message.delete()
    if not member:
        member = ctx.message.author 
    embed=discord.Embed(title="Ты - мусор",color=0xff689a)
    embed.set_footer(text="Yrda")
    avatar = str(member.avatar_url) [:-10]+'?size=512&width=512&height=512'
    embed.set_image(url = f'https://api.cool-img-api.ml/trash?image='+str(avatar))
    await ctx.send(embed=embed)
@bot.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def sniper(ctx,member:discord.Member=None):
    if ctx.message.author.bot:
        return
        await ctx.message.delete()
    if not member:
        member = ctx.message.author
    embed=discord.Embed(title="ААЙ,меня снайпнули в полете!",color=0xff689a)
    embed.set_footer(text="Yrda")
    avatar = str(member.avatar_url) [:-10]+'?size=512&width=512&height=512'
    embed.set_image(url = f'https://api.no-api-key.com/api/v2/shoot?image='+str(avatar))
    await ctx.send(embed=embed)
@bot.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def photo(ctx,member:discord.Member=None):
    if ctx.message.author.bot:
        return
        await ctx.message.delete()
    if not member:
        member = ctx.message.author 
    embed=discord.Embed(title="Я скучаю по тебе!",color=0xff689a)
    embed.set_footer(text="Yrda")
    avatar = str(member.avatar_url) [:-10]+'?size=512&width=512&height=512'
    embed.set_image(url = f'https://vacefron.nl/api/wolverine?user='+str(avatar))
    await ctx.send(embed=embed)
@bot.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def fox(ctx):
    r = randint(1, 100)
    embed=discord.Embed(title="Juniper Bot оценит",color=0xff689a)
    embed.set_footer(text="Yrda")
    embed.set_image(url = 'http://randomfox.ca/images/'+str(r)+'.jpg')
    await ctx.send(embed=embed)
@bot.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def wasted(ctx,member:discord.Member=None):
    if ctx.message.author.bot:
        return
        await ctx.message.delete()
    if not member:
        member = ctx.message.author
    embed=discord.Embed(title="Потрачено",color=0xff689a)
    embed.set_footer(text="Yrda")
    avatar = str(member.avatar_url) [:-10]+'?size=512&width=512&height=512'
    embed.set_image(url = f'https://some-random-api.ml/canvas/wasted?avatar='+str(avatar))
    await ctx.send(embed=embed)
@bot.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def hearts(ctx,member:discord.Member=None):
    if ctx.message.author.bot:
        return
        await ctx.message.delete()
    if not member:
        member = ctx.message.author
    embed=discord.Embed(title="Сердечки:)",color=0xff689a)
    embed.set_footer(text="Yrda")
    avatar = str(member.avatar_url) [:-10]+'?size=512&width=512&height=512'
    embed.set_image(url = f'https://api.devs-hub.xyz/hearts?image='+str(avatar))
    await ctx.send(embed=embed)
@bot.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def covid(ctx, r):
    embed=discord.Embed(title="Статистика Covid-19 в "+str(r),color=0xff689a)
    embed.set_footer(text="Flip Team bot")
    embed.set_image(url = f'https://covid-img.herokuapp.com/country/'+str(r))
    await ctx.send(embed=embed)
@bot.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def twitter(ctx,arg1, *, arg2="."):
    emb = discord.Embed(title='Новый твит от Трампа',color=0xff689a)
    emb.set_image(url = "https://api.no-api-key.com/api/v2/trump?message="+str(arg1.replace(' ','+'))+"+"+str(arg2.replace(' ','+')))
    await ctx.send(embed = emb)
@bot.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def invite(ctx):
    if ctx.message.author.bot:
        return
    emb = discord.Embed(title='Пригласить бота',description='[-клик-](https://discordapp.com/oauth2/authorize?client_id=800295255916150816&scope=bot&permissions=2146958847)')
    await ctx.send(embed = emb)
@bot.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def support(ctx):
    if ctx.message.author.bot:
        return
    emb = discord.Embed(title='Поддержка',description='[-клик-](https://discord.gg/flip-team)')
    await ctx.send(embed = emb)
@bot.command()
@commands.cooldown(1, 20,commands.BucketType.user)
async def popit(ctx):
    embed=discord.Embed(title="Pop it или simple dimple?",color=0xff689a)
    embed.add_field(name = '~~-------------------------------------------~~',value = '| ||:white_large_square:||||:red_square:||||:orange_square:||||:yellow_square:||||:green_square:||||:blue_square:||||:purple_square:||||:white_large_square:|| |',inline=False)
    embed.add_field(name = '~~-------------------------------------------~~',value = '| ||:white_large_square:||||:red_square:||||:orange_square:||||:yellow_square:||||:green_square:||||:blue_square:||||:purple_square:||||:white_large_square:|| |',inline=False)
    embed.add_field(name = '~~-------------------------------------------~~',value = '| ||:white_large_square:||||:red_square:||||:orange_square:||||:yellow_square:||||:green_square:||||:blue_square:||||:purple_square:||||:white_large_square:|| |',inline=False)
    embed.add_field(name = '~~-------------------------------------------~~',value = '| ||:white_large_square:||||:red_square:||||:orange_square:||||:yellow_square:||||:green_square:||||:blue_square:||||:purple_square:||||:white_large_square:|| |',inline=False)
    embed.add_field(name = '~~-------------------------------------------~~',value = '| ||:white_large_square:||||:red_square:||||:orange_square:||||:yellow_square:||||:green_square:||||:blue_square:||||:purple_square:||||:white_large_square:|| |',inline=False)
    embed.add_field(name = '~~-------------------------------------------~~',value = '| ||:white_large_square:||||:red_square:||||:orange_square:||||:yellow_square:||||:green_square:||||:blue_square:||||:purple_square:||||:white_large_square:|| |',inline=False)
    embed.set_footer(text="Yrda")
    await ctx.send(embed=embed)
@bot.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def table(ctx,member:discord.Member=None):
    if ctx.message.author.bot:
        return
        await ctx.message.delete()
    if not member:
        member = ctx.message.author
    embed=discord.Embed(title="Пользователь опрокинул стул",color=0xff689a)
    embed.set_footer(text="Yrda")
    avatar = str(member.avatar_url) [:-10]+'?size=512&width=512&height=512'
    embed.set_image(url = f'https://vacefron.nl/api/tableflip?user='+str(avatar))
    await ctx.send(embed=embed)
@bot.command()
@commands.cooldown(1, 30, commands.BucketType.user)
async def skin(ctx, nick):
    if await is_overloaded(ctx):
        return
    url = f"https://ru.namemc.com/profile/{nick}.1"
    async with ctx.typing():
        guild = discord.utils.get(bot.guilds, id = 851082001950965816)
        channel = discord.utils.get(guild.channels, name = "log")
        await channel.send(url, delete_after = 5)
        await asyncio.sleep(1)
        message = await channel.send(url, delete_after = 5)
    if "Поиск" in message.embeds[0].title:
        emb = discord.Embed(description = ':x: Лицензионного аккаунта с таким ником нет.',color=0xff689a)
        await ctx.send(embed = emb, delete_after = 2)
        return
    skin = message.embeds[0].thumbnail.url
    name = message.embeds[0].title.split(' | Учётная запись Minecraft')[0]
    emb = discord.Embed(title = f"Скин {name}",color=0xff689a)
    skin = skin.split("&width=")[0] + "&width=600&height=300&scale=4&overlay=true&theta=30&phi=20&time=90&shadow_color=000&shadow_radius=0&shadow_x=0&shadow_y=0&front_and_back=true"
    emb.set_image(url = skin)
    await ctx.send(embed = emb)
@bot.command()
@commands.cooldown(1, 15,commands.BucketType.user)
async def userinfo(ctx, Target:discord.Member=None):
    if Target is None:
        Target = ctx.author
    embed=discord.Embed(title=f"Инфо о {Target}",color=0xff689a)
    embed.add_field(name =f"Название аккаунта", value=f"{Target.name}",inline=False)
    embed.add_field(name =f"Тэг", value=f"{Target.discriminator}",inline=False)
    embed.add_field(name =f"ID", value=f"{Target.id}",inline=False)
    embed.add_field(name =f"Главная роль", value=f"{Target.top_role}",inline=False)
    embed.add_field(name =f"Время создание аккаунта", value=Target.created_at.strftime("%d/%m/%Y %H:%M:%S"),inline=False)
    embed.add_field(name =f"Время захода на сервер", value=Target.joined_at.strftime("%d/%m/%Y %H:%M:%S"),inline=False)
    embed.add_field(name ="Статус",value=str(Target.status).title(),inline=False)
    embed.add_field(name="Текущая активность",value=f"{str(Target.activity.type).title().split('.')[1]} {Target.activity.name}" if Target.activity is not None else "Нету",inline=False)
    await ctx.send(embed=embed)
@bot.command()
async def status(ctx):
    CPU = psutil.cpu_percent()
    mem = psutil.virtual_memory().percent
    global nullTime # ето в самой команде
    t = int(time.time() - nullTime) 
    t = datetime.timedelta(seconds=t)
    embed = discord.Embed(title='Статистика бота (ядро 1)',color=0xff689a)
    embed.add_field(name='Аптайм',value=t,inline=False)
    embed.add_field(name='ЦП',value=f'{CPU}%' ,inline=False)
    embed.add_field(name='ОЗУ',value=f'{mem}%',inline=False)
    await ctx.send(embed=embed)
#----------------------
bot.run(token, bot = True)
