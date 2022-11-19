

from datetime import datetime
start_time = datetime.now()

import pandas as pd

df = pd.read_excel("octant_input.xlsx")

mod=5000 

# made a global list of octants
octant = [1, -1, 2, -2, 3, -3, 4, -4]

octant_name_id_mapping = {
        "1"  : ["Internal outward interaction", 0], # [name of the octant, freq of getting ranked 1]
        "-1" : ["External outward interaction", 0], 
        "2"  : ["External Ejection", 0],
        "-2" : ["Internal Ejection", 0],
        "3"  : ["External inward interaction", 0],
        "-3" : ["Internal inward interaction", 0],
        "4"  : ["Internal sweep", 0],
        "-4" : ["External sweep", 0]
        }


def headings():

    df.insert(4, "U_avg", value="")
    df.insert(5, "V_avg", value="")
    df.insert(6, "W_avg", value="")

    df.insert(7, "U' = U - U_avg", value="")
    df.insert(8, "V' = V - V_avg", value="")
    df.insert(9, "W' = W - W_avg", value="")

    df.insert(10, "Octant", value="")

    df.insert(11, "", value="")                   # Inserted an empty column
    df.insert(12, "Octant ID", value="")

    for i in range(8):                            # octants
        df.insert(i+13, octant[i], value="")
    
    for i in range(8):                            # Rank of octant
        df.insert(21+i, f"Rank of {octant[i]}", value="")

    df.insert(29, "Rank 1 Octant", value="")
    df.insert(30, "Rank 1 Octant Name", value="")


def octant_identity():

    df.at[0, "U_avg"] = df['U'].mean()
    df.at[0, "V_avg"] = df['V'].mean()
    df.at[0, "W_avg"] = df['W'].mean()
    
    df["U' = U - U_avg"] = (df['U'] - df['U'].mean())
    df["V' = V - V_avg"] = (df['V'] - df['V'].mean())
    df["W' = W - W_avg"] = (df['W'] - df['W'].mean())
    

    octant = []                              # array to store the octant values of points
    
    for i in range(len(df)):
        A = df.loc[i, "U' = U - U_avg"]
        B = df.loc[i, "V' = V - V_avg"]
        C = df.loc[i, "W' = W - W_avg"]

            # when U is +ve
        if A>0:
            #when V is +ve
            if B>0:
                if C>0:
                    octant.append(int(1))
                else:
                    octant.append(int(-1))

            # when V is -ve
            else:
                if C>0:
                    octant.append(int(4))
                else:
                    octant.append(int(-4))

        # when U is -ve
        else:
            # when V is +ve
            if B>0:
                if C>0:
                    octant.append(int(2))
                else:
                    octant.append(int(-2))

            # when V is -ve
            else:
                if C>0:
                    octant.append(int(3))
                else:
                    octant.append(int(-3))
    
    df["Octant"] = octant


def rank_(row):

    # filling the dictionary with count values in the given interval of that octant 
    oct_count = {
            "1"  : df.at[row, 1],
            "-1" : df.at[row, -1],
            "2"  : df.at[row, 2],
            "-2" : df.at[row, -2],
            "3"  : df.at[row, 3],
            "-3" : df.at[row, -3],
            "4"  : df.at[row, 4],
            "-4" : df.at[row, -4],
            }

    occ_l = [oct_count[str(oc)] for oc in octant] # simple list containing the occurances of octant
    occ_l.sort(reverse=True) # reversing the list

    for i in range(8):
        # get the index of a taken octant's count value in a sorted list and insert it in the rank_ column (same row, given interval)
        # * '+1' since indices start from 0
        df.at[row, f"Rank of {octant[i]}"] = occ_l.index( oct_count[ str(octant[i]) ] ) + 1

    for oc in octant:
        if oct_count[str(oc)]==occ_l[0]:
            df.at[row, "Rank 1 Octant"] = oc
            df.at[row, "Rank 1 Octant Name"] = octant_name_id_mapping[str(oc)][0]

            
            return oc  # returning rank 1 octant


from platform import python_version
ver = python_version()

if ver == "3.8.10":
    print("Correct Version Installed")
else:
    print("Please install 3.8.10. Instruction are present in the GitHub Repo/Webmail. Url: https://pastebin.com/nvibxmjw")




headings()
octant_identity()
#octant_range_names(mod)


df.to_excel('octant_output_rank__excel.xlsx', index=False)


#This shall be the last lines of the code.
end_time = datetime.now()
print('Duration of Program Execution: {}'.format(end_time - start_time))
