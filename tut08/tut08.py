
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



from platform import python_version
ver = python_version()

if ver == "3.8.10":
	print("Correct Version Installed")
else:
	print("Please install 3.8.10. Instruction are present in the GitHub Repo/Webmail. Url: https://pastebin.com/nvibxmjw")



#This shall be the last lines of the code.
end_time = datetime.now()
print('Duration of Program Execution: {}'.format(end_time - start_time))
