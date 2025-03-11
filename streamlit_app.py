# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
st.text(smoothiefroot_response.json())


# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    "Choose the fruits you want in your custom Smoothie!"
)

name_on_order = st.text_input("Name on Smoothie:", "")
st.write("The name on your smoothie will be", name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients :',
    my_dataframe,
    max_selections = 6
)

if ingredients_list:
    # st.write(ingredients_list)
    # st.text(ingredients_list)
    ingredients_string = ''
    for fruit in ingredients_list:
        ingredients_string += fruit + ' '
    # st.write(ingredients_string)

time_to_insert = st.button('Submit Order')

if time_to_insert: 
        
    if ingredients_string:
        my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
                        values ('""" + ingredients_string + """','"""+name_on_order+"""')"""
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie is ordered, {name_on_order}!', icon="✅")
