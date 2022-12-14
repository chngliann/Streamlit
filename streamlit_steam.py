from dataclasses import dataclass
import streamlit as st #to host on web app
import pandas as pd #to read/manipulate data
import numpy as np #to perform calcs
import plotly.express as px #to plot diagrams
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt #to plot and prevent xticks and yticks

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
    #df[''] = pd.to_datetime(df['']) #this converts the datetime to pandas datetime format
    return df

#argument to pass to display
df = load_data()

#st.write(df.query("user_suggestion == 1")) #to debug

st.sidebar.subheader('Show random review')
#radio buttons to select sentiment type
random_review = st.sidebar.radio('Select Recommendation', (1, 0))
#use pandas to query dataset for a random tweet corresponding to sentiment selected in radio
st.sidebar.markdown(df.query("user_suggestion == @random_review")[["user_review"]].sample(n=1).iat[0,0])



######### plot graphs based on user selection ##########

st.sidebar.markdown("### Number of reviews by recommendation")
select_widget = st.sidebar.selectbox('Visualisation type', ['Histogram', 'Pie chart'], key='1')

rec_count = df['user_suggestion'].value_counts() #new dataframe (cause plotly expects tidy df)

#st.write(rec_count) shows 1s and 0s as rows, and their counts

rec_count = pd.DataFrame({'Recommendation': rec_count.index, 'Number':rec_count.values}) #creating dataframe out of dictionary
                                                                                        #actual reviews stored in index of pandas series, count of tweets stored in values of the pandas series

if not st.sidebar.checkbox("Hide", True): #by default, checkbox is checked (True)
    st.markdown("### Number of Reviews by Recommendation")
    if select_widget == "Histogram":
        fig = px.bar(rec_count, x='Recommendation', y='Number', color='Number', height=500)
        st.plotly_chart(fig)
    else:
        fig = px.pie(rec_count, names='Recommendation', values='Number')
        st.plotly_chart(fig)


####### plot location data on interactive map #######

st.sidebar.subheader("When and where are users writing from?")
hour = st.sidebar.slider("Hour of day", 0, 23)
#another input method
#st.sidebar.number_input("Hour of day", min_value=1, max_value=24)

#this dataset doesnt have long and lat though
#need 2 conditions 1) longitude and langitude columns 2) no missing data in those columns
#st.map(df) -> will just plot the map of all the points

# modified_data = df[df[''].dt.hour == hour]
# if not st.sidebar.checkbox("Close", True, key='1'):
#     st.markdown("Tweets location based on time of day")
#     st.markdown("%i tweets between %i:00 and %i:00" % len(modified_data), hour, (hour+1)%24)
#     st.map(modified_data)
#     if not st.sidebar.checkbox("Show Raw Data", False):
#         st.write(modified_data)








##### plot num of tweets by sentiment for each airline ######
st.sidebar.subheader("Breakdown Steam games recommendations by recommendation")
game_list = df.title.unique() # list of games
choice = st.sidebar.multiselect('Pick game', (game_list), key='0') #tuple of string as input

if len(choice) > 0:
    choice_data = df[df.title.isin(choice)]
    fig_choice = px.histogram(choice_data, x='title', y='user_suggestion', histfunc='count', color='user_suggestion',
    facet_col='user_suggestion', labels={'user_suggestion':'recommendations'}, height=500, width=600)
    #another way of presenting
    #fig_choice = px.histogram(choice_data, x="title", y="user_suggestion", color="title", pattern_shape="user_suggestion", histfunc='count')
    st.plotly_chart(fig_choice)



##### word cloud for positive/negative recommendations ##############
st.sidebar.header("Word Cloud")
word_radio = st.sidebar.radio("Display word cloud based on recommendation sentiment", (1, 0))

if not st.sidebar.checkbox("Close", True, key='3'):
    st.subheader('Word Cloud for %s sentiment' % word_radio)
    df_cloud = df[df['user_suggestion'] == word_radio] #get rows where match sentiment
    words = ' '.join(df_cloud['user_review']) #add spacing between words
    #word processing
    processed_words = ' '.join([word for word in words.split() if 'Early' not in word and not word.startswith('-') and word != 'Access'])
    word_cloud = WordCloud(stopwords=STOPWORDS, background_color='black', height=600, width=800).generate(processed_words)
    plt.imshow(word_cloud)
    plt.xticks([])
    plt.yticks([])
    st.pyplot() # plot the matlib figures