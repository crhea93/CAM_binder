import numpy as np

def valenceCalc(dataframe):
    '''
    Calculate average valence using two methods
    1 - counting ambivalent nodes once
    2 - couunting ambivalent nodes twice
    '''
    valence_avg = 0
    if len(dataframe['shape']) > 0:  # If there are any concepts!!
        for valence in dataframe['shape']:
            if valence == 'neutral':
                valence_avg += 0
            elif 'positive' in valence:
                if 'weak' in valence:
                    valence_avg += 1
                elif valence == 'positive':
                    valence_avg += 2
                elif 'strong' in valence:
                    valence_avg += 3
            elif 'negative' in valence:
                if 'weak' in valence:
                    valence_avg -= 1
                elif valence == 'negative':
                    valence_avg -= 2
                elif 'strong' in valence:
                    valence_avg -= 3
        option1 = np.round(valence_avg/len(dataframe['shape']), 2)
        option2 = np.round(valence_avg/(len(dataframe['shape'])+len(dataframe[dataframe['shape'] == 'ambivalent'])), 2)
        return option1, option2
    else:
        return 0, 0
