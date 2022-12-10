import imagehash
import os
import shutil
import numpy as np
from PIL import Image
from glob import iglob

def alpharemover(image):
    if image.mode != 'RGBA':
        return image
    canvas = Image.new('RGBA', image.size, (255,255,255,255))
    canvas.paste(image, mask=image)
    return canvas.convert('RGB')

def with_ztransform_preprocess(hashfunc, hash_size=8):
    def function(path):
        image = alpharemover(Image.open(path))
        image = image.convert("L").resize((hash_size, hash_size), Image.ANTIALIAS)
        data = image.getdata()
        quantiles = np.arange(100)
        quantiles_values = np.percentile(data, quantiles)
        zdata = (np.interp(data, quantiles_values, quantiles) / 100 * 255).astype(np.uint8)
        image.putdata(zdata)
        return hashfunc(image)
    return function
  
dhash_z_transformed = with_ztransform_preprocess(imagehash.dhash, hash_size = 12)
src_dir = "C:/Users/Abhishek/neural-image-assessment-master/selected_images"
hash_keys=dict()

for jpgfile in iglob(os.path.join(src_dir, "*.jpg")):
        print("Copying",jpgfile)
        # dhash_z_transformed = with_ztransform_preprocess(imagehash.dhash, hash_size = 8)
        hash_keys[jpgfile] = str(dhash_z_transformed(jpgfile))[0]

for w in hash_keys:
    
    print(w," ",hash_keys[w])

sorted_dict = {}
sorted_keys = sorted(hash_keys, key  = hash_keys.get)
print("-"*20,end="")
print("After sorting",end ="")
print("-"*20)
for w in sorted_keys:
    sorted_dict[w] = hash_keys[w]
    print(w," ",hash_keys[w])

i=0
lol = []

lenSortedKeys = len(sorted_keys)

while i<lenSortedKeys:
    start_key = sorted_keys[i]
    start_value = hash_keys [start_key]
    l = list()
    while i<lenSortedKeys:
        if(hash_keys[sorted_keys[i]] == start_value):
            l.append(sorted_keys[i])
        else:
            break
        i+= 1
    
    lol.append(l)

print("List Of Lists")
print(lol)

for l in lol:
    l.sort()
    print(l)
    ll = len(l)
    i=1
    while i<=ll-1:
        if os. path. exists(l[i]):
            os. remove(l[i])
            print("Removed",l[i])

        i+=1
    
    

