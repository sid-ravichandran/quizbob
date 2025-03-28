import os
import streamlit as st
from serpapi import GoogleSearch
from dotenv import load_dotenv


load_dotenv()

def get_openai_key():
    return os.getenv("OPENAI_API_KEY")


def get_serpapi_key():
    return os.getenv("SERPAPI_API_KEY")


def generate_qa(client, entities, difficulty):
    """
    Generate a quiz question and answer based on the provided entities.
    Args:
        client: The OpenAI API client.
        entities: A list of entities (people, places, events, or things)."""

    if len(entities) > 1:
        entities_str = ", ".join(entities[:-1]) + " and " + entities[-1]
    else:
        entities_str = entities[0] if entities else ""

    question = f"What links the following entities: {entities_str}? The entities can be people, places, events or things."

    response = client.responses.create(
        model="gpt-4o",
        instructions=f"You are a clever quiz question generation assistant. \
            Use your vast bank of knowledge of world personalities, events and trivia to generate a quiz question and its answer \
            that links the provided personalities and events. Make it fun, interesting and engaging and at the same provide clues that will help in working out the answer. \
            The question should be of difficulty level {difficulty}\
            The answer should be a concrete person, place, event or thing. \
            The question and answer should each be at least 1 full sentence minimum and 2 full sentences maximum. \
            In addition, also generate a very short summary phrase that best captures the answer \
            Format your response like this: 'Question: <question>? | Answer: <answer> | Summary: <summary>'",
        input=question,
        temperature=0.0,
    )

    return response.output_text


def extract_qa(qa):
    """Extract the question, answer, and summary from the generated QA string (output from "generate_qa" function).
    Args:
        qa: The generated QA string."""
    
    question, answer, summary = qa.split("|")
    question = question.replace("Question:", "").strip()
    answer = answer.replace("Answer:", "").strip()
    summary = summary.replace("Summary:", "").strip()
    
    return question, answer, summary


def serp_search(query):
    """ Search for google images using SerpAPI.
    Args:
        query: The search query."""

    results = GoogleSearch({
        'serp_api_key': get_serpapi_key(),
        'tbm': 'isch',
        'q': query,
    })

    return results.get_dict()['images_results'][0]['original']


def generate_qa_with_image(client):
    """Generate a quiz question and answer based on the provided entities and search for an image using SerpAPI.
    Args:
        client: The OpenAI API client.
    """
    
    qa = generate_qa(client, st.session_state['entities'], st.session_state['difficulty'])
    question, answer, summary = extract_qa(qa)
    image = serp_search(summary)

    return question, answer, summary, image


#########################################

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def set_sessionstate():
    if 'question_available' not in st.session_state:
        st.session_state['question_available'] = False

    if 'question' not in st.session_state:
        st.session_state['question'] = None

    if 'answer' not in st.session_state:
        st.session_state['answer'] = None

    if 'summary' not in st.session_state:
        st.session_state['summary'] = None

    if 'image' not in st.session_state:
        st.session_state['image'] = None

    if 'answer_revealed' not in st.session_state:
        st.session_state['answer_revealed'] = False

    if 'entities' not in st.session_state:
        st.session_state['entities'] = []

    if 'difficulty' not in st.session_state:
        st.session_state['difficulty'] = None


def reset_sessionstate():
    """Reset the session state variables."""

    st.session_state['question_available'] = False
    st.session_state['question'] = None
    st.session_state['answer'] = None
    st.session_state['summary'] = None
    st.session_state['image'] = None
    st.session_state['answer_revealed'] = False
    st.session_state['entities'] = []
    st.session_state['difficulty'] = None
    st.session_state['entity1'] = None
    st.session_state['entity2'] = None
    st.session_state['entity3'] = None
    # st.rerun()


def reveal_answer():
    """Reveal the answer when the button is clicked."""
    st.session_state['answer_revealed'] = True
