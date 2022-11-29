import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError


streamlit.title('My Parents New Healthy Diner')

streamlit.header('Breakfast Menu')
streamlit.text('🥣Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞Avocado Toast')   

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)

# New Section to display fruityvice api response
streamlit.header("Fruityvice Fruit Advice!")
##
fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
#streamlit.write('The user entered ', fruit_choice)

#
#fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)

#streamlit.text(fruityvice_response.json())  # just view data

# write your own comment -what does the next line do? 
#fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())

# create a function
def get_fruityvice_data(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized
  
# output it the screen as a table
streamlit.header('Fruityvice Fruit Advice!')
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information.")
  else:
    back_from_function = get_fruityvice_data(fruit_choice)
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    streamlit.dataframe(back_from_function)
except URLError as e:
  streamlit.error()

streamlit.stop()

#

##
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * from fruit_load_list")
my_data_rows = my_cur.fetchall()
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_rows)

##
# New Section to display fruityvice api response
streamlit.header("Fruityvice Fruit Advice! 2")
##
add_my_fruit = streamlit.text_input('What fruit would you like to add?')
streamlit.write('Thanks for you add ', add_my_fruit)
my_cur.execute("insert into pc_rivery_db.public.FRUIT_LOAD_LIST values('from streamlit')")
