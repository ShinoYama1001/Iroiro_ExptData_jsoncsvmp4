#-*- coding: utf-8 -*-

import os
import json
import cv2
import numpy as np

class csv_to_mp4:

    def __init__(self):
        self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')

        self.totalframe_number = 0
        self.time = 0
        self.image_name = ""
        self.frame_number = 0
        self.emotions = [0,0,0,0,0,0,0]
        self.emo_name = ["neutral", "sadness", "disgust", "anger", "surprise", "fear", "happiness"]
        self.persons = ['A','B','C','D','E','F','G','H','I']
        self.comics = {0:"start", 1:"asb", 2:"kgy", 3:"bkr", 4:"jk", 5:"sig", 6:"uen"}

        self.x_max = 1280
        self.y_max = 720


    def write_emotion(self, frame):
        for i in range(7):
            #文字表示
            cv2.rectangle(frame, (self.x_max-200, 0 + 17*i), (self.x_max-100, 17*(i+1)), (0,0,0), -1)
            cv2.putText(frame, self.emo_name[i], (self.x_max-195, 10 + 17*i), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (255,255,255), 1)
            #バー表示
            cv2.rectangle(frame, (self.x_max-100, 0 + 17*i), (self.x_max, 17*(i+1)), (0,0,0), -1)
            cv2.rectangle(frame, (self.x_max-100, 0 + 17*i), (self.x_max - (100 - int(self.emotions[i])), 17*(i+1)), (100,100,255), -1)


    def main(self):
        for person in self.persons:
            #log_emotion.csv開いとく
            csv = open("Data/"+person+'/'+person+"_log_emotion.csv", "r")
            line = csv.readline()#最初の一行要らん
            #jsonから漫画読んだ順を取得しておく
            with open("Data/"+person+'/'+person+".json", "r") as j:
                js = json.load(j)
                order = [0] + js["order"]

            for comic in order: #漫画を読んだ順で
                #漫画ごとに動画開く
                cap = cv2.VideoCapture("Data/"+person+'/Video/'+person+"_"+self.comics[comic]+".mp4")
                out = cv2.VideoWriter("Data/"+person+'/Video/'+person+"_"+self.comics[comic]+"2.mp4", self.fourcc, 30, (1280,720), True)

                while(cap.isOpened()):
                    ret, frame = cap.read()     #フレーム読み込んで
                    if ret:
                        line = csv.readline().split(',') #一行読み込んで
                        #各種変数に入力
                        self.totalframe_number = int(line.pop(0))
                        self.time = int(line.pop(0))
                        self.image_name = line.pop(0)
                        self.frame_number = int(line.pop(0))
                        self.emotions = [float(n) for n in line[0:7]]; del line[0:7]

                        #todo 画像への書き込み
                        self.write_emotion(frame) #表情分類の書き込み

                        #out.write(frame)
                        cv2.imshow("",frame)
                        cv2.waitKey(0)
                    else:
                        break

                print "end "+ person + ' ' + self.comics[comic]
                cap.release()
                out.release()






            #ファイル閉じる
            csv.close()
        print "end all"



if __name__ == "__main__":
    CTM = csv_to_mp4()
    CTM.main()