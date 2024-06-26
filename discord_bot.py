import discord
from discord.ext import commands, tasks
import requests
intents = discord.Intents.default()
intents.members = True  # To get member count
bot = commands.Bot(command_prefix='!', intents=intents)


url = "https://gmgn.ai/defi/quotation/v1/tokens/sol/3B5wuUrMEi5yATD7on46hKfej3pfmd7t1RKgrsN3pump"
response = requests.get(url)
data = response.json()
def format_value(value):
    if value >= 1e9:
        return f"{value / 1e9:.2f}B"
    elif value >= 1e6:
        return f"{value / 1e6:.2f}M"
    elif value >= 1e3:
        return f"{value / 1e3:.2f}K"
    else:
        return f"{value:.2f}"

gmgn_data = data["data"]["token"]
mc = format_value(gmgn_data['fdv'])
holder_count = gmgn_data['holder_count']




CHANNEL_ID = 1255632614136479867 #members

channel_2 = 1255633417798811792 #marketcap

channel_3= 1255633048427565195 #holders

GUILD_ID = 1255497284628648077

@bot.event
async def on_ready():
    print(f'Bot is ready. Logged in as {bot.user}')
    update_member_count.start()  

@tasks.loop(minutes=5)  
async def update_member_count():
    guild = bot.get_guild(GUILD_ID)
    if guild:
        channel = guild.get_channel(CHANNEL_ID)
        if channel:
            member_count = guild.member_count
            await channel.edit(name=f'Members: {member_count}')
            print(f'Updated channel name to "Members: {member_count}"')
        else:
            print(f'Channel with ID {CHANNEL_ID} not found.')
        channel2 = guild.get_channel(channel_2)
        if channel2:
            
            await channel2.edit(name=f'MarketCap: {mc}')
            print(f'Updated channel name to "Marketcap: {mc}"')
        else:
            print(f'Channel with ID {channel_2} not found.')
        channel3 = guild.get_channel(channel_3)
        if channel3:
            
            await channel3.edit(name=f'Holders: {holder_count}')
            print(f'Updated channel name to "Holders: {holder_count}"')
        else:
            print(f'Channel with ID {channel_2} not found.')
    else:
        print(f'Guild with ID {GUILD_ID} not found.')
