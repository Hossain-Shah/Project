from PIL import Image,ImageEnhance
im = Image.open('IMG_20170323_104738.jpg')
im.show()
enh = ImageEnhance.Contrast(im)
enh.enhance(1.8).show("30% more contrast")