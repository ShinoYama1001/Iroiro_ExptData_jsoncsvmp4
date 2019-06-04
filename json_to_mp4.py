#-*- coding: utf-8 -*-

import os
import json
import cv2
import numpy as np
import math

import calc_modules

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

    #試し書き用関数
    def write_something(self, frame, landmarks):
        #口の外側面積
        mouth_out = []
        mouth_out.append(landmarks["mouth_left_corner"])
        mouth_out.append(landmarks["mouth_lower_lip_left_contour2"])
        mouth_out.append(landmarks["mouth_lower_lip_right_contour3"])
        mouth_out.append(landmarks["mouth_lower_lip_bottom"])
        mouth_out.append(landmarks["mouth_lower_lip_right_contour3"])
        mouth_out.append(landmarks["mouth_lower_lip_right_contour2"])
        mouth_out.append(landmarks["mouth_right_corner"])
        mouth_out.append(landmarks["mouth_upper_lip_right_contour2"])
        mouth_out.append(landmarks["mouth_upper_lip_right_contour1"])
        mouth_out.append(landmarks["mouth_upper_lip_top"])
        mouth_out.append(landmarks["mouth_upper_lip_left_contour1"])
        mouth_out.append(landmarks["mouth_upper_lip_left_contour2"])
        mouth_outarea = calc_modules.calc_area(mouth_out)
        mouth_outarea = mouth_outarea*10000 / calc_modules.calc_distance([landmarks["nose_contour_left1"], landmarks["nose_contour_right1"]])**2
        r = int((mouth_outarea / math.pi) ** 0.5)
        cv2.circle(frame, (self.x_max-100, 200), r, (255,0,0), -1)

        #目の面積平均
        eye_right = []
        eye_right.append(landmarks["right_eye_left_corner"])
        eye_right.append(landmarks["right_eye_lower_left_quarter"])
        eye_right.append(landmarks["right_eye_bottom"])
        eye_right.append(landmarks["right_eye_lower_right_quarter"])
        eye_right.append(landmarks["right_eye_right_corner"])
        eye_right.append(landmarks["right_eye_upper_right_quarter"])
        eye_right.append(landmarks["right_eye_top"])
        eye_right.append(landmarks["right_eye_upper_left_quarter"])
        eye_left = []
        eye_left.append(landmarks["left_eye_left_corner"])
        eye_left.append(landmarks["left_eye_lower_left_quarter"])
        eye_left.append(landmarks["left_eye_bottom"])
        eye_left.append(landmarks["left_eye_lower_right_quarter"])
        eye_left.append(landmarks["left_eye_right_corner"])
        eye_left.append(landmarks["left_eye_upper_right_quarter"])
        eye_left.append(landmarks["left_eye_top"])
        eye_left.append(landmarks["left_eye_upper_left_quarter"])
        eye_area = (calc_modules.calc_area(eye_right)+calc_modules.calc_area(eye_left))*0.5
        eye_area = eye_area*10000 / calc_modules.calc_distance([landmarks["nose_contour_left1"], landmarks["nose_contour_right1"]])**2
        r = int((eye_area / math.pi) ** 0.5)
        cv2.circle(frame, (self.x_max-100, 300), r, (0,255,0), -1)

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
                                self.mark_landmarks(frame, js["faces"][0]["landmark"]) #顔特徴点書き込み
                                self.write_something(frame, js["faces"][0]["landmark"]) #試しに口の面積書き込み

                        #表示するか保存するか選べ
                        #out.write(frame)
                        cv2.imshow("",frame)
                        cv2.waitKey(0)
                    else:
                        break

                print "end "+ person + ' ' + self.comics[comic]
                cap.release()
                out.release()

        print "end all"



if __name__ == "__main__":
    JTM = json_to_mp4()
    JTM.main()