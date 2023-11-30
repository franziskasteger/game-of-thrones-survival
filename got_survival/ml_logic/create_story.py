from got_survival.params import *
from langchain.llms import OpenAI


def create_story():
    client = OpenAI(
        # defaults to os.environ.get("OPENAI_API_KEY")
        api_key = OPENAI_API_KEY
    )

    # Prompt for the AI model
    text_prompt = "I'm gonna give you some a character in the world of game of \
        thrones, please create a short funny story about their death, at age is 26, \
            member of house stark"

    # Make a request to the API to generate text
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0613",  # Use the engine of your choice
        messages = [{"role": "system", "content": "You are a historian and you \
            are writing a book about game of thrones"},
                    {"role": "user", "content": text_prompt}],
        max_tokens = 100,
    )

    return response.choices[0].message.content
