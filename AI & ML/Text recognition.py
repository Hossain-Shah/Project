import pytesseract
from PIL import Image
from langdetect import detect_langs
img = Image.open('F:/Photos/Campus life(Tangail)/20190727_105517.jpg')
pytesseract.pytesseract.tesseract_cmd = r'D:\Softwares and apps\tesseract.exe'
text = pytesseract.image_to_string(img, config='')
print(text)
print(detect_langs(text))
