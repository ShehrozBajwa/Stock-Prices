import discord, asyncpg
from discord.ext import tasks, commands
from bs4 import BeautifulSoup, BeautifulStoneSoup
import requests


channel_id = 864579823301427221
client = discord.Client()
bot_token = 'ODY0MTg1MTcyNzkwMjE0Njk2.YOxxKA.BqqPjCQXf607yV2nXVOZlWfGSUE'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
ticker = ['GME', 'BB', 'AMC']

@client.event
async def on_ready():
    print('Bot Ready.')
    dailyNotification.start()

  
@tasks.loop(seconds = 5)
async def dailyNotification():
    channel = client.get_channel(channel_id)
    await channel.send(view(ticker)) 
    
    
@client.event
async def on_message(message):
    duplicates(ticker)
    
    if message.author == client.user:
        return

    if message.content.startswith('!view'):
        await message.channel.send(view(ticker))

    elif message.content.startswith('!add'):
        messageSplit = message.content.split(' ', 1)
        print(message.channel)
        ticker.append(messageSplit[1].upper())
        if duplicates(ticker) == False: 
            try:
                url = 'https://finance.yahoo.com/quote/%s' % messageSplit[1].upper()
                r = requests.get(url, headers=headers)
                soup = BeautifulSoup(r.text, 'html.parser')
                stockName = soup.find('div', {'class': 'D(ib) Mt(-5px) Mend(20px) Maw(56%)--tab768 Maw(52%) Ov(h) smartphone_Maw(85%) smartphone_Mend(0px)'}).find('h1').text
                await message.channel.send("Added %s." % stockName)
            except:
                ticker.remove(messageSplit[1].upper())
                await message.channel.send("Couldn't Find that Stock.")
        else:
            ticker.remove(messageSplit[1].upper())
            await message.channel.send("That Stock is Already Added.")
            
          
    elif message.content.startswith('!clear'):
        messageSplit = message.content.split(' ', 1)
        ticker.clear() 
        await message.channel.send("Removed All Stocks.")
        
    elif message.content.startswith('!remove'):
        messageSplit = message.content.split(' ', 1)
        try:
            ticker.remove(messageSplit[1].upper())
            url = 'https://finance.yahoo.com/quote/%s' % messageSplit[1].upper()
            r = requests.get(url, headers=headers)
            soup = BeautifulSoup(r.text, 'html.parser')
            stockName = soup.find('div', {'class': 'D(ib) Mt(-5px) Mend(20px) Maw(56%)--tab768 Maw(52%) Ov(h) smartphone_Maw(85%) smartphone_Mend(0px)'}).find('h1').text
            await message.channel.send("Removed %s." % stockName)
        except:
            await message.channel.send("Couldn't Find That Stock.")
        
    elif message.content.startswith('!help'):
        messageSplit = message.content.split(' ', 1)
        await message.channel.send("Commands:\n\n!view - View All Stocks.\n!add - Add a Stock\n!remove - Remove a Stock\n!clear - Remove All Stocks")
    
    
def view(ticker):
    stockPriceOutput  = ""
    ticker = list(set(ticker))
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
        stockPriceOutput += "%s:\n        Current Price: %s \n        Change in Price: %s \n\n" % (stockName, currPrice, changeInPrice)
    return stockPriceOutput


def duplicates(ticker):
    check = list(set(ticker))
    if len(check) == len(ticker):
        return False
    else:
        ticker = list(set(ticker))
        return True
        
    
                

    

client.run(bot_token)
