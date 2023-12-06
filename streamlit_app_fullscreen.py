import streamlit as st
import base64
import os
from got_survival.ml_logic.model_character_creation import get_character
from got_survival.interface.main import episode_pred, death_pred
from got_survival.ml_logic.create_story_dead import create_character_dead
from got_survival.ml_logic.create_story_alive import create_character_alive
from got_survival.ml_logic.create_character_image import create_image
from got_survival.ml_logic.create_story_house import get_house_text
from got_survival.ml_logic.t_sne import get_tsne

CLIMATE_OPTIONS = ['Cold', 'Medium', 'Warm']

# Set page config
st.set_page_config(
    page_title="Create your Game of Thrones character",
    page_icon=":chart_with_upwards_trend:",
    layout="centered",
)

# Function to read image file as base64 string
def get_img_as_base64(file):
    try:
        with open(file, "rb") as f:
            data = f.read()
            return base64.b64encode(data).decode()
    except Exception as e:
        print(f"Error reading image file: {e}")
        return None

# Get the image as base64 string
img = get_img_as_base64("processed_data/images/awesome_picture.png")

# Function to change the style of the labels
def change_label_style(label,
                       font_size='18px',
                       font_color='white',
                       font_family='sans-serif',
                       text_align='justify'):
    html = f"""
    <script>
        var elems = window.parent.document.querySelectorAll('label');
        var elem = Array.from(elems).find(x => x.innerText == '{label}');
        elem.style.fontSize = '{font_size}';
        elem.style.color = '{font_color}';
        elem.style.fontFamily = '{font_family}';
        elem.style.textAlign = '{text_align}';
        elem.style.fontWeight = 'bold';
        elem.style.textShadow = '2px 2px 4px #000000';
    </script>
    """
    st.components.v1.html(html,height=0)

    #elem.style.webkitTextStroke = '1px black'; /* Webkit browsers like Chrome and Safari */
    #elem.style.textStroke = '1px black'; /* Standard syntax */

# Custom CSS for background image
page_element = f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: url("data:image/png;base64,{img}");
        background-size: cover;
        background-repeat: no-repeat;
        background-position: center;
    }}
    [data-testid="stMarkdownContainer"] > p{{
        border-color: #ffffff;  /* Color of the slider line */
        color: #ffffff;  /* Font color of the slider */
        font-size: 18px;  /* Font size of the slider */
        font-weight: bold;  /* Font weight of the slider number */
        text.shadow: 2px 2px 4px #ffffff;  /* Shadow of the slider font */
    }}
</style>
"""

# Custom CSS styles
custom_styles = """
<style>
    .stSlider div {
        border-color: #ffffff;  /* Color of the slider line */
        color: #ffffff;  /* Font color of the slider */
        font-size: 18px;  /* Font size of the slider */
        text.shadow: 2px 2px 4px #ffffff;  /* Shadow of the slider font */
    }

    .stSlider .slider-value {
        font-weight: bold;  /* Font weight of the slider number */
        color: #ffffff;  /* Font color of the slider number */
    }
</style>
"""

# Display the page elements
st.markdown(page_element, unsafe_allow_html=True)
st.markdown(custom_styles, unsafe_allow_html=True)

# Function to run the app
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
        st.markdown("<h1 style='text-align: center; color: white;'>Create your Game of Thrones character</h1>", unsafe_allow_html=True)

        label_1_header = 'What kind of climate do you prefer?'
        change_label_style(label_1_header)

        col1, col2 = st.columns(2,gap='medium')

        #labels col1
        #label_1_questions = 'Rate the following traits on a scale form 1 to 5:'
        label_1_empathic = 'How empathic are you?'
        label_1_fighting = 'How good are you at fighting?'
        label_1_honor = 'How honorable and loyal are you?'
        label_1_negotiation = 'How good are you at negotiating, networking and building connections?'
        label_1_belief = 'How likely are you to stand by what you believe regardless of whether someone is trying to influence you in a different direction?'


        #labels col1 transformations
        #change_label_style(label_1_questions)
        change_label_style(label_1_empathic)
        change_label_style(label_1_fighting)
        change_label_style(label_1_honor)
        change_label_style(label_1_negotiation)
        change_label_style(label_1_belief)


        with col1:
            st.slider(label_1_empathic, 1, 5, 3, 1, key='empathy')
            st.slider(label_1_fighting, 1, 5, 3, 1, key='fighting')
            st.slider(label_1_honor, 1, 5, 3, 1, key='honor')
            st.slider(label_1_negotiation, 1, 5, 3, 1, key='connections')
            st.slider(label_1_belief, 1, 5, 3, 1, key='unyielding')

        #labels col2
        label_2_outcast = 'Are you an outcast?'
        label_2_luck = 'Test your luck! Choose a number from 1 to 100!'
        label_2_age = 'How old are you?'
        label_2_gender = 'Choose the gender for your character:'
        label_2_marriage = 'Are you married?'

        #labels col2 transformations
        change_label_style(label_2_outcast)
        change_label_style(label_2_luck)
        change_label_style(label_2_age)
        change_label_style(label_2_gender)
        change_label_style(label_2_marriage)

        with col2:
            st.selectbox(label_1_header, CLIMATE_OPTIONS, key='warm')
            st.selectbox(label_2_outcast, ['No', 'Yes'], key='outcast')
            if st.session_state['outcast'] == 'Yes':
                st.session_state.cache['outcast'] = 1
            else:
                st.session_state.cache['outcast'] = 0
            st.number_input(label_2_luck, 1, 100, 50, 1, key='guess')
            st.number_input(label_2_age, 1, 60, 30, 1, key='age')
            st.selectbox(label_2_gender, ['Female', 'Male'], key='gender')
            st.selectbox(label_2_marriage, ['Yes', 'No'], key='marriage')
            st.write('')
            st.button('Create character', on_click=click_button_character)

    '\n\n'
    # Create character and display information
    if st.session_state.character and (not st.session_state.prediction):
        st.markdown("<h1 style='text-align: center; color: white;'>Your Amazing Game of Thrones Character</h1>", unsafe_allow_html=True)

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

        # Display the 'house space'
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

        house_description = character['origin'][0]
        print(f"house_description: {house_description}")

        col1, col2 = st.columns(2, gap='large')
        with col1:
            path_to_house = f"processed_data/images/houses_images/{house_description}.png"
            full_path = os.path.join(os.getcwd(), path_to_house)
            if os.path.exists(full_path):
                st.image(image=full_path, use_column_width="auto")
            else:
                st.write("Image not found!")

        with col2:
            house_description = get_house_text()[house_description]
            st.write(house_description)


        st.button('Will you survive?', on_click=click_button_prediction)

    if st.session_state.prediction:
        character = st.session_state.cache['character']
        age = st.session_state.cache['age']
        st.markdown("<h1 style='text-align: center; color: white;'>Will you survive ?</h1>", unsafe_allow_html=True)

        if death_pred(character.drop(columns='lucky')):
            st.markdown("<h2 style='text-align: center; color: white;'>You made it </h2>", unsafe_allow_html=True)

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
            st.markdown("<h1 style='text-align: center; color: white;'>Nooooo .... you are dead </h1>", unsafe_allow_html=True)
            episode_number = episode_pred(character.drop(columns="lucky"))

            st.markdown(f"<h2 style='text-align: center; color: white;'>You die in season {episode_number} 😢</h2>", unsafe_allow_html=True)

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

if __name__ == "__main__":
    run()
