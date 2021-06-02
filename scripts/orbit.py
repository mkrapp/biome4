import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys

fnm = "orbit.dat"
df = pd.read_csv(fnm,index_col=0,delim_whitespace=True,header=None)
columns = ["orbit%ecc", "orbit%pre", "orbit%perh", "orbit%xob"]
df.index.name = "time (in ka BP)"
df.columns = columns

df.plot(subplots=True)
print(df.index[0])
plt.xlim(df.index[0],0)
plt.show()
