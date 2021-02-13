# coinport
coinport is a minimalist cryptocurrency tracker written in Python, leveraging the CoinGecko API to track prices of your favorite cryptocurrencies.

It retrieves information from a spreadsheet to display the balance of your holdings, its book value, market value and profit/loss.

## Requirements

**Python**

This is a Python script, so make sure you have Python installed. This was tested with Python 3.9 and works in Linux, Mac and Windows.

**Dependencies**

A few things are required in order to run this script. After installing Python, do the following commands to install the dependencies. Whilte not required, it is a good practice to do this within a virtual environment:

`pip install pycoingecko`

`pip install pandas`

`pip install xlrd`

`pip install pyexcel_ods`

`pip install sty`

Depending on your environment, you may or may not need to type "pip3" instead of just "pip".

## Usage

Download ZIP above or just git clone the repo:

`git clone https://github.com/zcyph/coinport`

Change to the directory you just downloaded into, ie:

`cd coinport`

Edit the included Excel spreadsheet to your liking (ODS is supported if you prefer LibreOffice), then run the script:

`python coinport.py`

The script will stay running unless you stop it (you can do that with `CTRL-C`). It will automatically refresh frequently to retrieve updated prices. If you save changes to the spreadsheet it will automatically update with your new additions.


![](https://github.com/zcyph/coinport/blob/main/screenshot.png)

