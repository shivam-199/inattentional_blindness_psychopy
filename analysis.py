import pandas as pd

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', -1)

raw_data = pd.read_csv("data/IB_Response_main.csv")

# print(raw_data)

cleaned_data = raw_data.drop(["Name", "Email", "Phone", ], axis=1)

cleaned_data["Participant"] = [x[:3].upper() for x in raw_data["Name"]]
print(cleaned_data)
