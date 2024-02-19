import pandas as pd
import streamlit as st
import plotly.express as px
import altair as at

st.header('Analysis of Vehicle Markets')
st.write('Filter by vehicle make in the drop down below')

df = pd.read_csv('vehicles_us.csv')

#drop the column containing 'date posted'
df = df.drop(df.columns[11], axis=1)

#dropping rows where the model_year is older than 1950
# Identifying the index of rows where model_year is older than 1950
index_to_drop = df[df['model_year'] < 1950].index
# Dropping these rows
df.drop(index_to_drop, axis='rows', inplace=True)


#separate the make and model strings into new columns
df[['make','model']] = df['model'].str.split(" ", n=1, expand=True)


#create a dropdown selection filtered by vehicle make/brand
make_options = df['make'].unique()

selected_make = st.selectbox('Select a make', make_options)


#create a slider to filter year range
min_year, max_year = int(df['model_year'].min()), int(df['model_year'].max())

year_range = st.slider("Choose Year Range", value=(min_year, max_year), min_value = min_year, max_value = max_year)

actual_range = list(range(year_range[0], year_range[1]+1))



#specify the range of vehicles to be shown after filtering
df_filtered = df[ (df.make == selected_make) & (df.model_year.isin(list(actual_range)) )]

st.dataframe(df_filtered)

#moving on to price analysis
st.header('Price Analysis')
st.write('Here is a look at what conditions have the most impact on the price of the vehicle')

list_for_hist = ['condition', 'transmission', 'type']

selected_variable = st.selectbox('Select a variable', list_for_hist)

fig1 = px.histogram(df, x="price", color= selected_variable, range_x=[0, 50000] )
fig1.update_layout(title= "<b> Visual of price by {}</b>".format(selected_variable))

st.plotly_chart(fig1)

#moving on to scatterplot analysis of different variables

#adding a column that calculates age of vehicle from the max value of the model_year
df['age'] = 2019 - df['model_year']

#creating a function that separates vehicles into ranges by their age in years
def age_category(x):
    if x<5: return '<5'
    elif x>=5 and x<10: return '5-10'
    elif x>=10 and x<20: return '10-20'
    else: return '>20'

#applying the age category function to the age column to create a new column
df['age_category'] = df['age'].apply(age_category)

list_for_scatter = ['odometer', 'cylinders', 'days_listed']

choice_for_scatter = st.selectbox('Select a variable', list_for_scatter)

fig2 = px.scatter(df, x= "price", y= choice_for_scatter, color= "age_category", hover_data=['model_year'], range_x=[0, 100000])
fig2.update_layout(title= "<b> Visual of price by {}</b>".format(choice_for_scatter))

st.plotly_chart(fig2)
