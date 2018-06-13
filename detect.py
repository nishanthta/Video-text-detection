import cv2
import numpy as np


def bboxes(inp):
	img = inp
	#img2gray = cv2.imread(fname,0)
	#img = cv2.namedWindow(img,cv2.WINDOW_NORMAL)
	#img = cv2.resizeWindow(img,600,600)

	img_final = inp
	#img_final = cv2.namedWindow(fname,cv2.WINDOW_NORMAL)
	#img_final = cv2.resizeWindow(fname,600,600)

	img2gray = cv2.cvtColor(inp, cv2.COLOR_BGR2GRAY)
	ret, mask = cv2.threshold(img2gray,180, 255, cv2.THRESH_BINARY)
	image_final = cv2.bitwise_and(img2gray, img2gray, mask=mask)
	ret, new_img = cv2.threshold(img_final, 180, 255, cv2.THRESH_BINARY)  # for black text , cv.THRESH_BINARY_INV
	newimg = cv2.cvtColor(new_img, cv2.COLOR_BGR2GRAY)

	#remove noise from image
	kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3,
	                                                     3))  # to manipulate the orientation of dilution , large x means horizonatally dilating  more, large y means vertically dilating more
	dilated = cv2.dilate(newimg, kernel, iterations=3)  # dilate 

	contours, hierarchy = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)  # get contours


	for contour in contours:
	    # get rectangle bounding contour
	    [x, y, w, h] = cv2.boundingRect(contour)

	    # remove small false positives that aren't text
	    if w < 80 and h < 80:
	        continue
	    if h/w > 9.0 or w/h > 9.0:
	    	continue

	    # draw rectangle around contour on original image
	    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), 2)

	    '''
	    cropped = img_final[y :y +  h , x : x + w]

	    s = fname + '/crop_' + str(index) + '.jpg' 
	    cv2.imwrite(s , cropped)
	    index = index + 1

	    '''
	# write original image with added contours to disk
	imgres = cv2.resize(img, (1050,800))
	cv2.imshow('captcha_result', imgres)
	

#add the source file location here
srcfile = ''	

cap = cv2.VideoCapture(srcfile)
'''
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi',fourcc, 20.0, (640,480))
'''
while(cap.isOpened()):
	ret,inp = cap.read() 
	bboxes(inp)
	if cv2.waitKey(1) and 0xFF == ord('q'):
		break
	

cap.release()
cv2.destroyAllWindows()
