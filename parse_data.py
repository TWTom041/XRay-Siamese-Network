import multiprocessing as mp

from tqdm import tqdm
import istarmap
import pandas as pd
import cv2

import logging
import argparse
import os
import sys

parser = argparse.ArgumentParser()
parser.add_argument("save_file")
args = parser.parse_args()
save_file = args.save_file

file_all_exists = os.path.exists("train_x.p") and os.path.exists("train_y.p") and os.path.exists("test_x.p") and os.path.exists("test_y.p")
file_part_exists = os.path.exists("train_x.p") or os.path.exists("train_y.p") or os.path.exists("test_x.p") or os.path.exists("test_y.p")

if save_file == "yes":
    if file_part_exists:
        print("WARNING: AFTER PARSING DATA, THE PROGRAM WILL OVERWRITE THE DATA")
    else:
        print("INFO: will write the data")

logger = mp.log_to_stderr()
logger.setLevel(mp.SUBDEBUG)

df = pd.read_csv("Data_Entry_2017.csv")
train_data = []
train_label = []
test_data = []
test_label = []

with open("train_val_list.txt") as f:
    train_num = f.read().split("\n")
    
with open("test_list.txt") as f:
    test_num = f.read().split("\n")
    
print("list read done")
    
def main_map(ser, dd):
    try:
        a = cv2.imread(f"images_{str(ser).zfill(3)}/images/{dd}", cv2.IMREAD_GRAYSCALE)
        a = cv2.resize(a, (224, 224))

        label = df.loc[df["Image Index"] == dd]["Finding Labels"].values[0].split("|")
        in_train_test = 0 if dd in train_num else 1 if dd in test_num else 2
    except Exception as e:
        print("there is some error", e)
    return a, label, in_train_test

_ser_dd = ((_ser, _dd) for _ser in range(1, 13) for _dd in os.listdir(f"images_{str(_ser).zfill(3)}/images"))
print("serial and images name loaded")

with mp.Pool(mp.cpu_count()) as pool:
    for (a, label, in_train_test) in tqdm(pool.istarmap(
        main_map, _ser_dd
    ), total=sum(1 for _ser in range(1, 13) for _ in os.listdir(f"images_{str(_ser).zfill(3)}/images")), miniters=1, file=sys.stdout):
        if in_train_test == 0:
            train_data.append(a)
            train_label.append(label)
        if in_train_test == 1:
            test_data.append(a)
            test_label.append(label)

if save_file == "yes" or not file_part_exists:
    print("saving file")
    import pickle
    with open('train_x.p', 'wb') as f:
        pickle.dump(train_data, f)
    with open('train_y.p', 'wb') as f:
        pickle.dump(train_label, f)
    with open('test_x.p', 'wb') as f:
        pickle.dump(test_data, f)
    with open('test_y.p', 'wb') as f:
        pickle.dump(test_label, f)
else:
    print("not saving the data")
print("done")
