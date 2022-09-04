import cv2 as cv

def  find_peak_zero(self, gray):
        gray_hist=cv.calcHist([gray],[0],None,[256],[0,256])
        for i in range(0,256):
            if self.peak_val < gray_hist[i]:
                self.peak_val=gray_hist[i]
                self.peak=i

            if gray_hist[i]== 0:
                self.zero=i
        print('Peak Point: '+ str(self.peak)+" and pixel count is :"+ str(gray_hist[self.peak]))
        print('Zero Point : '+ str(self.zero))

gray =cv.imread('photos/lena_image.jpg')  
gray = cv.cvtColor(gray,cv.COLOR_BGR2GRAY)
cv.imshow('gray',gray)
find_peak_zero(gray)