import requests
import csv
import os


def get_houses(url):
    response = requests.get(url)

    if response.status_code == 200:
        houses = response.json()

        file_path = 'raw_data/scrapped_houses.csv'

        if not os.path.exists(file_path):
            with open(file_path, 'w') as csvfile:
                pass

        with open(file_path, 'a', newline='') as csvfile:
            fieldnames = [
                "Name", "Region", "Coat of Arms", "Words", "Titles", "Seats",
                "Current Lord", "Heir", "Overlord", "Founded", "Founder",
                "Died Out", "Ancestral Weapons", "Cadet Branches", "Sworn Members", "URL"
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            if csvfile.tell() == 0:
                writer.writeheader()

            for house in houses:
                writer.writerow({
                    "Name": house["name"],
                    "Region": house["region"],
                    "Coat of Arms": house["coatOfArms"],
                    "Words": house["words"],
                    "Titles": house["titles"],
                    "Seats": house["seats"],
                    "Current Lord": house["currentLord"],
                    "Heir": house["heir"],
                    "Overlord": house["overlord"],
                    "Founded": house["founded"],
                    "Founder": house["founder"],
                    "Died Out": house["diedOut"],
                    "Ancestral Weapons": house["ancestralWeapons"],
                    "Cadet Branches": house["cadetBranches"],
                    "Sworn Members": house["swornMembers"],
                    "URL": house["url"]
                })

        # Check if there are more pages
        if 'Link' in response.headers:
            links = response.headers['Link'].split(', ')
            for link in links:
                if 'rel="next"' in link:
                    next_page_url = link.split('; ')[0][1:-1]
                    get_houses(next_page_url)
                    break
    else:
        print("Failed to retrieve data. Status code:", response.status_code)

if __name__ == "__main__":
    base_url = "https://www.anapioficeandfire.com/api/houses"
    get_houses(base_url)
