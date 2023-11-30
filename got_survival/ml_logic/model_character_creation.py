import pandas as pd
from random import randint
from got_survival.ml_logic.model_houses import houses_model_predict


def get_house(outcast, climate, empathy, fighting, honor, connections, unyielding):
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

    return houses_model_predict(X)

def get_luck(guess):
    truth = randint(1, 100)
    if abs(truth - guess) > 95 or abs(truth - guess) < 5:
        return 'lucky'
    if abs(truth - guess) > 65 or abs(truth - guess) < 35:
        return 'normal'
    return 'unlucky'





########## TESTS ##########

if __name__ == '__main__':

    # print(get_house(0, 2, 4, 3, 4, 2, 5))
    # print(get_luck(59))


    pass
