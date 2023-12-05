import streamlit as st
from got_survival.ml_logic.model_character_creation import get_character
from got_survival.interface.main import episode_pred, death_pred_RF
from got_survival.ml_logic.create_story_dead import create_character_dead
from got_survival.ml_logic.create_story_alive import create_character_alive
from got_survival.ml_logic.create_character_image import create_image
from got_survival.ml_logic.create_story_house import get_house_text

CLIMATE_OPTIONS = ['Cold', 'Medium', 'Warm']

st.set_page_config(
    page_title="Create your Game of Thrones character",
    page_icon=":chart_with_upwards_trend:",
    layout="centered",
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

        col1, col2 = st.columns(2,gap='large')

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
        st.markdown("<h1 style='text-align: center; color: grey;'>Your Amazing Game of Thrones Character</h1>", unsafe_allow_html=True)

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

        col1, col2 = st.columns(2,gap='large')
        with col1:
            st.image(image="processed_data/images/test_image.png",use_column_width="auto")

        with col2:
            house_description = get_house_text().keys()
            st.write(house_description)


        st.button('Will you survive?', on_click=click_button_prediction)

    if st.session_state.prediction:
        character = st.session_state.cache['character']
        age = st.session_state.cache['age']
        st.markdown("<h1 style='text-align: center; color: grey;'>Will you survive ?</h1>", unsafe_allow_html=True)

        if death_pred_RF(character.drop(columns='lucky')):
            st.markdown("<h2 style='text-align: center; color: grey;'>You made it </h2>", unsafe_allow_html=True)

            # Change comments from the default image to have one created:
            # st.image(create_image(character, st.session_state.cache["age"]))
            # st.image("processed_data/images/3186f9f7-9b16-467c-a913-7d3e79050863.png")

            if "image" not in st.session_state:
                st.session_state["story"] = create_character_alive(character, age)
                img_alive, filename_alive = create_image(character, age, st.session_state["story"])
                st.session_state["image"] = img_alive
                st.session_state["image_path"] = filename_alive

            st.write(st.session_state["story"])
            st.image(st.session_state["image"])

            #if st.button("Download image"):
            with open(st.session_state["image_path"], "rb") as file:
                st.download_button(
                    label="Download image",
                    data=file.read(),
                    file_name=st.session_state["image_path"],
                    key="download_button",
                    help="Click to download the image",
                )

        else:
            st.markdown("<h1 style='text-align: center; color: grey;'>Nooooo .... you are dead </h1>", unsafe_allow_html=True)
            episode_number = episode_pred(character.drop(columns="lucky"))
            if episode_number == 0:
                st.markdown("<h2 style='text-align: center; color: grey;'>You die in EARLY episodes 😢</h2>", unsafe_allow_html=True)
            else:
                st.markdown("<h2 style='text-align: center; color: grey;'>You die in LATER episodes 😢😢</h2>", unsafe_allow_html=True)

            if "image" not in st.session_state:

                st.session_state["story"] = create_character_dead(character, age)

                img_alive, filename_alive = create_image(character, age, st.session_state["story"])
                st.session_state["image"] = img_alive
                st.session_state["image_path"] = filename_alive

            st.write(st.session_state["story"])
            st.image(st.session_state["image"])

            #if st.button("Download image"):
            with open(st.session_state["image_path"], "rb") as file:
                st.download_button(
                    label="Download image",
                    data=file.read(),
                    file_name=st.session_state["image_path"],
                    key="download_button",
                    help="Click to download the image",
                )

            #st.image("processed_data/images/3186f9f7-9b16-467c-a913-7d3e79050863.png")

            #st.write(f'Here is how you die:')
            #st.write(create_story(character, age))


run()
