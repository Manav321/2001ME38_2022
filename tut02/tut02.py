import pandas as pd

from platform import python_version
ver = python_version()

# if ver == "3.8.10":
#     print("Correct Version Installed")
# else:
#     print("Please install 3.8.10. Instruction are present in the GitHub Repo/Webmail. Url: https://pastebin.com/nvibxmnw")

mod = 5000

df = pd.read_excel("input_octant_transition_identify.xlsx")

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

# Printing and tabulating octant data
row_top = ["", "Octant ID", "1", "-1", "2", "-2", "3", "-3", "4", "-4"]
for i in range(len(row_top)):
    df.insert(i+11, row_top[i], value="")

df.iloc[0, 12] = "Overall count"

for i in range(8):
    df.iloc[0, i+13] = octant.count(int(row_top[2+i]))


df.iloc[1, 11] = "User input"
df.iloc[1, 12] = "Mod " + str(mod)

x, k = 0, 3
df.iloc[2,12] = f"{x}-{x+mod-1}"
x = x + mod


while x < len(df):
    # printing ranges
    df.iloc[k, 12] = f"{x+1}-{min(x+mod-1, len(df))}"
    k = k + 1         # moving to next row k=k+1
    x = x + mod


chunk_size = mod
chunked_list = []

for i in range(0, len(octant), chunk_size):
    chunked_list.append(octant[i:i+chunk_size])

for m in range(len(chunked_list)):
    for n in range(8):
        df.iloc[m+2, n+13] = chunked_list[m].count(int(row_top[2+n]))

#----------Tut-2

#list containing octants
octants = [1, -1, 2, -2, 3, -3, 4, -4]


#function to make skeleton
def make_table(s_row, s_col, heading, range_):

    df.iloc[s_row, s_col] = heading
    df.iloc[s_row+3, s_col-1] = "From"
    df.iloc[s_row+1, s_col+1] = "To"
    df.iloc[s_row+2, s_col] = "Count"
    df.iloc[s_row+1, s_col] = range_

    for i in range(len(octants)):
        # column and row titles of table (octant values)
        df.iloc[s_row+2, s_col+1+i] = octants[i]
        df.iloc[s_row+3+i, s_col] = octants[i]

    # initially all values in the table are zero
    for i in range(8):
        for j in range(8):
            df.iloc[s_row+3+i, s_col+1+j]=0

df.to_excel("output_octant_transition_identify.xlsx",index=False)