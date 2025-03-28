import cv2
image=cv2.imread('20180404_120426.jpg')
cv2.imshow('people',image)
cv2.waitKey(0)
gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
template=cv2.imread('20180404_120426.jpg',0)
result=cv2.matchTemplate(gray,template,cv2.TM_CCOEFF)
sin_val, max_val, min_loc, max_loc=cv2.minMaxLoc(result)
top_left=max_loc
bottom_right=(top_left[0]+50,top_left[1]+50)
cv2.rectangle(image, top_left, bottom_right, (0,255,0),5)
cv2.imshow('object found',image)
cv2.waitKey(0)
cv2.destroyAllWindows()