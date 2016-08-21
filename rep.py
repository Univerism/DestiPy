import requests
from Tkinter import *
import ttk
root = Tk() 

API_KEY = 'YOUR API KEY'
HEADERS = {"X-API-Key": API_KEY}

charDict = {}
vendorDict = {3871980777: 'New Monarchy', 529303302: 'Cryptarch', 2161005788: 'Iron Banner', 452808717: 'Queen', 3233510749: 'Vanguard', 1357277120: 'Crucible', 2778795080: 'Dead Orbit', 1424722124: 'Future War Cult', 1716568313: 'Character Level', 2335631936: 'Gunsmith', 3641985238: 'House of Judgment', 174528503: 'Crota\'s Bane', }
progessDict = {}

def searchForMembership(membershipType, displayName):
    res = requests.get("https://www.bungie.net/Platform/Destiny/SearchDestinyPlayer/" + membershipType + "/" + displayName, headers=HEADERS)
    if len(res.json()["Response"]) == 0:
        print "Error! Wrong username or console."
    else:
        user = res.json()["Response"][0]["membershipId"]
        handleSearchResponse(membershipType, user)

def handleSearchResponse(membershipType, user):
    res = requests.get("https://www.bungie.net/Platform/Destiny/" + membershipType + "/Account/" + user + "/", headers=HEADERS)
    charData = res.json()["Response"]["data"]["characters"]
    for char in charData:
        if str(char["characterBase"]["classHash"]) == "3655393761":
            charDict['titan'] = str(char["characterBase"]["characterId"])
        if str(char["characterBase"]["classHash"]) == "671679327":
            charDict['hunter'] = str(char["characterBase"]["characterId"]) 

    
    f = Entry(root, textvariable=charChoice).grid(row=1, column=2)
    Button(root, text="Select", command=lambda: charInfo(user)).grid(row=1, column=3)
    
def charInfo(user):
    global charChoice
    tree.delete(*tree.get_children())
    handleProgressData(str(charChoice.get()), user)

def handleProgressData(charChoice, user):
    global tree
    res = requests.get("https://www.bungie.net/Platform/Destiny/" + str(membershipType.get()) + "/Account/" + user + "/Character/" + charDict[charChoice] + "/Progression/", headers=HEADERS)
    progressData = res.json()["Response"]["data"]["progressions"]

    for i in range(34):
        
        if int(progressData[i]["level"]) <= 1 and int(progressData[i]["progressToNextLevel"]) == 0:
            continue
        else:
            tree.insert("", 0, values=("%s" % vendorDict.get(int(progressData[i]["progressionHash"]), str(progressData[i]["progressionHash"])), str(progressData[i]["level"]), str(progressData[i]["progressToNextLevel"])))
        
def gatherInfo():
    searchForMembership(str(membershipType.get()), str(displayName.get()))
        
if __name__ == '__main__':
    
    
    charChoice = StringVar()
    membershipType = IntVar()
    displayName = StringVar()
    e = Entry(root, textvariable=displayName).grid(row=0, column=2)
    
    Radiobutton(root, text="Xbox", variable=membershipType, value=1).grid(row=0, column=0)
    Radiobutton(root, text="PS", variable=membershipType, value=2).grid(row=0, column=1)
    Button(root, text="Search", command=gatherInfo).grid(row=0, column=3)
 
    tree = ttk.Treeview(root, columns=3, show="headings")
 
    tree["columns"]=("vendors", "level", "progress")
    tree.column("vendors")
    tree.column("level")
    tree.column("progress")
    tree.heading("vendors", text="Vendor")
    tree.heading("level", text="Current Level")
    tree.heading("progress", text="Current Progress") 
    tree.grid(row=1)

    root.mainloop()
