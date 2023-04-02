# -*- coding: utf-8 -*-
"""
Pizza Place Customers

Created on Sat Mar 25 13:11:49 2023

@author: ryantvackner
"""

#import libraries
import pandas as pd
import streamlit as st
import altair as alt
import numpy as np
from datetime import datetime

st.set_page_config(
    page_title = "Pizza Place Analysis",
    page_icon = ":pizza:"
    )

# import main dataframes
df_order_details = st.session_state['df_order_details']
df_orders = st.session_state['df_orders']
df_pizza_types = st.session_state['df_pizza_types']
df_pizzas = st.session_state['df_pizzas']

# date slider
sl_order_start_date = st.sidebar.date_input("Start Date:", datetime(2015, 1, 1))
sl_order_end_date = st.sidebar.date_input("End Date:", datetime(2015, 12, 31))
df_orders = df_orders[(df_orders["datetime"] >= datetime.strptime(str(sl_order_start_date), "%Y-%m-%d")) & (df_orders["datetime"] <= datetime.strptime(str(sl_order_end_date), "%Y-%m-%d"))]


# title of page
st.title(":clipboard: Orders")

# Key Performace Indcators
st.subheader(":bar_chart: Key Performance Indicators")

# some metrics
st.metric("Total Orders", str(df_orders["order_id"].max()))

# historgram of data
st.subheader(':calendar: Pizza Orders by Date')

tab_orders_by_day, tab_orders_by_month, tab_orders_by_quarter = st.tabs(["Day", "Month", "Quarter"])

