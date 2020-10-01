from PIL import Image 
import time
import argparse, sys 
from functools import partial 


# drawing area 
center_x = -0.75
center_y = 0.0

delta_x_left, delta_x_right = -1.25, 1.75 
delta_y_left, delta_y_right = -1.5, 1.5 


# max iterations allowed 
maxIt = 512
# image size 
width = 512
height = 512

#<- 
mag = 0  # number , 1,2,3....
#delta 
delta = 0.1      # delta for magnification (used for power)
mag_delta = 0.5  #delta for magnification when on click results 

#Click gives in Window cordinate 
#transform into our data cordinate 
def translate(value, leftMin, leftMax, rightMin, rightMax):
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin
    valueScaled = float(value - leftMin) / float(leftSpan)
    return rightMin + (valueScaled * rightSpan)
    
#<-

from numba import jit
import numpy as np 
import matplotlib.pyplot as plt 

@jit
def mandelbrot4(creal,cimag,maxiter):
    real = creal
    imag = cimag
    for n in range(maxiter):
        real2 = real*real
        imag2 = imag*imag
        if real2 + imag2 > 4.0:
            return n
        imag = 2* real*imag + cimag
        real = real2 - imag2 + creal       
    return 0  



@jit
def mandelbrot_set4(xmin,xmax,ymin,ymax,width,height,maxiter):
    #(start, stop, num)
    r1 = np.linspace(xmin, xmax, width)
    r2 = np.linspace(ymin, ymax,height)
    lst = np.empty(width*height, dtype=[('x', int), ('y', int),('z', int)])
    cnt = 0
    for i in range(width):
        for j in range(height):
            v = mandelbrot4(r1[i],r2[j],maxiter)
            lst[cnt] = (i, j, v) 
            cnt += 1
    return lst.tolist()  


 
def all_calculate(center_x,center_y, mag, delta):
    #change here
    magnification = delta ** mag
    xmin,xmax = center_x + delta_x_left*magnification,  center_x + delta_x_right*magnification
    ymin, ymax = center_y+ delta_y_left*magnification,  center_y+delta_y_right*magnification 
    return xmin,xmax, ymin, ymax
    
def draw(ax,center_x,center_y, maxIt , mag, delta, width=width, height=height): #change here
    ax.clear()
    xmin,xmax, ymin, ymax = all_calculate(center_x,center_y, mag, delta)   #change here          
    image = Image.new("RGB", (width, height)) 
    st = time.time()    
    pixels  = mandelbrot_set4(xmin,xmax,ymin,ymax,width,height,maxIt)    
    print("-"*40)
    print("time taken", time.time()-st, "seconds")
    for x,y,i in pixels:
        image.putpixel((x, y), (i % 4 * 64, i % 8 * 32, i % 16 * 16)) 
    ax.imshow(np.asarray(image), aspect="equal")#"auto"
    return None 

#<- 
cid = None 

def calculate_mag(button, omag):
    if omag == 0 and button == 3: #right click, can not go below 0 
        return omag 
    if button == 1:  #left click 
        return omag + mag_delta
    if button == 2:   #middle click 
        return omag 
    if button == 3 :
        return omag - mag_delta
        
def onclick_gen(event, ax, center_x, center_y, mag, delta, maxIt, width,height):
    global cid 
    if event.inaxes:
        xmin,xmax, ymin, ymax = all_calculate(center_x,center_y, mag, delta)
        x,y = event.xdata, event.ydata  # this is part of width x height
        #convert to 
        x = translate(x, 0,width, xmin, xmax)
        y = translate(y,0, height, ymin, ymax)
        new_mag = calculate_mag(event.button, mag)
        plt.gcf().canvas.mpl_disconnect(cid)
        onclick = partial(onclick_gen, ax=ax, center_x=x,center_y=y, mag=new_mag, delta=delta, maxIt=maxIt,width=width,height=height)
        cid = plt.gcf().canvas.mpl_connect('button_press_event', onclick)
        draw(ax,x,y,  maxIt, new_mag , delta, width, height)
        plt.gcf().canvas.draw_idle()


#<-


if __name__ == '__main__':
    fig, ax = plt.subplots()
    #change here
    onclick = partial(onclick_gen, ax=ax, center_x=center_x,center_y=center_y, mag=mag, delta=delta, maxIt=maxIt,width=width,height=height)
    cid = plt.gcf().canvas.mpl_connect('button_press_event', onclick)
    draw(ax, center_x,center_y, maxIt,mag, delta,width, height) #change here
    plt.show()
