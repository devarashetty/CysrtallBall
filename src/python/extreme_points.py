# USAGE
# python extreme_points.py

# import the necessary packages
import imutils
import cv2
import numpy as np
import json
import segment
import time

def calculatingMinDistance(x1SubArr, x2SubArr, center):
    sortArray(x1SubArr)
    sortArray(x2SubArr)
    d1= center-x1SubArr[len(x1SubArr)-1];
    d2=d1;
    if(len(x2SubArr)>0):
        d2= x2SubArr[0] - center;
    minD= 2*min(d1,d2);
    return 2*minD

def calculatingMaxDistance(x1SubArr, x2SubArr, center):
    sortArray(x1SubArr)
    sortArray(x2SubArr)
    d1=0;
    if(len(x1SubArr)>0):
        d1= center-x1SubArr[0];
    d2= x2SubArr[len(x2SubArr)-1] - center;
    maxD= 2*max(d1,d2);
    return 2*maxD

def sortArrays(arr1, arr2):
    for i in range(0, len(arr1)):    
        for j in range(i+1, len(arr1)):    
            if(arr1[i] > arr1[j]):    
                temp1 = arr1[i];    
                temp2 = arr2[i];
                arr1[i] = arr1[j];    
                arr2[i] = arr2[j];
                arr1[j] = temp1;  
                arr2[j] = temp2;

def sortArray(arr1):
    for i in range(0, len(arr1)):    
        for j in range(i+1, len(arr1)):    
            if(arr1[i] > arr1[j]):    
                temp1 = arr1[i];    
                arr1[i] = arr1[j]; 
                arr1[j] = temp1;  
                
def removeNoisePoints(arr1, length, cX):
    tempArr = list()
    for i in range(0, len(arr1)):
        if(abs(arr1[i]-cX) < length): 
            tempArr.append(arr1[i])
        i=i+1;
    return tempArr;

def findBodyType(head, shoulder, chest,waist, hips):
    bustHipRatio = chest/hips >=1.05 or chest/hips <= 0.95
    if((waist/shoulder <=.075 or waist/chest >= 0.75) and waist/hips <=0.75 and bustHipRatio):
        return "Hourglass";
    if((waist/shoulder  >= 1.05 or waist/chest >= 1.05 )and bustHipRatio):
        return "apple";
    if((waist/shoulder  >=0.75 or waist/chest >=0.75) and bustHipRatio ):
        return "Rectangular";
    if((shoulder/hips) >=1.5 or (chest/hips) >=1.5 ):
        return "Inverted Triangle";
    if(hips/shoulder  >=1.05 or hips/chest >= 1.05 ):
        return "Triangular";
    else:
        return "Rectangular"

