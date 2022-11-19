

from datetime import datetime
start_time = datetime.now()

import pandas as pd
import os

from platform import python_version
ver = python_version()

if ver == "3.8.10":
    print("Correct Version Installed")
else:
    print("Please install 3.8.10. Instruction are present in the GitHub Repo/Webmail. Url: https://pastebin.com/nvibxmjw")

attendance_data = pd.read_csv('input_attendance.csv')
students_registered = pd.read_csv('input_registered_students.csv')


holidays = ['15-08-2022', '19-09-2022', '22-09-2022']   # dates on which class wasn't taken and were Monday/Thrusday

# identify Mondays and Thursdays from unique dates on which attendance was marked
def class_dates():

    real_class_dates = []

    # date is the first element of the list formed when an entry of Timestamp column is splitted by " " character 
    dates = [str(timestamp).split(' ')[0] for timestamp in attendance_data["Timestamp"]]

    dates = [date for date in dates if date not in holidays] # only considering dates on which class took place

    dates = sorted((set(dates)), key=lambda date: datetime.strptime(date, "%d-%m-%Y"))    # converting list to set

    for date in dates:

        # identifying the day at date using datetime function
        # split date with respect to "-" character
        day = datetime(int(date.split('-')[2]), int(date.split('-')[1]), int(date.split('-')[0])).strftime('%a')
        if day in ["Mon", "Thu"]:
            real_class_dates.append(date)

    return real_class_dates

real_class_dates = class_dates()

all_mon_thurs = sorted(real_class_dates + holidays, key=lambda date: datetime.strptime(date, "%d-%m-%Y"))

# total lecture taken is the length of real_class_dates
total_lec_taken = len(real_class_dates) 






#This shall be the last lines of the code.
end_time = datetime.now()
print('Duration of Program Execution: {}'.format(end_time - start_time))
