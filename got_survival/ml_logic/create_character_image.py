from got_survival.params import *
from openai import OpenAI
from IPython.display import Image
from PIL import Image
from io import BytesIO
import requests
import os
import uuid
import os
from pathlib import Path

def create_image(new_character):

    client = OpenAI(
        api_key=OPENAI_API_KEY
    )

    #generate image
    response = client.images.generate(
        model="dall-e-3",
        prompt=f"""
        Character Overview:

        House: {new_character.get('house')}
        Age: {new_character.get('age')}
        Popularity Index: {new_character.get('popularity')}
        Gender: {'male' if new_character.get('male') else 'female'}
        Nobility Status: {'Noble' if new_character.get('nobility') else 'Commoner'}
        Marital Status: {'married' if new_character.get('married') else 'unmarried'}

        Description:

        Create a portrait of a Game of Thrones character from
        {new_character.get('house')}.
        The character's age, popularity, gender, nobility status, and marital
        status should all be reflected in the image. The portrait should be
        evocative of the rich and complex world of Westeros.

        Instructions:

            Do not include any text in the image.
            Ensure the character's attire, hairstyle, and overall appearance
            align with their house, age, nobility status, and marital status.
            Capture the character's personality and the implications of their
            unique life experiences.
            Create an image that seamlessly blends into the visual aesthetic
            of Game of Thrones.,
                quality="standard",
                size="1024x1024",
                n=1
        """
    )

    #extract image url
    image_url = response.data[0].url

    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))
    print(f"Initial size: {img.size}")

    #resize image to 256x256
    img = img.resize((512, 512), Image.Resampling.LANCZOS)
    print(f"Final size: {img.size}")

    # save image in processed_data/images
    # Generate a unique filename
    unique_filename = str(uuid.uuid4()) + ".png"
    folder_path = "./processed_data/images/"

    # Create the images folder if it doesn't exist
    Path(folder_path).mkdir(parents=True, exist_ok=True)

    filename = os.path.join(folder_path, unique_filename)
    img.save(filename)

    img.show()
    #show image
    return img


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

    print(create_image(new_character))
