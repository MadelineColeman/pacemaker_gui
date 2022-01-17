import pandas as pd
import itertools
import numpy as np
from layoutFunctions import pacingModePar, paramNameList

#%% Functions

# Define value ranges for parameter input
def inputValues(param):
    df = pd.read_csv("parameters.csv")
    
    df['values'] = ""
    
    for i in range(len(df)):
        if(pd.notnull(df['Lower Limit'][i])):
            df['values'][i] = list([*np.arange(df["Lower Limit"][i], df["Upper Limit"][i]+df['Increment'][i], df['Increment'][i])])
            df['values'][i] = [round(num, 2) for num in df['values'][i]]
        else:
            df['values'][i] = []
        if(pd.notnull(df['Not Pattern'][i])):
            try:
                df['values'][i].append(float(df['Not Pattern'][i]))
            except ValueError:
                df['values'][i].append(df['Not Pattern'][i])
    
    df = df.groupby(['Parameter']).agg(list)
    
    for i in range(len(df)):
        df['values'][i] = list(itertools.chain(*df['values'][i]))     
        np.sort(df['values'][i])
    
    for i in df.index:
        if (i in param):
            break;
        
    return df['values'][i]

## verify the user input
def inputVerify(mode, window, values):
    verifyInputs = []
    inputs = []
    paramList = paramNameList()
    for keyVal in pacingModePar(mode):
        window[f'-Par{keyVal}-'].update(text_color = 'black')
        try:
            values[f'-ParIN{keyVal}-'] = float(values[f'-ParIN{keyVal}-'])
            if(not(values[f'-ParIN{keyVal}-'] in inputValues(paramList[keyVal].rstrip()))):
                verifyInputs.append(False)
                window[f'-Par{keyVal}-'].update(text_color = 'red')
            else:
                verifyInputs.append(True)
        except ValueError:
            verifyInputs.append(False)
            window[f'-Par{keyVal}-'].update(text_color = 'red')

        inputs.append(values[f'-ParIN{keyVal}-'])
    ##print(type(values['-ParIN0-']))
    ## Check to ensure lower limit < upper limit
    if (type(values['-ParIN0-']) == float and type(values['-ParIN1-']) == float and values['-ParIN0-']>= values['-ParIN1-']):
        verifyInputs.append(False)
        window['-Par0-'].update(text_color = 'red')
        window['-Par1-'].update(text_color = 'red')
        
    return verifyInputs