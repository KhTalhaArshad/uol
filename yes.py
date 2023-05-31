import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

tag = st.selectbox('Choose a topic', ['love', 'humor', 'life', 'books'])

generate = st.button('Generate CSV')

url = f"https://quotes.toscrape.com/tag/{tag}/"

res = requests.get(url)

content = BeautifulSoup(res.content, 'html.parser')

quotes = content.find_all('div', class_='quote')

quote_file = []  # Create an empty list to store quotes

for quote in quotes:
    text = quote.find('span', class_='text').text
    author = quote.find('small', class_='author').text
    link = quote.find('a')
    st.success(text)
    st.markdown(f"<a href='https://quotes.toscrape.com{link['href']}'>{author}</a>", unsafe_allow_html=True)
    quote_file.append([text, author, link['href']])

if generate:
    try:
        df = pd.DataFrame(quote_file, columns=['Quote', 'Author', 'Link'])
        df.to_csv('quotes.csv', index=False, encoding='utf-8-sig')
        st.write("CSV file generated successfully!")
    except:
        st.write('Error generating CSV file.')
