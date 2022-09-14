import pandas as pd


from platform import python_version
ver = python_version()

if ver == "3.8.10":
    print("Correct Version Installed")
else:
    print("Please install 3.8.10. Instruction are present in the GitHub Repo/Webmail. Url: https://pastebin.com/nvibxmjw")

mod=5000

df = pd.read_csv("octant_input.csv")

U_avg = df['U'].mean()     # Taking average of U
V_avg = df['V'].mean()    # Taking average of V
W_avg = df['W'].mean()   # Taking average of W

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


df.to_csv("octant_output.csv",index=False)