with tab_orders_by_day:
    x = df_orders.datetime.dt.date
    # create dataframe of pizza orders by period
    df_orders_count_orders = (df_orders.groupby([x])["order_id"].count().rename("Number of Orders")).to_frame()
    df_orders_count_orders["datetime"] = df_orders_count_orders.index
    df_orders_count_orders.rename(columns = {'datetime':'Date'}, inplace = True)

    col_avg_orders, col_max_orders, col_min_orders = st.columns(3)

    # average orders by period
    col_avg_orders.metric("Daily Average Orders", round(df_orders_count_orders["Number of Orders"].mean()))
    col_max_orders.metric("Daily Max Orders", round(df_orders_count_orders["Number of Orders"].max()))
    col_min_orders.metric("Daily Min Orders", round(df_orders_count_orders["Number of Orders"].min()))

    # create the chart
    c_count_orders = alt.Chart(df_orders_count_orders).mark_line() \
                                 .encode(x=alt.X('Date', sort=["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]), 
                                         y='Number of Orders')
    # write the chart to streamlit
    st.altair_chart(c_count_orders, use_container_width=True)
    
with tab_orders_by_month:
    x = df_orders.datetime.dt.month_name()
    # create dataframe of pizza orders by period
    df_orders_count_orders = (df_orders.groupby([x])["order_id"].count().rename("Number of Orders")).to_frame()
    df_orders_count_orders["datetime"] = df_orders_count_orders.index
    df_orders_count_orders.rename(columns = {'datetime':'Date'}, inplace = True)

    col_avg_orders, col_max_orders, col_min_orders = st.columns(3)

    # average orders by period
    col_avg_orders.metric("Monthly Average Orders", round(df_orders_count_orders["Number of Orders"].mean()))
    col_max_orders.metric("Monthly Max Orders", round(df_orders_count_orders["Number of Orders"].max()))
    col_min_orders.metric("Monthly Min Orders", round(df_orders_count_orders["Number of Orders"].min()))

    # create the chart
    c_count_orders = alt.Chart(df_orders_count_orders).mark_line(point=True) \
                                 .encode(x=alt.X('Date', sort=["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]), 
                                         y='Number of Orders')
    # write the chart to streamlit
    st.altair_chart(c_count_orders, use_container_width=True)

with tab_orders_by_quarter:
    df_orders["quarter"] = ((df_orders.datetime.dt.month - 1) // 3) + 1
    x = df_orders["quarter"]
    # create dataframe of pizza orders by period
    df_orders_count_orders = (df_orders.groupby([x])["order_id"].count().rename("Number of Orders")).to_frame()
    df_orders_count_orders["quarter"] = df_orders_count_orders.index
    df_orders_count_orders.rename(columns = {'quarter':'Quarter'}, inplace = True)

    col_avg_orders, col_max_orders, col_min_orders = st.columns(3)

    # average orders by period
    col_avg_orders.metric("Quartly Average Orders", round(df_orders_count_orders["Number of Orders"].mean()))
    col_max_orders.metric("Quartly Max Orders", round(df_orders_count_orders["Number of Orders"].max()))
    col_min_orders.metric("Quartly Min Orders", round(df_orders_count_orders["Number of Orders"].min()))

    # create the chart
    c_count_orders = alt.Chart(df_orders_count_orders).mark_line(point=True) \
                                 .encode(x=alt.X('Quarter', sort=["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]), 
                                         y='Number of Orders')
    # write the chart to streamlit
    st.altair_chart(c_count_orders, use_container_width=True)



   

# histogram of specific hour
st.subheader(':clock3: Pizzas Ordered by Hour')
hist_values = np.histogram(df_orders["datetime"].dt.hour, bins=24, range=(0,24))[0]
df_orders_by_hour = pd.DataFrame()
df_orders_by_hour["Orders"] = hist_values
df_orders_by_hour["Hour"] = df_orders_by_hour.index

df_orders_by_hour_avg = df_orders_by_hour.copy()
days_range = sl_order_end_date - sl_order_start_date
df_orders_by_hour_avg["Orders"] = df_orders_by_hour_avg["Orders"] / days_range.days

tab_orders_by_hour_total, tab_orders_by_hour_avg = st.tabs(["Total", "Average"])

with tab_orders_by_hour_total:
    c_orders_by_hour = alt.Chart(df_orders_by_hour).mark_bar(size=20).encode(alt.X('Hour', scale=alt.Scale(domain=(0, 23))), y='Orders')
    st.altair_chart(c_orders_by_hour, use_container_width=True)
    
with tab_orders_by_hour_avg:
    c_orders_by_hour = alt.Chart(df_orders_by_hour_avg).mark_bar(size=20).encode(alt.X('Hour', scale=alt.Scale(domain=(0, 23))), y='Orders')
    st.altair_chart(c_orders_by_hour, use_container_width=True)





# number of pizzas in a typical order
st.subheader(':page_with_curl: Pizzas in a Typical Order')
ls_date_range = df_orders["order_id"].to_list()
df_order_details = df_order_details.loc[df_order_details['order_id'].isin(ls_date_range)]

df_order_details_sort = df_order_details.groupby(["order_id"])["quantity"].sum().to_frame()
avg_pizza_order = df_order_details_sort.mean()

col_avg_pizza, col_max_pizza, col_min_pizza = st.columns(3)
col_avg_pizza.metric("Average Amount of Pizzas in Order", round(avg_pizza_order, 1))
col_max_pizza.metric("Most Amount of Pizzas in Order", df_order_details_sort["quantity"].max())
col_min_pizza.metric("Least Amount of Pizzas in Order", df_order_details_sort["quantity"].min())




# best sellers by pizza id
st.subheader(':chart_with_upwards_trend: Best Sellers')
df_order_bestsellers = (df_order_details.groupby(["pizza_id"])["quantity"].sum()).to_frame().reset_index()


# best sellers
df_order_bestsellers = pd.merge(df_pizzas, df_order_bestsellers, on='pizza_id', how='left')
df_order_bestsellers = pd.merge(df_pizza_types, df_order_bestsellers, on='pizza_type_id', how='left') 
df_order_pizza_id_bestsellers = (df_order_bestsellers.groupby(["pizza_id"])["quantity"].sum()).to_frame().reset_index()
df_order_name_bestsellers = (df_order_bestsellers.groupby(["name"])["quantity"].sum()).to_frame().reset_index()
df_order_size_bestsellers = (df_order_bestsellers.groupby(["size"])["quantity"].sum()).to_frame().reset_index()
df_order_category_bestsellers = (df_order_bestsellers.groupby(["category"])["quantity"].sum()).to_frame().reset_index()

# create ingredients list
ingredients = df_order_bestsellers
ingredients["ingredients"] = ingredients["ingredients"].str.split(', ')
ingredients = ingredients.explode('ingredients')
df_order_ingredients_bestsellers = (ingredients.groupby(["ingredients"])["quantity"].sum()).to_frame().reset_index()

tab_name, tab_type, tab_category, tab_size, tab_ingredients = st.tabs(["Name", "Type", "Category", "Size", "Ingredients"])

with tab_name:
    # chart name by quantity
    df_order_name_bestsellers.rename(columns = {'quantity':'Quantity', 'name':'Name'}, inplace = True)
    st.dataframe(df_order_name_bestsellers.sort_values(by=['Quantity'], ascending=False), use_container_width=True)

with tab_type:
    # chart pizza type and size by quantity
    df_order_pizza_id_bestsellers.rename(columns = {'quantity':'Quantity', 'pizza_id':'Pizza ID'}, inplace = True)
    st.dataframe(df_order_pizza_id_bestsellers.sort_values(by=['Quantity'], ascending=False), use_container_width=True)

with tab_category:
    # chart category by quantity
    df_order_category_bestsellers.rename(columns = {'quantity':'Quantity', 'category':'Category'}, inplace = True)
    st.dataframe(df_order_category_bestsellers.sort_values(by=['Quantity'], ascending=False), use_container_width=True)

with tab_size:
    # chart size by quantity
    df_order_size_bestsellers.rename(columns = {'quantity':'Quantity', 'size':'Size'}, inplace = True)
    st.dataframe(df_order_size_bestsellers.sort_values(by=['Quantity'], ascending=False), use_container_width=True)

with tab_ingredients:
    # chart ingredients by quantity
    df_order_ingredients_bestsellers.rename(columns = {'quantity':'Quantity', 'ingredients':'Ingredients'}, inplace = True)
    st.dataframe(df_order_ingredients_bestsellers.sort_values(by=['Quantity'], ascending=False), use_container_width=True)





