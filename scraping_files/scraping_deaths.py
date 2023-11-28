import requests
from bs4 import BeautifulSoup
import csv
import codecs

# URL of the page containing the data
url = 'https://listofdeaths.fandom.com/wiki/Game_of_Thrones#Deaths'

file_path = 'raw_data/scrapped_deaths_season_episode.csv'

# Send a GET request to the URL
response = requests.get(url)

# grab season one text
soup = BeautifulSoup(response.text, 'html.parser')

# grab all seasons
seasons = [season.text for season in soup.find_all('h3') if season.text.startswith('Season')]


# Open the CSV file in append mode outside the loop
with codecs.open(file_path, 'a', encoding='utf-8') as f:
    writer = csv.writer(f)

    # Write header only once outside the loop
    writer.writerow(['Season', 'Episode', 'Deaths'])

    # Loop through each season
    for season in seasons:
        print(f"season ---> {season}")

        # grab all episodes names for the current season
        episodes = [episode.text for episode in soup.find_all('h4') if episode.find_previous('h3').text == season]

        # loop through each episode
        for episode in episodes:
            print(f"\tEpisode ---> {episode}")

            # grab all deaths text for the current episode
            deaths = [death.text for death in soup.find_all('li') if death.find_previous('h4') and death.find_previous('h4').text == episode]

            # loop through each death and write to CSV
            for death in deaths:
                writer.writerow([season, episode, death])

        print(f"Deaths for Season {season} saved to got_deaths.csv")
