from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler,filters, ContextTypes,MessageHandler
# import Schedule
import time
# import alpaca_trade_api as tradeapi
import yfinance as yf
import pandas as pd
import pycoingecko
from pycoingecko import CoinGeckoAPI


google_ticker = ["BTC-USD", "DOGE-USD", "ETH-USD"]
live_crypto_list=["bitcoin"]
Token: Final='#apikey'
Bot_username: Final = '#@botname'
def get_live_stock_data(ticker_symbols):
    results = []
    for stocks in ticker_symbols:
        stock_data = yf.Ticker(stocks)
        live_data = stock_data.info
        market_day_high = live_data.get("dayHigh", "N/A")
        market_day_low = live_data.get("dayLow", "N/A")
        results.extend([
            f"Stock: {stocks}\n",
            f"Market High: {market_day_high}\n",
            f"Market Low: {market_day_low}\n",
            "-----------------------\n"
        ])
    return '\n'.join(''.join(result) for result in results)



def get_crypto_data(crypto_symbol):
    cg = CoinGeckoAPI()
    result_live=[]
    for items in crypto_symbol:
         crypto_data = cg.get_price(ids=items, vs_currencies='usd')

    result_live.extend([
            f"Stock:{items}\n",
            f"Live price: {crypto_data}\n",
            "-----------------------\n"
        ])
    return '\n'.join(''.join(result) for result in result_live)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("hello !!")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("created by KK")

async def Custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("KK in custom")

async def Get_data_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    stock_data=get_live_stock_data(google_ticker)
    await update.message.reply_text(stock_data)

async def get_live_data_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    live_data=get_crypto_data(live_crypto_list) 
    await update.message.reply_text(live_data)







def handle_response(text: str)-> str:
    if 'hello' in text:
        return 'hi how are you'
    if 'bye' in text:
        return 'bye'


    
    return 'i dont understand...'

async def handle_message(update: Update,context:ContextTypes.DEFAULT_TYPE):
    message_type:str=update.message.chat.type
    text: str=update.message.text

    print(f'user({update.message.chat.id}) in {message_type}: "{text}"')

    if message_type=='group':
        if Bot_username in text:
            new_text:str=text.replace(Bot_username, '').strip()
            response:str=handle_response(new_text)
        else:
            return
    else:
        response:str=handle_response(text)

    print('Bot:',response)
    await update.message.reply_text(response)

async def error(update: Update,context:ContextTypes.DEFAULT_TYPE):
    print(f'Update{update} caused error {context.error}')


if __name__ == '__main__':
    print('starting bot')
    app=Application.builder().token(Token).build()

    app.add_handler(CommandHandler('start',start_command))
    app.add_handler(CommandHandler('help',help_command))
    app.add_handler(CommandHandler('Custom',Custom_command))
    app.add_handler(CommandHandler('get',Get_data_command))
    app.add_handler(CommandHandler('cur',get_live_data_command))
    #app.add_handler(CommandHandler('Add_stock_in_list',Add_stock_in_list))

    app.add_handler(MessageHandler(filters.TEXT,handle_message))

    

    app.add_error_handler(error)

    print('polling....')
    
    app.run_polling(poll_interval=3) 
