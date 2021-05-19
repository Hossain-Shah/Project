from PIL import Image, ImageEnhance, ImageFilter
import os
import pytesseract
im = Image.open("download.jpg")
im = im.filter(ImageFilter.MedianFilter())
enhancer = ImageEnhance.Contrast(im)
im = enhancer.enhance(2)
im = im.convert('1')
im.save("bangla_ocr.jpg")
pytesseract.pytesseract.tesseract_cmd = r'D:\Softwares and apps\tesseract.exe'
text = pytesseract.image_to_string(Image.open("bangla_ocr.jpg"), lang="ben")
print(text)
print(pytesseract.image_to_string(Image.open('download.jpg'), lang='ben'))

