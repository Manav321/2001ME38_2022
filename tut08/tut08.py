
from datetime import datetime
start_time = datetime.now()

import os
import openpyxl
import pandas as pd


ind = open("india_inns2.txt","r+")                # Input files reading
pak = open("pak_inns1.txt","r+")
teams = open("teams.txt","r+")

team_ind_n_pak = teams.readlines()

pak_team = team_ind_n_pak[0]
pak_player = pak_team[23:-1:].split(",")

ind_team = team_ind_n_pak[2]
ind_player = ind_team[20:-1:].split(",")



ind_lines = ind.readlines()                       # Read the lines of input files
for i in ind_lines:
    if i == '\n':                                 # Removes extra line
        ind_lines.remove(i)
      
pak_lines = pak.readlines()                       # Same as for ind_lines
for i in pak_lines:
    if i == '\n':
        pak_lines.remove(i)

wb = openpyxl.Workbook()
sheet = wb.active

ind_wickets = 0                                   
pak_wickets = 0
ind_b = 0
pak_b = 0
total_bowler_ind = 0
total_bowler_pak = 0

ind_out={}
pak_out={}
ind_bowl={}
pak_bowl={}
ind_bat={}
pak_bat={}


for i in pak_lines:
    x = i.index(".")
    pak_over = i[0:x + 2]
    temp = i[x + 2::].split(",")
    cb = temp[0].split("to")

    if f"{cb[0].strip()}" not in ind_bowl.keys() :
        ind_bowl[f"{cb[0].strip()}"] = [1,0,0,0,0,0,0]

    elif "wide" in temp[1]:                                   # If ball was wide
        pass

    elif "bye" in temp[1]:                                    # adding runs
        if "FOUR" in temp[2]:
            pak_b += 4
        elif "1" in temp[2]:
            pak_b += 1
        elif "2" in temp[2]:
            pak_b += 2
        elif "3" in temp[2]:
            pak_b += 3
        elif "4" in temp[2]:
            pak_b += 4
        elif "5" in temp[2]:
            pak_b += 5

    else:
        ind_bowl[f"{cb[0].strip()}"][0] += 1
    
    if f"{cb[1].strip()}" not in pak_bat.keys() and temp[1] != "wide":
        pak_bat[f"{cb[1].strip()}"] = [0,1,0,0,0]

    elif "wide" in temp[1] :
        pass

    else:
        pak_bat[f"{cb[1].strip()}"][1] += 1
    
    if "out" in temp[1]:
        ind_bowl[f"{cb[0].strip()}"][3] += 1
        if "Bowled" in temp[1].split("!!")[0]:
            pak_out[f"{cb[1].strip()}"] = ("b" + cb[0])

        elif "Caught" in temp[1].split("!!")[0]:
            w = (temp[1].split("!!")[0]).split("by")
            pak_out[f"{cb[1].strip()}"] = ("c" + w[1] +" b " + cb[0])

        elif "Lbw" in temp[1].split("!!")[0]:
            pak_out[f"{cb[1].strip()}"] = ("lbw  b "+cb[0])

    if "no run" in temp[1] or "out" in temp[1]:
        ind_bowl[f"{cb[0].strip()}"][2] += 0
        pak_bat[f"{cb[1].strip()}"][0] += 0

    elif "1 run" in temp[1]:
        ind_bowl[f"{cb[0].strip()}"][2] += 1
        pak_bat[f"{cb[1].strip()}"][0] += 1

    elif "2 run" in temp[1]:
        ind_bowl[f"{cb[0].strip()}"][2] += 2
        pak_bat[f"{cb[1].strip()}"][0] += 2

    elif "3 run" in temp[1]:
        ind_bowl[f"{cb[0].strip()}"][2] += 3
        pak_bat[f"{cb[1].strip()}"][0] += 3

    elif "4 run" in temp[1]:
        ind_bowl[f"{cb[0].strip()}"][2] += 4
        pak_bat[f"{cb[1].strip()}"][0] += 4

    elif "FOUR" in temp[1]:
        ind_bowl[f"{cb[0].strip()}"][2] += 4
        pak_bat[f"{cb[1].strip()}"][0] += 4
        pak_bat[f"{cb[1].strip()}"][2] += 1

    elif "SIX" in temp[1]:
        ind_bowl[f"{cb[0].strip()}"][2] += 6
        pak_bat[f"{cb[1].strip()}"][0] += 6
        pak_bat[f"{cb[1].strip()}"][3] += 1

    elif "wide" in temp[1]:
        if "wides" in temp[1]:
            ind_bowl[f"{cb[0].strip()}"][2] += int(temp[1][1])
            ind_bowl[f"{cb[0].strip()}"][5] += int(temp[1][1])

        else:
            ind_bowl[f"{cb[0].strip()}"][2] += 1
            ind_bowl[f"{cb[0].strip()}"][5] += 1



from platform import python_version
ver = python_version()

if ver == "3.8.10":
	print("Correct Version Installed")
else:
	print("Please install 3.8.10. Instruction are present in the GitHub Repo/Webmail. Url: https://pastebin.com/nvibxmjw")



#This shall be the last lines of the code.
end_time = datetime.now()
print('Duration of Program Execution: {}'.format(end_time - start_time))
