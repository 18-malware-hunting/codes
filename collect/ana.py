import os
import pandas as pd
import json

data_dict = {'data': [], 'datetime': []}
exclude = set(['__pycache__'])
for root,dirs,filenames in os.walk(os.path.join(os.path.expanduser("~"), "%s" % "mytest".lower()),topdown=True):
    dirs[:] = [d for d in dirs if d not in exclude]
    print(filenames)
    print(root)
for filename in sorted(filenames):
    csv_data = pd.read_csv(root+'/'+filename,names=["addr","type","source"])
    csv_df = pd.DataFrame(csv_data)
    csv_df = csv_df["addr"]
    csv_df.drop_duplicates(inplace=True)
    print(csv_df.shape[0])
    ftime=filename[:-4]
    data_dict["data"].append(csv_df.shape[0])
    data_dict["datetime"].append(ftime)
with open(os.path.join(os.path.join(os.path.expanduser("~"), "%s" % "anadata".lower()),"data.json"),'w') as dump_f:
    json.dump(data_dict,dump_f)
