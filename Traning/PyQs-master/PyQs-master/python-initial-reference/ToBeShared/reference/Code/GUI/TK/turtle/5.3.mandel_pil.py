from PIL import Image 
import time
import argparse, sys 
from functools import partial 
from colors import *

# drawing area 
center_x = -0.75
center_y = 0.0
mag = 0  # number , 1,2,3....
#delta 
delta = 0.1      # delta for magnification (used for power)
mag_delta = 0.5  #delta for magnification when on click results 

#power Mandelbort set 
N = 2

delta_x_left, delta_x_right = -1.25, 1.75 
delta_y_left, delta_y_right = -1.5, 1.5 


# max iterations allowed 
maxIt = 255
# image size 
width = 512
height = 512
#global 
cid = None 


def include_mag(cx, d_x_l, d_x_r, mag, delta = delta):
    magnification = delta ** mag 
    return cx + d_x_l*magnification, cx + d_x_r*magnification

def translate(value, leftMin, leftMax, rightMin, rightMax):
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin
    valueScaled = float(value - leftMin) / float(leftSpan)
    return rightMin + (valueScaled * rightSpan)




#Z_n+1 = Z_n * Z_n + c 

#For Julia sets, c is the same complex number for all pixels, 
#and there are many different Julia sets based on different values of c
# .26+.54i
# -1.04+0.04i
# -1.135+.2475i
# -1.1825+.3175i
# -.72-.3275i
# -1.1675+.645i
# -.79+.15i
# -.162+1.04i
# .3-.01i
# .1476+0i
# -.12-.77i
# .28+.008i


#For the Mandelbrot set, c instead differs for each pixel and is the initial z value(Z_0)

def mandelbrot(re,img,pow, maxiter): 
    z = re + img * 1j
    c = z 
    for i in range(maxIt): 
        if abs(z) > 2.0: return i
        z = z ** pow + c 
    else:
        return 0 




def mandelbrot_set(pow, xmin,xmax,ymin,ymax,width,height,maxiter):
    lst = []
    for y in range(height): 
        img = translate(y, 0, height, ymin, ymax)
        for x in range(width): 
            re = translate(x, 0, width, xmin, xmax)            
            i = mandelbrot(re, img, pow, maxIt)
            lst.append((x, y,i)) 
    return lst 



from numba import jit
import numpy as np 
import matplotlib.pyplot as plt 

@jit
def mul(ar,ai,br,bi):
    return (ar*br-ai*bi, ai*br+ar*bi, ar*br+ai*bi)

@jit
def mandelbrot4(creal,cimag,pow, maxiter):
    real = creal
    imag = cimag
    for n in range(maxiter):
        for _ in range(1,pow):
            real,imag, abs = mul(real,imag, real, imag)
        if abs > 4.0:
            return n
        imag = imag + cimag
        real = real + creal       
    return 0    



@jit
def mandelbrot_set4(pow, xmin,xmax,ymin,ymax,width,height,maxiter):
    #(start, stop, num)
    r1 = np.linspace(xmin, xmax, width)
    r2 = np.linspace(ymin, ymax,height)
    lst = np.empty(width*height, dtype=[('x', int), ('y', int),('z', int)])
    cnt = 0
    for i in range(width):
        for j in range(height):
            v = mandelbrot4(r1[i],r2[j],pow, maxiter)
            lst[cnt] = (i, j, v) 
            cnt += 1
    return lst.tolist()  


from numba import jit, vectorize, guvectorize, float64, complex64, int32, float32, float64, complex128

@jit(int32(complex128, int32, int32))
def mandelbrot2(z,pow,maxiter):
    real = z.real
    imag = z.imag
    for n in range(maxiter):
        for _ in range(1,pow):
            real,imag, abs = real*real-imag*imag, imag*real+real*imag, real*real+imag*imag
        if abs > 4.0:
            return n
        imag = imag + z.imag
        real = real + z.real      
    return 0 

#(n),()->(n) tells NumPy that the function takes a n-element one-dimension array, 
#a scalar (symbolically denoted by the empty tuple ()) 
#and returns a n-element one-dimension array;
@guvectorize([(complex128[:], int32, int32, int32[:])], '(n),(),()->(n)',target='parallel')
def mandelbrot_numpy(c, pow, maxit, output):
    maxiter = maxit     #[0]
    for i in range(c.shape[0]):
        output[i] = mandelbrot2(c[i],pow, maxiter)  #for full row(all cols) at a time , hence vectorized 

      
def mandelbrot_set2(pow,xmin,xmax,ymin,ymax,width,height,maxiter):
    r1 = np.linspace(xmin, xmax, width, dtype=np.float64)
    index1 = np.arange(0, width)
    r2 = np.linspace(ymin, ymax, height, dtype=np.float64)
    index2 = np.arange(0, height)
    c = r1 + r2[:,None]*1j  #2D, width x height or use meshgrid 
    n3 = mandelbrot_numpy(c,pow, maxiter)
    XX, YY = np.meshgrid(index1, index2)
    i = XX.ravel().tolist()
    j = YY.ravel().tolist()
    lst = n3.ravel().tolist()
    return list(zip(i,j,lst))
    
    
def all_calculate(center_x,center_y, mag):
    #derived
    xmin,xmax = include_mag(center_x ,delta_x_left,  delta_x_right ,mag)
    ymin, ymax = include_mag(center_y , delta_y_left,  delta_y_right , mag)
    return xmin,xmax, ymin, ymax
    
