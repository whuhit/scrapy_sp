import json
import pandas as pd
import glob


res = 0
path = "data/4-crawler-ip-block-2.txt"
for line in open(path):
    if "[" in line:
        res += int(line.split()[1])
print(res)