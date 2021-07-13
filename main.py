import discord, asyncpg
from discord.ext import tasks, commands
from bs4 import BeautifulSoup, BeautifulStoneSoup
import requests

channel_id = '<@180804112567369728>'
client = discord.Client()
bot_token = 'ODY0MTg1MTcyNzkwMjE0Njk2.YOxxKA.BqqPjCQXf607yV2nXVOZlWfGSUE'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
ticker = ['GME', 'BB', 'AMC']


@client.event
async def on_ready():
    print('Bot Ready.')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!view'):
        await message.channel.send(view())

    elif message.content.startswith('!add'):
        stockTicker[1] = message.content.split(' ', 1)
        ticker.append(stockTicker.toUpperCase())
        await message.channel.send("Added $%s" % stockTicker)

    elif message.content.startswith('!remove'):
        stockTicker[1] = message.content.split(' ', 1)
        ticker.remove(stockTicker.toUpperCase())
        await message.channel.send("Removed $%s" % stockTicker)
    
def view():
    stockPriceOutput  = ""
    for i in range(0, len(ticker)):
        url = 'https://finance.yahoo.com/quote/%s' % ticker[i]
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        stockData = soup.find('div', {'class': 'D(ib) Mend(20px)'}).find_all('span')
        currPrice = stockData[0].text.strip()
        changeInPrice = stockData[1].text.strip()
        percent = changeInPrice.split('(', 1)[1].split(')')[0]
        percent = percent.strip('%-+')
        percent = float(percent)
        stockPriceOutput += "%s:\n    Current Price: %s \n    Change in Price: %s \n\n" % (ticker[i], currPrice, changeInPrice)
    return stockPriceOutput


client.run(bot_token)
