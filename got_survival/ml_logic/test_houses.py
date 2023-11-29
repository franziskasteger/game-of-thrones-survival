import streamlit as st
from got_survival.ml_logic.model_houses import get_dict, houses_model_predict

def run():
    st.title('Check your Game of Thrones House')

    # FIRST QUESTION
    #'What kind of climate do you prefer?'
    warm = st.selectbox('What kind of climate do you prefer?', ['Medium', 'Warm', 'Cold'])
    if warm == 'Warm':
        climate = 2
    elif warm == 'Medium':
        climate = 1
    else:
        climate = 0
    '\n\n'

    st.write('Rate the following traits on a scale form 1 to 5:\n\n')
    # SECOND QUESTION
    #st.write('How empathic are you?')
    empathy = st.slider('How empathic are you?', 1, 5, 3, 1, key='emp')
    '\n\n'

    # THIRD QUESTION
    #st.write('How good are you at fighting?')
    fighting = st.slider('How good are you at fighting?', 1, 5, 3, 1, key='fight')
    '\n\n'

    # FOURTH QUESTION
    #st.write('How honorable and loyal are you?')
    honor = st.slider('How honorable and loyal are you?', 1, 5, 3, 1, key='hon')
    '\n\n'

    # FIFTH QUESTION
    #st.write('How good are you at negotiating, networking and building connections?')
    connections = st.slider('How good are you at negotiating, networking and building connections?', 1, 5, 3, 1, key='con')
    '\n\n'

    #SIXTH QUESTION
    # they are not easily influenced and they are unlikely to change their mind
    #st.write('How likely are you to stand by what you believe regardless of whether\
    #    someone is trying to influence you in a different direction?')
    unyielding = st.slider('How likely are you to stand by what you believe regardless of whether\
        someone is trying to influence you in a different direction?', 1, 5, 3, 1, key='uny')
    '\n\n'

    # SEVENTH QUESTION
    #st.write('Are you an outcast?')
    yes = st.selectbox('Are you an outcast?', ['No', 'Yes'])
    if yes == 'Yes':
        outcast = 1
    else:
        outcast = 0

    traits = get_dict(outcast, climate, empathy, fighting, honor, connections, unyielding)
    house = houses_model_predict(traits)[0]
    '\n\n'
    if st.button('Assign allegiance'):
        if house in ['Wildling', 'Dothraki', 'Soldier', 'Foreign Noble', 'Foreign Peasant',
                    'Noble', 'Peasant']:
            st.write(f'In the world of Game of Thrones you would be a {house}!')
        elif 'House' in house:
            st.write(f'In the world of Game of Thrones you would be part of {house}!')
        elif house == 'Outlaw':
            st.write(f'In the world of Game of Thrones you would be an {house}!')
        else:
            st.write(f'In the world of Game of Thrones you would be part of the {house}!')




run()
