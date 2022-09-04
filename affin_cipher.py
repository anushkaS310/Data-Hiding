import string
import math
import sys
import cv2 as cv
class Data_Hiding:

    def __init__(self,a,b,mod):
        self.a=a
        self.b=b
        self.mod=mod
        self.peak=0
        self.zero=0
        self.arr=[]
        self.data=""
        
        
    def  find_peak_zero(self, gray):
        peak_val=float('-inf')
        zero_val=float('inf')
        gray_hist=cv.calcHist([gray],[0],None,[256],[0,256])
        for i in range(0,256):
            if peak_val < gray_hist[i]:
                peak_val=gray_hist[i]
                self.peak=i

            if gray_hist[i]== 0:
                self.zero=i
        print('Peak Point: '+ str(self.peak)+" and pixel count is :"+ str(gray_hist[self.peak]))
        print('Zero Point : '+ str(self.zero))


    def encrypt_rdh(self,gray):
        data_to_be_embedded="Hello World.This world is beautiful and amazing."

        # converting strig to binary
        bin_data=''.join(format(ord(i), '08b') for i in data_to_be_embedded)
        bin_data_len=len(bin_data)
        self.data=bin_data
        print("Data to be embedded : "+ str(bin_data))

        
        index=0
        
        # traversing the gray-scale image
        for i in range(0,len(gray)):
            for j in range(0,len(gray[0])):
                if gray[i][j] == 253 or gray[i][j]==254 or gray[i][j]==255 or gray[i][j] > self.zero:
                    self.arr.append([i,j,gray[i][j]])
                if gray[i][j] > self.peak  and  gray[i][j] <self.zero :
                    if gray[i][j] != 253 and gray[i][j]!=254 and gray[i][j]!=255:
                        gray[i][j]=gray[i][j]+3
                
        for i in range(0,len(gray)):
            for j in range(0,len(gray[0])):
                if gray[i][j] == self.peak :
                    if index<bin_data_len-1: 
                        if bin_data[index]=="0" and bin_data[index+1]=="1" :
                            gray[i][j]=gray[i][j]+1 
                        elif bin_data[index]=="1" and bin_data[index+1]=="0" :
                            gray[i][j]=gray[i][j]+2
                        elif bin_data[index]=="1" and bin_data[index+1]=="1" :
                            gray[i][j]=gray[i][j]+3
                        else :
                            pass
                        index+=2
        return gray

    def decrypt_rdh(self,gray):
        extracted_data=""
        # EXTRACTION
        for i in range(0,len(gray)):
            for j in range(0,len(gray[0])):
                if gray[i][j] == self.peak :
                    extracted_data += "00"
                elif gray[i][j] ==self.peak+1 :
                    extracted_data += "01"
                    gray[i][j]=gray[i][j]-1
                elif gray[i][j] == self.peak+2 :
                    extracted_data += "10"
                    gray[i][j]=gray[i][j]-2
                elif gray[i][j] == self.peak +3:
                    extracted_data += "11"
                else :
                    pass
        for i in range(0,len(gray)):
            for j in range(0,len(gray[0])):
                if gray[i][j] > self.peak +2  and  gray[i][j] <=self.zero +2:
                    gray[i][j]=gray[i][j]-3        
        # for i in range(0,len(self.arr)):
            # print(str(self.arr[i][0])+" "+ str(self.arr[i][1]) + " "+str(self.arr[i][2]))

        print("again")
        for i in range(0,len(self.arr)):
            gray[self.arr[i][0]][self.arr[i][1]]=self.arr[i][2]
        # for i in range(0,len(self.arr)):
            # print(str(self.arr[i][0])+" "+ str(self.arr[i][1]) + " "+str(self.arr[i][2])+" "+str(gray[self.arr[i][0]][self.arr[i][1]]))
                
    
        print("Data extracted : "+ extracted_data)
        for i in range(0,len(self.data)):
            print("here")
            if self.data[i]!=extracted_data[i]:
                print(i)
        return gray

    def encrypt_affine(self,gray):
        # ENCRYPTION
        for i in range(0,len(gray)):
            for j in range(0,len(gray[0])):
                gray[i][j] = (self.a*gray[i][j]+ self.b)% self.mod
        return gray

    def decrypt_affine(self , gray,modulo_multiplicative_inverse,g1):
        for i in range(0,len(gray)):
            for j in range(0,len(gray[0])):
                gray[i][j]= (modulo_multiplicative_inverse*(gray[i][j]-self.b))% self.mod
        print("here")
        for i in range(0,len(gray)):
            for j in range(0,len(gray[0])):
                if gray[i][j]!=g1[i][j]:
                    # gray[i][j]=100
                    print(str(i)+" "+str(j)+" "+str(gray[i][j])+" "+str(g1[i][j]))
        return gray

# 4 5 wrong
#5 8 correct
while True :
    a=int(input("Enter value of key a :"))
    b=int(input("Enter value of key b :"))
    mod=int(input("Enter value of mod :"))
    if math.gcd(a,mod)  != 1:
        print("a and mod values must be co-prime.")
        ch=int(input("\n1.Re-enter\n2.Quit\nEnter choice:"))
        if ch == 2:
            sys.exit()
    else:
        break
# a,b,mod=5,8,256
gray =cv.imread('photos/lena_image.jpg')  
gray = cv.cvtColor(gray,cv.COLOR_BGR2GRAY)
g1 =cv.imread('photos/lena_image.jpg')  
g1 = cv.cvtColor(g1,cv.COLOR_BGR2GRAY)
cv.imshow('gray',gray) 
print("in original image "+str(gray[508][480]))
obj=Data_Hiding(a,b,mod)
# image encryption using affine cipher
gray=obj.encrypt_affine(gray)
print("after affine cipher "+str(gray[508][480]))
#finding peak and zero values
obj.find_peak_zero(gray)

#embedding data using rdh algo
gray=obj.encrypt_rdh(gray)
print("after enc rdh "+str(gray[508][480]))
# cv.imshow('encrypted_img',gray)  

#decoding data using rdh algo
gray=obj.decrypt_rdh(gray)
print("after de rdh "+str(gray[508][480]))
obj.find_peak_zero(gray)
# image decryption using affine cipher
modulo_multiplicative_inverse=pow(a,-1,mod)
print(modulo_multiplicative_inverse)
gray=obj.decrypt_affine(gray,modulo_multiplicative_inverse,g1)
print("in dec image "+str(gray[508][480]))


cv.imshow('decrypted',gray)
cv.imshow('original',g1)
cv.waitKey(0)

        



