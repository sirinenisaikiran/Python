from PIL import Image 
import time
import argparse, sys 
from functools import partial 
import math, random

# drawing area 
center_x = 0.0
center_y = 0.0
mag = 0  # number , 1,2,3....
#delta 
delta = 0.1      # delta for magnification (used for power)
mag_delta = 0.5  #delta for magnification when on click results 

#boundary, -2, 2
delta_x_left, delta_x_right = -2, 2
delta_y_left, delta_y_right = -2, 2 


# max iterations allowed 
maxIt = 512
# image size 
width = 1024
height = 1024
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

#For the Mandelbrot set, c instead differs for each pixel and is the initial z value(Z_0)


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

C_S = [
.26 + .54j,
-1.04 + 0.04j,
-1.135 + .2475j,
-1.1825 + .3175j,
-.72 - .3275j,
-1.1675 + .645j,
-.79 + .15j,
-.162 + 1.04j,
.3 - .01j,
.1476 + 0j,
-.12 - .77j,
.28 + .008j]

class Prop:
    def __init__(self, ax, c, c_x,c_y, mag, maxIt, width, height, n):
        self.ax = ax 
        self.c = c 
        self.cx = c_x 
        self.cy = c_y 
        self.mag = mag 
        self.maxIt = maxIt 
        self.width = width 
        self.height = height 
        self.n = n 
        #const 
        self.delta = 0.1 
        self.mag_delta = 0.5
        #derived 
        self.palette = self.getPalette()
    def getColor(self, n):
        return self.palette[n % 256]
    def getColor2(self, n):    
        return (n % 4 * 64, n % 8 * 32, n % 16 * 16)
    def all_calculate(self):
        #derived
        xmin,xmax = include_mag(self.cx ,delta_x_left,  delta_x_right ,self.mag)
        ymin, ymax = include_mag(self.cy , delta_y_left,  delta_y_right , self.mag)
        return xmin,xmax, ymin, ymax  
    def calculate_mag(self, button):
        if self.mag == 0 and button == 3: #right click, can not go below 0 
            return self.mag 
        if button == 1:  #left click 
            return self.mag + self.mag_delta
        if button == 2:   #middle click 
            return self.mag 
        if button == 3 :
            return self.mag - self.mag_delta    
    def __str__(self):
        return ("%s,"*10) % (str(self.ax),str(self.c),str(self.cx),str(self.cy),str(self.mag),str(self.maxIt),str(self.width),str(self.height),str(self.delta),str(self.mag_delta))
    def getPalette(self):
        palette = [(0, 0, 0)]
        redb = 2 * math.pi / (random.randint(0, 128) + 128)
        redc = 256 * random.random()
        greenb = 2 * math.pi / (random.randint(0, 128) + 128)
        greenc = 256 * random.random()
        blueb = 2 * math.pi / (random.randint(0, 128) + 128)
        bluec = 256 * random.random()
        for i in range(256):
            r = self.clamp(int(256 * (0.5 * math.sin(redb * i + redc) + 0.5)))
            g = self.clamp(int(256 * (0.5 * math.sin(greenb * i + greenc) + 0.5)))
            b = self.clamp(int(256 * (0.5 * math.sin(blueb * i + bluec) + 0.5)))
            palette.append((r, g, b))
        return palette
    def clamp(self,x):
        return max(0, min(x, 255))



def julia(re,img,c, maxiter): 
    z = re + img * 1j
    for i in range(maxIt): 
        if abs(z) > 2.0: return i
        z = z * z + c 
    else:
        return 0 




def julia_set(c, xmin,xmax,ymin,ymax,width,height,maxiter):
    lst = []
    for y in range(height): 
        img = translate(y, 0, height, ymin, ymax)
        for x in range(width): 
            re = translate(x, 0, width, xmin, xmax)            
            i = julia(re, img, c, maxIt)
            lst.append((x, y,i)) 
    return lst 



