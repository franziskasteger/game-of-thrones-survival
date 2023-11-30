import streamlit as st
# from got_survival.ml_logic.model_houses import houses_model_predict
from got_survival.ml_logic.model_character_creation import get_house, get_luck, \
    get_popularity, get_nobility, get_male


def run(social=False):
    st.title('Create your Game of Thrones character')

    if 'clicked' not in st.session_state:
        st.session_state.clicked = False

    def click_button():
        st.session_state.clicked = True

    # FIRST QUESTION
    warm = st.selectbox('What kind of climate do you prefer?',\
        ['Medium', 'Warm', 'Cold'])
    # if warm == 'Warm':
    #     climate = 2
    # elif warm == 'Medium':
    #     climate = 1
    # else:
    #     climate = 0
    '\n\n'

    st.write('Rate the following traits on a scale form 1 to 5:\n\n')
    # SECOND QUESTION
    empathy = st.slider('How empathic are you?', 1, 5, 3, 1, key='emp')
    '\n\n'

    # THIRD QUESTION
    fighting = st.slider('How good are you at fighting?', 1, 5, 3, 1, key='fight')
    '\n\n'

    # FOURTH QUESTION
    honor = st.slider('How honorable and loyal are you?', 1, 5, 3, 1, key='hon')
    '\n\n'

    # FIFTH QUESTION
    connections = st.slider('How good are you at negotiating, networking and\
        building connections?', 1, 5, 3, 1, key='con')
    '\n\n'

    #SIXTH QUESTION
    unyielding = st.slider('How likely are you to stand by what you believe\
        regardless of whether someone is trying to influence you in a different\
            direction?', 1, 5, 3, 1, key='uny')
    '\n\n'

    # SEVENTH QUESTION
    yes = st.selectbox('Are you an outcast?', ['No', 'Yes'])
    if yes == 'Yes':
        outcast = 1
    else:
        outcast = 0

    guess = st.number_input('Test your luck! Choose a number from 1 to 100!',
                            1, 100, 50, 1, key='luck')
    luck = get_luck(guess)

    age = st.number_input('How old are you?', 1, 60, 30, 1, key='age')

    if social:
        followers = st.selectbox('Do you have a lot of followers on socal media?',
                                ['Yes', 'No'])
        invite = st.selectbox('Do you frequently get invited to events and social\
            gatherings?', ['Yes', 'No'])
        attention = st.selectbox('Do people listen when you talk?', ['Yes', 'No'])
    else:
        followers = 0
        invite = 0
        attention = 0

    gender = st.selectbox('Choose the gender for your character:', ['Female', 'Male'])

    house = get_house(outcast, warm, empathy, fighting, honor, connections, unyielding)
    if 'House' in house or house in ['Noble', 'Foreign Noble']:
        noble = 'noble'
    else:
        noble = 'not noble'

    nobility = get_nobility(noble)
    popularity = get_popularity(followers, invite, attention, outcast, empathy,
                                fighting, honor, connections, unyielding, social=social)
    male = get_male(gender)

    '\n\n'
    st.button('Create character', on_click=click_button)

    '\n\n'
    if st.session_state.clicked:
        if house in ['Wildling', 'Dothraki', 'Soldier', 'Foreign Noble',
                     'Foreign Peasant', 'Noble', 'Peasant']:
            st.write(f'In the world of Game of Thrones you would be a {house}!')
        elif 'House' in house:
            st.write(f'In the world of Game of Thrones you would be part of {house}!')
        elif house == 'Outlaw':
            st.write(f'In the world of Game of Thrones you would be an {house}!')
        else:
            st.write(f'In the world of Game of Thrones you would be part of the {house}!')

        st.write(f'In terms of luck you are {luck}, you are {age} years old, \
            {round(popularity * 100)}% popular, {gender} and {noble}!')


        '\n\n'
        if st.button('Will you survive?'):
            'INSERT PREDICTION HERE'



run(social = False)
