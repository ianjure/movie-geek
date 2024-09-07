import os
import time
import streamlit as st
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

# [STREAMLIT] PAGE CONFIGURATION
st.set_page_config(page_title="MovieGeek", page_icon=":robot:")

# [STREAMLIT] ADJUST TOP PADDING
top = """
    <style>
    .block-container {
        padding-top: 5rem;
        padding-bottom: 0rem;
        margin-top: 0rem;
    }
    </style>
        """
st.markdown(top, unsafe_allow_html=True)

# [LANGCHAIN] GOOGLE API KEY CONFIGURATION
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]

# [LANGCHAIN] STREAM AI RESPONSE
def stream_data(content):
    for word in content.split(" "):
        yield word + " "
        time.sleep(0.08)

# LIST OF ALL MOVIE GENRES
movie_genres = [
    "Action",
    "Adventure",
    "Animation",
    "Biography",
    "Comedy",
    "Crime",
    "Documentary",
    "Drama",
    "Family",
    "Fantasy",
    "History",
    "Horror",
    "Musical",
    "Mystery",
    "Romance",
    "Sci-Fi",
    "Sport",
    "Thriller",
    "War",
    "Western"
]

# [STREAMLIT] MAIN UI
with st.container(border=True):
    options = st.multiselect(label="Select movie genres", options=movie_genres, max_selections=3)
    generate = st.button("Generate", type="primary", use_container_width=True)
    
    # [STREAMLIT] WHEN BUTTON IS CLICKED
    if generate:

        # [LANGCHAIN] GENERATE A RESPONSE USING THE GEMINI LLM
        template = """
        Generate a movie title and synopsis based on these genres:
        {genres}

        Follow this format and make sure that the output is in markdown form:
        (TITLE)
        (SYNOPSIS)
        """
        prompt = PromptTemplate.from_template(template)

        llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=GOOGLE_API_KEY)
        chain = prompt | llm
        result = chain.invoke({"genres": options})
        content = result.content

        # [STREAMLIT] SHOW RESPONSE
        st.write(stream_data(content))