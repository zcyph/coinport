import locale, time
from pycoingecko import CoinGeckoAPI
from pyexcel_ods import get_data
from os import system, name
from termcolor import colored

def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')

while True:
    # clear screen & set locale for currency formatting
    clear()
    locale.setlocale(locale.LC_ALL, '')

    # define symbols
    symbols = {'BTC': 'bitcoin', 'ETH': 'ethereum', 'XMR': 'monero', 'ADA': 'cardano', 'XLM': 'stellar', 'ZEC': 'zcash', 'LINK': 'chainlink', 'COMP': 'compound-governance-token', 'GLM': 'golem', 'SNX': 'havven', 'UNI': 'uniswap', 'NANO': 'nano', 'DOT': 'polkadot', 'XRP': 'ripple', 'DOGE': 'dogecoin'}

    # retrieve prices from CoinGecko API, flatten with dictionary comprehension
    getprices = CoinGeckoAPI().get_price(ids='bitcoin,ethereum,monero,cardano,stellar,zcash,chainlink,compound-governance-token,golem,havven,uniswap,nano,polkadot,ripple,dogecoin', vs_currencies='cad')
    time.sleep(1)
    prices = {k:getprices[v]['cad'] for (k,v) in symbols.items()}

    # get current holdings & book value from spreadsheet, convert nested OrderedDict to dictionary
    data = get_data("crypto.ods", start_row=0, row_limit=2, start_column=2)
    holdings = dict(zip(data['Sheet1'][0], data['Sheet1'][1]))
    bookvalue = (get_data("crypto.ods", start_row=1, row_limit=1, start_column=1, column_limit=1))['Sheet1'][0][0]

    # current cryptocurrencies held, and total dollar amount
    holdings_value = {k:(holdings[k] * prices[k]) for k in holdings}
    total_holdings = sum(holdings_value.values())

    # display portfolio book/market value and profit/loss in dollars
    print(colored(f"P/L: ", "yellow", attrs=['bold']) + colored(locale.currency(total_holdings - bookvalue), "green") + colored("\nBOOK: ", "yellow", attrs=['bold']) + locale.currency(bookvalue) + colored("\nMARKET: ", "yellow", attrs=['bold']) + locale.currency(total_holdings) + "\n")
    print(colored("Symbol   Price       Balance              Value", "yellow", attrs=['bold']))
    print(colored("---------------------------------------------------", "green", attrs=['bold']))

    # display individual holdings in cryptocurrency and dollars
    for i in symbols:
        spaces = (6 - len(i)) * ' '
        spaces2 = (10 - len(str(locale.currency(prices[i])))) * ' '
        spaces3 = (20 - len(str(holdings[i]))) * ' '
        print(colored(f"{i}:", "yellow", attrs=['bold']) + (f"{spaces}  {locale.currency(prices[i])} {spaces2} {holdings[i]} {spaces3}" + colored(locale.currency(holdings_value[i]), "blue", attrs=['bold'])))
    time.sleep(8)
