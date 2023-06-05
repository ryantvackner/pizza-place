# -*- coding: utf-8 -*-
"""
Pizza Place Sales

Created on Thu Mar 23 20:37:12 2023

@author: ryantvackner
"""

#import libraries
import streamlit as st
import pandas as pd
import altair as alt
import matplotlib as plt
from datetime import datetime 
from statsmodels.tsa import seasonal as smts

st.set_page_config(
    page_title = "Pizza Place Analysis",
    page_icon = ":pizza:"
    )

# title of page
st.title(":moneybag: Sales")

# import main dataframes
df_order_details = st.session_state['df_order_details']
df_orders = st.session_state['df_orders']
df_pizza_types = st.session_state['df_pizza_types']
df_pizzas = st.session_state['df_pizzas']

# date slider
sl_order_start_date = st.sidebar.date_input("Start Date:", datetime(2015, 1, 1))
sl_order_end_date = st.sidebar.date_input("End Date:", datetime(2015, 12, 31))
df_orders = df_orders[(df_orders["datetime"] >= datetime.strptime(str(sl_order_start_date), "%Y-%m-%d")) & (df_orders["datetime"] <= datetime.strptime(str(sl_order_end_date), "%Y-%m-%d"))]
    
# price per order
df_order_price = pd.merge(df_order_details, df_pizzas, on='pizza_id', how='left')
df_order_price = (df_order_price.groupby(["order_id"])["price"].sum()).to_frame().reset_index()
df_order_price = pd.merge(df_orders, df_order_price, on='order_id', how='left')
tot_sales = round(df_order_price["price"].sum(), 2)
avg_order_price = round(df_order_price["price"].mean(), 2)
max_order_price = round(df_order_price["price"].max(), 2)
min_order_price = round(df_order_price["price"].min(), 2)

# Key Performace Indcators
st.subheader(":bar_chart: Key Performance Indicators")

# some metrics
st.metric("Total Sales", "${:,.2f}".format(tot_sales))
col_avg_sales, col_max_sales, col_min_sales = st.columns(3)
col_avg_sales.metric("Average Order Sale", "${:,.2f}".format(avg_order_price))
col_max_sales.metric("Largest Order Sale", "${:,.2f}".format(max_order_price))
col_min_sales.metric("Smallest Order Sale", "${:,.2f}".format(min_order_price))


# how much money did we make this year?
st.subheader(':calendar: Sales by Date')

# create tabs
tab_sales_by_day, tab_sales_by_month, tab_sales_by_quarter = st.tabs(["Day", "Month", "Quarter"])

