from turtle import clear
from PIL import Image
import os
import glob

done = []
pasted = []

# print('making results directory in main content')

# dir = 'content/U-2-Net/results'
# if os.path.exists(dir):
#     shutil.rmtree(dir)
# os.makedirs(dir)

# src_dir = "C:/Users/Abhishek/neural-image-assessment-master/content/U-2-Net/results"
# dst_dir = "C:/Users/Abhishek/ML Projects/content/U-2-Net/results"
        
# for jpgfile in iglob(os.path.join(src_dir, "*.png")):
#     print("Copying",jpgfile)
#     shutil.copy(jpgfile, dst_dir)
#     # !mkdir images


# dir = 'content/U-2-Net/cropped_results'
# if os.path.exists(dir):
#     shutil.rmtree(dir)
# os.makedirs(dir)

# src_dir = "C:/Users/Abhishek/neural-image-assessment-master/content/U-2-Net/cropped_results"
# dst_dir = "C:/Users/Abhishek/ML Projects/content/U-2-Net/cropped_results"
        
# for jpgfile in iglob(os.path.join(src_dir, "*.jpg")):
#     print("Copying",jpgfile)
#     shutil.copy(jpgfile, dst_dir)

# print('making selected images directory')
# dir = 'content/U-2-Net/selected_images'
# if os.path.exists(dir):
#     shutil.rmtree(dir)
# os.makedirs(dir)

# src_dir = "C:/Users/Abhishek/neural-image-assessment-master/selected_images"
# dst_dir = "C:/Users/Abhishek/ML Projects/content/U-2-Net/selected_images"
        
# for jpgfile in iglob(os.path.join(src_dir, "*.jpg")):
#     print("Copying",jpgfile)
#     shutil.copy(jpgfile, dst_dir)



def convertImage(fgImageName,trFG):
        img = Image.open(fgImageName)
        img = img.convert("RGBA")

        datas = img.getdata()

        newData = []

        for item in datas:
            if item[0] == 0 and item[1] == 0 and item[2] == 0:
                newData.append((255, 255, 255, 0))
            else:
                newData.append(item)

        img.putdata(newData)
        img.save(trFG)


def pasteImage(bgName,fgName, scaleDownRatio, x, y):
        
#         im1 = Image.open("frame00025.png")
#         im2 = Image.open('NewPNG.png')

#         back_im = im1.copy()
#         back_im.paste(im2)
#         back_im.save('./Embedded.png', quality=95)

            
        

        background = Image.open(bgName)
        foreground = Image.open(fgName)

        height = foreground.height*scaleDownRatio
        width = foreground.width*scaleDownRatio

        print("Foreground name:",fgName)
        print("Scale down ratio:",scaleDownRatio)
        print("Foreground height:",height)
        print("Foreground width:",width)
        
        foreground.thumbnail(size=(height,width))
        foreground.save('NewPNG.png', optimize=True, quality=65)

        foreground = Image.open("NewPNG.png")
        
        background.paste(foreground, (x, y), foreground)
        background.save('./Embedded.png', quality=95)
        pasted.append('Embedded.png')
        background.show()
        
        print("Successful")
        

def rotate(image,trSend):
    
    
   
    # Open an already existing image
    imageObject = Image.open(image)
    

    # Do a flip of left and right or top an bottom
    flippedImage = imageObject.transpose(trSend)

    # Show the original image
    #imageObject.show()
    

    # Show the horizontal flipped image
    flippedImage.show()
    flippedImage.save("maskCopy.png")


