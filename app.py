import time
from PIL import Image
import streamlit as st
from streamlit_lottie import *
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI, HarmCategory, HarmBlockThreshold

# [STREAMLIT] PAGE CONFIGURATION
icon = Image.open("icon.png")
st.set_page_config(page_title="MovieGeek", page_icon=icon)
st.logo("logo.svg", link="https://moviegeek.streamlit.app/")

def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

lottie_anim1 = load_lottiefile('film.json')

# [LANGCHAIN] GOOGLE API KEY CONFIGURATION
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]

# [STREAMLIT] HIDE MENU
hide_menu = """
    <style>
    #MainMenu {
        visibility: hidden;
    }
    footer {
        visibility: hidden;
    }
    div[data-testid="stDecoration"] {
        visibility: hidden;
        height: 0%;
        position: fixed;
    }
    div[data-testid="stStatusWidget"] {
        visibility: hidden;
        height: 0%;
        position: fixed;
    }
    </style>
    """
st.markdown(hide_menu, unsafe_allow_html = True)

# [STREAMLIT] ADJUST TOP PADDING
top = """
    <style>
    .block-container {
        padding-top: 3rem;
        padding-bottom: 3rem;
        margin-top: 0rem;
    }
    </style>
    """
st.markdown(top, unsafe_allow_html=True)

# [STREAMLIT] JUSTIFY MARKDOWN TEXT
justify = """
    <style>
    [data-testid="stMarkdownContainer"] {
        text-align: justify;
    }
    </style>
    """
st.markdown(justify, unsafe_allow_html=True)

# [STREAMLIT] CENTER IMAGE
center = """
    <style>
    [data-testid="stImage"] {
        justify-content: center;
    }
    </style>
    """
st.markdown(center, unsafe_allow_html=True)

# [STREAMLIT] HIDE IMAGE FULLSCREEN BUTTON
fsbutton = """
    <style>
    [data-testid="StyledFullScreenButton"] {
        visibility: hidden;
    }
    </style>
    """
st.markdown(fsbutton, unsafe_allow_html=True)

# [LANGCHAIN] FUNCTION TO STREAM AI RESPONSE
def stream_data(content):
    for word in content.split(" "):
        yield word + " "
        time.sleep(0.05)

# [STREAMLIT] LOGO
st.image(image="logo.svg", width=400, use_column_width="auto")

# [STREAMLIT] SUBHEADER
st.markdown("<p style='text-align: center; font-size: 1.2rem;'>Generate movie ideas with AI.</p>", unsafe_allow_html=True)

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

# [STREAMLIT] IF TRUE, SHOW RESPONSE
generated = False

# [STREAMLIT] MAIN UI
with st.container(border=True):
    options = st.multiselect(label="**GENRES**",
                            options=movie_genres,
                            placeholder="Choose a genre",
                            max_selections=3)

    generate = st.button(label="**GENERATE**",
                        type="primary",
                        use_container_width=True)
    
    # [STREAMLIT] WHEN BUTTON IS CLICKED
    if generate:
        
        # [LANGCHAIN] GENERATE A RESPONSE USING THE GEMINI LLM
        try:
            if 'Romance' not in options:
                options = ', '.join(options)
                template = """
                Please generate a non-explicit movie title and medium-length synopsis based on these genres:
                {genres}
                """
            else:
                options = ', '.join(options)
                template = """
                Please generate a family-friendly, lighthearted and non-explicit movie title and synopsis based on these genres:
                {genres}
                """
            prompt = PromptTemplate.from_template(template)
    
            llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash",
                                         temperature=1.0,
                                         google_api_key=GOOGLE_API_KEY,
                                         safety_settings={HarmCategory.HARM_CATEGORY_UNSPECIFIED: HarmBlockThreshold.BLOCK_NONE,
                                                          HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE})
            chain = prompt | llm
            result = chain.invoke({"genres": options})
            content = result.content

            # [LANGCHAIN] MAKE SURE CONTENT IS NOT EMPTY
            while len(content) == 0:
                time.sleep(2)
                result = chain.invoke({"genres": options})
                content = result.content
                
            generated = True

        # [STREAMLIT] RERUN APP IF ERROR OCCURS
        except Exception as e:
            st.rerun()

# [STREAMLIT] SHOW RESPONSE
if generated:
    st_lottie(lottie_anim1, loop=True, quality='high', height=100)
    time.sleep(2)
    #progress_text = "Writing the script. Please wait."
    #my_bar = st.progress(0, text=progress_text)
    #for percent_complete in range(100):
        #time.sleep(0.01)
        #my_bar.progress(percent_complete + 1, text=progress_text)
    #time.sleep(1)
    #my_bar.empty()
    
    content = content.replace("Synopsis:", "^").replace("*","").replace("Movie Title:","").replace("Title:","").replace('"', '').replace("#","").replace("\n","")
    content_list = content.split("^")
    title = f"###{content_list[0]}"
    synopsis = content_list[1]
    
    st.write(stream_data(title))
    st.write(stream_data(synopsis))
