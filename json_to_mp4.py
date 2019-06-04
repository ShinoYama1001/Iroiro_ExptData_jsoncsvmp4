#-*- coding: utf-8 -*-

import os
import json
import cv2
import numpy as np

class json_to_mp4:

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

        self.framecount = 0

    #特徴点書き込み
    def mark_landmarks(self, frame, landmarks):
        for mark in landmarks:
            cv2.circle(frame, (int(landmarks[mark]['x']),int(landmarks[mark]['y'])), 1, (0,0,255), -1)

    def main(self):
        for person in self.persons:
            #jsonから漫画読んだ順を取得しておく
            with open("Data/"+person+'/'+person+".json", "r") as j:
                js = json.load(j)
                order = [0] + js["order"]

            for comic in order: #漫画を読んだ順で
                #漫画ごとに動画開く
                cap = cv2.VideoCapture("Data/"+person+'/Video/'+person+"_"+self.comics[comic]+"2.mp4")
                out = cv2.VideoWriter("Data/"+person+'/Video/'+person+"_"+self.comics[comic]+"_points.mp4", self.fourcc, 30, (1280,720), True)
                self.framecount = 0

                while(cap.isOpened()):
                    ret, frame = cap.read()     #フレーム読み込んで
                    if ret:
                        self.framecount += 1

                        #json開いて書き込み
                        with open("Data/"+person+"/Json/"+person+"_"+self.comics[comic]+"/"+person+"_"+self.comics[comic]+"_"+str(self.framecount)+".json") as j:
                            js = json.load(j)
                            if len(js["faces"]) == 1:
                                #関数使おう
                                self.mark_landmarks(frame, js["faces"][0]["landmark"])


                        out.write(frame)
                        #cv2.imshow("",frame)
                        #cv2.waitKey(0)
                    else:
                        break

                print "end "+ person + ' ' + self.comics[comic]
                cap.release()
                out.release()

        print "end all"



if __name__ == "__main__":
    JTM = json_to_mp4()
    JTM.main()