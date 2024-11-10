import pandas as pd

read_file = pd.read_csv("csv.txt")
read_file.to_csv("dataset_csv.csv", index=None)
