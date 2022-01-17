import PySimpleGUI as sg
from inputVerify import inputValues
from layoutFunctions import paramNameList
from egram import create_plot, draw_figure

## Returns the layout for each gui screen
def layout(layout):
    
    sg.theme('Teal Mono')
    
    # Button layout for select screen
    modeButLay = {'size':(7,2), 'font':('Franklin Gothic Book', 24), 'button_color':("Black","#FFC0CB"), 'border_width':2}
    
    # Parameters list for mode screens
    paramList = paramNameList()
    
    # Layouts for parameter layout elements
    paramButLay = {'font':('Franklin Gothic Book', 14), 'button_color':("Black","#FFC0CB"), 'border_width':2}       
    paramTextLay = {'font':('Franklin Gothic Book', 14), 'visible':False, 'justification':'centre', 'size':(30,1)}
    paramInputLay = {'font':('Franklin Gothic Book', 14), 'visible':False, 'size':(20,1)}  
    refreshButLay = {'button_color':"#ADD8E6"}
    
    # Login screen layout
    loginButLay = {'font':('Franklin Gothic Book', 12), 'button_color':'#000000', 'border_width':2}
    if layout == "login":
        layout = [[sg.Text('Welcome to the Pace Maker', font=("Franklin Gothic Book",30))],
          [sg.Text('Please Login below', font=("Franklin Gothic Book",15))],
          [sg.Text('  Username ', font=("Helvetica",15), size=(12,1)), sg.Input(font=("Helvetica",15,),size=(25,1),key='-User-')],
          [sg.Text('  Password ', font=("Helvetica",15), size=(12,1)), sg.Input(font=("Helvetica",15), size=(25,1),key='-Pass-', password_char="*")],
          [sg.pin(sg.Text('Username or Password are Incorrect', font=("Helvectica", 15), text_color = 'red', visible = False, key="-Incorrect-"))],
          [sg.Button("Login", **loginButLay), sg.Button('New User? Register here ', **loginButLay)]]
        
    # Signup screen layout
    elif layout == "signup":
        layout = [[sg.Button("Back to Login")],
            [sg.Text('Please Register below', font=("Helvetica",15))],
            [sg.Text('Username ', font=("Helvetica",15)), sg.Input(font=("Helvetica",15), key="-newUser-")],
            [sg.Text('Password ', font=("Helvetica",15)), sg.Input(font=("Helvetica",15), key="-newPass-",password_char="*")],
            [sg.Text('Re-enter Password ', font=("Helvetica",15)), sg.Input(font=("Helvetica",15), key="-verifyPass-",password_char="*")],
            [sg.pin(sg.Text('Maximum Number of Users Already', font=("Helvetica",15),  text_color = 'red', visible = False, key = '-Max-'))],
            [sg.pin(sg.Text('Username Already in Use or Invalid', font=("Helvetica",15),  text_color = 'red', visible = False, key = '-inUse-'))],
            [sg.pin(sg.Text('Passwords Do Not Match or Password Invalid (Must not have spaces or be blank)', font=("Helvetica",15),  text_color = 'red', visible = False, key = '-Match-'))],
            [sg.Button("Sign Up", font=("Helvetica",12))]]
    
    # Select mode screen layout background_color = '#FAEBD7'
    elif layout == "select":
        layout = [[sg.Button("Logout",size=(10,1)),sg.Text(key='-allignText1-'),
                   sg.Image(filename='',size=(16,16),key='-serIndImg1-'),
                   sg.Text('', key='-serialInd1-', font=('Helvetica',12)),
                   sg.Button("",**refreshButLay,key='-RefreshBut1-' ,image_filename="refresh.png" )],
                  [sg.Canvas(size=(1,1))],
                  [sg.Text('Select Pacing Mode', font=("Franklin Gothic Book",30), justification='c')],
                  [sg.Text('\t  '),sg.Button("AOO",**modeButLay), sg.Button("VOO",**modeButLay),sg.Button("AAI",**modeButLay), 
                   sg.Button("VVI",**modeButLay), sg.Button("DOO",**modeButLay), sg.Text('\t')],
                  [sg.Text('\t  '),sg.Button("AOOR",**modeButLay), sg.Button("VOOR",**modeButLay), sg.Button("AAIR",**modeButLay),
                   sg.Button("VVIR",**modeButLay), sg.Button("DOOR",**modeButLay), sg.Text('\t')],
                   [sg.Button("View Egram", size = (20,1))]]
                  
    # Pacing mode layouts  
    # elif layout == "mode":
    #     layout = [[sg.Button("Go Back",size=(10,1)),sg.Text(key='-allignText2-'),
    #                sg.Image(filename='',size=(16,16),key='-serIndImg2-'),
    #                sg.Text('', key='-serialInd2-', font=('Helvetica',12)),
    #                sg.Button("",**refreshButLay,key='-RefreshBut2-' ,image_filename="refresh.png" )],
    #               [sg.Canvas(size=(1,1))],
    #               [sg.Text('', font=("Franklin Gothic Book",30), key = "-ParTitle-")],
    #               [sg.pin(sg.Text('Parameter Input Invalid', text_color='red', font=("Helvetica",15), visible=False,key="-FalseParIN-"))],
    #               [sg.Text('', font=("Helvetica",15), visible=True, key='-ParSubTitle-')],
    #               *[[sg.pin(sg.Text(str(paramList[i]), key=f'-Par{i}-', **paramTextLay)), 
    #                  sg.pin(sg.Combo(inputValues(paramList[i]), enable_events = True, key=f'-ParIN{i}-',**paramInputLay)),
    #                  sg.pin(sg.Text('preval', visible = False, key = f'-ParPrev{i}-'))] for i in range(len(paramList))],
    #               [sg.pin(sg.Text('Parameters Set', text_color='green', font=("Helvetica",15), visible=False,key="-TrueParIN-"))],
    #               [sg.pin(sg.Button("Set Parameters",**paramButLay, enable_events = True, visible=False,key = 'Set Parameters')),
    #                sg.pin(sg.Button("Change Parameters",**paramButLay, visible = True, key = 'Change Parameters')),
    #                sg.pin(sg.Button("Cancel",**paramButLay, visible = False, key = 'Cancel'))]]

    elif layout == "mode":
        layout = [[sg.Button("Go Back",size=(10,1)),sg.Text(key='-allignText2-'),
                   sg.Image(filename='',size=(16,16),key='-serIndImg2-'),
                   sg.Text('', key='-serialInd2-', font=('Helvetica',12)),
                   sg.Button("",**refreshButLay,key='-RefreshBut2-' ,image_filename="refresh.png" )],
                  [sg.Canvas(size=(1,1))],
                  [sg.Text('', font=("Franklin Gothic Book",30), key = "-ParTitle-")],
                  [sg.Text('Set Parameters Using Dropdowns', font=("Helvetica",15), visible=True)],
                  [sg.Text('Parameter Input Out of Range', text_color='red', font=("Helvetica",15), visible=False,key="-FalseParIN-")],
                  *[[sg.pin(sg.Text(str(paramList[i]), key=f'-Par{i}-', **paramTextLay)), 
                     sg.pin(sg.Combo(inputValues(paramList[i]), enable_events = True, key=f'-ParIN{i}-',**paramInputLay))] for i in range(len(paramList))],
                  [sg.Text('Parameters Set', text_color='green', font=("Helvetica",15), visible=False,key="-TrueParIN-")],
                  [sg.Button("Set Parameters",**paramButLay)]]
        
    elif layout == "egram":
        layout = [[sg.Button("Exit Egram",size=(10,1)),
                       sg.Image(filename='',size=(16,16),key='-serIndImg3-'),
                       sg.Text('', key='-serialInd3-', font=('Helvetica',12)),
                       sg.Button("",**refreshButLay,key='-RefreshBut3-' ,image_filename="refresh.png" )],
                [sg.Text('Egram', font=("Franklin Gothic Book",30), justification = 'center')],
                [sg.Canvas(size=(700,700), key = "-CANVAS-")],
                [sg.Text('Select data to plot:')],
                  [sg.Checkbox("Atrial", key = "-atrial-", default = True), 
                   sg.Checkbox("Ventrical", key = "-vent-", default = True)]]
    
    
    return layout
