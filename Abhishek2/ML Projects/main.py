from findframe import *
import cv2
import numpy as np
import sys
from imutils import paths
import argparse
import os
import glob
import shutil

parser = argparse.ArgumentParser(description='Call main script')
parser.add_argument('--video', type=str, required=True) 
parser.add_argument('--src', type=str, required=True, default = 1)
args = parser.parse_args()                


if __name__ == "__main__":

    
    
    
    if(args.src == "1"):
        
        # dataload
        videopath = args.video
        cap = cv2.VideoCapture(str(videopath))
        frame_rate = cap.get(5)
        print("Frame rate = %s" % frame_rate)
        curr_frame = None
        prev_frame = None
        outFolder = None
        frame_diffs = []
        frames = []
        success, frame = cap.read()
        i = 0
        FRAME = Frame(0, 0)
        
        while (success):
            luv = cv2.cvtColor(frame, cv2.COLOR_BGR2LUV)
            curr_frame = luv
            
            """
            write the frames to a folder
            
            """
            outFolder = "frames"
            cv2.imwrite(os.path.join(outFolder , "frame"+str(format(i, '05'))+".jpg"), frame)
            #print("Image written to:"+os.path.join(outFolder , "frame"+str(f"{i:05}")+".png"))
            
            
            
            """
            
            calculate the difference between frames 
            
            """

            if curr_frame is not None and prev_frame is not None:
                diff = cv2.absdiff(curr_frame, prev_frame)
                diff_sum = np.sum(diff)
                diff_sum_mean = diff_sum / (diff.shape[0] * diff.shape[1])
                frame_diffs.append(diff_sum_mean)
                frame = Frame(i, diff_sum_mean)
                frames.append(frame)
            elif curr_frame is not None and prev_frame is None:
                diff_sum_mean = 0
                frame_diffs.append(diff_sum_mean)
                frame = Frame(i, diff_sum_mean)
                frames.append(frame)

            prev_frame = curr_frame
            i = i + 1
            success, frame = cap.read()
        cap.release()


        #detect the possible frame
        frame_return, start_id_spot_old, end_id_spot_old = FRAME.find_possible_frame(frames)

        #optimize the possible frame
        new_frame, start_id_spot, end_id_spot = FRAME.optimize_frame(frame_return, frames)

        #store the result
        start = np.array(start_id_spot)[np.newaxis, :]
        end = np.array(end_id_spot)[np.newaxis, :]
        #for ele in start: ele = ele/frame_rate
        #for ele in end: ele = ele/frame_rate
        spot = np.concatenate((start.T, end.T), axis=1)
        print("array type:", type(start))
        print("start id frame numbers:",start)
        sArr = start[0]
        eArr = end[0]
        i=0
        print("sArray length:",len(sArr))
        print("0th Element:",sArr[i])
        print("1st Element:",sArr[i+1])
        
        #deleting existing shot folders from prev run of the algorithm
        path = "C:/Users/Abhishek/neural-image-assessment-master"
        pathList = glob.glob("%s\shot_folder*" %path)

        print ("Before printing pathList list")
        print (pathList) 

        for shotFolder in pathList:
            shutil.rmtree(shotFolder)
            print("removed: ", shotFolder)

        pathList = glob.glob("%s\shot_folder*" %path)
        print ("Ater printing pathList list")
        print (pathList)

        
        #Read images from the frames folder and divide it shot wise
        
        index = 0

        
        shotFoldersList = ""
        while index<len(sArr):
            
            shotFolder = "shot_folder"+str(index+1)
            shotFoldersList = shotFoldersList+" "+shotFolder
            
            curDir = os.getcwd()
            os.chdir("C:/Users/Abhishek/neural-image-assessment-master")
            
            if os.path.exists(shotFolder):
                shutil.rmtree(shotFolder)
            os.makedirs(shotFolder)
    #         os.mkdir(shotFolder)
            os.chdir(curDir)
            
            startFrame = sArr[index]
            endFrame  = eArr[index]
            
            
            i= startFrame
            writePath = "C:/Users/Abhishek/neural-image-assessment-master"
            while i<endFrame:
                shotFolderPath = writePath+"/"+shotFolder
                image = cv2.imread(os.path.join(outFolder , "frame"+str(format(i, '05'))+".jpg"))
                cv2.imwrite(shotFolderPath+"/"+"frame"+str(format(i, '05'))+".jpg", image)
                i=i+1
                
            index = index+1
        
            
        np.savetxt('./result.txt', spot, fmt='%d', delimiter='\t')
        
        print("Shot folder list:"+shotFoldersList+" type:",type(shotFoldersList))
        
        os.chdir("C:/Users/Abhishek/neural-image-assessment-master")
        os.system("python evaluate_mobilenet.py -dirs "+ shotFoldersList)
    #     os.system('cmd /k git clone https://github.com/shreyas-bk/U-2-Net')
    #     os.system("python evaluate_mobilenet.py -dirs "+ shotFoldersList)
        
        print("Curr WD, in main before cropper call is: ",os.getcwd())
        os.system("python u_2_netp_cropper_colab.py")
       
        

    if(args.src == "2"):
        # print("Back in Main")
        # print("Curr WD, in main, before pp call is: ",os.getcwd())
        # os.system("python processPixels.py")

        os.chdir("C:/Users/Abhishek/neural-image-assessment-master")
        # os.system("python processPixels.py")
        os.system("python duplicate_remover.py")
        # os.chdir("C:/Users/Abhishek/ML Projects")
        os.system("python processPixels2.py")