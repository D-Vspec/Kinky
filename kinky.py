import discord
from discord.ext import commands
from discord import emoji
from discord.utils import get
from bs4 import BeautifulSoup
import random
import requests
import praw
import json

prefix = '+'
client = commands.Bot(command_prefix=prefix)
client.remove_command('help')

reddit = praw.Reddit(client_id='4hcWd6NR85u7Eg',
                     client_secret='-1Hv7cbajBw407obpyAnIYZ5-P0',
                     username='ARandomGuy_On_Reddit',
                     password='d1623WimpyKid',
                     user_agent='DiscordBotLmao',)

memecounter = 1
memelist = []

subreddit = reddit.subreddit('dankmemes')
memes_hot = subreddit.hot()
for submission in memes_hot:
    if not submission.stickied:
        print(submission.thumbnail)
        memelist.append(submission.url)

pastacounter = 1
pastalist = []

subreddit = reddit.subreddit('copypasta')
pasta_hot = subreddit.hot()
for submission in pasta_hot:
    if not submission.stickied:
        print(submission.selftext)
        pastalist.append(submission.selftext)

counter = 1
list = []

subreddit = reddit.subreddit('hentai')
post_hot = subreddit.hot()
for submission in post_hot:
    if not submission.stickied:
        list.append(submission.url)

@client.event
async def on_message(message):

    if message.author == ('@MEE6#4876'):
        message.channel.send("Die MEE6, you inferior piece of crap")

    if 'fuck' in message.content:
        await message.channel.send('no u')

    if '69' in message.content:
        await message.channel.send('Nice')

    if '420' in message.content:
        await message.channel.send('Nice')

    if message.author.bot == False:
        with open('users.json', 'r') as f:
            users = json.load(f)

        await update_data(users, message.author)
        await add_experience(users, message.author, 5)
        await level_up(users, message.author, message)

        with open('users.json', 'w') as f:
            json.dump(users, f)

    await client.process_commands(message)

async def update_data(users, user):
    if not f'{user.id}' in users:
        users[f'{user.id}'] = {}
        users[f'{user.id}']['experience'] = 0
        users[f'{user.id}']['level'] = 1


async def add_experience(users, user, exp):
    users[f'{user.id}']['experience'] += exp


async def level_up(users, user, message):
    with open('levels.json', 'r') as g:
        levels = json.load(g)
    experience = users[f'{user.id}']['experience']
    lvl_start = users[f'{user.id}']['level']
    lvl_end = int(experience ** (1 / 4))
    if lvl_start < lvl_end:
        await message.channel.send(f'{user.mention} has leveled up to level {lvl_end}')
        users[f'{user.id}']['level'] = lvl_end

@client.command()
async def level(ctx, member: discord.Member = None):
    if not member:
        id = ctx.message.author.id
        with open('users.json', 'r') as f:
            users = json.load(f)
        lvl = users[str(id)]['level']
        await ctx.send(f'You are at level {lvl}!')
    else:
        id = member.id
        with open('users.json', 'r') as f:
            users = json.load(f)
        lvl = users[str(id)]['level']
        await ctx.send(f'{member} is at level {lvl}!')

@client.command()
async def ping(ctx):
    await ctx.send('Pong! {0}'.format(round(client.latency, 1)))


@client.command(aliases = ['CoronaCases'])
async def corona(ctx):
    response = requests.get('https://www.worldometers.info/coronavirus/')
    soup = BeautifulSoup(response.text, 'html.parser')

    number = []

    for numbers in soup.find_all('span'):
        # print(numbers.text)
        number.append(numbers.text)

    TestEmbed=discord.Embed(title='Corona Cases')
    TestEmbed.add_field(name='Number of Cases', value=str(number[4]))
    TestEmbed.add_field(name='Number of Deaths', value=str(number[5]), inline=False)
    TestEmbed.add_field(name='Number of Recoveries', value=str(number[6]))
    TestEmbed.add_field(name='Number of Mild Cases', value=str(number[8]), inline=False)
    TestEmbed.add_field(name='Number of Critical Cases', value=str(number[9]))

    await ctx.send(embed=TestEmbed)

@client.command(aliases = ['HealthNews'])
async def _news(ctx):
    response = requests.get('https://www.who.int/news-room/releases')
    soup = BeautifulSoup(response.text, 'html.parser')

    number = []

    for numbers in soup.find_all('a'):
        #print(numbers.text)
        number.append(numbers.get('aria-label'))

    TestEmbed=discord.Embed(title='Corona Cases')
    TestEmbed.add_field(name='News#1', value=str(number[184]))
    TestEmbed.add_field(name='News#2', value=str(number[185]), inline=False)
    TestEmbed.add_field(name='News#3', value=str(number[186]))
    TestEmbed.add_field(name='News#4', value=str(number[187]), inline=False)
    TestEmbed.add_field(name='News#5', value=str(number[188]))

    await ctx.send(embed=TestEmbed)

@client.command(pass_context = True)
async def help(ctx):
    DiscordEmbed = discord.Embed(title = 'HELP', color = discord.Color.dark_gold())
    DiscordEmbed.add_field(name='Basic', value='+ping - tests if bot is active and gives ping\n+help - opens this menu\n+level - shows your level')
    DiscordEmbed.add_field(name='Current topics related', value='+CoronaCases - gives current number of global corona cases\n+HealthNews - shows latest health news')
    DiscordEmbed.add_field(name='Cute pics', value='+foxes - gives pictures of foxes\n+doggos - gives pictures of good bois', inline=False)
    DiscordEmbed.add_field(name='Reddit Shit', value='+meme - gives you meme\n+copypasta - sends a copypasta\n')
    await ctx.send(embed=DiscordEmbed)

@client.command(pass_context = True, aliases = ['foxes'])
async def fox(ctx):
    response = requests.get('https://randomfox.ca/floof')
    fox = response.json()
    print(fox)
    await ctx.send(fox['image'])

@client.command(pass_context = True, aliases = ['doggos'])
async def doggo(ctx):
    response = requests.get('https://dog.ceo/api/breeds/image/random')
    dog = response.json()
    print(dog)
    await ctx.send(dog['message'])

@client.command(pass_context = True, aliases = ['meme'])
async def _meme(ctx):

    global memecounter

    memepic = memelist[memecounter]
    memecounter = memecounter + 1
    await ctx.send(memepic)

@client.command(pass_context = True, aliases = ['unspeakable'])
async def _unspeakablething(ctx):

    global counter

    pic = list[counter]
    counter = counter + 1
    await ctx.author.send(pic)


@client.command(pass_context = True, aliases = ['copypasta'])
async def _pasta(ctx):

    global pastacounter

    pasta = pastalist[pastacounter]
    pastacounter = pastacounter + 1
    await ctx.send(pasta)

@client.command(pass_context = True, aliases=['TextChannel'])
async def _newtextchannel(ctx, *, name):
    guild = ctx.message.guild
    await guild.create_text_channel(name)

@client.command(pass_context = True, aliases=['VoiceChannel'])
async def _newvoicechannel(ctx, *, name):
    guild = ctx.message.guild
    await guild.create_voice_channel(name)

@client.command(pass_context = True, aliases=['DeleteChannel'])
async def _deletechannel(ctx, *, name):
    guild = ctx.message.guild
    await guild.delete_voice_channel(name)

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game('with your sister'))
    print('Ready')

client.run(TOKEN)

