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

    # Define the prompt
    text_prompt = f"""Character Overview:

    A charismatic and cunning member of House {character['origin'][0]},
    {'he' if character['male'][0] else 'she'} often uses their wit and charm
    to manipulate others. Despite their noble status,
    {'he' if character['male'][0] else 'she'} is not afraid
    often using their wit and charm to manipulate others. Despite their
    noble status, {'he' if character['male'][0] else 'she'} is not afraid
    to get their hands dirty, making them a formidable adversary.

    Age: {age}
    Popularity Index: {character['popularity'][0]}
    Nobility Status: {'Noble' if character['isNoble'][0] else 'Commoner'}
    Marital Status: {'married' if character['isMarried'][0] else 'unmarried'}

    Description:

    Weave a captivating tale of this Game of Thrones character, incorporating
    their intricate personality and the treacherous world of Westeros.

    Instructions:

    Craft a story that delves into the character's cunning nature and
    their ability to navigate the political landscape of Westeros.
    Infuse the narrative with humor and intrigue, showcasing the character's
    resourcefulness and ability to turn even the most perilous situations
    to their advantage.

    """

    # Set the max_tokens parameter to a higher value
    max_tokens = 300

    # Make a request to the API to generate text
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0613",
        messages = [{"role": "system", "content": "You are a historian and you \
            know everything about game of thrones"},
                    {"role": "user", "content": text_prompt}],
        max_tokens=max_tokens,
    )

    # Return the generated story
    return response.choices[0].message.content