def draw(ax,center_x,center_y, pow, mag, maxIt , width=width, height=height):
    ax.clear()

    xmin,xmax, ymin, ymax = all_calculate(center_x,center_y, mag)
    #in window cordinates 
    center_x_win = translate(center_x, xmin, xmax, 0, width)  
    center_y_win = translate(center_y,ymin, ymax, 0, height)
    #otherway 
    #center_x_1 = translate(center_x_win, 0,width, xmin, xmax)
    #center_y_1 = translate(center_y_win,0, height, ymin, ymax)
    #print(center_x_1, center_y_1)
    
        
    image = Image.new("RGB", (width, height)) 
    st = time.time()    
    pixels  = mandelbrot_set2(pow, xmin,xmax,ymin,ymax,width,height,maxIt)    
    #pixels  = mandelbrot_set4(pow, xmin,xmax,ymin,ymax,width,height,maxIt)
    print("-"*40)
    print("[(x=%.10f,y=%.10f),left-top:[%.10f,%.10f],right-bottom:[%.10f,%.10f], mag=%3.2e pow=%d] iter=%d" %(center_x, center_y, xmin,ymin,xmax,ymax, 1/(delta ** mag),pow, maxIt), " took %3.2f seconds" %( (time.time()-st), ))
    print("few first=%s, few last=%s" %( pixels[0:5], pixels[-5:]))
    for x,y,i in pixels:
        image.putpixel((x, y), getColor(i)) 

    #image.show() 
    ax.imshow(np.asarray(image), aspect="equal")#"auto"
    ax.arrow(center_x_win, center_y_win, 0.1*center_x_win,0.1*center_y_win,color='white')
    return None 


def on_move(event):
    # get the x and y pixel coords
    x, y = event.x, event.y
    if event.inaxes:
        ax = event.inaxes  # the axes instance
        print('data coords %f %f' % (event.xdata, event.ydata))
        
def calculate_mag(button, omag):
    if omag == 0 and button == 3: #right click, can not go below 0 
        return omag 
    if button == 1:  #left click 
        return omag + mag_delta
    if button == 2:   #middle click 
        return omag 
    if button == 3 :
        return omag - mag_delta

       
def onclick_gen(event, ax, center_x, center_y, pow, mag, maxIt, width,height):
    global cid 
    if event.inaxes:
        #print('%s click(name:%s): button=%d\nNote: pixel 0,0 = bottom, left, from left(x) =%d, from bottom(y) =%d\nin data coords:(x=%7.2f, y=%7.2f)' %
        #      ('double' if event.dblclick else 'single', event.name, event.button,
        #       event.x, event.y, event.xdata, event.ydata))
        
        xmin,xmax, ymin, ymax = all_calculate(center_x,center_y, mag)
        print('%s click(name:%s): button=%d\nwindow coords:(x=%d:%7.2f:%d, y=%d:%7.2f:%d)' %
              ('double' if event.dblclick else 'single', event.name, event.button,
               0,event.xdata,width, 0,event.ydata,height), end= " ")
        x,y = event.xdata, event.ydata  # this is part of width x height
        #convert to 
        x = translate(x, 0,width, xmin, xmax)
        y = translate(y,0, height, ymin, ymax)
        new_mag = calculate_mag(event.button, mag)
        print("data coords:(x=%3.2f:%3.2f:%3.2f,y=%3.2f:%3.2f:%3.2f)" % (xmin,x,xmax,ymin,y,ymax))
        print("command=%s -i %d -x %.20f -y %.20f -m %3.2f -p %d" % (sys.argv[0], maxIt, x, y, new_mag, pow))
        plt.gcf().canvas.mpl_disconnect(cid)
        onclick = partial(onclick_gen, ax=ax, center_x=x,center_y=y, pow=pow, mag=new_mag, maxIt=maxIt,width=width,height=height)
        cid = plt.gcf().canvas.mpl_connect('button_press_event', onclick)
        draw(ax,x,y, pow, new_mag , maxIt)
        plt.gcf().canvas.draw_idle()
    
    


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate the Mandelbrot set')
    #generates the value of dest by taking the first long option string and stripping away the initial -- string
    #If not present, then derived from the first short option string by stripping the initial - character.
    parser.add_argument('-i', '--iterations', type=int, default=maxIt, help='The number of iterations done for each pixel. Higher is more accurate but slower.')
    parser.add_argument('-x', type=float, default=center_x, help='The x-center coordinate of the frame.')
    parser.add_argument('-y', type=float, default=center_y, help='The y-center coordinate of the frame.')
    parser.add_argument('-m', '--magnification', type=float, default=mag, help='The magnification level of the frame.')
    parser.add_argument('-p', '--power', type=int, default=N, help='The magnification level of the frame.')
    args = parser.parse_args()
    #
    center_x = args.x
    center_y = args.y
    mag = args.magnification  # number , 1,2,3....
    maxIt = args.iterations   
    N = args.power 
    
    fig, ax = plt.subplots()
    onclick = partial(onclick_gen, ax=ax, center_x=center_x,center_y=center_y, pow=N, mag=mag, maxIt=maxIt,width=width,height=height)
    draw(ax, center_x,center_y, N, mag, maxIt)
    cid = plt.gcf().canvas.mpl_connect('button_press_event', onclick)
    #binding_id = plt.connect('motion_notify_event', on_move)    
    plt.show()
