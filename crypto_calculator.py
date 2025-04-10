#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import requests

from dash import Dash, dcc, html
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc

from dash import jupyter_dash
jupyter_dash.default_mode = 'external'


# # Cryptocurrency Converter Calculator
# 
# In this notebook, we replicate some of the functionalities in the Cryptocurrency Converter Calculator found here: https://www.coingecko.com/en/converter. Our calculator allows the user to convert an amount of a cryptocurrency to either USD, EUR or GBP.
# 
# To get the real-time exchange rate for the conversion, we use the CURRENCY_EXCHANGE_RATE API from Alpha Vantage: https://www.alphavantage.co/documentation/#crypto-exchange.

# Our application allows the user to select any of the ten coins in `digital_currency_list.csv`.

# In[2]:


df_coins = pd.read_csv('digital_currency_list.csv')

df_coins


# ### Extract data from API
# 
# To make a request to the API, you must copy-paste one of the keys from `keys.txt` into the variable `my_key` below.

# In[3]:


my_key = 'PSPGHH6OJUGEPT7F'


# <div class="alert alert-info">
# <h3> Task 1</h3>
#     <p> Create a function called <code>get_current_rate</code> that extracts and returns the current conversion rate for a given coin and currency using the CURRENCY_EXCHANGE_RATE API from Alpha Vantage. The function should handle potential errors caused by either the coin or currency being unavailable, or caused by exceeding the limit of API calls.
#         
# </div>

# In[4]:


def get_current_rate(coin, currency, apikey = my_key):

    try: 
        url = 'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=' + coin + '&to_currency=' + currency + '&apikey=' + apikey
        data = requests.get(url).json()
        rate = float(data['Realtime Currency Exchange Rate']['5. Exchange Rate'])

    except:
        rate = None    # none means empty, there are no value here, returns nothing

    return rate


# In[5]:


get_current_rate('BTC', 'USD')


# ### Create selectors
# 
# We use a `Dropdown` component to create the selectors for both the coin and the currency. 

# <div class="alert alert-info">
# <h3> Task 2</h3>
#     <p> Create a <code>Dropdown</code> component called <code>coin</code> that allows the user to select between any of the cryptocurrencies in <code>df_coins</code>, and a <code>Dropdown</code> component called <code>currency</code> that allows the user to select either "USD", "EUR" or "GBP". 
#         
# </div>

# In[6]:


coin = dcc.Dropdown(
    id = 'my_coin',
    options = [{'value' : code, 'label' : name} for code, name in zip(df_coins['currency code'], df_coins['currency name'])],
    value = 'BTC',
    multi = False,
    clearable = False
)

currency =  dcc.Dropdown(
    id = 'my_currency',
    options = ['USD', 'EUR', 'GBP'],
    value = 'USD',
    multi = False,
    clearable = False  #user cannot remove any value
)


# ### Create app
# 
# We create a `Dash` application that replicates Coingekko's conversion calculator.
# 
# To replicate the layout of the coingekko's calculator, we create a `Row` component that contains three `Col` components:
# - In the first column, we use an `Input` component to allow the user to select an amount to convert. Note that we use the `Input` component from `dbc` (instead of from `dcc`) to get nicer styling of the component.
# - In the second column, we insert the coin selector.
# - In the third column, we insert the currency selector.
# 
# In addition, we create a second "row" that contains the output of the actual conversion. Note that instead of using a `Row` component, we create a seperate division by using a `Container` component. The division is currently empty as it will be updated in the callback.
# 
# Finally, we place our conversion calculator inside a `Card` component inside the app layout.

# <div class="alert alert-info">
# <h3> Task 3</h3>
#     <p> Create a <code>Dash</code> application that replicates the layout of Coingekko's calculator as described above. However, don't make the app interactive yet (i.e., no callbacks).
#         
# </div>

# In[7]:


input_row = dbc.Row(
    children = [
        dbc.Col(
            children = [
                html.H6('Enter amount'),
                dbc.Input(
                    id = 'my_amount',
                    type = 'number',
                    value = 1
                )
            ], width = 4
        ),
        dbc.Col([html.H6('Select coin'), coin], width = 4),
        dbc.Col([html.H6('Select currency'), currency], width = 4), 
    ]
)


output_row = dbc.Container(
    id = 'my_conversion',
    children = '',
    style = {'minHeight' : '2rem'}
)


# <div class="alert alert-info">
# <h3> Task 4</h3>
#     <p> Make the app above interactive by adding a callback function called <code>update_conversion</code>. The callback should be fired each time the user enters a new amount, selects a different coin or currency, and the callback should update the conversion displayed to the user. 
#         
# </div>

# In[8]:


app = Dash(__name__, external_stylesheets = [dbc.themes.JOURNAL])
server = app.server

description = """
Check the latest cryptocurrency price against USD, EUR and GBP.

Data is extracted from Alpha Vantage.
"""

app.layout = dbc.Container(
    children = [
        html.H1('Cryptocurrency converter calculator'),
        dcc.Markdown(description),
        dbc.Card(
            children = [
                input_row,
                html.Br(),
                output_row
            ],
            body = True,   # tells dash that all of the children belong to the card body
            className = 'shadow-sm p-3'  # creates a shadow around the card
        )
    ]
)

@app.callback(
    Output('my_conversion', 'children'),
    Input('my_coin', 'value'),  #The order for the inputs are important, because they are being passed to each other
    Input('my_currency', 'value'),
    Input('my_amount', 'value')
)

def update_conversion(coin, currency, amount):

    if amount is None:
        return ''

    else:
        rate = get_current_rate(coin, currency)

        if rate is None:
            return 'Data not available'

        else:
            conversion = rate * amount
            return html.H4(f'{amount} {coin} = {conversion:,.2f}')  #:,.2f er å sette tusenskilletegn og to desimaler

If __name__ == '__main__':
    app.run(debug =True)
    


# In[ ]:




