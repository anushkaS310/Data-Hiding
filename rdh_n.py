import math
import sys
import cv2 as cv

class Data_Hiding:

    def __init__(self,a,b,mod,n):
        self.a=a
        self.b=b
        self.mod=mod
        self.peak=0
        self.zero=0
        self.n=n
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
        # print('Peak Point: '+ str(self.peak)+" and pixel count is :"+ str(gray_hist[self.peak]))
        # print('Zero Point : '+ str(self.zero))
        return [self.peak,gray_hist[self.peak],self.zero]


    def encrypt_rdh(self,gray):
        data_to_be_embedded="Hello World."

        # converting strig to binary
        bin_d=''.join(format(ord(i), '08b') for i in data_to_be_embedded)
        bin_data_len=len(bin_d)
        bin_data=str(bin_d)
        self.data=bin_d
        # print("Data to be embedded : "+ str(bin_data))        
        shift=pow(2,self.n)-1
        # print("shift"+str(shift))
        # traversing the gray-scale image
        for i in range(0,len(gray)):
            for j in range(0,len(gray[0])):
                # checked for overflow, overflow will be of 256-shift values all these are stored in a separate array 
                if gray[i][j] >= 256-shift or gray[i][j] > self.zero:
                    self.arr.append([i,j,gray[i][j]])
                
                if gray[i][j] > self.peak  and  gray[i][j] <self.zero :
                    if gray[i][j] <256-shift:
                        gray[i][j]=gray[i][j]+shift
        # print("Overflows in this block: "+str(len(self.arr)))
# bin_data_len-(bin_data_len%self.n)
        index=0      
        for i in range(0,len(gray)):
            for j in range(0,len(gray[0])):
                if gray[i][j] == self.peak :
                    if index<bin_data_len:
                        cur_data=bin_data[index:index+self.n]
                        decimal_data=int(cur_data,2)
                        # print("bin "+str(cur_data) + str(decimal_data)) 
                        index=index+ self.n
                        # print(index)
                        gray[i][j]=gray[i][j]+decimal_data
                    else:
                        break

        return gray

    def decrypt_rdh(self,gray):
        extracted_data=""
        shift=pow(2,self.n)-1
        # EXTRACTION
        k=0
        for i in range(0,len(gray)):
            for j in range(0,len(gray[0])):
                if gray[i][j] >= self.peak and gray[i][j]<=self.peak+shift:
                    
                    extracted_bits=str(bin(gray[i][j]-self.peak).replace("0b", ""))
                    rem=self.n-len(extracted_bits)
                    z=""
                    for o in range(0,rem):
                        z+='0'
                    if k<len(self.data)/2:
                        k=k+1
                        # print(gray[i][j]-self.peak)
                        # print(z+extracted_bits)
                    extracted_data+=(z+extracted_bits)
                    gray[i][j]=gray[i][j]-(gray[i][j]-self.peak)
                else :
                    pass


        for i in range(0,len(gray)):
            for j in range(0,len(gray[0])):
                if gray[i][j] > self.peak + shift-1 and  gray[i][j] <=self.zero + shift-1:
                    gray[i][j] = gray[i][j]-(shift)     
        
        for i in range(0,len(self.arr)):
            gray[self.arr[i][0]][self.arr[i][1]]=self.arr[i][2]
        # print("Data extracted : "+ extracted_data)
        # for i in range(0,len(self.data)):
        #     if self.data[i]!=extracted_data[i]:
        #         print(i)
                
                   
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
        
        # for i in range(0,len(gray)):
        #     for j in range(0,len(gray[0])):
        #         if gray[i][j]!=g1[i][j]:
        #             # gray[i][j]=100
        #             print(str(i)+" "+str(j)+" "+str(gray[i][j])+" "+str(g1[i][j]))
        return gray

# while True :
#     a=int(input("Enter value of key a :"))
#     b=int(input("Enter value of key b :"))
#     mod=int(input("Enter value of mod :"))
#     n=int(input("Enter value of n :"))
#     if math.gcd(a,mod)  != 1:
#         print("a and mod values must be co-prime.")
#         ch=int(input("\n1.Re-enter\n2.Quit\nEnter choice:"))
#         if ch == 2:
#             sys.exit()
#     else:
#         break

# gray =cv.imread('photos/lena_image.jpg')  
# gray = cv.cvtColor(gray,cv.COLOR_BGR2GRAY)

# g1 =cv.imread('photos/lena_image.jpg')  
# g1 = cv.cvtColor(g1,cv.COLOR_BGR2GRAY)

# cv.imshow('gray',gray) 

# print("in original image "+str(gray[0][351]))
# # creating object of class
# obj=Data_Hiding(a,b,mod,n)

# # image encryption using affine cipher
# gray=obj.encrypt_affine(gray)

# print("after affine cipher "+str(gray[0][351]))

# #finding peak and zero values
# obj.find_peak_zero(gray)

# #embedding data using rdh algo
# gray=obj.encrypt_rdh(gray)

# print("after enc rdh "+str(gray[0][351]))
# # cv.imshow('encrypted_img',gray)  

# #decoding data using rdh algo
# gray=obj.decrypt_rdh(gray)

# print("after de rdh "+str(gray[0][351]))
# obj.find_peak_zero(gray)

# # image decryption using affine cipher
# modulo_multiplicative_inverse=pow(a,-1,mod)
# print(modulo_multiplicative_inverse)

# gray=obj.decrypt_affine(gray,modulo_multiplicative_inverse,g1)
# print("in dec image "+str(gray[0][351]))


# cv.imshow('decrypted',gray)

# cv.waitKey(0)

        



