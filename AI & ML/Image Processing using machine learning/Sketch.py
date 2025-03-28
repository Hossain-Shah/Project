import imageio
import numpy as np
import scipy.ndimage
import matplotlib.pyplot as plt
#img="http://static.cricinfo.com/db/PICTURES/CMS/263600/263697.20.jpg"
img="F:/Photos/Friends & Family(Dhaka)/20151231_224407.jpg"
start_img = imageio.imread(img)



def grayscale(rgb):
    return np.dot(rgb[...,:3], [0.299, 0.587, 0.114])


gray_img = grayscale(start_img)
inverted_img = 255-gray_img
blur_img = scipy.ndimage.filters.gaussian_filter(inverted_img,sigma=5)


def dodge(front,back):
    result=front*255/(255-back)
    result[result>255]=255
    result[back==255]=255
    return result.astype('uint8')


final_img= dodge(blur_img,gray_img)
plt.imshow(final_img, cmap="gray")
plt.show()
plt.imsave('img4.png', final_img, cmap='gray', vmin=0, vmax=255)