def predictEmbedding(maskStr,bgImgStr,fgImgStr,pOEmbedding):
     
        maskImg = Image.open(maskStr)
        maskCopy = maskImg.copy()
        maskCopy.save("maskCopy.png")

        maskImg = Image.open("maskCopy.png")
        maskImg = maskImg.convert("RGBA")

        fgImg = Image.open(fgImgStr)
        bgImg = Image.open(bgImgStr)

        if(pOEmbedding ==1):
            pass
        elif(pOEmbedding==2):
            rotate("maskCopy.png",Image.FLIP_LEFT_RIGHT)
        elif(pOEmbedding==3):
            rotate("maskCopy.png",Image.FLIP_LEFT_RIGHT)
            rotate("maskCopy.png",Image.FLIP_TOP_BOTTOM)
        elif(pOEmbedding==4):
            rotate("maskCopy.png",Image.FLIP_TOP_BOTTOM)

        maskImg = Image.open("maskCopy.png")
        
        bgHt = bgImg.height
        bgWth = bgImg.width

        bgSize = bgHt*bgWth

        fgHt = fgImg.height
        fgWth = fgImg.width

        # fgHt = 1
        # fgWth = 1

        varFgHt = fgHt
        varFgWth = fgWth

        print("Original req Height:", varFgHt)
        print("Original req Width:", varFgWth)

        bgMaskData = maskImg.getdata()
        
        imSize = fgHt*fgWth

        pixelCount = 0
        rowCount = 0
        colCount = 0
        embedCount = 0

        while(embedCount<imSize and pixelCount<bgSize):

            # print("Pixel number:", pixelCount)
            item = bgMaskData[pixelCount]
            indices = range(len(item))

            newItem = []

            for i in indices:
                if item[i]>=100:
                    newItem.append(255)
                else:
                    newItem.append(0)

            
            if(pixelCount<100):
                print(item)
            pixelCount+=1
            colCount+=1

            if(rowCount>=varFgHt):
                break


            if (colCount<varFgWth):
                if(newItem[0]!=0 or newItem[1]!=0 or newItem[2]!=0):
                # if(newItem[0]==255 and newItem[1]==255 and newItem[2]==255):
                    if  (colCount<0.1*fgWth):

                        print("Before breaking Column number",colCount)
                        break
                    else:
                        varFgWth = colCount-1
                        rat = varFgWth/fgWth
                        varFgHt = rat*fgHt

                        print("Row number:", rowCount)
                        print("Column number",colCount)
                        print("Obstruction encountered on row:", rowCount)
                        print("New req Height:", varFgHt)
                        print("New req Width:", varFgWth)

                        colCount = 0
                        rowCount+=1
                        print("Row count:", rowCount)
                        pixelCount=(bgWth*rowCount)
                        embedCount = varFgWth*rowCount

                else:
                    continue
            elif (colCount== varFgWth):
                colCount = 0
                rowCount+=1
                pixelCount=(bgWth*rowCount)
                embedCount = varFgWth*rowCount


        print("Row count:",rowCount)
        if(rowCount>=varFgHt):
            scaleDownRatio = varFgWth/fgWth
            print("Embedding possible")
            print("varfgHt:", varFgHt)
            print("varfgWth:", varFgWth)

            
            print("Ratio is:",scaleDownRatio)
            print ("Resize to:",scaleDownRatio )

            
            if(pOEmbedding==1 and (pOEmbedding not in done)):
                x,y=50,50
                done.append(1)
                
            elif(pOEmbedding  ==2 and (pOEmbedding not in done)):
                x,y=bgWth-varFgWth-20,50
                done.append(2)

            elif(pOEmbedding  ==3 and (pOEmbedding not in done)):
                x,y=bgWth-varFgWth,bgHt-varFgHt
                done.append(3)

            elif(pOEmbedding  ==4 and (pOEmbedding not in done)):
                x,y=50,bgHt-varFgHt
                done.append(4)
            
            if(len(done)==4): done.clear()

            #bgName = "frame00026 - Copy.png"
            # fgImgStr = r"content/U-2-Net/cropped_results/frame00000_cropped_no-bg.jpg"
            trFG = "./tranFG.png"
            
            convertImage(fgImgStr,trFG)
            pasteImage(bgImgStr,trFG, scaleDownRatio, int(x), int(y))
            return True
        
        print("Embedding not possible")
        return False


                
def callPredictEmbedding(maskStr, bgImg,fgImg):
         #to see if foreground fits in any one of the corners of the bg

         #fgImg =  r"content/U-2-Net/cropped_results/frame00000_cropped_no-bg.jpg"
         #for top left corner
         tl= False
         tr= False
         bl = False
         br = False
         if(1 not in done):
            tl = predictEmbedding(maskStr,bgImg,fgImg,1)
            if(tl):
             print("TL possible")
         elif(2 not in done):
            tr = predictEmbedding(maskStr,bgImg,fgImg,2)
            if(tr):
             print("TR possible")
         elif(3 not in done):
            br = predictEmbedding(maskStr,bgImg,fgImg,3)
            if(br):
             print("BR possible")
         elif(4 not in done):
            bl = predictEmbedding(maskStr,bgImg,fgImg,4)
            if(bl):
             print("BL possible")

         
        # #for top right corner
        #  else:
        #     t2 = predictEmbedding(imStr,bgImg,fgImg,2)
         
        #  tr = predictEmbedding(imStr,bgImg,fgImg,2)
        #  if(not(tl) and tr):
        #      print("TR possible")
        # #for bottom right corner
        
        #  br = predictEmbedding(imStr,bgImg,fgImg,3)
        #  if(not(tl) and not(tr) and br):
        #      print("BR possible")

        # #for bottom left corner
        
        #  bl = predictEmbedding(imStr,bgImg,fgImg,4)
        #  if(bl):
        #      print("BL possible")

        # #making image look same as beginning
        #  rotate(imStr,Image.FLIP_TOP_BOTTOM)

         if(tl or tr or bl or br):
             print("Possible to embed in call Embedding")