from numba import jit
import numpy as np 
import matplotlib.pyplot as plt 

@jit
def julia4(zreal,zimag,c, maxiter):
    real = zreal
    imag = zimag
    nreal = 0 
    for n in range(maxiter):
        nreal = real*real - imag*imag + c.real
        imag = 2* real*imag + c.imag
        real = nreal 
        if real * real + imag * imag > 4.0:
            return n  
    return 0  


@jit
def julia_set4(c,xmin,xmax,ymin,ymax,width,height,maxiter):
    #(start, stop, num)
    r1 = np.linspace(xmin, xmax, width)
    r2 = np.linspace(ymin, ymax,height)
    lst = np.empty(width*height, dtype=[('x', int), ('y', int),('z', int)])
    cnt = 0
    for i in range(width):
        for j in range(height):
            v = julia4(r1[i],r2[j],c,maxiter)
            lst[cnt] = (i, j, v) 
            cnt += 1
    return lst.tolist()  


from numba import jit, vectorize, guvectorize, float64, complex64, int32, float32, float64, complex128

@jit(int32(complex128, complex128, int32))
def julia2(z, c, maxiter):
    nreal = 0
    real = z.real
    imag = z.imag
    for n in range(maxiter):
        nreal = real*real - imag*imag + c.real
        imag = 2* real*imag + c.imag
        real = nreal
        if real * real + imag * imag > 4.0:
            return n
    return 0

#(n),(),()->(n) tells NumPy that the function takes a n-element one-dimension array, 
#a scalar (symbolically denoted by the empty tuple ()) 
#and returns a n-element one-dimension array;

@guvectorize([(complex128[:], complex128, int32, int32[:])], '(n),(),()->(n)',target='parallel')
def julia_numpy(z, c, maxiter, output):
    for i in range(z.shape[0]):
        output[i] = julia2(z[i],c, maxiter)  #for full row(all cols) at a time , hence vectorized 

      
def julia_set2(c, xmin,xmax,ymin,ymax,width,height,maxiter):
    r1 = np.linspace(xmin, xmax, width, dtype=np.float64)
    index1 = np.arange(0, width)
    r2 = np.linspace(ymin, ymax, height, dtype=np.float64)
    index2 = np.arange(0, height)
    z = r1 + r2[:,None]*1j  #2D, width x height or use meshgrid 
    n3 = julia_numpy(z, c, maxiter)
    XX, YY = np.meshgrid(index1, index2)
    i = XX.ravel().tolist()
    j = YY.ravel().tolist()
    lst = n3.ravel().tolist()
    return list(zip(i,j,lst))
    
    






        
def draw(ax, prop):
    prop.ax.clear()

    xmin,xmax, ymin, ymax = prop.all_calculate()
    #in window cordinates 
    center_x_win = translate(prop.cx, xmin, xmax, 0, prop.width)  
    center_y_win = translate(prop.cy,ymin, ymax, 0, prop.height)
    #otherway 
    #center_x_1 = translate(center_x_win, 0,prop.width, xmin, xmax)
    #center_y_1 = translate(center_y_win,0, prop.height, ymin, ymax)
    #print(center_x_1, center_y_1)    
        
    image = Image.new("RGB", (prop.width, prop.height)) 
    st = time.time()    
    pixels  = julia_set2(prop.c, xmin,xmax,ymin,ymax,prop.width,prop.height,prop.maxIt)    
    print("-"*40)
    print("[%s: (x=%.10f,y=%.10f),left-top:[%.10f,%.10f],right-bottom:[%.10f,%.10f], mag=%3.2e] iter=%d" %(str(prop.c),prop.cx, prop.cy, xmin,ymin,xmax,ymax, 1/(prop.delta ** prop.mag), maxIt), " took %3.2f seconds" %( (time.time()-st), ))
    #print("few first=%s, few last=%s" %( pixels[0:5], pixels[-5:]))
    for x,y,i in pixels:
        image.putpixel((x, y), prop.getColor2(i)) 

    #image.show() 
    prop.ax.imshow(np.asarray(image), aspect="auto")
    prop.ax.arrow(center_x_win, center_y_win, 0.1*center_x_win,0.1*center_y_win,color='white')
    return None 


