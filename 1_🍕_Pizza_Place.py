# -*- coding: utf-8 -*-
"""
Pizza Place 

Created on Sun Mar 19 11:09:23 2023

@author: ryantvackner
"""

# import libaries
import pandas as pd
import streamlit as st
import heapq

st.set_page_config(
    page_title = "Pizza Place Analysis",
    page_icon = ":pizza:"
    )

# add that cache money
# read data
@st.cache_data
def read_data():
    # list of csv 
    ls_loc = ["order_details.csv", "orders.csv", "pizza_types.csv", "pizzas.csv"]
    df = []
    for loc in ls_loc:
        df.append(pd.read_csv("https://raw.githubusercontent.com/ryantvackner/pizza-place/master/pizza_sales/" + loc, encoding = 'unicode_escape'))
    return df



# title of app
st.title(":pizza: Pizza Place Data Driven Analysis")
st.caption("Created by: Ryan T Vackner")

# some text about data loading or something
data_load_state = st.text('Loading data...')
# read in dataframes
df_order_details, df_orders, df_pizza_types, df_pizzas = read_data()
# change dtypes
df_orders["datetime"] = df_orders["date"] + " " + df_orders["time"]
df_orders["datetime"] = pd.to_datetime(df_orders["datetime"])
df_orders = df_orders.drop(["date", "time"], axis=1)
# notify when data loading is done
data_load_state.text('Loading data...Done!')


# Key Performance Indicators
st.header(":bar_chart: Key Performance Indicators")

col_orders, col_sales = st.columns(2)

x = df_orders.datetime.dt.month
y = df_orders.datetime.dt.year
# create dataframe of pizza orders by period
df_orders_count_orders = (df_orders.groupby([x, y])["order_id"].count().rename("Number of Orders")).to_frame()
df_orders_count_orders["datetime"] = df_orders_count_orders.index
df_orders_count_orders.rename(columns = {'datetime':'Date'}, inplace = True)

current_month, last_month  = heapq.nlargest(2, df_orders_count_orders["Date"])

most_recent_orders = df_orders_count_orders[df_orders_count_orders['Date'] == current_month]
second_most_recent_orders = df_orders_count_orders[df_orders_count_orders['Date'] == last_month]
diff = most_recent_orders["Number of Orders"].iloc[0] - second_most_recent_orders["Number of Orders"].iloc[0]


col_orders.metric("Current Monthly Orders", most_recent_orders["Number of Orders"], str(diff))



# price per order
df_order_price = pd.merge(df_order_details, df_pizzas, on='pizza_id', how='left')
df_order_price = (df_order_price.groupby(["order_id"])["price"].sum()).to_frame().reset_index()
df_order_price = pd.merge(df_orders, df_order_price, on='order_id', how='left')
a = df_order_price.datetime.dt.month
b = df_order_price.datetime.dt.year
df_sales = (df_order_price.groupby([a, b])["price"].sum()).to_frame()
df_sales["datetime"] = df_sales.index
df_sales.rename(columns = {'datetime':'Date', 'price':'Sales'}, inplace = True)

current_month_sales, last_month_sales  = heapq.nlargest(2, df_sales["Date"])

most_recent_sales = df_sales[df_sales['Date'] == current_month]
second_most_recent_sales = df_sales[df_sales['Date'] == last_month]
diff_sales = most_recent_sales["Sales"].iloc[0] - second_most_recent_sales["Sales"].iloc[0]


col_sales.metric("Current Monthly Sales", "$" + str(round(most_recent_sales['Sales'].iloc[0], 2)), str(round(diff_sales, 2)))




# Analysis
st.header(":bookmark_tabs: Analysis")
st.write("Pizza Place has an average of 60 Customers per day. \
          This stays fairly consistent thoughout the 2015 year. \
          Except for around the end of year holidays where the average drops to 44 customers a day. \
          That is a 25% decrease in average customers during the holiday season.")
st.write("**My recommendation is to close up shop a couple days before Christmas and reopen after the New Year. \
          This will increase your profit margins as you will not be opening up on known low profit margin days.**")
st.write("Pizza Place has some pizzas that are really big hits. \
          Like The Classic Deluxe Pizza, The Barbecue Chicken Pizza, The Hawaiian Pizza, and The Pepperoni Pizza. \
          Which all had over 2,400 orders in 2015. \
          While The Brie Carre Pizza wasn't a very popular option as it didn't even break 500 orders. \
          The XL and XXL sizes were also not very popular. \
          Adding up to only 579 orders in 2015.")
st.write("**My recommendation is to remove The Brie Carrie and other underperforming pizzas from the menu. \
          I also recommend removing the XL and XXL options from the menu as they are not very popular choices. \
          Removing these options allows Pizza Place to focus on maximizing profits on pizzas that are known to sell.**")










# load data into session state for other pages
if 'df_order_details' not in st.session_state:
    st.session_state['df_order_details'] = df_order_details
if 'df_orders' not in st.session_state:
    st.session_state['df_orders'] = df_orders
if 'df_pizza_types' not in st.session_state:
    st.session_state['df_pizza_types'] = df_pizza_types
if 'df_pizzas' not in st.session_state:
    st.session_state['df_pizzas'] = df_pizzas
        
# looking at the raw data
if st.checkbox('Show raw data'):
    # create tabs for the raw data
    tab_orders, tab_order_details, tab_pizzas, tab_pizza_types = st.tabs(["Orders", "Order Details", "Pizzas", "Pizza Types"])
    
    with tab_orders:
        st.subheader("Orders")
        if st.checkbox('Show Orders Dictionary'):
            st.caption("**order_id**: Unique identifier for each order placed by a table")
            st.caption("**datetime**: Date and time the order was placed (entered into the system prior to cooking & serving)")
        st.write(df_orders)
        
    with tab_order_details:
        st.subheader("Order Details")
        if st.checkbox('Show Order Details Dictionary'):
            st.caption("**order_details_id**: Unique identifier for each pizza placed within each order (pizzas of the same type and size are kept in the same row, and the quantity increases)")
            st.caption("**order_id**: Foreign key that ties the details in each order to the order itself")
            st.caption("**pizza_id**: Foreign key that ties the pizza ordered to its details, like size and price")
            st.caption("**quantity**: Quantity ordered for each pizza of the same type and size")
        st.write(df_order_details)
        
    with tab_pizzas:
        st.subheader("Pizzas")
        if st.checkbox('Show Pizzas Dictionary'):
            st.caption("**pizza_id**: Unique identifier for each pizza (constituted by its type and size)")
            st.caption("**pizza_type_id**: Foreign key that ties each pizza to its broader pizza type")
            st.caption("**size**: Size of the pizza (Small, Medium, Large, X Large, or XX Large)")
            st.caption("**price**: Price of the pizza in USD")
        st.write(df_pizzas)
        
    with tab_pizza_types:
        st.subheader("Pizza Types")
        if st.checkbox('Show Pizza Types Dictionary'):
            st.caption("**pizza_type_id**: Unique identifier for each pizza type")
            st.caption("**name**: Name of the pizza as shown in the menu")
            st.caption("**category**: Category that the pizza fall under in the menu (Classic, Chicken, Supreme, or Veggie)")
            st.caption("**ingredients**: Comma-delimited ingredients used in the pizza as shown in the menu (they all include Mozzarella Cheese, even if not specified; and they all include Tomato Sauce, unless another sauce is specified)")
        st.write(df_pizza_types)















