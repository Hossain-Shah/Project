from PIL import Image, ImageEnhance, ImageFilter
import cv2
import cvzone
from cvzone.SelfiSegmentationModule import SelfiSegmentation

# open the original image
file_name = "E:/Official purpose/2022/Q3S5/Rice_Stem_Borer_dividation/Stem_borer_larva/train/20220822_145422.jpg"
original_img = Image.open(file_name)

vertical_img = original_img.transpose(method=Image.FLIP_TOP_BOTTOM)
vertical_img.save("E:/Official purpose/2022/Q3S5/Rice_Stem_Borer_dividation/Stem_borer_larva/c.jpg")

horz_img = original_img.transpose(method=Image.FLIP_LEFT_RIGHT)
horz_img.save("E:/Official purpose/2022/Q3S5/Rice_Stem_Borer_dividation/Stem_borer_larva/d.jpg")

rotated_image = original_img.rotate(45)
rotated_image.save("E:/Official purpose/2022/Q3S5/Rice_Stem_Borer_dividation/Stem_borer_larva/e.jpg")

resized_image = original_img.resize((round(original_img.size[0]*1.5), round(original_img.size[1]*1)))
resized_image.save("E:/Official purpose/2022/Q3S5/Rice_Stem_Borer_dividation/Stem_borer_larva/f.jpg")

transposed_image = original_img.transpose(Image.FLIP_TOP_BOTTOM)
transposed_image.save("E:/Official purpose/2022/Q3S5/Rice_Stem_Borer_dividation/Stem_borer_larva/g.jpg")

detailed_image = original_img.filter(ImageFilter.DETAIL)
detailed_image.save("E:/Official purpose/2022/Q3S5/Rice_Stem_Borer_dividation/Stem_borer_larva/h.jpg")

enhanced_edged_image = original_img.filter(ImageFilter.EDGE_ENHANCE)
enhanced_edged_image.save("E:/Official purpose/2022/Q3S5/Rice_Stem_Borer_dividation/Stem_borer_larva/i.jpg")

src = cv2.imread(file_name, 1)
tmp = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
_, alpha = cv2.threshold(tmp, 0, 255, cv2.THRESH_BINARY)
b, g, r = cv2.split(src)
rgba = [b, g, r, alpha]
dst = cv2.merge(rgba, 4)
cv2.imwrite("E:/Official purpose/2022/Q3S5/Rice_Stem_Borer_dividation/Stem_borer_larva/j.JPG", dst)

segmentor = SelfiSegmentation()
img = cv2.imread(file_name)

#resize office to 640x480
img = cv2.resize(img, (640, 480))

background_removed = (0, 0, 0)
image_without_background = segmentor.removeBG(img, background_removed, threshold=0.50)
cv2.imwrite("E:/Official purpose/2022/Q3S5/Rice_Stem_Borer_dividation/Stem_borer_larva/b.JPG", image_without_background)

