import requests
import csv
import os

def get_characters(url):
    response = requests.get(url)

    if response.status_code == 200:
        characters = response.json()

        file_path = 'raw_data/scrapped_characters.csv'

        if not os.path.exists(file_path):
            with open(file_path, 'w') as csvfile:
                pass

        with open(file_path, 'a', newline='') as csvfile:
            fieldnames = [
                "Name", "Culture", "Born", "Died", "Titles", "Aliases", "Father",
                "Mother", "Spouse", "Allegiances", "Books", "POV Books",
                "TV Series", "Played By", "URL"
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            if csvfile.tell() == 0:
                writer.writeheader()

            for character in characters:
                writer.writerow({
                    "Name": character["name"],
                    "Culture": character["culture"],
                    "Born": character["born"],
                    "Died": character["died"],
                    "Titles": character["titles"],
                    "Aliases": character["aliases"],
                    "Father": character["father"],
                    "Mother": character["mother"],
                    "Spouse": character["spouse"],
                    "Allegiances": character["allegiances"],
                    "Books": character["books"],
                    "POV Books": character["povBooks"],
                    "TV Series": character["tvSeries"],
                    "Played By": character["playedBy"],
                    "URL": character["url"]
                })


        # Check if there are more pages
        if 'Link' in response.headers:
            links = response.headers['Link'].split(', ')
            for link in links:
                if 'rel="next"' in link:
                    next_page_url = link.split('; ')[0][1:-1]
                    get_characters(next_page_url)
                    break
    else:
        print("Failed to retrieve data. Status code:", response.status_code)

if __name__ == "__main__":
    base_url = "https://www.anapioficeandfire.com/api/characters"
    get_characters(base_url)
