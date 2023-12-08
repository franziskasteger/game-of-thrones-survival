import streamlit as st
import base64
import os
from got_survival.ml_logic.model_character_creation import get_character
from got_survival.interface.main import season_pred, death_pred
from got_survival.ml_logic.create_story_dead import create_character_dead
from got_survival.ml_logic.create_story_alive import create_character_alive
from got_survival.ml_logic.create_character_image import create_image
from got_survival.ml_logic.create_story_house import get_house_text
from got_survival.ml_logic.t_sne import get_tsne
import time

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
        text-shadow: 2px 2px 4px #000000;  /* Shadow of the slider font */
        text-align: justify;  /* align text */
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

    div.row-widget.stButton{
        text-align: center;
    }

    div.row-widget.stDownloadButton > div.stTooltipIcon {
        text-align: center;
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
        st.markdown("<h1 style='text-align: center; \
                    color: white; text-shadow: 2px 2px 4px #000000;\
                        '>Create your Game of Thrones character</h1>",
                    unsafe_allow_html=True)

        col1, col2 = st.columns(2,gap='medium')

        #labels col1
        label_1_empathic = 'How empathic are you?'
        label_1_fighting = 'How good are you at fighting?'
        label_1_honor = 'How honorable and loyal are you?'
        label_1_negotiation = 'How good are you at negotiating, networking and building connections?'
        label_1_belief = 'How likely are you to stand by what you believe regardless of whether someone is trying to influence you in a different direction?'

        #labels col1 transformations
        change_label_style(label_1_empathic)
        change_label_style(label_1_empathic)
        change_label_style(label_1_fighting)
        change_label_style(label_1_honor)
        change_label_style(label_1_negotiation)
        change_label_style(label_1_belief)

        # display column 1
        with col1:
            st.slider(label_1_empathic, 1, 5, 3, 1, key='empathy')
            st.slider(label_1_fighting, 1, 5, 3, 1, key='fighting')
            st.slider(label_1_honor, 1, 5, 3, 1, key='honor')
            st.slider(label_1_negotiation, 1, 5, 3, 1, key='connections')
            st.slider(label_1_belief, 1, 5, 3, 1, key='unyielding')

        #labels col2
        label_2_climate = 'What kind of climate do you prefer?'
        label_2_outcast = 'Are you an outcast?'
        label_2_luck = 'Test your luck! Choose a number from 1 to 100!'
        label_2_age = 'How old are you?'
        label_2_gender = 'Choose the gender for your character:'
        label_2_marriage = 'Are you married?'

        #labels col2 transformations
        change_label_style(label_2_climate)
        change_label_style(label_2_outcast)
        change_label_style(label_2_luck)
        change_label_style(label_2_age)
        change_label_style(label_2_gender)
        change_label_style(label_2_marriage)

        # display column 2
        with col2:
            st.selectbox(label_2_climate, CLIMATE_OPTIONS, key='warm')
            st.selectbox(label_2_outcast, ['No', 'Yes'], key='outcast')
            st.number_input(label_2_luck, 1, 100, 50, 1, key='guess')
            st.number_input(label_2_age, 1, 100, 30, 1, key='age')
            st.selectbox(label_2_gender, ['Female', 'Male'], key='gender')
            st.selectbox(label_2_marriage, ['No', 'Yes'], key='marriage')
            st.write('')
            st.button('Create character', on_click=click_button_character)

    # Create character and display information
    if st.session_state.character and (not st.session_state.prediction):
        st.markdown("<h1 style='text-align: center; color: white;\
            text-shadow: 2px 2px 4px #000000;'>Who are you in Game of Thrones?</h1>",
            unsafe_allow_html=True)
        st.write('')

        # create character
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

        character_info = st.session_state.cache['character']

        actual_house = character_info['origin'][0]
        you_are = 'You '
        if 'House' in actual_house:
            you_are += 'are part of '
        elif actual_house == 'Outlaw':
            you_are += 'are an '
        elif actual_house == "Night's Watch":
            if st.session_state['marriage'] == 'Yes':
                you_are += 'left your spouse and became '
            else:
                you_are += 'are '
            you_are += 'part of the '
        else:
            you_are += 'are a '

        you_are += actual_house + '!'

        st.markdown(f"<h2 style='text-align: center; color: white;\
            text-shadow: 2px 2px 4px #000000;'>{you_are}</h2>",
            unsafe_allow_html=True)
        # elements to pass to create_image_character
        character = {
            'origin': character_info['origin'],
            'popularity': character_info['popularity'],
            'male': character_info['male'],
            'isNoble': character_info['isNoble'],
            'isMarried': character_info['isMarried'],
        }

        age = st.session_state['age']

        # Add a spacer between the image and buttons
        st.write("")

        house_description = character['origin'][0]

        col1, col2 = st.columns(2, gap='large')

        # display sigil
        with col1:
            path_to_house = f"processed_data/images/houses_images/{house_description}.png"
            full_path = os.path.join(os.getcwd(), path_to_house)
            if os.path.exists(full_path):
                st.image(image=full_path, use_column_width="auto")
            else:
                st.write("Image not found!")

        # display info about group
        with col2:
            house_description = get_house_text()[house_description]
            st.write(house_description)

        st.markdown('''---''')

        # if you are outcast, explain which house you would've been in:
        if st.session_state['outcast'] =='Yes' and \
            actual_house != character_info['ex_house'][0]:
            saying = 'You grew up as '
            ex_house = character_info['ex_house'][0]
            if 'House' in ex_house:
                saying += f'part of {ex_house}'
            else:
                saying += f'a {ex_house}'
            saying += ', but an unfortunate event caused you to leave your \
                comfortable life and become '
            if actual_house == 'Outlaw':
                saying += 'an '
            elif actual_house == "Night's Watch":
                saying += 'part of the '
            else:
                saying += 'a '
            saying += actual_house + '.'
            st.write(saying)

        st.write('Explore how similar you are to the prominent groups in Game of \
            Thrones. Hovering over a bubble will reveal the name of the group.')
        st.write('(To zoom back out, double click/tap the map)')
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
        st.plotly_chart(fig, use_container_width=True)

        st.button('Will you survive?', on_click=click_button_prediction)

    # calculate predictions
    if st.session_state.prediction:
        character = st.session_state.cache['character']
        age = st.session_state.cache['age']

        st.markdown("<h1 style='text-align: center; color: white;\
            text-shadow: 2px 2px 4px #000000;'>Will you survive?</h1>", unsafe_allow_html=True)
        # death prediction
        pred = death_pred(character.drop(columns='lucky'))
        if pred:
            st.markdown("<h2 style='text-align: center; color: white;\
                text-shadow: 2px 2px 4px #000000;'>Congratulations! You are part \
                    of the elite group that through hardships, battles and against \
                        all odds survives until the end of what will be forever \
                            known as the Game of Thrones.</h2>", unsafe_allow_html=True)
        else:
            season_number = season_pred(character.drop(columns="lucky"))
            st.markdown(f"<h2 style='text-align: center; color: white;\
                text-shadow: 2px 2px 4px #000000;'>Unfortunately, the hardships, \
                    battles and horrible events you encountered along the way got \
                        the best of you and you lost your life in <u>season {season_number}</u>.\
                        </h2>", unsafe_allow_html=True)

        st.markdown('''---''')

        # progress bar
        if "clear" not in st.session_state:
            _left, mid, _right, four, five = st.columns(5)
            with _left:
                st.write('')
            with mid:
                st.markdown(f'<img style="transform:scaleX(-1); text-align: center;" \
                    src="https://media.tenor.com/ZU_roo1-yLoAAAAi/wolf-rennt-run.gif" \
                        alt="wolf gif">',
                    unsafe_allow_html=True)

            my_bar = st.progress(1)
            st.write('Loading...')
            for i in range(5):
                st.write(" ")

            time.sleep(0.5)
            my_bar.progress(10)

        # create image and story only once
        if "image" not in st.session_state:
            if pred:
                st.session_state["story"] = create_character_alive(character, age)
            else:
                st.session_state["story"] = create_character_dead(character, age, season_number)

            my_bar.progress(50)
            try:
                # import time; time.sleep(5)
                # raise
                img_alive, filename_alive = create_image(character, age,
                                                         st.session_state["story"])
            except:
                img_alive, filename_alive = (None, None)
                st.markdown(f"<h2 style='text-align: center; color: white; \
                    text-shadow: 2px 2px 4px #000000;'>Something went wrong...</h2>",
                    unsafe_allow_html=True)

            st.session_state["image"] = img_alive
            st.session_state["image_path"] = filename_alive

            my_bar.progress(99)
            time.sleep(0.5)

        # display story once it is created and only once:
        if "clear" in st.session_state:
            if st.session_state["image"]:
                if pred:
                    st.markdown(f"<h3 style='text-align: center; color: white;\
                    text-shadow: 2px 2px 4px #000000;'>Read about your happily ever after:\
                            </h3>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<h3 style='text-align: left; color: white;\
                    text-shadow: 2px 2px 4px #000000;'>Here's how it happened:\
                            </h3>", unsafe_allow_html=True)

                st.image(st.session_state["image"])
                with open(st.session_state["image_path"], "rb") as file:
                    st.download_button(
                        label="Download image",
                        data=file.read(),
                        file_name=st.session_state["image_path"],
                        key="download_button",
                        help="Click to download the image",
                    )
            if st.session_state["image"] is None:
                st.write('Unfortunately this picture cannot be displayed, as it \
                    is too gruesome... Refresh the page to start over!')
                st.markdown('''---''')
            st.write(st.session_state["story"])

        else:
            st.session_state["clear"] = True
            st.experimental_rerun()



if __name__ == "__main__":
    run()
