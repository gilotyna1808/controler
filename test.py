import numpy as np
import pandas as pd


l = np.zeros(99)

temp = pd.DataFrame()

temp["A"] = l
temp["B"] = l

print(temp)

print(l)