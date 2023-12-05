import pandas as pd
from openai import OpenAI
from got_survival.params import *

def create_character_story(
    character: pd.DataFrame,
    age: int,
) -> str:
    """
    Generates a short narrative about a Game of Thrones character based on their given information.
    """

    # Initialize OpenAI client with the API key
    client = OpenAI(api_key=OPENAI_API_KEY)

    # Craft the text prompt based on character details
    text_prompt = f"""
    Instructions:

    Create a short narrative about a made up Game of Thrones character with the
    following characteristics:

    • House: {character['origin'][0]}
    • Gender: {'male' if character['male'][0] else 'female'}
    • Age: {age}
    • Popularity Index: {'popular' if character['popularity'][0] > 0.5 else 'not popular'}
    • Nobility Status: {'Noble' if character['isNoble'][0] else 'Commoner'}
    • Marital Status: {'married' if character['isMarried'][0] else 'unmarried'}
    """

    # Set the maximum number of tokens for each prompt chunk
    max_tokens = 100

    # Split the prompt into smaller chunks for better processing
    chunks = text_prompt.split(".")

    # Initialize an empty string to store the generated story
    generated_story = ""

    # Generate the story one chunk at a time
    for chunk in chunks:
        # Send each chunk to the OpenAI API and capture the response
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-0613",
            messages=[
                {"role": "system", "content": "You are a narrator and you know everything about game of thrones"},
                {"role": "user", "content": chunk}
            ],
            max_tokens=max_tokens
        )

        # Append the generated text from each chunk to the story string
        generated_story += response.choices[0].message.content + '. '

    # Return the complete generated story
    return generated_story
