import cv2 as cv
import matplotlib.pyplot as plt


#nd numpy array of the image
gray =cv.imread('photos/lena_image.jpg')

# convert to gray scale image
gray = cv.cvtColor(gray,cv.COLOR_BGR2GRAY)
cv.imshow('Gray',gray)
print(gray)

# compute histogram for passed image
gray_hist=cv.calcHist([gray],[0],None,[256],[0,256])

# plotting the histogram
plt.figure()
plt.title("Histogram")
plt.plot(gray_hist)
plt.show()

# finding the peak and zero value
peak_val,zero_val=float('-inf'),float('inf')
for i in range(0,256):
    if peak_val < gray_hist[i]:
        peak_val=gray_hist[i]
        peak=i

    if gray_hist[i]== 0:
        zero=i
print('Peak Point: '+ str(peak)+" and pixel count is :"+ str(gray_hist[peak]))
print('Zero Point : '+ str(zero))

data_to_be_embedded="Hello World . This world is beautiful and amazing."

# converting strig to binary
bin_data=''.join(format(ord(i), '08b') for i in data_to_be_embedded)
bin_data_len=len(bin_data)

print("Data to be embedded : "+ str(bin_data))

index=0
# traversing the gray-scale image
for i in range(0,len(gray)):
    for j in range(0,len(gray[0])):
        if gray[i][j] > peak  and  gray[i][j] <zero :
            gray[i][j]=gray[i][j]+1 
        
for i in range(0,len(gray)):
    for j in range(0,len(gray[0])):
        if gray[i][j] == peak :
            if index<bin_data_len:
                if bin_data[index]=="1":
                    gray[i][j]=gray[i][j]+1 
                else :
                    pass
                index+=1

print(bin_data_len)
print(index)
gray_hist_shifted=cv.calcHist([gray],[0],None,[256],[0,256])
plt.plot(gray_hist_shifted)
plt.show()
cv.imshow('Gray',gray)
# print(plt.hist(gray_hist))
print(gray)
extracted_data=""
c=0
# EXTRACTION
for i in range(0,len(gray)):
    for j in range(0,len(gray[0])):
        if gray[i][j] == peak+1 :
            extracted_data += "1"
        elif gray[i][j] == peak :
            extracted_data += "0"
            c+=1
        else :
            pass
print("c : "+str(c))
for i in range(0,len(gray)):
        for j in range(0,len(gray[0])):
            if gray[i][j] > peak  and  gray[i][j] <=zero :
                gray[i][j]=gray[i][j]-1        
            

print("Data extracted : "+ extracted_data)
for i in range(0,len(bin_data)):
    print("here")
    if bin_data[i]!=extracted_data[i]:
        print(i)
peak_val,zero_val=float('-inf'),float('inf')
for i in range(0,256):
    if peak_val < gray_hist[i]:
        peak_val=gray_hist[i]
        peak=i

    if gray_hist[i]== 0:
        zero=i
print('Peak Point after decryption: '+ str(peak)+" and pixel count is :"+ str(gray_hist[peak]))
cv.waitKey(0)