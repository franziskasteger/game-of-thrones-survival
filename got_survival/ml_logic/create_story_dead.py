import pandas as pd
from openai import OpenAI
from got_survival.params import *

def create_character_dead(
    character: pd.DataFrame,
    age: int,
    season_number:int,
    api_key:str=''
) -> str:
    """
    Generates a short narrative about a Game of Thrones character based on
    their given information.
    """
    # Initialize OpenAI client with the API key
    # if api_key=='':
    #     client = OpenAI(api_key=OPENAI_API_KEY)
    # else:
    #     client = OpenAI(api_key=api_key)
    client = OpenAI(api_key=api_key)

    # Craft the text prompt based on character details
    sentence = f"""
        I'm gonna give you a made up character in the world of game of
        thrones, please create a very short funny story of the character's death
        in season {season_number}. It should be inspired by the events in game of
        thrones in season {season_number}. Make it shorter than 2 paragraphs!
            age: {age},
            house: {character['origin'][0]},
            luck: {character['lucky'][0]},
            popularity: {'popular' if character['popularity'][0]>0.4 else 'unpopular'},
            gender: {'male' if character['male'][0] else 'female'},
            nobility: {'noble' if character['isNoble'][0] else 'not noble'},
            married: {'married' if character['isMarried'][0] else 'not married'}.
    """

    # Set the maximum number of tokens for each prompt chunk
    max_tokens = 400

    # Generate the story one chunk at a time
    # Send each chunk to the OpenAI API and capture the response
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0613",
        messages=[
            {"role": "system", "content": "You are a historian and you are \
                writing a book about game of thrones"},
            {"role": "user", "content": sentence}
        ],
        max_tokens=max_tokens
    )

    # Return the complete generated story
    return response.choices[0].message.content