# image_list = []
# for filename in glob.iglob('C:/Users/Abhishek/neural-image-assessment-master/selected_images'):
#     # im=Image.open(filename)
#     image_list.append(filename)

# ilLen = len(image_list)

# image_list.sort()

    
# inc = (ilLen-1)//4

# if(inc==0):
#     inc = 1

# bg_index = 0    
# first_index = ilLen-1
# second_index = ilLen-1-inc
# third_index = ilLen-1-(inc*2)
# fourth_index = ilLen-1-(inc*3)
         
# print("First index:", first_index)
# print("Second index:", second_index)
# print("First index:", third_index)
# print("First index:", fourth_index)

# print("BG image:",image_list[bg_index])
# print("1 FG image:",image_list[first_index][-9:-4])
# print("2 FG image:",image_list[second_index][-9:-4])
# print("3 FG image:",image_list[third_index][-9:-4])
# print("4 FG image:",image_list[fourth_index][-9:-4])

# print("Current directory", os.getcwd())
# pasted.append(r"content/U-2-Net/selected_images/00001.jpg")
# callPredictEmbedding("content/U-2-Net/results/00001-Copy.png", r"content/U-2-Net/cropped_results/00002_cropped_no-bg.jpg",pasted[-1])
# old = pasted[-1]
# pasted.clear()
# pasted.append(old)
# callPredictEmbedding("content/U-2-Net/results/00001-Copy.png", r"content/U-2-Net/cropped_results/00003_cropped_no-bg.jpg",pasted[-1] )
# old = pasted[-1]
# pasted.clear()
# pasted.append(old)
# callPredictEmbedding("content/U-2-Net/results/00001-Copy.png", r"content/U-2-Net/cropped_results/00004_cropped_no-bg.jpg",pasted[-1])
# old = pasted[-1]
# pasted.clear()
# # pasted.append(old)
# # callPredictEmbedding("content/U-2-Net/results/00001.png", r"content/U-2-Net/cropped_results/00005_cropped_no-bg.jpg",pasted[-1])
# # old = pasted[-1]
# # pasted.clear()
# pasted.append(old)


image_list = []

directory = 'C:/Users/Abhishek/neural-image-assessment-master/selected_images'
 


for filename in os.listdir(directory):
    image_list.append(filename)

print("Image List:", image_list)
ilLen = len(image_list)

image_list.sort()

    
inc = (ilLen-1)//4

if(inc==0):
    inc = 1

bg_index = 0    
first_index = ilLen-1
second_index = ilLen-1-inc
third_index = ilLen-1-(inc*2)
fourth_index = ilLen-1-(inc*3)
         
print("First index:", first_index)
print("Second index:", second_index)
print("Third index:", third_index)
print("Fourth index:", fourth_index)

print("BG image:",image_list[bg_index])
print("1 FG image:",image_list[first_index][-9:-4])
print("2 FG image:",image_list[second_index][-9:-4])
# print("3 FG image:",image_list[third_index][-9:-4])
# print("4 FG image:",image_list[fourth_index][-9:-4])


print("Current directory", os.getcwd())

if(ilLen-1>=1):
    pasted.append(r"selected_images/00001.jpg")
    callPredictEmbedding("content/U-2-Net/results/00001.png",pasted[-1], r"content/U-2-Net/cropped_results/"+image_list[first_index][-9:-4]+r"_cropped_no-bg.jpg")
    old = pasted[-1]
    pasted.clear()
if(ilLen-1>=2):
    pasted.append(old)
    callPredictEmbedding("content/U-2-Net/results/00001.png",pasted[-1], r"content/U-2-Net/cropped_results/"+image_list[second_index][-9:-4]+r"_cropped_no-bg.jpg")
    old = pasted[-1]
    pasted.clear()
