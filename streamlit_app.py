# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!
    """
)

name_on_order = st.text_input('Name on Smoothie:')
st.write("The name on your Smoothie will be:", name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    ,my_dataframe
    ,max_selections=5
)
if ingredients_list:
    ingredients_string = ''

    for fruit_chosen in ingredients_list: 
        ingredients_string += fruit_chosen + ' '
        
    #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """', '""" + name_on_order + """')"""

    st.write(my_insert_stmt)
    st.stop
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        
        st.success('Your Smoothie is ordered!', icon="✅")

#new code to display fruityvice nutrition information
import requests

try:
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
    fruityvice_response.raise_for_status()  # Check if the request was successful
    response_json = fruityvice_response.json()  # Parse JSON response
    st.text(response_json)  # Display the JSON response
except requests.exceptions.HTTPError as http_err:
    st.error(f"HTTP error occurred: {http_err}")
except requests.exceptions.RequestException as req_err:
    st.error(f"Request error occurred: {req_err}")
except ValueError:  # includes JSONDecodeError
    st.error("Error decoding JSON, response might be empty or malformed")
except Exception as err:
    st.error(f"An error occurred: {err}")

        
        
