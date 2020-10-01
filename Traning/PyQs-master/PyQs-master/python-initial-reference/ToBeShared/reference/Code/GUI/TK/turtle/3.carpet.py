import turtle
import tkinter as tk
import random 

X = 1000 
Y = 500
T_X = X//2 - 3
T_Y = Y//2 - 3
root = tk.Tk()
canvas = tk.Canvas(master = root, width = X, height = Y)
canvas.pack(fill=tk.BOTH, expand=1)

elsa = turtle.RawTurtle(canvas)



def getMid(p1,p2):
    return ( (p1[0]+p2[0]) // 2, (p1[1] + p2[1]) // 2) #find midpoint

def triangle(points, depth):
    elsa.up()
    elsa.goto(points[0][0],points[0][1])
    elsa.down()
    elsa.goto(points[1][0],points[1][1])
    elsa.goto(points[2][0],points[2][1])
    elsa.goto(points[0][0],points[0][1])
    if depth>0:
        triangle([points[0],
                        getMid(points[0], points[1]),
                        getMid(points[0], points[2])],
                   depth-1)
        triangle([points[1],
                        getMid(points[0], points[1]),
                        getMid(points[1], points[2])],
                   depth-1)
        triangle([points[2],
                         getMid(points[2], points[1]),
                         getMid(points[0], points[2])],
                   depth-1)



points = [[-175,-125],[0,175],[175,-125]] #size of triangle
def redraw():
    elsa.reset()
    elsa.speed(0) 
    elsa.hideturtle()
    triangle(points,5)
        
tk.Button(master = root, text = "Draw", command = redraw).pack(side = tk.LEFT)
root.mainloop()