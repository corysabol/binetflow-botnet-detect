import os.path
import pandas as pd

# create a sample of the data we will be working with, using pandas.
basepath = os.path.dirname(__file__)
filepath = os.path.abspath(os.path.join(basepath,"..","CTU-13-Dataset","capture20110810.binetflow"))

print(pd.read_csv(filepath, nrows=100))
