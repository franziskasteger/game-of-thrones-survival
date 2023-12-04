import streamlit as st
import pandas as pd
from got_survival.ml_logic.model_character_creation import get_character
from got_survival.interface.main import death_pred, episode_pred
from got_survival.ml_logic.create_story import create_story
from got_survival.ml_logic.create_character_image import create_image

# Constants
CLIMATE_OPTIONS = ['Cold', 'Medium', 'Warm']

def display_character_questions():
    st.sidebar.title('Character Questions')
    st.sidebar.selectbox('What kind of climate do you prefer?', CLIMATE_OPTIONS, key='warm')
    st.sidebar.write('Rate the following traits on a scale form 1 to 5:\n\n')
    st.sidebar.slider('How empathic are you?', 1, 5, 3, 1, key='empathy')
    st.sidebar.slider('How good are you at fighting?', 1, 5, 3, 1, key='fighting')
    st.sidebar.slider('How honorable and loyal are you?', 1, 5, 3, 1, key='honor')
    st.sidebar.slider('How good are you at negotiating, networking and building connections?', 1, 5, 3, 1, key='connections')
    st.sidebar.slider('How likely are you to stand by what you believe regardless of whether someone is trying to influence you in a different direction?', 1, 5, 3, 1, key='unyielding')
    st.sidebar.selectbox('Are you an outcast?', ['No', 'Yes'], key='outcast')
    if st.session_state['outcast'] == 'Yes':
        st.session_state.cache['outcast'] = 1
    else:
        st.session_state.cache['outcast'] = 0
    st.sidebar.number_input('Test your luck! Choose a number from 1 to 100!', 1, 100, 50, 1, key='guess')
    st.sidebar.number_input('How old are you?', 1, 60, 30, 1, key='age')
    st.sidebar.selectbox('Choose the gender for your character:', ['Female', 'Male'], key='gender')
    st.sidebar.selectbox('Are you married', ['Yes', 'No'], key='marriage')
    st.sidebar.button('Create character', on_click=run_character_creation)

def run_character_creation():
    st.title('Your character')

    st.session_state.cache['character'] = get_character(
        st.session_state['guess'],
        st.session_state.cache['outcast'],
        st.session_state['warm'],
        st.session_state['empathy'],
        st.session_state['fighting'],
        st.session_state['honor'],
        st.session_state['connections'],
        st.session_state['unyielding'],
        st.session_state['gender'],
        st.session_state['marriage']
    )

    character = st.session_state.cache['character']

    if character['isNoble'][0]:
        nobility = 'noble'
    else:
        nobility = 'not noble'

    if character['origin'][0] in ['Wildling', 'Dothraki', 'Soldier', 'Foreign Noble', 'Foreign Peasant', 'Noble', 'Peasant']:
        st.write(f'In the world of Game of Thrones you would be a {character["origin"][0]}!')
    elif 'House' in character['origin'][0]:
        st.write(f'In the world of Game of Thrones you would be part of {character["origin"][0]}!')
    elif character['origin'][0] == 'Outlaw':
        st.write(f'In the world of Game of Thrones you would be an {character["origin"][0]}!')
    else:
        st.write(f'In the world of Game of Thrones you would be part of the {character["origin"][0]}!')

    st.write(f'In terms of luck you are {character["lucky"][0]}, you are {st.session_state["age"]} years old, {round(character["popularity"][0] * 100)}% popular, {st.session_state["gender"].lower()} and {nobility}!')
    if character["isMarried"][0]:
        st.write('You are also married!')

    # elements to pass to create_image_character
    character = {
        'origin': character['origin'],
        'popularity': character['popularity'],
        'male': character['male'],
        'isNoble': character['isNoble'],
        'isMarried': character['isMarried'],
    }

    age = st.session_state['age']

    # work and gets the image
    #image, filename = create_image(character,age)

    # TODO: "call generate image for character" - create_image_character module - create_image(character,age) function
    #st.image(image=filename,use_column_width="auto") #this works

    #temporary solution
    filename = "processed_data/images/test_image.png"
    st.image(image="processed_data/images/test_image.png",use_column_width="auto")

    # Add a spacer between the image and buttons
    st.write("")

    col1, col2 = st.columns(2)

    with col1:
        try:
            # TODO: if i click the button it leaves the page, need to understand why
            with open(filename, "rb") as file: #filename
                st.download_button(
                    label="Download image",
                    data=file.read(),
                    file_name=filename,
                    key="download_button",
                    help="Click to download the image",
                )
        except FileNotFoundError:
            st.error("File not found. Please check the file path.")

    with col2:
        st.button('Will you survive?', on_click=display_survival_prediction)

def display_survival_prediction():
    character = st.session_state.cache['character']
    if death_pred(character.drop(columns='lucky')):
        st.title('You are alive 🎉')
        st.write('YES! YOU MADE IT')

        # TODO: "create story fo alive character"
        st.image("processed_data/images/test_image_alive.png")
    else:
        st.title('You went to Hell 😢')
        st.write('Nooooo......')

        # TODO: "call prediction for episode of death" - create_story module - create_story(character,age) function
        #st.write(f'You die in episode {episode_pred(character.drop(columns="lucky"))} 😢')

        st.image("processed_data/images/test_image_dead.png")
        st.write(f'Here is how you die:')
        # TODO: "create story fo dead character"- - create_story module - create_story(character,age) function
        st.write('You pass away tragically.')

def run():
    if 'title' not in st.session_state:
        st.session_state.title = False
        st.title('Create your Game of Thrones character')

    if 'character' not in st.session_state:
        st.session_state.character = False

    if 'prediction' not in st.session_state:
        st.session_state.prediction = False

    if 'cache' not in st.session_state:
        st.session_state.cache = {
            'title': '',
            'character': '',
            'nobility': '',
            'outcast': '',
        }

    if not st.session_state.character and not st.session_state.prediction:
        display_character_questions()

    if st.session_state.character and not st.session_state.prediction:
        run_character_creation()

    if st.session_state.prediction:
        display_survival_prediction()

if __name__ == "__main__":
    run()
