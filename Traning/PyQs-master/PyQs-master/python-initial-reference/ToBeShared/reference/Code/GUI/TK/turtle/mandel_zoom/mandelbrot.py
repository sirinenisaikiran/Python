from multiprocessing import Pool
import sys
import os


        
        
class Mandelbrot():
    def __init__(self, canvasW, canvasH, x=-0.75, y=0, m=1.5, iterations=None, w=None, h=None, zoomFactor=0.1, multi=True, opt1=False, opt2=False):
        self.w, self.h = (round(canvasW*0.9), round(canvasH*0.9)) if None in {w, h} else w, h
        self.iterations = 200 if iterations is None else iterations
        self.xCenter, self.yCenter = x, y
        if canvasW > canvasH:
            self.xDelta = m/(canvasH/canvasW)
            self.yDelta = m
        else:
            self.yDelta = m/(canvasW/canvasH)
            self.xDelta = m
        self.delta = m
        self.multi = multi
        self.xmin = x - self.xDelta
        self.xmax = x + self.xDelta
        self.ymin = y - self.yDelta
        self.ymax = y + self.yDelta
        self.zoomFactor = zoomFactor
        self.yScaleFactor = self.h/canvasH
        self.xScaleFactor = self.w/canvasW
        self.c, self.z = 0, 0
        self.opt1 = opt1
        self.opt2 = opt2

    def shiftView(self, event):
        self.xCenter = translate(event.x*self.xScaleFactor, 0, self.w, self.xmin, self.xmax)
        self.yCenter = translate(event.y*self.yScaleFactor, self.h, 0, self.ymin, self.ymax)
        self.xmax = self.xCenter + self.xDelta
        self.ymax = self.yCenter + self.yDelta
        self.xmin = self.xCenter - self.xDelta
        self.ymin = self.yCenter - self.yDelta

    def zoomOut(self, event):
        self.xCenter = translate(event.x*self.xScaleFactor, 0, self.w, self.xmin, self.xmax)
        self.yCenter = translate(event.y*self.yScaleFactor, self.h, 0, self.ymin, self.ymax)
        self.xDelta /= self.zoomFactor
        self.yDelta /= self.zoomFactor
        self.delta /= self.zoomFactor
        self.xmax = self.xCenter + self.xDelta
        self.ymax = self.yCenter + self.yDelta
        self.xmin = self.xCenter - self.xDelta
        self.ymin = self.yCenter - self.yDelta

    def zoomIn(self, event):
        print(event.x, event.y)
        self.xCenter = translate(event.x*self.xScaleFactor, 0, self.w, self.xmin, self.xmax)
        self.yCenter = translate(event.y*self.yScaleFactor, self.h, 0, self.ymin, self.ymax)
        self.xDelta *= self.zoomFactor
        self.yDelta *= self.zoomFactor
        self.delta *= self.zoomFactor
        self.xmax = self.xCenter + self.xDelta
        self.ymax = self.yCenter + self.yDelta
        self.xmin = self.xCenter - self.xDelta
        self.ymin = self.yCenter - self.yDelta

    def getPixels(self):
        if self.opt2 :
            print("Using namba vectorize...")
            #mandelbrot_set4(xmin,xmax,ymin,ymax,width,height,maxiter)
            pixels = mandelbrot_set2(self.xmin, self.xmax, self.ymin, self.ymax, self.w, self.h, self.iterations)
            self.pixels = pixels
            #self.debug(self.pixels)
            return 
        if self.opt1 :
            print("Using namba...")
            #mandelbrot_set4(xmin,xmax,ymin,ymax,width,height,maxiter)
            pixels = mandelbrot_set4(self.xmin, self.xmax, self.ymin, self.ymax, self.w, self.h, self.iterations)
            self.pixels = pixels
            #self.debug(self.pixels)
            return 

        coordinates = []
        for x in range(self.w):
            for y in range(self.h):
                coordinates.append((x, y))
        if self.multi:
            print("Using all core...")
            pool = Pool()
            self.pixels = pool.starmap(self.getEscapeTime, coordinates)
            pool.close()
            pool.join()
            #self.debug(self.pixels)
        else:
            print("Using 1 core...")
            pixels = []
            for coord in coordinates:
                pixels.append(self.getEscapeTime(coord[0], coord[1]))
            self.pixels = pixels
            #self.debug(self.pixels)
            
    def getEscapeTime(self, x, y):
        re = translate(x, 0, self.w, self.xmin, self.xmax)
        im = translate(y, 0, self.h, self.ymax, self.ymin)
        z, c = complex(re, im), complex(re, im)
        for i in range(1, self.iterations):
            if abs(z) > 2:
                return (x, y, i)
            z = z*z + c
        return (x, y, 0)
        
    def debug(self, lst):
        print(type(lst), len(lst), type(lst[0]), len(lst[0]))
        print(lst[0:3])
        

def translate(value, leftMin, leftMax, rightMin, rightMax):
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin
    valueScaled = float(value - leftMin) / float(leftSpan)
    return rightMin + (valueScaled * rightSpan)

from numba import jit
import numpy as np 

@jit
def mandelbrot(creal,cimag,maxiter):
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
    r2 = np.linspace(ymax,ymin,height)
    lst = np.empty(width*height, dtype=[('x', int), ('y', int),('z', int)])
    cnt = 0
    for i in range(width):
        for j in range(height):
            v = mandelbrot(r1[i],r2[j],maxiter)
            lst[cnt] = (i, j, v) 
            cnt += 1
    return lst.tolist()
    

from numba import jit, vectorize, guvectorize, float64, complex64, int32, float32, float64, complex128

@jit(int32(complex128, int32))
def mandelbrot2(c,maxiter):
    nreal = 0
    real = 0
    imag = 0
    for n in range(maxiter):
        nreal = real*real - imag*imag + c.real
        imag = 2* real*imag + c.imag
        real = nreal;
        if real * real + imag * imag > 4.0:
            return n
    return 0

@guvectorize([(complex128[:], int32[:], int32[:])], '(n),()->(n)',target='parallel')
def mandelbrot_numpy(c, maxit, output):
    maxiter = maxit[0]
    for i in range(c.shape[0]):
        output[i] = mandelbrot2(c[i],maxiter)
       
      
def mandelbrot_set2(xmin,xmax,ymin,ymax,width,height,maxiter):
    r1 = np.linspace(xmin, xmax, width, dtype=np.float64)
    index1 = np.arange(0, width)
    r2 = np.linspace(ymax, ymin, height, dtype=np.float64)
    index2 = np.arange(height-1, -1,-1)
    c = r1 + r2[:,None]*1j  #2D, width x height or use meshgrid 
    n3 = mandelbrot_numpy(c,np.array([maxiter]))
    XX, YY = np.meshgrid(index1, index2)
    i = XX.T.ravel().tolist()
    j = YY.T.ravel().tolist()
    lst = n3.T.ravel().tolist()
    return list(zip(i,j,lst))