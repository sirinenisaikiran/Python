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


    
def all_calculate(center_x,center_y):
    xmin,xmax = center_x + delta_x_left,  center_x + delta_x_right
    ymin, ymax = center_y+ delta_y_left,  center_y+delta_y_right 
    return xmin,xmax, ymin, ymax
    
def draw(ax,center_x,center_y, maxIt , width=width, height=height):
    ax.clear()
    xmin,xmax, ymin, ymax = all_calculate(center_x,center_y)            
    image = Image.new("RGB", (width, height)) 
    st = time.time()    
    pixels  = mandelbrot_set4(xmin,xmax,ymin,ymax,width,height,maxIt)    
    print("-"*40)
    print("time taken", time.time()-st, "seconds")
    for x,y,i in pixels:
        image.putpixel((x, y), (i % 4 * 64, i % 8 * 32, i % 16 * 16)) 
    ax.imshow(np.asarray(image), aspect="equal")#"auto"
    return None 

  


if __name__ == '__main__':
    fig, ax = plt.subplots()
    draw(ax, center_x,center_y, maxIt)
    plt.show()
