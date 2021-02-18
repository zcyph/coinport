import sys, time, locale, json
from os import system, name, path
from pycoingecko import CoinGeckoAPI
import pandas as pd
from sty import fg, bg, ef, rs, Style, RgbFg
from tabulate import tabulate

################################################# configuration #
coin_list = 'coinlist.json'
coinport_config = 'conf.json'
with open(coinport_config) as config_file:
    coinport_config_data = json.load(config_file)
    spreadsheet = coinport_config_data['spreadsheet']['filepath']
    user_currency = coinport_config_data['stats']['currency']
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
                # load changes to config automatically
                with open(coinport_config) as config_file:
                    coinport_config_data = json.load(config_file)
                    spreadsheet = coinport_config_data['spreadsheet']['filepath']
                    user_currency = coinport_config_data['stats']['currency']
                # spreadsheet -> Pandas df (dataframe)
                df = pd.ExcelFile(spreadsheet).parse(pd.ExcelFile(spreadsheet).sheet_names[0])

                # portfolio coins to track
                coins_to_track = df.columns[2:].tolist()

                # get list of coins from CoinGecko if missing
                if not path.isfile(coin_list):
                    allcoins = cg.get_coins_list()
                    with open(coin_list, 'w') as coinlist_file:
                        json.dump(allcoins, coinlist_file, sort_keys=True, indent=4, separators=(',', ': '))
                else:
                    with open(coin_list) as coinlist_file:
                        allcoins = json.load(coinlist_file)

                # look up CoinGecko ID or ticker symbol with coin name
                def name_to_id(coin_name):
                    return next(i['id'] for i in allcoins if i["name"] == coin_name)
                def name_to_symbol(coin_name):
                    return next(i['symbol'] for i in allcoins if i["name"] == coin_name)
                # turn price percent change green if positive, red if negative
                def colorize_percent(num):
                    color = fg.red if num < 0 else fg(10,255,10)
                    return f'{color}{num:.2f}%' + fg.rs

                # set symbols & coin ID
                coin_ids = []
                for coin in coins_to_track:
                    coin_id = name_to_id(coin)
                    coin_ids.append(coin_id)
                symbols = {}
                for coin in coins_to_track:
                    coin_id = name_to_id(coin)
                    symbol = name_to_symbol(coin)
                    symbols.update({symbol:coin_id})

                # get current prices and 24h change from CoinGecko API
                prices = {k:(CoinGeckoAPI().get_price(ids=coin_ids, vs_currencies=user_currency))[v][user_currency] for (k,v) in symbols.items()}
                prices24h = {k:(CoinGeckoAPI().get_price(ids=coin_ids, include_24hr_change="true", vs_currencies=user_currency))[v][user_currency + '_24h_change'] for (k,v) in symbols.items()}

                # get holdings, book, market, profit/loss values
                holdings = dict(zip(symbols.keys(), df.iloc[0:,2:].sum().to_list()))
                total_book_value = df.iloc[0:,1].sum()
                holdings_market_value = {k:(holdings[k] * prices[k]) for k in holdings}
                total_market_value = sum(holdings_market_value.values())
                profit_loss = total_market_value - total_book_value

                # figure out the spacing issue
                profit_loss_percent = colorize_percent((profit_loss/total_book_value)*100)
                profit_loss_length = len(locale.currency(profit_loss,grouping=True)) + len(profit_loss_percent)
                ansi_len = len(fg.red) if profit_loss < 0 else len(fg(10,255,10)) #to calc spacing
                subtract_length = 42 - (profit_loss_length - ansi_len)
                clear()

                # display header: book, market value and profit/loss in local currency
                portfolio_header = (
                f"_______________________________________________________________\n\n" +
                fg.orange + '  [ ' + fg.rs + ef.bold + fg.yellow + "p/l" + fg.rs + rs.bold_dim + fg.orange + '  ]    ' + fg.rs  + locale.currency(total_market_value - total_book_value,grouping=True) + " (" + f"{profit_loss_percent}" + ")" + fg.orange + ef.bold + (' ' * subtract_length) + '[ ' + fg.rs + fg.yellow + f'{user_currency}' + fg.rs + fg.orange + ' ]' + fg.rs + rs.bold_dim +
                fg.orange + '\n  [ ' + fg.rs + ef.bold + fg.yellow + "book " + fg.rs + rs.bold_dim + fg.orange + ']    ' + fg.rs + locale.currency(total_book_value,grouping=True) +
                fg.orange + '\n  [' + fg.rs + ef.bold + fg.yellow + f" mrkt " + fg.rs + rs.bold_dim + fg.orange + ']    ' + fg.rs + locale.currency(total_market_value,grouping=True) + "\n" +
                f"_______________________________________________________________\n"
                )
                print(portfolio_header)

                # put holdings & prices into Pandas dataframe then format to print with tabulate
                dataset = []
                for i in symbols:
                	dataset.append({'  [ tikr ]':fg.orange + '  [ ' + fg.rs + fg.yellow + ef.bold + i + fg.rs + rs.bold_dim + (fg.orange + ' ' * (4 - len(i)) + ' ]' + fg.rs), '[ price ]':f'${prices[i]:n}', '[ 1d ]':colorize_percent(prices24h[i]), '[ balance ]':f'{holdings[i]}', '[ value ]': locale.currency(holdings_market_value[i],grouping=True)})
                dataset_df = pd.DataFrame(dataset)
                print(tabulate(dataset_df,headers=fg.orange + ef.bold + dataset_df.columns + fg.rs +rs.bold_dim + "\n",tablefmt="plain",stralign="left",floatfmt=".6f",showindex=False))
                time.sleep(10)

    # prompt user for valid file until one is provided, then add it to config
    else:
        while not path.isfile(spreadsheet):
            coinport_config_data['spreadsheet']['filepath'] = input("Woops, no spreadsheet found! Please specify filename: ")
            spreadsheet = coinport_config_data['spreadsheet']['filepath']
        with open(coinport_config, 'w') as config_file:
            json.dump(coinport_config_data, config_file, sort_keys=True, indent=4, separators=(',', ': '))
