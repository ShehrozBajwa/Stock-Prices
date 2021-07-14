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
        list(set(ticker))
        await message.channel.send(view())

    elif message.content.startswith('!add'):
        messageSplit = message.content.split(' ', 1)
        ticker.append(messageSplit[1].upper())
        list(set(ticker))
        stockName = soup.find('div', {'class': 'D(ib) Mt(-5px) Mend(20px) Maw(56%)--tab768 Maw(52%) Ov(h) smartphone_Maw(85%) smartphone_Mend(0px)'}).find('h1').text
        await message.channel.send("Added %s" % stockName)

    elif message.content.startswith('!remove allStocks'):
        messageSplit = message.content.split(' ', 1)
        ticker.clear() 
        await message.channel.send("Removed All Stocks.")
        
    elif message.content.startswith('!remove'):
        messageSplit = message.content.split(' ', 1)
        ticker.remove(messageSplit[1].upper())
        list(set(ticker))
        stockName = soup.find('div', {'class': 'D(ib) Mt(-5px) Mend(20px) Maw(56%)--tab768 Maw(52%) Ov(h) smartphone_Maw(85%) smartphone_Mend(0px)'}).find('h1').text
        await message.channel.send("Removed %s" % stockName)
        
        
    elif message.content.startswith('!help'):
        messageSplit = message.content.split(' ', 1)
        await message.channel.send("Commands:\n!view - View All Stocks.\n!add - Add a Stock\n!remove - Remove a Stock\n!remove allStocks - Remove All Stocks")
    
    
def view():
    stockPriceOutput  = ""
    for i in range(0, len(ticker)):
        url = 'https://finance.yahoo.com/quote/%s' % ticker[i]
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        stockData = soup.find('div', {'class': 'D(ib) Mend(20px)'}).find_all('span')
        currPrice = stockData[0].text.strip()
        changeInPrice = stockData[1].text.strip()
        stockName = soup.find('div', {'class': 'D(ib) Mt(-5px) Mend(20px) Maw(56%)--tab768 Maw(52%) Ov(h) smartphone_Maw(85%) smartphone_Mend(0px)'}).find('h1').text
        percent = changeInPrice.split('(', 1)[1].split(')')[0]
        percent = percent.strip('%-+')
        percent = float(percent)
        stockPriceOutput += "%s:\n      Current Price: %s \n        Change in Price: %s \n\n" % (stockName, currPrice, changeInPrice)
    return stockPriceOutput


client.run(bot_token)
