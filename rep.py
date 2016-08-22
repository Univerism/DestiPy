import requests
from Tkinter import *
import ttk
root = Tk()
content = ttk.Frame(root, padding=(3,3,12,12))

API_KEY = 'YOUR API KEY'
HEADERS = {"X-API-Key": API_KEY}

charDict = {}
progessDict = {}
vendorDict = {1707948164: 'Moon Chests', 3298204156: 'Character EXP', 2158037182: 'Venus Chests',
              807090922: 'Queen', 3186678724: 'Calcified Fragments', 45089664: 'Terminals',
              2175864601: 'Moments of Triumph', 2060414935: 'Base Item Level', 2030054750: 'Character Prestige',
              1774654531: 'Cosmodrome Chests', 3871980777: 'New Monarchy', 529303302: 'Cryptarch',
              2161005788: 'Iron Banner', 452808717: 'Queen', 3233510749: 'Vanguard', 1357277120: 'Crucible',
              2778795080: 'Dead Orbit', 1424722124: 'Future War Cult', 1716568313: 'Character Level',
              2335631936: 'Gunsmith', 3641985238: 'House of Judgment', 174528503: 'Crota\'s Bane',
              2763619072: 'SRL Racing', 2193513588: 'Mars Chests', 2033897742: 'Vanguard Marks',
              594203991: 'Iron Banner Medallions'}

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
            charDict['Titan'] = str(char["characterBase"]["characterId"])
        if str(char["characterBase"]["classHash"]) == "671679327":
            charDict['Hunter'] = str(char["characterBase"]["characterId"])
        if str(char["characterBase"]["classHash"]) == "2271682572":
            charDict['Warlock'] = str(char["characterBase"]["characterId"])    

    Label(searchFrame, text="Select Character: ").grid(row=0, column=4)
    f = ttk.Combobox(searchFrame, values=charDict.keys(), textvariable=charChoice).grid(row=0, column=5)
    Button(searchFrame, text="Select", command=lambda: charInfo(user)).grid(row=0, column=6, padx=5)
    
def charInfo(user):
        
    handleProgressData(str(charChoice.get()), user)

def handleProgressData(charChoice, user):
    global tree
    res = requests.get("https://www.bungie.net/Platform/Destiny/" + str(membershipType.get()) + "/Account/" + user + "/Character/" + charDict[charChoice] + "/Progression/", headers=HEADERS)
    progressData = res.json()["Response"]["data"]["progressions"]
    tree.delete(*tree.get_children())
    for i in range(34):
        
        if int(progressData[i]["level"]) <= 1 and int(progressData[i]["progressToNextLevel"]) == 0:
            continue
        else:
            tree.insert("", 0, values=("%s" % vendorDict.get(int(progressData[i]["progressionHash"]), str(progressData[i]["progressionHash"])), str(progressData[i]["level"]), str(progressData[i]["progressToNextLevel"])))
        
if __name__ == '__main__':
    charChoice = StringVar()
    membershipType = IntVar()
    displayName = StringVar()
    content.grid(column=0,row=0)
    searchFrame = Frame(content)
    searchFrame.grid(row=0, column=0, columnspan=8, pady=5, sticky=W)
    Radiobutton(searchFrame, text="Xbox", variable=membershipType, value=1).grid(row=0, column=0)
    Radiobutton(searchFrame, text="PS", variable=membershipType, value=2).grid(row=0, column=1)
    e = Entry(searchFrame, textvariable=displayName).grid(row=0, column=2)
    Button(searchFrame, text="Search", command=lambda: searchForMembership(str(membershipType.get()), str(displayName.get()))).grid(row=0, column=3, padx=5)
 
    tree = ttk.Treeview(content, columns=3, show="headings")
 
    tree["columns"]=("vendors", "level", "progress")
    tree.column("vendors")
    tree.column("level")
    tree.column("progress")
    tree.heading("vendors", text="Vendor")
    tree.heading("level", text="Current Level")
    tree.heading("progress", text="Current Progress") 
    tree.grid(row=1)

    root.mainloop()
