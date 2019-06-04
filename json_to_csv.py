#-*- coding: utf-8 -*-

import os
import json

class json_to_csv:

    def __init__(self):
        self.totalframe_count = 1
        self.frame_count = 1
        self.persons = ['A','B','C','D','E','F','G','H','I']
        self.comics = {0:"start", 1:"asb", 2:"kgy", 3:"bkr", 4:"jk", 5:"sig", 6:"uen"}


    def write_emotion(self, log, log2, emotion, frame):
        log2.write(log)
        log2.write(','+str(frame))
        log2.write(','+str(emotion["neutral"]))
        log2.write(','+str(emotion["sadness"]))
        log2.write(','+str(emotion["disgust"]))
        log2.write(','+str(emotion["anger"]))
        log2.write(','+str(emotion["surprise"]))
        log2.write(','+str(emotion["fear"]))
        log2.write(','+str(emotion["happiness"]))
        log2.write("\n")

    def main(self):
        for person in self.persons: #被験者ごとに
            #log csvを開いておく
            log = open("Data/"+person+'/'+person+"_log.csv", "r")
            #書き込み用csvを作っておく
            log2 = open("Data/"+person+'/'+person+"_log_emotion.csv", "w")
            #jsonから漫画読んだ順を取得しておく
            with open("Data/"+person+'/'+person+".json", "r", encoding="utf-8_sig") as j:
                js = json.load(j)
                order = [0] + js["order"]
            #一行目かいとこう
            log2.write("total frames,seconds,images,frames,neutral,sadness,disgust,anger,surprise,fear,happiness\n")

            for comic in order: #漫画を読んだ順で
                self.frame_count = 1
                #例えば Data/A/Json/A_asb/A_asb_?.json があるかを判断
                while os.path.isfile("Data/"+person+"/Json/"+person+"_"+self.comics[comic]+"/"+person+"_"+self.comics[comic]+"_"+str(self.frame_count)+".json"):
                    #ここから各jsonに対する処理
                    with open("Data/"+person+"/Json/"+person+"_"+self.comics[comic]+"/"+person+"_"+self.comics[comic]+"_"+str(self.frame_count)+".json") as j:
                        js = json.load(j)
                        if len(js["faces"]) == 1:
                            #関数使おう
                            self.write_emotion(log.readline().strip(), log2, js["faces"][0]["attributes"]["emotion"], self.frame_count)
                        else:
                            log2.write(log.readline().strip())
                            log2.write(','+str(self.frame_count))
                            log2.write(',0,0,0,0,0,0,0')
                            log2.write("\n")

                    self.frame_count += 1
                    #ここまでかくjsonに対する処理
                print("end "+person+self.comics[comic])
            #ファイル閉じる
            log.close()
            log2.close()
        print("end all")


if __name__ == "__main__":
    JTC = json_to_csv()
    JTC.main()