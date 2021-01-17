import json, locale, time
from pycoingecko import CoinGeckoAPI
from pyexcel_ods import get_data
from os import system

while True:
    # clear screen
    system('clear')

    # set locale to enable currency formatting
    locale.setlocale(locale.LC_ALL, '')

    # set the CoinGecko API
    cg = CoinGeckoAPI()

    # retrieve current price info in CAD from Coin Gecko
    prices = cg.get_price(ids='bitcoin,ethereum,monero,cardano,stellar', vs_currencies='cad')

    # get current holdings from spreadsheet and put into dictionary with format: {'BTC': 0.01, 'ETH': 0.15})
    data = get_data("crypto.ods", start_row=2, row_limit=2, start_column=2)
    current_holdings = json.dumps(data) # json dump (returns string)
    dictionary = eval(current_holdings) # convert to dictionary
    holdings = dictionary['Sheet1']
    l1 = holdings[0]
    l2 = holdings[1]
    d1=zip(l1,l2)
    holdings_dict = dict(d1)

    # get the book value of fiat deposits
    getbookvalue = get_data("crypto.ods", start_row=3, row_limit=1, start_column=1, column_limit=1)
    bookvaluedump = json.dumps(getbookvalue)
    bookdict = eval(bookvaluedump)
    bookvalue = bookdict['Sheet1'][0][0]
    bookvalue_cad = locale.currency(bookvalue)

    # current prices
    btc_current_price = prices['bitcoin']['cad']
    btc_cad = locale.currency(prices['bitcoin']['cad'])
    eth_current_price = prices['ethereum']['cad']
    eth_cad = locale.currency(prices['ethereum']['cad'])
    xmr_current_price = prices['monero']['cad']
    xmr_cad = locale.currency(prices['monero']['cad'])
    ada_current_price = prices['cardano']['cad']
    ada_cad = locale.currency(prices['cardano']['cad'])
    xlm_current_price = prices['stellar']['cad']
    xlm_cad = locale.currency(prices['stellar']['cad'])

    # current holdings
    current_holdings_btc_cad = (holdings_dict['BTC'] * prices['bitcoin']['cad'])
    current_holdings_eth_cad = (holdings_dict['ETH'] * prices['ethereum']['cad'])
    current_holdings_xmr_cad = (holdings_dict['XMR'] * prices['monero']['cad'])
    current_holdings_ada_cad = (holdings_dict['ADA'] * prices['cardano']['cad'])
    current_holdings_xlm_cad = (holdings_dict['XLM'] * prices['stellar']['cad'])
    total_holdings = (current_holdings_btc_cad + current_holdings_eth_cad + current_holdings_xmr_cad + current_holdings_ada_cad + current_holdings_xlm_cad)

    # print current prices of all held coins
    print(f"BTC: " + btc_cad + " | ETH: " + eth_cad + " | XMR: " + xmr_cad + " | ADA: " + ada_cad + " | XLM: " + xlm_cad + "\n")

    # display current holdings and value
    print(f"PORTFOLIO:\n")
    print(f"BOOK VALUE: " + bookvalue_cad)
    print(f"MARKET VALUE: " + locale.currency(total_holdings))
    print(f"BTC: {holdings_dict['BTC']} ({locale.currency(current_holdings_btc_cad)})")
    print(f"ETH: {holdings_dict['ETH']} ({locale.currency(current_holdings_eth_cad)})")
    print(f"XMR: {holdings_dict['XMR']} ({locale.currency(current_holdings_xmr_cad)})")
    print(f"ADA: {holdings_dict['ADA']} ({locale.currency(current_holdings_ada_cad)})")
    print(f"XLM: {holdings_dict['XLM']} ({locale.currency(current_holdings_xlm_cad)})")
    time.sleep(10)
