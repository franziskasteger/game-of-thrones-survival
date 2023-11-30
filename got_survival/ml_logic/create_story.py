from got_survival.params import *
from openai import OpenAI


def create_story(character):
    client = OpenAI(
        api_key=OPENAI_API_KEY
    )
    if character['male'] == 1:
        gender = 'male'
    else:
        gender = 'female'

    if character['popularity'] > 0.75:
        pop = 'popular'
    elif character['popularity'] < 0.25:
        pop = 'unpopular'
    else:
        pop = 'normal'

    if character['married'] == 1:
        mar = 'married'
    else:
        mar = 'unmarried'

    # Prompt for the AI model
    text_prompt = f"I'm gonna give you a made up character in the world of game of \
        thrones, please create a short funny story about their death. It should not\
            be longer than three paragraphs.\
            age: {character['age']}, \
            house: {character['house']}, \
            luck: {character['luck']}, \
            'popularity': {pop}, \
            'male': {gender},\
            'nobility': {character['nobility']},\
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


if __name__ == '__main__':
    new_character = {
        'house': 'House Stark',
        'luck': 'unlucky',
        'age': 28,
        'popularity': 0.78,
        'male': 0,
        'nobility': 1,
        'married': 1
    }

    print(create_story(new_character))
