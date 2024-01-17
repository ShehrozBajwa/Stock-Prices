# Stock Market Alerts

What it does:

A discord bot that uses web scraping to get data from yahoo finance and then sends daily price alerts at the closing bell.

Commands:

- !view
  - view all stocks 
- !add stockName
  - add the stock with ticker stockName
- !remove stockName
  - remove the stock with ticker stockName 
- !clear
  - clear all stocks 
- !help
  - lists all the commands
  

Technologies and Platforms Used:

- Heroku for hosting the bot 
- Amazon AWS for storing the database (DynamoDB)
- BeautifulSoup for parsing HTML and XML files
- Requests to send requests to the HTML server
- Discord API to get user commands and send messages