if(ilLen-1>=3):
    pasted.append(old)
    callPredictEmbedding("content/U-2-Net/results/00001.png",pasted[-1], r"content/U-2-Net/cropped_results/"+image_list[third_index][-9:-4]+r"_cropped_no-bg.jpg")
    old = pasted[-1]
    pasted.clear()
if(ilLen-1>=4):
    pasted.append(old)
    callPredictEmbedding("content/U-2-Net/results/00001.png",pasted[-1], r"content/U-2-Net/cropped_results/"+image_list[fourth_index][-9:-4]+r"_cropped_no-bg.jpg")
    old = pasted[-1]
    pasted.clear()
pasted.append(old)

# print("Current directory", os.getcwd())

# imageObject = Image.open("content/U-2-Net/results/00001.png")
# flippedImage = imageObject.transpose(Image.FLIP_LEFT_RIGHT)
# flippedImage.save("content/U-2-Net/results/00001-Copy.png")


# pasted.append(r"selected_images/00001.jpg")
# callPredictEmbedding("content/U-2-Net/results/00001.png",pasted[-1], r"content/U-2-Net/cropped_results/00002_cropped_no-bg.jpg")
# old = pasted[-1]
# pasted.clear()

# pasted.append(old)
# callPredictEmbedding("content/U-2-Net/results/00001.png",pasted[-1], r"content/U-2-Net/cropped_results/00003_cropped_no-bg.jpg")
# old = pasted[-1]
# pasted.clear()

# pasted.append(old)
# callPredictEmbedding("content/U-2-Net/results/00001.png",pasted[-1], r"content/U-2-Net/cropped_results/00004_cropped_no-bg.jpg")
# old = pasted[-1]
# pasted.clear()

# pasted.append(old)
# callPredictEmbedding("content/U-2-Net/results/00001-Copy.png", r"content/U-2-Net/cropped_results/00005_cropped_no-bg.jpg",pasted[-1])
# old = pasted[-1]
# pasted.clear()

# pasted.append(old)
# callPredictEmbedding("content/U-2-Net/results/00001-Copy.png", r"content/U-2-Net/cropped_results/_cropped_no-bg.jpg",pasted[-1])
# old = pasted[-1]
# pasted.clear()
# pasted.append(old)

# print("Current directory", os.getcwd())
# pasted.append(r"content/U-2-Net/selected_images/00001.jpg")
# callPredictEmbedding("content/U-2-Net/results/00001-Copy.png", r"content/U-2-Net/cropped_results/00002_cropped_no-bg.jpg",pasted[-1])
# old = pasted[-1]
# pasted.clear()
# pasted.append(old)
# callPredictEmbedding("content/U-2-Net/results/00001-Copy.png", r"content/U-2-Net/cropped_results/00003_cropped_no-bg.jpg",pasted[-1] )
# old = pasted[-1]
# pasted.clear()
# pasted.append(old)
# callPredictEmbedding("content/U-2-Net/results/00001-Copy.png", r"content/U-2-Net/cropped_results/00004_cropped_no-bg.jpg",pasted[-1])
# old = pasted[-1]
# pasted.clear()
# pasted.append(old)
# # callPredictEmbedding("content/U-2-Net/results/00001.png", r"content/U-2-Net/cropped_results/00005_cropped_no-bg.jpg",pasted[-1])
# # old = pasted[-1]
# # pasted.clear()
# pasted.append(old)


# print("Current directory", os.getcwd())
# pasted.append(r"content/U-2-Net/results/black&white.png")
# callPredictEmbedding("content/U-2-Net/results/black&white.png", r"content/U-2-Net/cropped_results/00002_cropped_no-bg.jpg",pasted[-1])
# old = pasted[-1]
# pasted.clear()
# pasted.append(old)
# callPredictEmbedding("content/U-2-Net/results/black&white.png", r"content/U-2-Net/cropped_results/00003_cropped_no-bg.jpg",pasted[-1] )
# old = pasted[-1]
# pasted.clear()
# pasted.append(old)
# callPredictEmbedding("content/U-2-Net/results/black&white.png", r"content/U-2-Net/cropped_results/00004_cropped_no-bg.jpg",pasted[-1])
# old = pasted[-1]
# pasted.clear()
# # pasted.append(old)
# # callPredictEmbedding("content/U-2-Net/results/00001.png", r"content/U-2-Net/cropped_results/00005_cropped_no-bg.jpg",pasted[-1])
# # old = pasted[-1]
# # pasted.clear()
# pasted.append(old)



            
                
                    
        

            
            
#         img.putdata(newData)
#         img.save("./NewFGOfBGPNG.png")