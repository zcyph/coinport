import locale, time, json
import pandas as pd
from pycoingecko import CoinGeckoAPI
from os import system, name, path
from termcolor import colored

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
    else:
        _ = system('clear')
# configuration #################################################

# keep program running, prompt user for spreadsheet filepath if not found
while True:
    if path.isfile(spreadsheet):
        while True:
                # clear screen, setlocale to format currency
                clear()
                locale.setlocale(locale.LC_ALL, '')

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

                # retrieve current prices and flatten with dictionary comprehension
                # prices = {k:(cg.get_price(ids=coin_ids, vs_currencies='cad'))[v]['cad'] for (k,v) in symbols.items()}

                # get holdings and book value from spreadsheet
                holdings = dict(zip(symbols.keys(),df.iloc[0:,2:].sum().to_list()))
                total_book_value = df.iloc[0:,1].sum()

                # current cryptocurrencies held, and total dollar amount
                holdings_market_value = {k:(holdings[k] * prices[k]) for k in holdings}
                total_market_value = sum(holdings_market_value.values())

                # display portfolio book/market value and profit/loss in dollars
                print(colored(f"P/L: ", "yellow", attrs=['bold']) + locale.currency(total_market_value - total_book_value) + " (" + colored(f"{(total_market_value - total_book_value)/total_book_value:.2%}", "green") + ")" + colored("\nBOOK: ", "yellow", attrs=['bold']) + locale.currency(total_book_value) + colored("\nMARKET: ", "yellow", attrs=['bold']) + locale.currency(total_market_value) + "\n")
                print(colored("Symbol   Price       Balance              Value", "yellow", attrs=['bold']))
                print(colored("---------------------------------------------------", "green", attrs=['bold']))

                # display individual holdings in cryptocurrency and dollars
                for i in symbols:
                    spaces = (6 - len(i)) * ' '
                    spaces2 = (10 - len(str(locale.currency(prices[i])))) * ' '
                    spaces3 = (20 - len(str(holdings[i]))) * ' '
                    print(colored(f"{i}:", "yellow", attrs=['bold']) + (f"{spaces}  {locale.currency(prices[i])} {spaces2} {holdings[i]} {spaces3}" + colored(locale.currency(holdings_market_value[i]), "blue", attrs=['bold'])))
                time.sleep(15)

    # prompt user for valid file until one is provided, then add it to config
    else:
        while not path.isfile(spreadsheet):
            coinport_config_data['spreadsheet']['filepath'] = input("Woops, no spreadsheet found! Please specify filename: ")
            spreadsheet = coinport_config_data['spreadsheet']['filepath']
        with open(coinport_config, 'w') as config_file:
            json.dump(coinport_config_data, config_file, sort_keys=True, indent=4, separators=(',', ': '))
