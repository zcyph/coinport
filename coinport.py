import sys, time, locale, json
from os import system, name, path
from pycoingecko import CoinGeckoAPI
import pandas as pd
from sty import fg, bg, ef, rs, Style, RgbFg

################################################# configuration #
coin_list = 'coinlist.json'
coinport_config = 'conf.json'
with open(coinport_config) as config_file:
    coinport_config_data = json.load(config_file)
    spreadsheet = coinport_config_data['spreadsheet']['filepath']
cg = CoinGeckoAPI()
def clear():
    if name == 'nt':
        _ = system('cls')
        system('color')
    else:
        _ = system('clear')
locale.setlocale(locale.LC_ALL, '')
fg.orange = Style(RgbFg(255, 150, 50))
# configuration #################################################


# keep program running, prompt user for spreadsheet filepath if not found
while True:
    if path.isfile(spreadsheet):
        while True:
                # get list of coins from CoinGecko
                allcoins = cg.get_coins_list()

                # spreadsheet -> Pandas df (dataframe)
                df = pd.ExcelFile(spreadsheet).parse(pd.ExcelFile(spreadsheet).sheet_names[0])

                # portfolio coins to track
                coins_to_track = df.columns[2:].tolist()

                # if not already there, download & save complete list of coins from CoinGecko
                if not path.isfile(coin_list):
                    with open('coinlist.json', 'w') as coinlist_file:
                        json.dump(allcoins, coinlist_file, sort_keys=True, indent=4, separators=(',', ': '))

                # functions to look up CoinGecko ID or ticker symbol with coin name
                def name_to_id(coin_name):
                    try:
                        return next(i['id'] for i in allcoins if i["name"] == coin_name)
                    except:
                        print(f"Woops, {coin_name} doesn't seem to be there, please check spelling and case sensitivity")

                def name_to_symbol(coin_name):
                    try:
                        return next(i['symbol'] for i in allcoins if i["name"] == coin_name)
                    except:
                        print(f"Woops, {coin_name} doesn't seem to be there, please check spelling and case sensitivity")

                # set coin ID, symbols and prices
                coin_ids = []
                for coin in coins_to_track:
                    coin_id = name_to_id(coin)
                    coin_ids.append(coin_id)
                symbols = {}
                for coin in coins_to_track:
                    coin_id = name_to_id(coin)
                    symbol = name_to_symbol(coin)
                    symbols.update({symbol.upper():coin_id})
                prices = {}
                for coin in coins_to_track:
                    coin_id = name_to_id(coin)
                    symbol = name_to_symbol(coin)
                    prices.update({symbol.upper():cg.get_price(ids=coin_id, vs_currencies='cad')[coin_id]['cad']})

                # get holdings and book value from spreadsheet
                holdings = dict(zip(symbols.keys(),df.iloc[0:,2:].sum().to_list()))
                total_book_value = df.iloc[0:,1].sum()

                # current cryptocurrencies held, and total dollar amount
                holdings_market_value = {k:(holdings[k] * prices[k]) for k in holdings}
                total_market_value = sum(holdings_market_value.values())

                # display portfolio book/market value and profit/loss in dollars
                clear()
                print(ef.bold + fg.yellow + "P/L: " + fg.rs + rs.bold_dim + locale.currency(total_market_value - total_book_value) + " (" + ef.bold + fg(10, 255, 10) + f"{(total_market_value - total_book_value)/total_book_value:.2%}" + fg.rs + rs.bold_dim + ")" + ef.bold + fg.yellow + "\nBOOK: " + fg.rs + rs.bold_dim + locale.currency(total_book_value) + ef.bold + fg.yellow + "\nMARKET: " + fg.rs + rs.bold_dim + locale.currency(total_market_value) + "\n")
                print(ef.bold + fg.yellow + "Symbol   Price       Balance              Value" + fg.rs + rs.bold_dim)
                print(ef.bold + fg.orange + "---------------------------------------------------" + fg.rs + rs.bold_dim)

                # display individual holdings in cryptocurrency and dollars
                for i in symbols:
                    spaces = (6 - len(i)) * ' '
                    spaces2 = (10 - len(str(locale.currency(prices[i])))) * ' '
                    spaces3 = (20 - len(str(holdings[i]))) * ' '
                    print(ef.bold + fg.yellow + f"{i}:" + fg.rs + rs.bold_dim  + f"{spaces}  {locale.currency(prices[i])} {spaces2}" + fg.grey + f" {holdings[i]}" + fg.rs + f"{spaces3} " + fg.green + locale.currency(holdings_market_value[i]) + fg.rs)
                time.sleep(5)

    # prompt user for valid file until one is provided, then add it to config
    else:
        while not path.isfile(spreadsheet):
            coinport_config_data['spreadsheet']['filepath'] = input("Woops, no spreadsheet found! Please specify filename: ")
            spreadsheet = coinport_config_data['spreadsheet']['filepath']
        with open(coinport_config, 'w') as config_file:
            json.dump(coinport_config_data, config_file, sort_keys=True, indent=4, separators=(',', ': '))
