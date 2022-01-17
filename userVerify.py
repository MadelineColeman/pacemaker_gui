import os

#%% Verify user logins
def verify(username, password):
    login = False
    users = os.listdir("Users/")
    for s in range(len(users)): 
        users[s] = users[s].strip(".txt")
    if ((username in users) == False):
        return login
    name = "Users/" + username +".txt"
    file = open(name, "r")
    if (password == file.read()):
        login = True
    return login 

#%% Register a new user
def register(username, password, verifyPass):
    newUser = [False, False]
    if (password != verifyPass or (" " in password) or password == ""):
        newUser = [False, True]
        return newUser
    path = "Users/"
    numUsers = len(os.listdir(path))
    if numUsers < 10:
        users = os.listdir(path)
        for s in range(len(users)): 
            users[s] = users[s].strip(".txt")
        if (username in users or username == "" or (" " in username)):
            newUser = [True, False]
        else:
            name = path + username +".txt"
            file = open(name, "w")
            file.write(password)
            file.close()
            newUser = [True, True]
    return newUser
