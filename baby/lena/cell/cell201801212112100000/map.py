import matplotlib.pyplot as plt
import numpy as np

image=plt.imread("002.jpg")
img=image[::,::]
imgr=(img/50)*50
imgm=imgr[::1,::1]
'''
imgmt=np.dsplit(imgm,3)
imgmc=zip(imgmt[0].flatten(), imgmt[1].flatten(), imgmt[2].flatten())
lisc=[]
for item in imgmc:
    if item not in lisc:
        lisc.append(item)
print("number of colors: {}".format(len(lisc)))
print lisc
'''
plt.imshow(imgm)
plt.show()
