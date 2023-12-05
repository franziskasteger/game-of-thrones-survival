import streamlit as st
from got_survival.ml_logic.model_character_creation import get_character
from got_survival.interface.main import death_pred, episode_pred
from got_survival.ml_logic.create_story import create_story
from got_survival.ml_logic.create_story_char import create_character_story
from got_survival.ml_logic.create_story_dead import create_character_dead
from got_survival.ml_logic.create_story_alive import create_character_alive
from got_survival.ml_logic.create_character_image import create_image

CLIMATE_OPTIONS = ['Cold', 'Medium', 'Warm']

st.set_page_config(
    page_title="Create your Game of Thrones character",
    page_icon=":chart_with_upwards_trend:",
    layout="wide",
)


def run():
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
            'age': '',
        }

    # Define functions to be called when buttons are clicked
    def click_button_character():
        st.session_state.character = True

    def click_button_prediction():
        st.session_state.prediction = True
        st.session_state.character = False


    # Display the questions for the character creation
    if (not st.session_state.character) and (not st.session_state.prediction):
        st.markdown("<h1 style='text-align: center; color: grey;'>Create your Game of Thrones character</h1>", unsafe_allow_html=True)

        st.selectbox('What kind of climate do you prefer?', CLIMATE_OPTIONS, key='warm')

        col1, col2 = st.columns(2,gap='medium')

        with col1:
            st.write('Rate the following traits on a scale form 1 to 5:\n\n')
            st.slider('How empathic are you?', 1, 5, 3, 1, key='empathy')
            st.slider('How good are you at fighting?', 1, 5, 3, 1, key='fighting')
            st.slider('How honorable and loyal are you?', 1, 5, 3, 1, key='honor')
            st.slider('How good are you at negotiating, networking and building connections?', 1, 5, 3, 1, key='connections')
            st.slider('How likely are you to stand by what you believe regardless of whether someone is trying to influence you in a different direction?', 1, 5, 3, 1, key='unyielding')

        with col2:
            st.selectbox('Are you an outcast?', ['No', 'Yes'], key='outcast')
            if st.session_state['outcast'] == 'Yes':
                st.session_state.cache['outcast'] = 1
            else:
                st.session_state.cache['outcast'] = 0
            st.number_input('Test your luck! Choose a number from 1 to 100!', 1, 100, 50, 1, key='guess')
            st.number_input('How old are you?', 1, 60, 30, 1, key='age')
            st.selectbox('Choose the gender for your character:', ['Female', 'Male'], key='gender')
            st.selectbox('Are you married', ['Yes', 'No'], key='marriage')

        st.button('Create character', on_click=click_button_character)

    '\n\n'
    # Create character and display information
    if st.session_state.character and (not st.session_state.prediction):
        st.title('Your Amazing Game of Thrones Character')

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

        # elements to pass to create_image_character
        character = {
            'origin': character['origin'],
            'popularity': character['popularity'],
            'male': character['male'],
            'isNoble': character['isNoble'],
            'isMarried': character['isMarried'],
        }

        age = st.session_state['age']

        # Add a spacer between the image and buttons
        st.write("")

        # store with chatAPI
        #story = create_character_story(character,age)
        story = "This is a story"
        st.write(story)

        # work and gets the image
        #filename = create_image(character,age)
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
            st.button('Will you survive?', on_click=click_button_prediction)


    if st.session_state.prediction:
        character = st.session_state.cache['character']
        age = st.session_state.cache['age']
        st.write('Will you survive?')

        if death_pred(character.drop(columns='lucky')):
            st.write('YES! YOU MADE IT')

            # Change comments from the default image to have one created:
            #st.image(create_image(character, st.session_state.cache["age"]))
            # st.image("processed_data/images/3186f9f7-9b16-467c-a913-7d3e79050863.png")
            st.write(create_character_alive(character, age))

        else:
            st.write('Nooooo......')
            episode_number = episode_pred(character.drop(columns="lucky"))

            #st.write(f'You die in episode {episode_number} 😢')
            story_death = create_character_dead(character, age, episode_number)
            st.write(story_death)

            # Change comments from the default image and story to have them created:
            st.image(create_image(character, age, story_death))
            #st.image("processed_data/images/3186f9f7-9b16-467c-a913-7d3e79050863.png")

            #st.write(f'Here is how you die:')
            #st.write(create_story(character, age))
            st.write('You pass away tragically.')


run()
