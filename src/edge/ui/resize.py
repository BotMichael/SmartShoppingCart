from os import listdir
from os.path import isfile, join
from PIL import Image

##mypath = "train2014/"
##files = [f for f  in listdir(mypath) if isfile(join(mypath,f)) and f[-4:]==".jpg"]
##outpath = "training_val2014/"
f = "dis.jpg"
##for i in range(82783):
image = Image.open(f)
new_image = image.resize((400,400))
new_image.save(f"dis1.jpg")

print(1)
