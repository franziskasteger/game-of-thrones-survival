import pandas as pd
from random import randint
from got_survival.ml_logic.model_houses import houses_model_predict


def get_house(
        outcast:int,
        climate:int,
        empathy:int,
        fighting:int,
        honor:int,
        connections:int,
        unyielding:int
    ) -> str:

    new_character = {
        'outcast': [outcast],
        'climate': [climate],
        'empathy': [empathy],
        'fighting': [fighting],
        'honor': [honor],
        'connections': [connections],
        'unyielding': [unyielding]
    }
    X =  pd.DataFrame.from_dict(new_character)

    return houses_model_predict(X)[0]

def get_outcast(out:str) -> int:
    if out == 'Yes':
        return 1
    return 0

def get_luck(guess:int) -> str:
    truth = randint(1, 100)
    if abs(truth - guess) > 95 or abs(truth - guess) < 5:
        return 'lucky'
    if abs(truth - guess) > 65 or abs(truth - guess) < 35:
        return 'normal'
    return 'unlucky'

def get_popularity(
        outcast:int,
        empathy:int,
        fighting:int,
        honor:int,
        connections:int,
        unyielding:int
    ) -> float:
    if outcast:
        outcast = 0
    else:
        outcast = 1

    return (empathy + fighting + honor + connections + unyielding) / 25

def get_nobility(house:str) -> int:
    if 'House' in house or house in ['Noble', 'Foreign Noble']:
        return 1
    return 0

def get_climate(warm:str) -> int:
    if warm == 'Warm':
        return 2
    elif warm == 'Medium':
        return 1
    return 0

def get_male(gender: str) -> int:
    if gender == 'Male':
        return 1
    return 0

def get_married(marriage:str) -> int:
    if marriage == 'Yes':
        return 1
    return 0

def get_character(
        guess:int,
        out:str,
        warm:str,
        empathy:int,
        fighting:int,
        honor:int,
        connections:int,
        unyielding:int,
        gender:str,
        marriage:str
    ) -> pd.DataFrame:
    outcast = get_outcast(out)
    climate = get_climate(warm)
    luck = get_luck(guess)
    house = get_house(outcast, climate, empathy, fighting, honor, connections, unyielding)
    nobility = get_nobility(house)
    popularity = get_popularity(outcast, empathy, fighting, honor, connections, unyielding)
    male = get_male(gender)
    married = get_married(marriage)

    character = {
        'lucky': [luck],
        'origin': [house],
        'isNoble': [nobility],
        'popularity': [popularity],
        'male': [male],
        'isMarried': [married]
    }

    return pd.DataFrame.from_dict(character)


###########################
########## TESTS ##########
###########################

if __name__ == '__main__':

    # print(get_house(0, 2, 4, 3, 4, 2, 5))
    # print(get_luck(59))

    pass