with tab_sales_by_day:
    # sales per day
    df_sales = (df_order_price.groupby([df_order_price.datetime.dt.date])["price"].sum()).to_frame().reset_index()
    df_sales.rename(columns = {'datetime':'Date', 'price':'Sales'}, inplace = True)
    
    col_avg_sales, col_max_sales, col_min_sales = st.columns(3)
    col_avg_sales.metric("Average Daily Sales", "${:,.2f}".format(round(df_sales["Sales"].mean())))
    col_max_sales.metric("Largest Daily Sales", "${:,.2f}".format(round(df_sales["Sales"].max())))
    col_min_sales.metric("Smallest Daily Sales", "${:,.2f}".format(round(df_sales["Sales"].min())))
    
    # create the chart
    c_sales = alt.Chart(df_sales).mark_line() \
                                 .encode(x=alt.X('Date', sort=["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]), 
                                         y='Sales')
    # write the chart to streamlit
    st.altair_chart(c_sales, use_container_width=True)
    
with tab_sales_by_month:
    # sales per day
    df_sales = (df_order_price.groupby([df_order_price.datetime.dt.month_name()])["price"].sum()).to_frame().reset_index()
    avg_sales_by_month = round(df_sales["price"].mean(), 2)
    df_sales.rename(columns = {'datetime':'Date', 'price':'Sales'}, inplace = True)
    
    col_avg_sales, col_max_sales, col_min_sales = st.columns(3)
    col_avg_sales.metric("Average Monthly Sales", "${:,.2f}".format(round(df_sales["Sales"].mean())))
    col_max_sales.metric("Largest Monthly Sales", "${:,.2f}".format(round(df_sales["Sales"].max())))
    col_min_sales.metric("Smallest Monthly Sales", "${:,.2f}".format(round(df_sales["Sales"].min())))
    
    # create the chart
    c_sales = alt.Chart(df_sales).mark_line(point=True) \
                                 .encode(x=alt.X('Date', sort=["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]), 
                                         y='Sales')
    # write the chart to streamlit
    st.altair_chart(c_sales, use_container_width=True)

with tab_sales_by_quarter:
    df_order_price["quarter"] = ((df_order_price.datetime.dt.month - 1) // 3) + 1
    x = df_order_price["quarter"]
    # sales per day
    df_sales = (df_order_price.groupby([x])["price"].sum()).to_frame().reset_index()
    avg_sales_by_month = round(df_sales["price"].mean(), 2)
    df_sales.rename(columns = {'quarter':'Quarter', 'price':'Sales'}, inplace = True)
    
    col_avg_sales, col_max_sales, col_min_sales = st.columns(3)
    col_avg_sales.metric("Average Quarterly Sales", "${:,.2f}".format(round(df_sales["Sales"].mean())))
    col_max_sales.metric("Largest Quarterly Sales", "${:,.2f}".format(round(df_sales["Sales"].max())))
    
    # create the chart
    c_sales = alt.Chart(df_sales).mark_line(point=True) \
                                 .encode(x=alt.X('Quarter', sort=["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]), 
                                         y='Sales')
    # write the chart to streamlit
    st.altair_chart(c_sales, use_container_width=True)


# best sellers by sales
st.subheader(":chart_with_upwards_trend: Best Sellers")
df_order_bestsellers = pd.merge(df_orders, df_order_details, on='order_id', how='left')
df_order_bestsellers = (df_order_bestsellers.groupby(["pizza_id"])["quantity"].sum()).to_frame().reset_index()


# best sellers
df_order_bestsellers = pd.merge(df_pizzas, df_order_bestsellers, on='pizza_id', how='left')
df_order_bestsellers = pd.merge(df_pizza_types, df_order_bestsellers, on='pizza_type_id', how='left') 
df_order_bestsellers["Sales"] = df_order_bestsellers["price"] * df_order_bestsellers["quantity"]
df_order_pizza_id_bestsellers = (df_order_bestsellers.groupby(["pizza_id"])["Sales"].sum()).to_frame().reset_index()
df_order_name_bestsellers = (df_order_bestsellers.groupby(["name"])["Sales"].sum()).to_frame().reset_index()
df_order_size_bestsellers = (df_order_bestsellers.groupby(["size"])["Sales"].sum()).to_frame().reset_index()
df_order_category_bestsellers = (df_order_bestsellers.groupby(["category"])["Sales"].sum()).to_frame().reset_index()

# create ingredients list
ingredients = df_order_bestsellers
ingredients["ingredients"] = ingredients["ingredients"].str.split(', ')
ingredients = ingredients.explode('ingredients')
df_order_ingredients_bestsellers = (ingredients.groupby(["ingredients"])["Sales"].sum()).to_frame().reset_index()

tab_name, tab_type, tab_category, tab_size, tab_ingredients = st.tabs(["Name", "Type", "Category", "Size", "Ingredients"])

with tab_name:
    # chart name by quantity
    df_order_name_bestsellers.rename(columns = {'name':'Name'}, inplace = True)
    st.dataframe(df_order_name_bestsellers.sort_values(by=['Sales'], ascending=False), use_container_width=True)

with tab_type:
    # chart pizza type and size by quantity
    df_order_pizza_id_bestsellers.rename(columns = {'pizza_id':'Pizza ID'}, inplace = True)
    st.dataframe(df_order_pizza_id_bestsellers.sort_values(by=['Sales'], ascending=False), use_container_width=True)

with tab_category:
    # chart category by quantity
    df_order_category_bestsellers.rename(columns = {'category':'Category'}, inplace = True)
    st.dataframe(df_order_category_bestsellers.sort_values(by=['Sales'], ascending=False), use_container_width=True)

with tab_size:
    # chart size by quantity
    df_order_size_bestsellers.rename(columns = {'size':'Size'}, inplace = True)
    st.dataframe(df_order_size_bestsellers.sort_values(by=['Sales'], ascending=False), use_container_width=True)

with tab_ingredients:
    # chart ingredients by quantity
    df_order_ingredients_bestsellers.rename(columns = {'ingredients':'Ingredients'}, inplace = True)
    st.dataframe(df_order_ingredients_bestsellers.sort_values(by=['Sales'], ascending=False), use_container_width=True)




# seasonality in sales
st.subheader(":sunny: :snowflake: Seasonality in Sales")
st.write("Looks like Pizza Place has weekly seasonality. With sales increasing throughout the week, peaking on weekends.")
days_range = sl_order_end_date - sl_order_start_date
if days_range.days < 14:
    st.error("Date Range Must Be Greater Than 14 Days To See Seasonality in Sales")
else:
    df_seasonal_sales = (df_order_price.groupby([df_order_price.datetime.dt.date])["price"].sum()).to_frame().reset_index()
    analysis = df_seasonal_sales[['price']].copy()
    
    
    decompose_result_mult = smts.seasonal_decompose(analysis, model="multiplicative", period=7)
    
    trend = decompose_result_mult.trend
    seasonal = decompose_result_mult.seasonal
    residual = decompose_result_mult.resid
    
    st.write(decompose_result_mult.plot())










