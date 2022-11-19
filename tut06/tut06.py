

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

attendance_report_consolidated_df = pd.DataFrame()

def attendance_report(roll_no, name):

    # declaring this dataframe as global so that it does not gets created in this function with local scope
    global attendance_report_consolidated_df

    roll_no_df = pd.DataFrame()

    roll_no_df.insert(0, "Date", value="")
    roll_no_df.insert(1, "Roll", value=[roll_no])
    roll_no_df.insert(2, "Name", value=[name])
    roll_no_df.insert(3, "Total Attendance Count", value="")
    roll_no_df.insert(4, "Real", value="")
    roll_no_df.insert(5, "Duplicate", value="")
    roll_no_df.insert(6, "Invalid", value="")
    roll_no_df.insert(7, "Absent", value="")
    
    # dictionary storing the dates and number of attendances marked on that date 
    att_dates = {date: {'R': 0, 'D': 0, 'I': 0} for date in all_mon_thurs}

    # searching for entries of roll_no in the attendance database
    for person, timestamp in zip(attendance_data["Attendance"], attendance_data["Timestamp"]):

        # if match is found
        if person.split(' ')[0] == roll_no:

            current_date = timestamp.split(' ')[0]
            current_time = timestamp.split(' ')[1]
            
            if current_date in real_class_dates: 
                
                if current_time.split(':')[0] == '14':              # if marked attendance in on time 14:00 - 14:59

                    if att_dates[current_date]['R'] == 1:           # if the real attendance has already been marked
                        att_dates[current_date]['D']+=1             # increase the duplicate by 1 (for who has marked mutiple attendance on same day)

                    else:
                        att_dates[current_date]['R']+=1             # else record real attendance

                else:
                    att_dates[current_date]['I']+=1                 # attendance is marked but outside lec time, increase invalid mark by 1
                    
            elif current_date in holidays:                          # if attendance is marked on a day which was holiday (class wasn't taken) {holidays are mon/thurs holidays}
                att_dates[current_date]['I']+=1

        # no else statement cause ignoring non-lec hours attendance marked

    for index,date in enumerate(all_mon_thurs, start=1):

        # printing dates from 1st row
        roll_no_df.at[index, "Date"] = date
        roll_no_df.at[index, "Total Attendance Count"] = att_dates[date]['R'] + att_dates[date]['D'] + att_dates[date]['I']
        roll_no_df.at[index, "Real"] = att_dates[date]['R']
        roll_no_df.at[index, "Duplicate"] = att_dates[date]['D']
        roll_no_df.at[index, "Invalid"] = att_dates[date]['I']
        

        if roll_no_df.at[index, "Total Attendance Count"]>0 and roll_no_df.at[index, "Real"]==1:        # real attendance = 1; present in class
            roll_no_df.at[index, "Absent"] = 0
        else:
            roll_no_df.at[index, "Absent"] = 1                                                          # else invalid/no marked attendance; absent in class

    
    roll_no_df.to_excel(f'output/{roll_no}.xlsx', index=False)                                          # write the data to roll_no's csv

    temp_df = pd.DataFrame(columns=["Roll", "Name"] + all_mon_thurs+ ["Actual Lecture Taken", "Total Real", "% Attendance"])
    temp_df["Roll"] = [roll_no]
    temp_df["Name"] = [name]

    total_real = 0
    for date in att_dates:
        if att_dates[date]['R'] == 1:
            temp_df[date] = 'P'
            total_real+=1
        else:
            temp_df[date] = 'A'

    temp_df["Actual Lecture Taken"] = total_lec_taken
    temp_df["Total Real"] = total_real
    temp_df["% Attendance"] = round(total_real/total_lec_taken*100, 2)

    attendance_report_consolidated_df = pd.concat([attendance_report_consolidated_df, temp_df])

#---------------------------------------------------------------


#---------------------------------------------------------------

# iterateting through the list of registered students
for roll_no, name in zip(students_registered["Roll No"], students_registered["Name"]):
    attendance_report(roll_no, name)

attendance_report_consolidated_df.to_excel(f'output/attendance_report_consolidated.xlsx', index=False)




#This shall be the last lines of the code.
end_time = datetime.now()
print('Duration of Program Execution: {}'.format(end_time - start_time))