def main():
    seg_image=segment.segmenter(cv2.imread('C:\\Users\\1025040\\Documents\\git\\CysrtallBall\\src\\python\\Cap1.jpg'))
    cv2.imwrite("first.jpg",seg_image)
    time.sleep(1)
    image = cv2.imread("first.jpg")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    canny = cv2.Canny(image,100,200)
    #cv2.imshow("image show",canny)
    thresh = cv2.threshold(gray, 45, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.erode(thresh, None, iterations=2)
    thresh = cv2.dilate(thresh, None, iterations=2)
    
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    c = max(cnts, key=cv2.contourArea)
    # Get the most extreme Body points along the boudy outline contours
    extLeft = tuple(c[c[:, :, 0].argmin()][0])
    extRight = tuple(c[c[:, :, 0].argmax()][0])
    extTop = tuple(c[c[:, :, 1].argmin()][0])
    extBot = tuple(c[c[:, :, 1].argmax()][0])
    cv2.circle(image, extLeft, 6, (255, 0, 255), -1)
    cv2.circle(image, extRight, 6, (255, 0, 255), -1)
    cv2.circle(image, extTop, 6, (255, 0, 255), -1)
    cv2.circle(image, extBot, 6,(255, 0, 255), -1)
    height = extBot[1] - extTop[1];
    width =  (int)(extRight[0] - extLeft[0]);
    cv2.rectangle(image,(extLeft[0],extTop[1]),(extRight[0],extBot[1]),(255,0,0),2)
    #Get the countor point in the approx Array
    epsilon = 0.001*cv2.arcLength(c,True)
    #peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c,epsilon,True)
    image= cv2.drawContours(image, [approx], 0 ,(0,255,0),1)
    cv2.drawContours(image, approx, -1, (0, 0, 255), 5)
    #cv2.drawContours(image, hull, -1, (200, 20, 255), 1, 8)
    n = approx.ravel() #Converts 3d to 1d Array
    i=0;
    length= len(n);
    xArr = list() #X-coordinate Array
    yArr = list() #Y-coordinate Array
    while i < length:
        if(i%2==0):
            xArr.append(n[i])
        else:
            yArr.append(n[i])
        i += 1
    
    j=0;
    while j < len(xArr):
        #image = cv2.putText(image, str(xArr[j]) +"," +str(yArr[j]), (xArr[j],yArr[j]), cv2.FONT_HERSHEY_SIMPLEX , 
         #              0.2, (255, 100, 100) , 1, cv2.LINE_AA)
        j +=1
    k= (int)(height/10);
    y= extTop[1];
    x= extLeft[0]
    center1= x+int(width/2);
    center2= y+int(height/2);
    cv2.rectangle(image,(extLeft[0],extTop[1]),(center1,center2),(255,0,200),3)
    
    M = cv2.moments(thresh)
     
    # calculate x,y coordinate of center
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
     
    # put text and highlight the center
    #cv2.circle(image, (cX, cY), 5, (255, 255, 255), -1)
    cv2.putText(image, "O", (cX - 25, cY - 25),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0),2)
    
    head=0;
    for p in range(0,10):
        cv2.rectangle(image, (x,y+k*p), (x+width, y+k*(p+1)), (0, 0,255), 3)
        y0= y+k*p+1
        y1= y0+k
        a=0;
        xSubArr =list();
        ySubArr =list();
        while a < len(yArr):
            if(yArr[a]>=y0 and yArr[a]<y1):
                xSubArr.append(xArr[a])
                ySubArr.append(yArr[a])
            a += 1
        sortArrays(ySubArr, xSubArr)
        x1SubArr=list();
        x2SubArr=list();
        y1SubArr=list();
        y2SubArr=list();
        for i in range(0, len(xSubArr)):
            if(xSubArr[i]< cX):
                x1SubArr.append(xSubArr[i])
                y1SubArr.append(ySubArr[i])
            else:
                x2SubArr.append(xSubArr[i])
                y2SubArr.append(ySubArr[i])
        if(p==0):
            head= calculatingMaxDistance(x1SubArr,x2SubArr,cX);
        if(p==1):
            neck= calculatingMinDistance(x1SubArr,x2SubArr,cX)
            sortArray(x2SubArr)
            x1SubArr=removeNoisePoints(x1SubArr, 3*neck, cX)
            x2SubArr=removeNoisePoints(x2SubArr, 3*neck , cX)
            shoulder= calculatingMaxDistance(x1SubArr,x2SubArr,cX)
        if(p==3):
            chest = calculatingMinDistance(x1SubArr,x2SubArr,cX)
        if(p==4):
            waist = calculatingMinDistance(x1SubArr,x2SubArr,cX)
        if(p==5):
            sortArray(x2SubArr)
            x1SubArr=removeNoisePoints(x1SubArr, 2*(x2SubArr[0]-cX), cX)
            x2SubArr=removeNoisePoints(x2SubArr, 2*(x2SubArr[0]-cX) , cX)
            hip = calculatingMaxDistance(x1SubArr,x2SubArr,cX)
            
    bodyType=findBodyType(head,shoulder,chest, waist,hip);
    scale= (68.4/height)
    
    data= {}
    data= {
           "height" : height*scale,
           "head"    : round(head*scale),
           "neck"    : round(neck*scale),
           "shoulder": round(shoulder*scale), 
           "waist"   : round(waist*scale), 
           "hip"     : round(hip*scale), 
           "chest"   : round(chest*scale),
           "bodyType": bodyType,
           "scale"   : scale
           }
    # show the output image
    # cv2.imshow("Image", image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    print (json.dumps(data))
    # return json.dumps(data)
if __name__=="__main__":
	main()
