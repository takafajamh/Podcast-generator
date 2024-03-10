"""Streamlit app to generate Tweets."""

# Import from standard library
import logging
import random
import re

# Import from 3rd party libraries
import streamlit as st
import streamlit.components.v1 as components
import streamlit_analytics

# Import modules
import tweets as twe
import oai

# Configure logger
logging.basicConfig(format="\n%(asctime)s\n%(message)s", level=logging.INFO, force=True)


# Define functions
def generate_text(topic: str, mood: str = "", length: str = ""):
    if st.session_state.n_requests >= 5:
        st.session_state.text_error = "Too many requests. Please wait a few seconds before generating another Tweet."
        logging.info(f"Session request limit reached: {st.session_state.n_requests}")
        st.session_state.n_requests = 1
        return

    st.session_state.tweet = ""
    st.session_state.text_error = ""

    if not topic:
        st.session_state.text_error = "Prosze wpisz temat"
        return

    with text_spinner_placeholder:
        with st.spinner("Proszę poczekać, podcast jest generowany..."):
            mood_prompt = f"{mood} " if mood else ""
            prompt = f"Napisz mi scenariusz podcastu, w podcaście rozmawiają dwie osoby, zacznij ich tekst od A:, lub B:. Podcast ma być na temat {topic}, ma być prowadzony w nastroju {mood}, długościowo ma być {length}. Tekst od razu ma zaczynać dialog, bez napisu - scenariusz, bez wypisania aktorów\n\n"
            
            openai = oai.Openai()
            flagged = openai.moderate(prompt)
            mood_output = f", Nastrój: {mood}" if mood else ""
            length_output = f", Długość: {length_output}" if length_output else ""

            if flagged:
                st.session_state.text_error = "Niepoprawny prośba."
                logging.info(f"Temat: {topic}{mood_output}{length_output}\n")
                return

            else:
                st.session_state.text_error = ""
                st.session_state.n_requests += 1
                streamlit_analytics.start_tracking()
                st.session_state.tweet = (
                    openai.complete(prompt=prompt).strip().replace('"', "")
                )
                logging.info(
                    f"Temat: {topic}{mood_output}{length_output}\n"
                )


# Configure Streamlit page and state
st.set_page_config(page_title="Generator podcastów", page_icon="🤖")

if "tweet" not in st.session_state:
    st.session_state.tweet = ""
if "text_error" not in st.session_state:
    st.session_state.text_error = ""
if "feeling_lucky" not in st.session_state:
    st.session_state.feeling_lucky = False
if "n_requests" not in st.session_state:
    st.session_state.n_requests = 0

# Force responsive layout for columns also on mobile
st.write(
    """<style>
    [data-testid="column"] {
        width: calc(50% - 1rem);
        flex: 1 1 calc(50% - 1rem);
        min-width: calc(50% - 1rem);
    }
    </style>""",
    unsafe_allow_html=True,
)

# Render Streamlit page
streamlit_analytics.start_tracking()
st.title("Generuj podcasty")
st.markdown(
    "Generuj podcast na dowolny temat :) Aplikacja służy za proof of concept projektu"
)

topic = st.text_input(label="Temat podcastu", placeholder="Teens in AI")
mood = st.text_input(
    label="Nastrój - profesjonalny, kreatywny, żartobliwy",
    placeholder="kreatywny",
)
length = st.text_input(
    label="Długość podcastu",
    placeholder="krótki",
)

col1, col2 = st.columns(2)
with col1:
    st.session_state.feeling_lucky = not st.button(
        label="Generuj podcast",
        type="primary",
        on_click=generate_text,
        args=(topic, mood, style),
    )

text_spinner_placeholder = st.empty()
if st.session_state.text_error:
    st.error(st.session_state.text_error)

if st.session_state.tweet:
    with col2:
        st.button(
            label="Generuj jeszcze raz",
            type="secondary",
            on_click=generate_text,
            args=(topic, mood, style),
        )


    image_spinner_placeholder = st.empty()
    if st.session_state.image_error:
        st.error(st.session_state.image_error)

    st.markdown("""---""")
    col1, col2 = st.columns(2)


streamlit_analytics.stop_tracking()
