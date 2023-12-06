import streamlit as st
from got_survival.ml_logic.model_character_creation import get_character
from got_survival.interface.main import death_pred, episode_pred
from got_survival.ml_logic.create_story import create_story
from got_survival.ml_logic.create_character_image import create_image
from got_survival.ml_logic.t_sne import get_tsne

def run():
    st.title('Create your Game of Thrones character')

    # Initiate button states
    if 'character' not in st.session_state:
        st.session_state.character = False
    if 'prediction' not in st.session_state:
        st.session_state.prediction = False

    # Create empty variables
    if 'cache' not in st.session_state:
        st.session_state.cache = {
            'character': '',
            'nobility': '',
            'outcast': '',
        }
    if 'outcast' not in st.session_state:
        st.session_state['outcast'] = 'No'
    if 'warm' not in st.session_state:
        st.session_state['warm'] = 'Warm'
    if 'empathy' not in st.session_state:
        st.session_state['empathy'] = 3
    if 'fighting' not in st.session_state:
        st.session_state['fighting'] = 3
    if 'honor' not in st.session_state:
        st.session_state['honor'] = 3
    if 'connections' not in st.session_state:
        st.session_state['connections'] = 3
    if 'unyielding' not in st.session_state:
        st.session_state['unyielding'] = 3
    if 'marriage' not in st.session_state:
        st.session_state['marriage'] = 'No'
    if 'gender' not in st.session_state:
        st.session_state['gender'] = 'Female'

    # Define functions to be called when buttons are clicked
    def click_button_character():
        st.session_state.character = True

    def click_button_prediction():
        st.session_state.prediction = True
        st.session_state.character = False


    # Display the questions for the character creation
    if (not st.session_state.character) and (not st.session_state.prediction):
        # Climate
        st.selectbox('What kind of climate do you prefer?',
                       ['Cold', 'Medium', 'Warm'], key='warm')
        '\n\n'
        st.write('Rate the following traits on a scale form 1 to 5:\n\n')
        st.slider('How empathic are you?', 1, 5, 3, 1, key='empathy')
        '\n\n'

        st.slider('How good are you at fighting?', 1, 5, 3, 1, key='fighting')
        '\n\n'

        st.slider('How honorable and loyal are you?', 1, 5, 3, 1, key='honor')
        '\n\n'

        st.slider('How good are you at negotiating, networking and building connections?',
                  1, 5, 3, 1, key='connections')
        '\n\n'

        st.slider('How likely are you to stand by what you believe regardless of \
            whether someone is trying to influence you in a different\
                direction?', 1, 5, 3, 1, key='unyielding')
        '\n\n'

        st.selectbox('Are you an outcast?', ['No', 'Yes'], key='outcast')
        st.number_input('Test your luck! Choose a number from 1 to 100!',
                                1, 100, 50, 1, key='guess')
        st.number_input('How old are you?', 1, 60, 30, 1, key='age')
        st.selectbox('Choose the gender for your character:', ['Female', 'Male'],
                     key='gender')
        st.selectbox('Are you married?', ['Yes', 'No'], key='marriage')

        '\n\n'
        st.button('Create character', on_click=click_button_character)

    '\n\n'
    # Create character and display information
    if st.session_state.character and (not st.session_state.prediction):
        st.session_state.cache['character'] = get_character(
            st.session_state['guess'],
            st.session_state['outcast'],
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

        if character['origin'][0] in ['Wildling', 'Dothraki', 'Soldier',
                        'Foreign Noble', 'Foreign Peasant', 'Noble', 'Peasant']:
            st.write(f'In the world of Game of Thrones you would be a \
                {character["origin"][0]}!')
        elif 'House' in character['origin'][0]:
            st.write(f'In the world of Game of Thrones you would be part of \
                {character["origin"][0]}!')
        elif character['origin'][0] == 'Outlaw':
            st.write(f'In the world of Game of Thrones you would be an \
                {character["origin"][0]}!')
        else:
            st.write(f'In the world of Game of Thrones you would be part of the \
                {character["origin"][0]}!')

        st.write(f'In terms of luck you are {character["lucky"][0]}, you are \
            {st.session_state["age"]} years old, \
            {round(character["popularity"][0] * 100)}% popular, \
                {st.session_state["gender"].lower()} and {nobility}!')
        if character["isMarried"][0]:
            st.write('You are also married!')

        '\n\n'
        st.button('Will you survive?', on_click=click_button_prediction)



    if st.session_state.prediction:
        character = st.session_state.cache['character']
        st.write('Will you survive?')
        if death_pred(character.drop(columns='lucky')):
            st.write('YES! YOU MADE IT')

            # Change comments from the default image to have one created:
            #st.image(create_image(character, st.session_state.cache["age"]))
            st.image("processed_data/images/3186f9f7-9b16-467c-a913-7d3e79050863.png")
        else:
            st.write('Nooooo......')
            st.write(f'You die in episode {episode_pred(character.drop(columns="lucky"))} 😢')

            # Change comments from the default image and story to have them created:
            # st.image(create_image(character, st.session_state.cache["age"]))
            st.image("processed_data/images/3186f9f7-9b16-467c-a913-7d3e79050863.png")

            st.write(f'Here is how you die:')
            # st.write(create_story(character, st.session_state.cache["age"]))
            st.write('You pass away tragically.')

        #st.write(st.session_state)

        fig = get_tsne(
                st.session_state['outcast'],
                st.session_state['warm'],
                st.session_state['empathy'],
                st.session_state['fighting'],
                st.session_state['honor'],
                st.session_state['connections'],
                st.session_state['unyielding'],
            )
        st.plotly_chart(fig)





run()
