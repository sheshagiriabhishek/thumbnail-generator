import numpy as np
import argparse
import os
import cv2
import shutil
from path import Path

from keras.models import Model
from keras.layers import Dense, Dropout
from keras.applications.mobilenet import MobileNet
from keras.applications.mobilenet import preprocess_input
from keras.preprocessing.image import load_img, img_to_array
import tensorflow as tf

from utils.score_utils import mean_score, std_score

parser = argparse.ArgumentParser(description='Evaluate NIMA(Inception ResNet v2)')
parser.add_argument('-dirs', type=str, default=None, nargs='+',
                    help='Pass a directory to evaluate the images in it')
print(parser.parse_args().dirs)

parser.add_argument('-img', type=str, default=[None], nargs='+',
                    help='Pass one or more image paths to evaluate them')

parser.add_argument('-resize', type=str, default='false',
                    help='Resize images to 224x224 before scoring')

parser.add_argument('-rank', type=str, default='true',
                    help='Whether to tank the images after they have been scored')

args = parser.parse_args()
resize_image = args.resize.lower() in ("true", "yes", "t", "1")
target_size = (224, 224) if resize_image else None
rank_images = args.rank.lower() in ("true", "yes", "t", "1")

dirList=args.dirs
# dirList=args.dirs.split(' ')
shotNum = 0

folderName = "highest_score_cand_images"
if os.path.exists(folderName):
    shutil.rmtree(folderName)
    os.makedirs(folderName)

for dir in dirList:
    
    shotNum+=1
    # give priority to directory
    if dir is not None:
        print("Loading images from directory : ", dir)
        imgs = Path(dir).files('*.png')
        imgs += Path(dir).files('*.jpg')
        imgs += Path(dir).files('*.jpeg')

    elif args.img[0] is not None:
        print("Loading images from path(s) : ", args.img)
        imgs = args.img

    else:
        raise RuntimeError('Either -dirs or -img arguments must be passed as argument')

    with tf.device('/CPU:0'):
        base_model = MobileNet((None, None, 3), alpha=1, include_top=False, pooling='avg', weights=None)
        x = Dropout(0.75)(base_model.output)
        x = Dense(10, activation='softmax')(x)

        model = Model(base_model.input, x)
        model.load_weights('weights/mobilenet_weights.h5')

        score_list = []

        for img_path in imgs:
            img = load_img(img_path, target_size=target_size)
            x = img_to_array(img)
            x = np.expand_dims(x, axis=0)

            x = preprocess_input(x)

            scores = model.predict(x, batch_size=1, verbose=0)[0]

            mean = mean_score(scores)
            std = std_score(scores)

            file_name = Path(img_path).name.lower()
            score_list.append((file_name, mean))

            print("Evaluating : ", img_path)
            print("NIMA Score : %0.3f +- (%0.3f)" % (mean, std))
            print()

        if rank_images:
            print("*" * 40, "Ranking Images", "*" * 40)
            score_list = sorted(score_list, key=lambda x: x[1], reverse=True)

            for i, (name, score) in enumerate(score_list):
                print("%d)" % (i + 1), "%s : Score = %0.5f" % (name, score))
                if(i==0):
                    
                    
                    
                    # if not os.path.exists(folderName):
                    #     os.makedirs(folderName)
                    
                    name = "shot_folder"+str(shotNum)+"/"+name
#                     img = load_img(name, target_size=target_size)
#                     x = img_to_array(img)
                    x = cv2.imread(name)
#                     cv2.imwrite(shotFolderPath+"/"+"frame"+str(f"{i:05}")+".jpg", image)
                    cv2.imwrite(os.path.join(folderName,str(f"{shotNum:05}")+".jpg"),x)
#                     os.chdir("C:/Users/Abhishek/collage_maker-master")


finalFolder = ""+folderName
os.chdir("C:/Users/Abhishek/neural-image-assessment-master")
os.system("python evaluate_mobilenet_hs.py -dirs "+ finalFolder)

                    