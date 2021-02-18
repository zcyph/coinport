# coinport
A minimalist cryptocurrency & portfolio tracker written in Python.

## Why?

The raison d'etre for this project is to track the coins I want, the coins I have, and see my overall progress - all without needing to create an account anywhere, provide sensitive personal information to any third party, be tracked or profiled, or expose any cryptocurrency.

## Requirements

**Python**

This is a Python script, so make sure you have Python installed. This was tested with Python 3.9 and works in Linux, Mac and Windows.

**Dependencies**

A few things are required in order to run this script. After installing Python, install them as follows. While not required, it is a good practice to do this within a virtual environment:

`pip install pycoingecko`

`pip install pandas`

`pip install tabulate`

`pip install xlrd`

`pip install pyexcel_ods`

`pip install 'openpyxl`

`pip install sty`

Depending on your environment, you may or may not need to type "pip3" instead of just "pip".

## Usage

LibreOffice and MS Office formats are supported. By default, the script will look for the included file, `crypto.xlsx`. You can point it to your file of choice by editing `conf.json` accordingly. When adding or removing coins from your spreadsheet, be sure to use the cryptocurrency name (ie, "Bitcoin", "Bitcoin Cash", "Synthetix Network Token"). The ticker/symbol is not used here because there are many duplicates. You may also specify the currency in the conf file:

![](https://github.com/zcyph/coinport/blob/main/screenshot_conf.png)

Download ZIP above or just git clone the repo:

`git clone https://github.com/zcyph/coinport`

Change to the directory you just downloaded into, ie:

`cd coinport`

Run the script:

`python coinport.py`

The script will stay running unless you stop it (you can do that with `CTRL-C`). It will automatically refresh frequently to retrieve updated prices. If you save changes to the spreadsheet it will automatically update with your new additions.


![](https://github.com/zcyph/coinport/blob/main/screenshot.png)

