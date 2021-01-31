# coinport
coinport is a minimalist cryptocurrency tracker written in Python, leveraging the CoinGecko API to show prices of your favorite cryptocurrencies.

It also retrieves information from a spreadsheet to display balance of your holdings, book value, market value and profit/loss.

## Requirements

**Python**

This is a Python script, so make sure you have Python installed. This was tested with Python 3.9.

**Dependencies**

It is recommended to do this within a virtual environment. You'll need to install pycoingecko, pyexcel_ods and termcolor:

`pip install pycoingecko`

`pip install pyexcel_ods`

`pip install termcolor`

## Usage

Make sure the spreadsheet is in the same folder as the script. 

Run the script with: 

`python coinport.py`

![](https://github.com/zcyph/coinport/blob/main/screenshot.png)
