#%% Import Libraries
import PySimpleGUI as sg
from userVerify import verify, register
from layouts import layout
from layoutFunctions import updateSerialInd, pacingModePar, updateText, cancelErrorReset, changeVisibility, paramInputs, clrParamInputs, clrTextInput, clrErrors, resetVisibility
from inputVerify import inputVerify
from egram import create_plot, update
from send_data import send_data
from serialComm import serialComm

#%% Display/Run app 
# keys for inputs of different screens
prevDevice = 'address'
loginKeys = ["-User-", "-Pass-"]
signupKeys = ['-newUser-', '-newPass-', '-verifyPass-']

# define app layout
layout = [[sg.Column(layout('login'), visible = True, key='-COL1-'),
           sg.Column(layout('signup'), visible=False, key='-COL2-'),
           sg.Column(layout('select'), visible = False, key='-COL3-'), 
           sg.Column(layout('mode'), visible=False, key='-COL4-'),
           sg.Column(layout('egram'), visible=False, key='-COL5-')]]

window = sg.Window('Pace Maker', layout, margins=(10,10))
layout = 1

flag = 0
serial= serialComm()
send_data = False
while True:
    
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    print(event)
    
    updateSerialInd(serial,window) 
    
    ## Go to register screen
    if (event == 'New User? Register here '):
        clrErrors(window)
        window[f'-COL{layout}-'].update(visible = False)
        layout = 2
        clrTextInput(loginKeys, window)
        window[f'-COL{layout}-'].update(visible = True)
    
    ## Verify Login
    if (event == 'Login'):
        clrErrors(window)
        updateSerialInd(serial,window) 
        if (verify(values['-User-'], values['-Pass-']) == True):
            clrTextInput(loginKeys, window)
            window[f'-COL{layout}-'].update(visible = False)
            layout = 3
            window[f'-COL{layout}-'].update(visible = True)
        else:
            window["-Incorrect-"].update(visible = True)
        serial.initDeviceStatus()
            
    ## Verify Registration        
    if event == "Sign Up":
        clrErrors(window)
        verifyReg = register(values['-newUser-'], values['-newPass-'], values['-verifyPass-'])
        if(verifyReg == [False, False]):
            window['-Max-'].update(visible = True)
        elif (verifyReg == [True, False]):
            window['-inUse-'].update(visible = True)
        elif (verifyReg == [False, True]):
            window['-Match-'].update(visible = True)
        else:
            clrTextInput(signupKeys, window)
            window[f'-COL{layout}-'].update(visible=False)
            layout = 1
            window[f'-COL{layout}-'].update(visible=True)
    
    ## Open mode screen  
    if event in ['AOO', 'VOO', 'AAI', 'VVI','DOO', 'AOOR', 'VOOR', 'AAIR', 'VVIR', 'DOOR']:
        updateSerialInd(serial,window) 
        mode = event
        paramInputs(window, False, True)
        updateText('-ParTitle-', f'{event} Parameters', window)
        pacingMode = event
        changeVisibility(pacingModePar(event), window)
        for keyVal in pacingModePar(mode):
            window[f'-Par{keyVal}-'].update(text_color = 'black')
        window[f'-COL{layout}-'].update(visible=False)
        layout = 4
        window[f'-COL{layout}-'].update(visible=True)
    
    ## Go to previous page
    if event == 'Go Back':
        updateSerialInd(serial,window) 
        resetVisibility(window)
        clrParamInputs(pacingMode, window)
        window[f'-COL{layout}-'].update(visible=False)
        layout = layout-1
        window[f'-COL{layout}-'].update(visible=True)
    
    ## Go back to login screen
    if (event == "Logout" or event == "Back to Login"):
        if event == "Back to Login":
            clrTextInput(signupKeys, window)
        clrErrors(window)
        window[f'-COL{layout}-'].update(visible=False)
        layout = 1
        window[f'-COL{layout}-'].update(visible=True)

                
    ## Set Parameters
    if(event == "Set Parameters"):
        print("\n\n Set Paremters \n\n")
        print(mode)
        if (False in inputVerify(mode, window, values)):
            paramInputs(window, False, False)
        else:
            send_data = True
            paramInputs(window, True, False)
            #parButtonsUpdate(True, False, False, window)
            changeVisibility(pacingModePar(mode), window)
    

    ##Egram
    if (event == "View Egram"):
        updateSerialInd(serial,window) 
        window[f'-COL{layout}-'].update(visible=False)
        layout = 5
        window[f'-COL{layout}-'].update(visible=True)
        if (flag == 0):
            ax, fig_agg = create_plot(window)
            flag = 1
        layout = update(window, values, ax, fig_agg, event, flag, layout)
        
    if (event == "Exit Egram"):
        updateSerialInd(serial,window) 
        window[f'-COL{layout}-'].update(visible=False)
        layout = 3
        window[f'-COL{layout}-'].update(visible=True) 

    #Refresh Serial Indicator status
    if((event == "-RefreshBut1-") or (event == "-RefreshBut2-") or (event == "-RefreshBut3-")):
        updateSerialInd(serial,window) 

window.close()

