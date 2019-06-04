#-*- coding: utf-8 -*-

import numpy as np
import cv2
import sys
import os
from facepp import API, File
import json

API_KEY = "E-ZR25izCNPUG_JGnXZNQ34GO7S-shXP"
API_SECRET = "c4gs2O4HBkXj_GGa7HtpdBfN9-6CB6-P"
api_server_international = 'https://api-us.faceplusplus.com/facepp/v3/'

class use_facepp:

    def __init__(self, path):
        self.path = path
        self.api = API(API_KEY, API_SECRET, srv=api_server_international)
        self.frame_count = 0
        self.per_frame = 1
        self.folder_list = []
        self.video_list = {}

        self.open_folder()

        with open("log.txt", "w") as log:
            print "reset log"

    def open_folder(self):
        self.folder_list = os.listdir(self.path)

        for folder in self.folder_list:
            #各フォルダーにJsonフォルダが無ければ作る
            try:
                os.mkdir(self.path+'/'+folder+"/Json")
            except OSError:
                pass
            #Videoフォルダ内のファイル一全てをvideo_listに追加
            self.video_list[folder] = os.listdir(self.path+'/'+folder+"/Video")

    def main(self):
        for folder in self.folder_list:
            for video in self.video_list[folder]:
                #カウントリセット
                self.frame_count = 0
                #動画名のフォルダを作成
                try:
                    os.mkdir(self.path+'/'+folder+"/Json/"+video.split('.')[0])
                except OSError:
                    pass
                #Opencv用意
                cap = cv2.VideoCapture(self.path+'/'+folder+"/Video/"+video)
                while True:
                    ret, frame = cap.read()
                    if ret == False:
                        break
                    self.frame_count += 1

                    if (self.frame_count-1) % self.per_frame == 0:
                        cv2.imwrite("current.jpg", frame)
                        #ファイルがあったらパス
                        if os.path.isfile(self.path+'/'+folder+"/Json/"+video.split('.')[0]+'/'+video.split('.')[0]+'_'+str(self.frame_count)+".json") is True:
                            continue
                        res = self.api.detect(image_file=File("current.jpg"))
                        with open(self.path+'/'+folder+"/Json/"+video.split('.')[0]+'/'+video.split('.')[0]+'_'+str(self.frame_count)+".json", "w") as file:
                            json.dump(res, file, indent=4)

                print "Finish: "+self.path+'/'+folder+'/Video/'+video
                with open("log.txt", "a") as log:
                    log.write("Finish: "+self.path+'/'+folder+'/Video/'+video+'\n')

            print "Finish: "+self.path+'/'+folder
            with open("log.txt", "a") as log:
                log.write("Finish: "+self.path+'/'+folder+'\n')
        print "Finish All"
        with open("log.txt", "a") as log:
            log.write("Finish All")
        os.remove("current.jpg")








def main(path):
    print "Select "+path
    UF = use_facepp(path)
    UF.main()


if __name__ == "__main__":
    #頂点フォルダを引数で取得
    args = sys.argv
    main(args[1])