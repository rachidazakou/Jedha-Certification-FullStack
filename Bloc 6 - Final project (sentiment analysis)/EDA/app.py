import joblib
import streamlit as st
import pandas as pd
import plotly.express as px 
import plotly.graph_objects as go
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from plotly.subplots import make_subplots
from wordcloud import WordCloud, STOPWORDS
import matplotlib.colors as colors
sns.set_palette("deep")
from PIL import Image

# Page configuration 
st.set_page_config(
    page_title="CHATGPT - EDA",
    page_icon=" ",
    layout="wide"
)

st.title("Sentiment analysis on tweets about ChatGPT")

st.markdown("---")

data_path = ('df_new_labels.csv')

# Show a sample of the dataset
st.subheader("Load and showcase data")

@st.cache_data
def load_data():
    data = pd.read_csv(data_path, index_col=0)
    return data

data_load_state = st.text('Loading data...')
data = load_data()
data_shown = data.loc[:100,["tweets", "labels"]]
data_load_state.text("") 


if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data_shown)    

st.markdown("""
""")

st.subheader("EDA with Sunburst")

col00, col01 = st.columns(2)

with col00:
    method1 = st.selectbox("Method 1 ", ["Label", "Vader", "Afinn", "Textblob"])

with col01:
    method2 = st.selectbox("Method 2", ["Afinn", "Vader", "Textblob", "Label"])

if method1 == "Label":
    col1 = "labels"
elif method1 == "Vader":
    col1 = "vader_labels"
elif method1 == "Afinn":
    col1 = "afinn_labels"
else:
    col1 = "textblob_labels"

if method2 == "Label":
    col2 = "labels"
elif method2 == "Vader":
    col2 = "vader_labels"
elif method2 == "Afinn":
    col2 = "afinn_labels"
else:
    col2 = "textblob_labels"

palette = [colors.to_hex(c) for c in sns.color_palette("deep")]

fig = px.sunburst(
    data,
    path = [col1, col2],
    color = col1,
    color_discrete_sequence=palette)
fig.update_traces(textinfo='label+percent parent')
fig.update_layout(autosize=False,width=400,height=600)
st.plotly_chart(fig, use_container_width=True)


st.subheader("EDA with wordcloud")

st.markdown("""
    Postive / Negative words :

""")

choice = st.selectbox("Common words for : ", ["Positive", "Negative"])

if choice == "Positive":
    label = 'good'
else:
    label = 'bad'

mask = np.array(Image.open("comment.png"))


words = ''

stop_words = ['chatgpt', 'chatbot', 'openai', 'ai', 'use','write','google','ask', 'see','make','go','code'] + list(STOPWORDS)

for val in data.loc[data.labels==label,'cleaned_tweets_dl']:
  val = str(val)
  tokens = val.split()

  
  words += " ".join(tokens)+" "

wordcloud = WordCloud(width = 100, 
                      height = 100,
                      background_color ='white',
                      max_words=300,
                      collocations = False,
                      stopwords = stop_words,
                      min_font_size = 2,
                      color_func=lambda *args, **kwargs: np.random.choice(palette), 
                      mask=mask).generate(words)

fig, ax =plt.subplots()
plt.figure(facecolor = None)
ax.imshow(wordcloud,interpolation='bilinear')
ax.axis("off")

st.pyplot(fig)




col1, col2 = st.columns(2)

with col1:
    st.markdown("<h5 style='text-align: center;'>Before preprocessing</h5>", unsafe_allow_html=True)
    words = ''

    for val in data.tweets:
        val = str(val)
        tokens = val.split()
    
        words += " ".join(tokens)+" "
    wordcloud = WordCloud(width = 800, 
                          height = 800,
                          background_color ='white',
                          max_words=200,
                          collocations = False,
                          min_font_size = 5, 
                          color_func=lambda *args, **kwargs: np.random.choice(palette),
                          mask=mask).generate(words)

    # plot the WordCloud image 
    fig, ax =plt.subplots()
    plt.figure(figsize = (8, 8), facecolor = None)
    ax.imshow(wordcloud)
    ax.axis("off")
    plt.tight_layout(pad = 0)
    st.pyplot(fig)
    

with col2:
    st.markdown("<h5 style='text-align: center;'>After preprocessing</h5>", unsafe_allow_html=True)
    words = ''

    for val in data.cleaned_tweets_dl:
        val = str(val)
        tokens = val.split()

        words += " ".join(tokens)+" "
    wordcloud = WordCloud(width = 800, 
                          height = 800,
                          background_color ='white',
                          max_words=200,
                          stopwords = stop_words,
                          collocations = False,
                          min_font_size = 5,
                          color_func=lambda *args, **kwargs: np.random.choice(palette),
                          mask=mask).generate(words)

    # plot the WordCloud image 
    fig, ax =plt.subplots()
    plt.figure(figsize = (8, 8), facecolor = None)
    ax.imshow(wordcloud)
    ax.axis("off")
    plt.tight_layout(pad = 0)
    st.pyplot(fig)
