from got_survival.params import *
from openai import OpenAI
import pandas as pd

def create_story(
        character: pd.DataFrame,
        age: int
    ) -> str:
    '''
    Given information about a character will create a story about their death
    using the OpenAI api.
    '''
    # Instantiate OpenAI with the key
    client = OpenAI(
        api_key=OPENAI_API_KEY
    )
    # Translate character information into words
    if character['male'][0] == 1:
        gender = 'male'
    else:
        gender = 'female'

    if character['popularity'][0] > 0.75:
        pop = 'popular'
    elif character['popularity'][0] < 0.25:
        pop = 'unpopular'
    else:
        pop = 'normal'

    if character['isMarried'][0] == 1:
        mar = 'married'
    else:
        mar = 'unmarried'

    # Prompt for the AI model
    text_prompt = f"I'm gonna give you a made up character in the world of game of \
        thrones, please create a very short funny story of how they die. Don't make it \
            longer than two paragraphs!\
            age: {age}, \
            house: {character['origin'][0]}, \
            luck: {character['lucky'][0]}, \
            'popularity': {pop}, \
            'male': {gender},\
            'nobility': {character['isNoble'][0]},\
            'married': {mar}. "

    # Make a request to the API to generate text
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0613",  # Use the engine of your choice
        messages = [{"role": "system", "content": "You are a historian and you \
            are writing a book about game of thrones"},
                    {"role": "user", "content": text_prompt}],
        max_tokens = 300,
    )

    return response.choices[0].message.content


###########################
########## TESTS ##########
###########################

character = {
    'origin': ['House Stark'],
    'popularity': [0.78],
    'lucky': ['lucky'],
    'male': [0],
    'isNoble': [1],
    'isMarried': [1]
}
age = 28
new_character = pd.DataFrame.from_dict(character)

if __name__ == '__main__':

    # print(create_story(new_character, age))
    pass
