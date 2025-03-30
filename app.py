import streamlit as st
from openai import OpenAI
from functions import *


# Set page configuration
st.set_page_config(page_title="Quizbob!", page_icon=":brain:")
set_sessionstate()
local_css("style.css")

#############################

st.image("quizbob_banner.png")

st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Josefin+Sans:ital,wght@0,100..700;1,100..700&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# Title and description
# st.markdown('<p class="title-font">🧠 Quizbob!</p>', unsafe_allow_html=True)
st.title("🧠 :blue[QuizBob!]")

st.markdown('<div class="description-text">Explore the connections in the world around us through Quizzing 🌍<br><br>\
            Here\'s how it to play:<ul><li>\
            Provide <strong>up to 3</strong> entities and I\'ll generate a question for you that connects them</li><li>\
            To test your knowledge - take some time and try to work out the answer before you enter it, or you could just choose to reveal the answer if you prefer!</li><li>\
            Get a score that evaluates how well you got the answer!</li></ul><br>HAPPY QUIZZING! 🎉</div><br>', unsafe_allow_html=True)

# st.markdown('<p style="text-align: center; font-size: 1.2rem;">Happy Quizzing! 🎉</p>', unsafe_allow_html=True)

#############################

openai_client = OpenAI(api_key=get_openai_key())

#############################
ccol1, col2, col3 = st.columns([1, 6, 1])

with col2:
    with st.form(key='input_form'):
        st.write("Enter up to three entities (people, places, events, or things) to generate a quiz question that connects them.\
                 \n\nFor most reliable results, please only enter well known personalities/events/places!")

        col1, col2 = st.columns([1,7])

        col1.write("1.")
        col2.text_input("dummy", placeholder="Enter a person, place, event or thing...", key="entity1", label_visibility='collapsed')

        col1.write("2.")
        col2.text_input("dummy", placeholder="Enter a person, place, event or thing...", key="entity2", label_visibility='collapsed')

        col1.write("3.")
        col2.text_input("dummy", placeholder="Enter a person, place, event or thing...", key="entity3", label_visibility='collapsed')

        diff = st.segmented_control("dummy", ["Normal please", "Challenge me!"], default="Normal please",
                                    selection_mode="single", key="diff_input", label_visibility='collapsed')
        if diff == "Normal please":
            st.session_state['difficulty'] = "medium"
        else:
            st.session_state['difficulty'] = "hard"

        # Submit button
        submit_button = st.form_submit_button(label='Go!')

        if submit_button:
            # Get the values from the form
            entity1 = st.session_state.entity1
            entity2 = st.session_state.entity2
            entity3 = st.session_state.entity3

            # Display the selected entities
            entities = [entity1, entity2, entity3]
            st.session_state['entities'] = [entity for entity in entities if entity is not None and entity.strip() != ""]

            if len(st.session_state['entities']) > 0:
                st.session_state['question'], st.session_state['answer'], st.session_state['summary'], st.session_state['image'] = generate_qa_with_image(openai_client)
                st.success("Quiz question generated!", icon="✅")
                st.session_state['question_available'] = True
                st.session_state['answer_revealed'] = False
            else:
                st.warning("Please enter at least one entity.", icon="⚠️")


#############################

if st.session_state['question_available']:
    st.subheader("The Question...")

    # st.write(st.session_state['question'])
    st.markdown(
        f'<div class="blockquote-wrapper"><div class="blockquote"><h1><span style="color:#ffffff">{st.session_state.question}</span></h1><h4>&mdash; Question</em></h4></div></div>',
        unsafe_allow_html=True,
    )

    answer_entered = st.text_input("dummy", placeholder="Enter your answer here...", key="user_answer", label_visibility='collapsed')
    answer_reveal = st.button("Just Tell me the Answer! :popcorn:", on_click=reveal_answer(), key='answer_button')

    if answer_entered:
        eval = evaluate_answer(openai_client, st.session_state['answer'], st.session_state['user_answer'])

        if eval is not None:
            st.write(eval)
            st.image(st.session_state['image'], caption=st.session_state['summary'])
            st.button("Cool! Let's go again :arrows_counterclockwise:", on_click=reset_sessionstate, key='start_over_button')

    elif answer_reveal & st.session_state['answer_revealed']:
        st.subheader("The Answer...")
        # st.write(st.session_state['answer'])
        st.markdown(
            f'<div class="blockquote-wrapper"><div class="blockquote"><h1><span style="color:#ffffff">{st.session_state.answer}</span></h1><h4>&mdash; Answer</em></h4></div></div>',
            unsafe_allow_html=True,
        )
        
        st.image(st.session_state['image'], caption=st.session_state['summary'])
        st.button("Cool! Let's go again :arrows_counterclockwise:", on_click=reset_sessionstate, key='start_over_button_2')
            
