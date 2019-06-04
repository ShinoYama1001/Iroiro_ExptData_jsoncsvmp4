#-*- coding: utf-8 -*-

import os
import json

#顔が映ってるフレーム
with open("Data/A/Json/A_asb/A_asb_1.json", "r", encoding="utf-8_sig") as j:
    js = (json.load(j))

    if len(js["faces"]) == 1:
        print(js["faces"][0]["attributes"]["emotion"]["neutral"])

#顔が映っていないフレーム
with open("Data/A/Json/A_bkr/A_bkr_9534.json", "r", encoding="utf-8_sig") as j:
    js = (json.load(j))

    if len(js["faces"]) == 1:
        print(js["faces"])


