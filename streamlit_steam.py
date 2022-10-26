from dataclasses import dataclass
import streamlit as st #to host on web app
import pandas as pd #to read/manipulate data
import numpy as np #to perform calcs

#create web app run on streamlit
#requires to run "streamlit run app.py" in Terminal
st.title("Sentiment Analysis of Tweets about Games/Banks?")
st.sidebar.title("Filters")

st.markdown("This is a Streamlit dashboard used to analyse the sentiments of Steam reviews 🎮 ")
st.sidebar.markdown("Contains some interactive filters")

#argument to be passed into pandas to be read as a df
DATA_URL = (r"C:\Users\chngl\OneDrive\Documents\GitHub\Streamlit\train.csv")

#function decorator in Streamlit to cache output data - function will not run unless input / code changes
@st.cache(persist=True)

#function to load/compute data manipulations
def load_data():
    df = pd.read_csv(DATA_URL)
    #column manipulation
    #df[''] = pd.to_datetime(df[''])
    return df

#argument to pass to display
df = load_data()

#st.write(df.query("user_suggestion == 1")) #to debug

st.sidebar.subheader('Show random review')
#radio buttons to select sentiment type
random_review = st.sidebar.radio('Select Recommendation', (1, 0))
#use pandas to query dataset for a random tweet corresponding to sentiment selected in radio
st.sidebar.markdown(df.query("user_suggestion == @random_review")[["user_review"]].sample(n=1).iat[0,0])