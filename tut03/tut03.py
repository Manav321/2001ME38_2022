import pandas as pd

from platform import python_version
ver = python_version()

if ver == "3.8.10":
    print("Correct Version Installed")
else:
    print("Please install 3.8.10. Instruction are present in the GitHub Repo/Webmail. Url: https://pastebin.com/nvibxmjw")


mod = 5000

df = pd.read_excel("input_octant_longest_subsequence.xlsx")

# Taking mean of U, V and W
U_avg = df['U'].mean()
V_avg = df['V'].mean()
W_avg = df['W'].mean()

df["U_avg"] = U_avg      #Defined columns

#To print U_avg once, Otherwise would have filled all the cells below with the same value(U_avg)
df["U_avg"] = df["U_avg"].head(1)

df["V_avg"] = V_avg
df["V_avg"] = df["V_avg"].head(1)

df["W_avg"] = W_avg
df["W_avg"] = df["W_avg"].head(1)

U_subt_U_avg = (df['U'] - U_avg)
V_subt_V_avg = (df['V'] - V_avg)
W_subt_W_avg = (df['W'] - W_avg)

#Subtracting U_avg from U. Similiarly with the others.
df["U' = U - U_avg"] = U_subt_U_avg
df["V' = V - V_avg"] = V_subt_V_avg
df["W' = W - W_avg"] = W_subt_W_avg    

octant = []

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

#octant names, length and frequency of longest subsequence
data = {
        "octants" : ["-4", "-3", "-2", "-1", "1", "2", "3", "4"],

        "length_of_longest_s" : {"1"  : 1,"-1" : 1,"2"  : 1,"-2" : 1,"3"  : 1,"-3" : 1,"4"  : 1,"-4" : 1,},

        "freq" : {"1"  : 0,"-1" : 0,"2"  : 0,"-2" : 0,"3"  : 0,"-3" : 0,"4"  : 0,"-4" : 0,}
        }

def ol_subsequence_count(): # octant longest subsequence count
    l_of_string = 1   # length of string
    for i in range(len(df) - 1):

        if df["Octant"][i] == df["Octant"][i+1]:

            l_of_string+=1

            # update the longest subsequence by comparing existing value and current length
            data["length_of_longest_s"][str(df["Octant"][i])] = max(data["length_of_longest_s"][str(df["Octant"][i])], l_of_string)

        #elements are different, reset l_of_string
        else:
            l_of_string = 1

#frequency of longest subsequence
    l_of_string = 1
    for i in range(len(df) - 1):
        if df["Octant"][i] == df["Octant"][i+1]:
            l_of_string+=1

            #current length of subsequence is equal to longest, increament the frequency by one
            if l_of_string == data["length_of_longest_s"][str(df["Octant"][i])]:
                data["freq"][str(df["Octant"][i])]+=1

        else:
            l_of_string = 1