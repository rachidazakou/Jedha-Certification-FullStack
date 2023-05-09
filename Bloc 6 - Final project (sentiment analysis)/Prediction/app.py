import joblib
import streamlit as st
import pandas as pd
import numpy as np
import transformers
import torch
import re
from tokenizers import Tokenizer
import tensorflow as tf
import spacy
import en_core_web_sm
nlp = en_core_web_sm.load()
en = spacy.load('en_core_web_sm')
stop = en.Defaults.stop_words

from nltk.corpus import stopwords


# Page configuration
st.set_page_config(
    page_title="CHATGPT - Prediction",
    page_icon=" ",
    layout="wide"
)


st.subheader("Predict the sentiment of a tweet")


tweet_text = st.text_input("Enter a sentence : ")

# Box to select a model
model = st.selectbox("Select a model : ", ["LSTM", "Roberta"])


# Manage predictions according to the chosen model
if model == "LSTM" and st.button("Submit"):
    with st.spinner(text="Please wait while the LSTM model is predicting..."):
        MAX_WORDS = 10000
        EMBEDDING_SIZE = 48

        labels = ['Negative','Neutral','Positive']
        
        model = tf.keras.models.load_model("model_lstm.h5")

        with open("tokenizer.pkl", "rb") as f:
            tokenizer = joblib.load(f)

        # Preprocessing 
        tweet_text = tweet_text.lower()    
        tweet_text = re.sub(r'@\w+', '', tweet_text)
        tweet_text = re.sub(r'#\w+', '', tweet_text)
        tweet_text = re.sub(r'http\S+', '', tweet_text)
        tweet_text = re.sub(r'https\S+', '', tweet_text)
        tweet_text = re.sub(r'&amp;', '&', tweet_text)
        tweet_text = re.sub(r'[^\w\s]', '', tweet_text)
        tweet_text = " ".join([token.lemma_ for token in nlp(tweet_text) if (token.lemma_ not in stop) & (token.text not in stop) & (token.lemma_.isalnum())])
        tweet_seq = tokenizer.texts_to_sequences([tweet_text])
        tweet_seq_padded = tf.keras.preprocessing.sequence.pad_sequences(tweet_seq,padding='post', maxlen=EMBEDDING_SIZE)
        
        # Predict the tweet sentiment
        sentiment_class = model.predict(tweet_seq_padded).argmax(axis=1)
        # Display the sentiment
        st.write("Prediction : ", labels[sentiment_class[0]])
        

elif model == "Roberta" and st.button("Submit"):

    with st.spinner(text="Please wait while the Roberta model is predicting..."):
        model_roberta = "cardiffnlp/twitter-roberta-base-sentiment"
        tokenizer = transformers.AutoTokenizer.from_pretrained(model_roberta)
        model1 = transformers.AutoModelForSequenceClassification.from_pretrained(model_roberta)
        
        encoded_tweet = tokenizer.encode_plus(
            tweet_text,
            add_special_tokens=True,
            max_length=128,
            pad_to_max_length=True,
            return_attention_mask=True,
            return_tensors="pt",
        )

        with torch.no_grad():
            logits = model1(encoded_tweet["input_ids"], encoded_tweet["attention_mask"])[0]

        sentiment = torch.argmax(logits).item()
        if sentiment == 0:
            st.write("Prediction : Negative")
        elif sentiment == 1:
            st.write("Prediction : Neutral")
        else:
            st.write("Prediction : Positive")