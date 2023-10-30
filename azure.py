import streamlit as st
import pandas as pd
import openai
import os

# Load your dataset
file_path = "lyrics_dataset_all.csv"  # Update the path to your dataset
df = pd.read_csv(file_path)

# Filter the dataset to keep only the 'artist' and 'lyrics' columns
artist_lyrics = df[['artist', 'lyrics']]


#config_ini_location = 'config.ini' # Change this to point to thelocation of your config.ini file.
openai.api_key = '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'

#import configparser
#config = configparser.ConfigParser()
#config.read(config_ini_location)
#openai_api_key = config['OpenAI']['API_KEY']


# Streamlit app title
st.title("Lyrics Generator")

# Dropdown to select the artist
selected_artist = st.selectbox('Select an artist:', artist_lyrics['artist'].unique())

# Function to generate lyrics based on selected artist
def generate_lyrics(artist):
    artist_lyrics = df[df['artist'] == artist]['lyrics'].dropna().tolist()
    combined_lyrics = '\n'.join(artist_lyrics[:5])  # Reduce the total lines to fit within context limits
    combined_lyrics = combined_lyrics[:2048]  # Limit the total characters to 2048 to fit token limits
    prompt = f"Generate lyrics in the style of {artist}\n\n{combined_lyrics}"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=100
    )
    return response['choices'][0]['text'].strip()

# Generate and display lyrics based on the selected artist when the button is clicked
if selected_artist:
    if st.button('Generate Lyrics'):
        generated_lyrics = generate_lyrics(selected_artist)
        st.write(generated_lyrics)
