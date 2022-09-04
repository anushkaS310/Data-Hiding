import cv2 as cv
import math
import sys
import rdh_n as rdh
import matplotlib.pyplot as plt

image =cv.imread('photos/misc/boat.tiff')  
image = cv.cvtColor(image,cv.COLOR_BGR2GRAY)
# Define the window size
while True :
    a=int(input("Enter value of key a :"))
    b=int(input("Enter value of key b :"))
    mod=int(input("Enter value of mod :"))
    n=int(input("Enter value of n :"))
    if math.gcd(a,mod)  != 1:
        print("a and mod values must be co-prime.")
        ch=int(input("\n1.Re-enter\n2.Quit\nEnter choice:"))
        if ch == 2:
            sys.exit()
    else:
        break
# a,b,mod,n=5,8,256,2
modulo_multiplicative_inverse=pow(a,-1,mod)
windowsize = int(input("Enter block size:"))
g1 =cv.imread('photos/lena_image.jpg')  
g1 = cv.cvtColor(g1,cv.COLOR_BGR2GRAY)
peak_count_dic={}
overflow={}
# Crop out the window and calculate the histogram
block=1
print(image.shape)
for r in range(0,image.shape[0] - windowsize+1, windowsize):
    for c in range(0,image.shape[1] - windowsize+1, windowsize):
        gray = image[r:r+windowsize,c:c+windowsize]
        g1 = image[r:r+windowsize,c:c+windowsize]
        cv.imshow('gray',gray) 
        gray_hist=cv.calcHist([gray],[0],None,[256],[0,256])
        # plt.plot(gray_hist)
        # plt.show()

        # creating object of class
        obj=rdh.Data_Hiding(a,b,mod,n)

        # image encryption using affine cipher
        # gray=obj.encrypt_affine(gray)

        #finding peak and zero values
        l=obj.find_peak_zero(gray)
        peak_count_dic[block]=l
        

        #embedding data using rdh algo
        gray=obj.encrypt_rdh(gray)
        frame="encrypt"+str(block)
        overflow[block]=len(obj.arr)
        cv.imshow('gray',gray) 
        # cv.imshow('encrypted_img',gray)  

        #decoding data using rdh algo
        gray=obj.decrypt_rdh(gray)

        # obj.find_peak_zero(gray)

        # image decryption using affine cipher
        print(modulo_multiplicative_inverse)

        # gray=obj.decrypt_affine(gray,modulo_multiplicative_inverse,g1)
        frame=str(block)
        cv.imshow(frame,gray)
        block=block+1
total_overflow=sum(overflow)
file_path = 'demo.txt'
sys.stdout = open(file_path, "a")

# print((peak_count_dic))
# print(sum(peak_count_dic.values()))

peak_count=0

for i in range(1,block):
    peak_count+= peak_count_dic[i][1][0]
    total_overflow+=overflow[i]
embedding_capacity=peak_count*n
pure_capacity=embedding_capacity-total_overflow
# print statements

print("\na : "+str(a))
print("b : "+str(b))
print("mod : "+str(mod))
print("bits per pixel (n) : "+str(n))
print("block size : "+str(windowsize))
print()
print("{:<10}| {:<10} | {:<10} | {:<10} | {:<10}".format("Block","Peak Value","Zero Value","Peak Count","Overflow"))
for i in range(1,block):
    print("{:<10}| {:<10} | {:<10} | {:<10} | {:<10}".format(i,peak_count_dic[i][0],peak_count_dic[i][2],peak_count_dic[i][1][0],overflow[i]))
print()
print("Total peak count : "+ str(peak_count)+" pixels")
print("Total overflow : "+ str(total_overflow)+" pixels")
print("Embedding Capacity : "+ str(embedding_capacity)+" pixels")
print("Pure Capacity : "+ str(pure_capacity)+" pixels")
# print("In paper : "+input("Enter in paper"))
prnt()
cv.waitKey(0)


