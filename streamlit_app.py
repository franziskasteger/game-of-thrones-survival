import streamlit as st
from got_survival.ml_logic.model_character_creation import get_character
from got_survival.interface.main import death_pred, episode_pred

def run():
    st.title('Create your Game of Thrones character')

    if 'clicked' not in st.session_state:
        st.session_state.clicked = False

    def click_button():
        st.session_state.clicked = True

    warm = st.selectbox('What kind of climate do you prefer?',\
        ['Medium', 'Warm', 'Cold'])
    '\n\n'

    st.write('Rate the following traits on a scale form 1 to 5:\n\n')

    empathy = st.slider('How empathic are you?', 1, 5, 3, 1, key='emp')
    '\n\n'

    fighting = st.slider('How good are you at fighting?', 1, 5, 3, 1, key='fight')
    '\n\n'

    honor = st.slider('How honorable and loyal are you?', 1, 5, 3, 1, key='hon')
    '\n\n'

    connections = st.slider('How good are you at negotiating, networking and\
        building connections?', 1, 5, 3, 1, key='con')
    '\n\n'

    unyielding = st.slider('How likely are you to stand by what you believe\
        regardless of whether someone is trying to influence you in a different\
            direction?', 1, 5, 3, 1, key='uny')
    '\n\n'

    yes = st.selectbox('Are you an outcast?', ['No', 'Yes'])
    if yes == 'Yes':
        outcast = 1
    else:
        outcast = 0

    guess = st.number_input('Test your luck! Choose a number from 1 to 100!',
                            1, 100, 50, 1, key='luck')
    age = st.number_input('How old are you?', 1, 60, 30, 1, key='age')
    gender = st.selectbox('Choose the gender for your character:', ['Female', 'Male'])
    marriage = st.selectbox('Are you married', ['Yes', 'No'])

    '\n\n'
    st.button('Create character', on_click=click_button)
    character = get_character(guess, outcast, warm, empathy, fighting, honor, connections,
                              unyielding, gender, marriage)
    if character["isNoble"][0]:
        nobility = 'noble'
    else:
        nobility = 'not noble'

    '\n\n'
    if st.session_state.clicked:
        if character['origin'][0] in ['Wildling', 'Dothraki', 'Soldier', 'Foreign Noble',
                     'Foreign Peasant', 'Noble', 'Peasant']:
            st.write(f'In the world of Game of Thrones you would be a {character["origin"][0]}!')
        elif 'House' in character['origin'][0]:
            st.write(f'In the world of Game of Thrones you would be part of {character["origin"][0]}!')
        elif character['origin'][0] == 'Outlaw':
            st.write(f'In the world of Game of Thrones you would be an {character["origin"][0]}!')
        else:
            st.write(f'In the world of Game of Thrones you would be part of the {character["origin"][0]}!')

        st.write(f'In terms of luck you are {character["lucky"][0]}, you are {age} years old, \
            {round(character["popularity"][0] * 100)}% popular, {gender.lower()} and {nobility}!')
        if character["isMarried"][0]:
            st.write('You are also married!')

        '\n\n'
        if st.button('Will you survive?'):
            if death_pred(character.drop(columns='lucky')):
                st.write('YES! YOU MADE IT')
            else:
                st.write('Nooooo......')
                st.write(f'You die in episode {episode_pred(character.drop(columns="lucky"))} 😢')



run()
