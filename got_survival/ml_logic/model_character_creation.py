import pandas as pd
from random import randint
from got_survival.ml_logic.model_houses import houses_model_predict


def get_house(outcast, warm, empathy, fighting, honor, connections, unyielding):
    if warm == 'Warm':
        climate = 2
    elif warm == 'Medium':
        climate = 1
    else:
        climate = 0

    test = {
        'outcast': [outcast],
        'climate': [climate],
        'empathy': [empathy],
        'fighting': [fighting],
        'honor': [honor],
        'connections': [connections],
        'unyielding': [unyielding]
    }
    X =  pd.DataFrame.from_dict(test)

    return houses_model_predict(X)[0]

def get_luck(guess):
    truth = randint(1, 100)
    if abs(truth - guess) > 95 or abs(truth - guess) < 5:
        return 'lucky'
    if abs(truth - guess) > 65 or abs(truth - guess) < 35:
        return 'normal'
    return 'unlucky'

def get_popularity(outcast, empathy,fighting, honor, connections, unyielding):
    if outcast:
        outcast = 0
    else:
        outcast = 1

    return (empathy + fighting + honor + connections + unyielding) / 25

def get_nobility(nobility):
    if nobility == 'noble':
        return 1
    return 0

def get_male(gender):
    if gender == 'Male':
        return 1
    return 0

def get_married(marriage):
    if marriage == 'Yes':
        return 1
    return 0

def get_character(
    guess,
    outcast,
    warm,
    empathy,
    fighting,
    honor,
    connections,
    unyielding,
    gender,
    marriage
):
    luck = get_luck(guess)
    house = get_house(outcast, warm, empathy, fighting, honor, connections, unyielding)
    if 'House' in house or house in ['Noble', 'Foreign Noble']:
        noble = 'noble'
    else:
        noble = 'not noble'
    nobility = get_nobility(noble)
    popularity = get_popularity(outcast, empathy, fighting, honor, connections, unyielding)
    male = get_male(gender)
    married = get_married(marriage)

    character = {
        'lucky': luck,
        'house': house,
        'isNoble': nobility,
        'isPopular': popularity,
        'male': male,
        'isMarried': married
    }

    return character

########## TESTS ##########

if __name__ == '__main__':

    # print(get_house(0, 2, 4, 3, 4, 2, 5))
    # print(get_luck(59))

    pass
