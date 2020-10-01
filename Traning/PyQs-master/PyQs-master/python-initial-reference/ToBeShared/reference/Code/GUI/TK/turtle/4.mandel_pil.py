'''
The Mandelbrot set is the set of complex numbers c for which the function f( z ) = z**2 + c 
does not diverge when iterated from z = 0 , i.e.,
for which the sequence f( 0 ) , f ( f ( 0 ) ) etc., remains bounded in absolute value. 

for each sample point c , whether the sequence f( 0 ) , f ( f ( 0 ) ) ,...
goes to infinity (in practice -- whether it leaves some predetermined bounded neighborhood of 0 
after a predetermined number of iterations).

Treating the real and imaginary parts of c as image coordinates on the complex plane, 
pixels may then be coloured according to how soon the sequence | f ( 0 ) | , | f ( f ( 0 ) ) | ,...
crosses an arbitrarily chosen threshold, 
with a special color (usually black) used for the values of c 
for which the sequence has not crossed the threshold after the predetermined number of iterations 
(this is necessary to clearly distinguish the Mandelbrot set image from the image of its complement). 


If c is held constant and the initial value of z —denoted by z0 
is variable instead, one obtains the corresponding Julia set for each point c 
in the parameter space of the simple function. 

'''

from PIL import Image 
from numpy import complex, array 
import colorsys 

# setting the width of the output image as 1024 
WIDTH = 1024

# a function to return a tuple of colors 
# as integer value of rgb 
def rgb_conv(i): 
	color = 255 * array(colorsys.hsv_to_rgb(i / 255.0, 1.0, 0.5)) 
	return tuple(color.astype(int)) 

# function defining a mandelbrot 
def mandelbrot(x, y): 
	c0 = complex(x, y) 
	c = 0
	for i in range(1, 1000): 
		if abs(c) > 2: 
			return rgb_conv(i) 
		c = c * c + c0 
	return (0, 0, 0) 

# creating the new image in RGB mode 
img = Image.new('RGB', (WIDTH, int(WIDTH / 2))) 
pixels = img.load() 

for x in range(img.size[0]): 

	# displaying the progress as percentage 
	print("%.2f %%" % (x / WIDTH * 100.0)) 
	for y in range(img.size[1]): 
		pixels[x, y] = mandelbrot((x - (0.75 * WIDTH)) / (WIDTH / 4), 
									(y - (WIDTH / 4)) / (WIDTH / 4)) 

# to display the created fractal after 
# completing the given number of iterations 
img.show() 
#img.save('file.png')