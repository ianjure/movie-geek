import os
import time
import streamlit as st
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

# [LANGCHAIN] GOOGLE API KEY CONFIGURATION
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]

# [LANGCHAIN] STREAM AI RESPONSE
def stream_data(content):
    for word in content.split(" "):
        yield word + " "
        time.sleep(0.08)

# [STREAMLIT] REMOVE TOP PADDING
top = """
    <style>
    .block-container {
        padding-top: 0rem;
        padding-bottom: 0rem;
        margin-top: 0rem;
    }
    </style>
        """
st.markdown(top, unsafe_allow_html=True)

# [STREAMLIT] PAGE CONFIGURATION
st.set_page_config(page_title="MovieGeek", page_icon=":robot:")

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
with st.container(Border=True):
    options = st.multiselect(label="Select movie genres", options=movie_genres, max_selections=3)
    generate = st.button("Generate", type="primary")
    
    # [STREAMLIT] WHEN BUTTON IS CLICKED
    if generate:

        # [LANGCHAIN] GENERATE A RESPONSE USING THE GEMINI LLM
        template = """
        Create a short movie synopsis based on these genres:
        {genres}
        """
        prompt = PromptTemplate.from_template(template)

        llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=GOOGLE_API_KEY)
        chain = prompt | llm
        result = chain.invoke({"genres": options})
        content = result.content

        # [STREAMLIT] SHOW RESPONSE
        st.write(stream_data(content))