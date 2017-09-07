import os.path
import pandas as pd

# create a sample of the data we will be working with, using pandas.
basepath = os.path.dirname(__file__)
filepath = os.path.abspath(os.path.join(basepath,"..","CTU-13-Dataset","capture20110810.binetflow"))
dataset_path = os.path.abspath(os.path.join(basepath,"..","CTU-13-Dataset"))

# generate a sample of the dataset
print(pd.read_csv(filepath, nrows=100))

# generate a summary of the dataset
# There are 13 files in the directory, for a total size of about 2.5GB
# dictionary to hold information about the dataset.
dataset_info = {}

directory = os.fsencode(dataset_path)
for f in os.listdir(directory):
    f_name = os.fsdecode(f)
    if f_name.endswith(".binetflow"):
        # in here we should us pandas to read the files and do some processing on them
        print(os.path.join(str(directory), f_name))


