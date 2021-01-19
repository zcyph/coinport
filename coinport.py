import locale, time
from pycoingecko import CoinGeckoAPI
from pyexcel_ods import get_data
from os import system

while True:
    # clear screen & set locale for currency formatting
    system('clear')
    locale.setlocale(locale.LC_ALL, '')

    # define symbols
    symbols = {'BTC': 'bitcoin', 'ETH': 'ethereum', 'XMR': 'monero', 'ADA': 'cardano', 'XLM': 'stellar'}

    # retrieve prices from CoinGecko API, flatten with dictionary comprehension
    getprices = CoinGeckoAPI().get_price(ids='bitcoin,ethereum,monero,cardano,stellar', vs_currencies='cad')
    prices = {k:getprices[v]['cad'] for (k,v) in symbols.items()}

    # get current holdings & book value from spreadsheet, convert nested OrderedDict to dictionary
    data = get_data("crypto.ods", start_row=2, row_limit=2, start_column=2)
    holdings = dict(zip(data['Sheet1'][0], data['Sheet1'][1]))
    bookvalue = (get_data("crypto.ods", start_row=3, row_limit=1, start_column=1, column_limit=1))['Sheet1'][0][0]

    # current cryptocurrencies held, and total dollar amount
    holdings_value = {k:(holdings[k] * prices[k]) for k in holdings}
    total_holdings = sum(holdings_value.values())

    # display current prices for all held coins
    for i in symbols:
        print(f"| {i}: " + locale.currency(prices[i]), end=" |")

    # display portfolio book/market value and profit/loss in dollars
    print(f"\n\nPORTFOLIO:\n")
    print(f"BOOK VALUE: " + locale.currency(bookvalue))
    print(f"MARKET VALUE: " + locale.currency(total_holdings))
    print(f"NET P/L: " + locale.currency(total_holdings - bookvalue) + "\n")

    # display individual holdings in cryptocurrency and dollars
    for i in symbols:
        print(f"{i}: {holdings[i]} ({locale.currency(holdings_value[i])})")
    time.sleep(10)
