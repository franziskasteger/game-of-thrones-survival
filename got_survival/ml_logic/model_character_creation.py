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

def get_popularity(followers, invite, attention, outcast, empathy,
                   fighting, honor, connections, unyielding, social=False):
    if social:
        if followers == 'Yes':
            followers = 1
        else:
            followers = 0

        if invite == 'Yes':
            invite = 1
        else:
            invite = 0

        if attention == 'Yes':
            attention = 1
        else:
            attention = 0

        return (followers + invite + attention + empathy / 5 + fighting / 5\
            + honor / 5 + connections / 5 + unyielding / 5) / 8

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

########## TESTS ##########

if __name__ == '__main__':

    # print(get_house(0, 2, 4, 3, 4, 2, 5))
    # print(get_luck(59))


    pass
