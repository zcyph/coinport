# coinport
coinport is a minimalist cryptocurrency tracker written in Python, leveraging the CoinGecko API to show prices of your favorite cryptocurrencies.

It also retrieves information from a spreadsheet to display balance of your holdings, book value, market value and profit/loss.

## Requirements

**Python**

This is a Python script, so make sure you have Python installed. This was tested with Python 3.9 and works in Linux, Mac and Windows.

**Dependencies**

A few things are required in order to run this script. After installing Python, do the following commands to install the dependencies. It is a good practice to do this within a virtual environment:

`pip install pycoingecko`

`pip install pyexcel_ods`

`pip install termcolor`

Depending on your environment, you may or may not need to type "pip3" instead of just "pip".

## Usage

Make sure the spreadsheet is in the same folder as the script, run it like this: 

`python coinport.py`


![](https://github.com/zcyph/coinport/blob/main/screenshot.png)

