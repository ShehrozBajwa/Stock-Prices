from datetime import date, datetime, sys
import boto3
import discord
import json
import os
import requests
from bs4 import BeautifulSoup
from discord.ext import tasks
from dotenv import load_dotenv

load_dotenv()
channel_id = 864963943164149811
client = discord.Client()
bot_token = os.getenv('BOT_TOKEN')
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
ticker = []


@client.event
async def on_ready():
    print('Bot Ready.')
    importAWS = import_stocks()
    for i in importAWS:
        ticker.append(list(i.values())[0])
    write_file(ticker)
    if not dailyNotification.is_running():
        dailyNotification.start()

        

@tasks.loop(minutes=1)
async def dailyNotification():
    today = date.today()
    time = datetime.now()
    current_time = time.strftime("%H:%M")
    if today.weekday() <= 4 and current_time == '21:00':
        channel = client.get_channel(channel_id)
        await channel.send(view(ticker))
    if current_time == '05:00':
        write_file(ticker)
        export_stocks()
        sys.exit()
        


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!view'):
        await message.channel.send(view(ticker))

    elif message.content.startswith('!add'):
        messageSplit = message.content.split(' ', 1)
        ticker.append(messageSplit[1].upper())
        if not duplicates(ticker):
            try:
                url = 'https://finance.yahoo.com/quote/%s' % messageSplit[1].upper()
                r = requests.get(url, headers=headers)
                soup = BeautifulSoup(r.text, 'html.parser')
                stockName = soup.find('div', {
                    'class': 'D(ib) Mt(-5px) Maw(38%)--tab768 Maw(38%) Mend(10px) Ov(h) smartphone_Maw(85%) smartphone_Mend(0px)'}).find(
                    'h1').text
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
            stockName = soup.find('div', {
                'class': 'D(ib) Mt(-5px) Mend(20px) Maw(56%)--tab768 Maw(52%) Ov(h) smartphone_Maw(85%) smartphone_Mend(0px)'}).find(
                'h1').text
            await message.channel.send("Removed %s." % stockName)
        except:
            await message.channel.send("Couldn't Find That Stock.")

    elif message.content.startswith('!help'):
        messageSplit = message.content.split(' ', 1)
        await message.channel.send(
            "Commands:\n\n!view - View All Stocks.\n!add - Add a Stock\n!remove - Remove a Stock\n!clear - Remove All Stocks")


def view(ticker):
    if len(ticker) != 0:
        stockPriceOutput = ""
        ticker = list(set(ticker))
        for i in range(0, len(ticker)):
            url = 'https://finance.yahoo.com/quote/%s' % ticker[i]
            r = requests.get(url, headers=headers)
            soup = BeautifulSoup(r.text, 'html.parser')
            stockData = soup.find('div', {'class': 'D(ib) Mend(20px)'}).find_all()
            currPrice = stockData[0].text.strip()
            changeInPrice = stockData[1].text.strip()
            percent = stockData[3].text.strip()
            stockName = soup.find('div', {
                'class': 'D(ib) Mt(-5px) Mend(20px) Maw(56%)--tab768 Maw(52%) Ov(h) smartphone_Maw(85%) smartphone_Mend(0px)'}).find(
                'h1').text
            stockPriceOutput += "%s:\n        Current Price: %s \n        Change in Price: %s %s \n\n" % (
                stockName, currPrice, changeInPrice, percent)
        return stockPriceOutput
    else:
        return "List is Empty."


def duplicates(ticker):
    check = list(set(ticker))
    if len(check) == len(ticker):
        return False
    else:
        return True


def write_file(ticker):
    with open("data.json", 'w') as file:
        json.dump(ticker, file)
        file.close()


def read_file():
    with open("data.json") as file:
        ticker = json.load(file)
        file.close()
        return ticker


def import_stocks():
    dynamodb = boto3.resource('dynamodb', aws_access_key_id= os.getenv('ACCESS_ID'),
         aws_secret_access_key= os.getenv('ACCESS_KEY'), region_name='us-east-2')
    try:
        table = dynamodb.Table("Stocks")
        data = table.scan()
        return data['Items']
    except dynamodb.meta.client.exceptions.ResourceNotFoundException:
        pass


def export_stocks():
    dynamodb = boto3.resource('dynamodb', aws_access_key_id= os.getenv('ACCESS_ID'),
         aws_secret_access_key= os.getenv('ACCESS_KEY'), region_name='us-east-2')
    table = dynamodb.Table("Stocks")
    try:
        table.delete()
        table.wait_until_not_exists()
    except dynamodb.meta.client.exceptions.ResourceNotFoundException:
        pass
    ticker = read_file()
    table = dynamodb.create_table(
        TableName='Stocks',
        KeySchema=[{
            'AttributeName': 'stockName',
            'KeyType': 'HASH'
        }],
        AttributeDefinitions=[{
            'AttributeName': 'stockName',
            'AttributeType': 'S'
        }],
        ProvisionedThroughput={
            'ReadCapacityUnits': len(ticker) + 1,
            'WriteCapacityUnits': len(ticker) + 1
        })
    table.wait_until_exists()
    for i in range(0, len(ticker)):
        table.put_item(Item={
            'stockName': ticker[i]
        })


client.run(bot_token)