def on_move(event):
    # get the x and y pixel coords
    x, y = event.x, event.y
    if event.inaxes:
        ax = event.inaxes  # the axes instance
        print('data coords %f %f' % (event.xdata, event.ydata))
        


       
def onclick_gen(event, props):
    cur_ax = event.inaxes
    for i, prop in enumerate(props):
        if cur_ax == prop.ax : #found this axes 
            xmin,xmax, ymin, ymax = prop.all_calculate()
            print('(c=%s) at %d, %s click(name:%s): button=%d\nwindow coords:(x=%d:%7.2f:%d, y=%d:%7.2f:%d)' %
                  (str(prop.c), i,'double' if event.dblclick else 'single',  event.name, event.button,
                   0,event.xdata,prop.width, 0,event.ydata,prop.height), end= " ")
            x,y = event.xdata, event.ydata  # this is part of width x height
            #convert to 
            x = translate(x, 0,prop.width, xmin, xmax)
            y = translate(y,0, prop.height, ymin, ymax)
            new_mag = prop.calculate_mag(event.button)
            print("data coords:(x=%3.2f:%3.2f:%3.2f,y=%3.2f:%3.2f:%3.2f)" % (xmin,x,xmax,ymin,y,ymax))
            print("command=%s -i %d -x %.20f -y %.20f -m %3.2f -n %d" % (sys.argv[0], prop.maxIt, x, y, new_mag, prop.n))
            prop.cx = x
            prop.cy = y
            prop.mag = new_mag 
            #create new palette if doubleclick 
            if event.dblclick:
                prop.palette = prop.getPalette()
            draw(prop.ax, prop)
            plt.gcf().canvas.draw_idle()  #only updated ax is drawn
    
    


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate the julia set')
    #generates the value of dest by taking the first long option string and stripping away the initial -- string
    #If not present, then derived from the first short option string by stripping the initial - character.
    parser.add_argument('-i', '--iterations', type=int, default=maxIt, help='The number of iterations done for each pixel. Higher is more accurate but slower.')
    parser.add_argument('-x', type=float, default=center_x, help='The x-center coordinate of the frame.')
    parser.add_argument('-y', type=float, default=center_y, help='The y-center coordinate of the frame.')
    parser.add_argument('-m', '--magnification', type=float, default=mag, help='The magnification level of the frame.')
    parser.add_argument('-n', type=str, default='all', help='which one')
    args = parser.parse_args()
    #
    center_x = args.x
    center_y = args.y
    mag = args.magnification  # number , 1,2,3....
    maxIt = args.iterations 
    props = []    
    if args.n == 'all':
        ncols = 4 
        nrows = len(C_S)//ncols 
        fig, axs = plt.subplots(nrows=nrows, ncols=ncols, sharex=True, sharey=True, subplot_kw=dict(visible=True))
        for i, (c, ax) in enumerate(zip(C_S, axs.ravel().tolist())):
            p = Prop(ax, c, center_x,center_y, mag, maxIt , width, height, i)
            draw(ax, p)
            props.append(p)
        #[print(p, end=",") for p in props]
        #print()  
    else:
        fig, ax = plt.subplots()
        n = int(args.n)
        p = Prop(ax, C_S[n], center_x,center_y, mag, maxIt , width, height, n)
        draw(ax, p)
        props.append(p)
    fig.tight_layout()    
    onclick = partial(onclick_gen, props=props)
    cid = plt.gcf().canvas.mpl_connect('button_press_event', onclick)
    #binding_id = plt.connect('motion_notify_event', on_move)
    plt.show()
