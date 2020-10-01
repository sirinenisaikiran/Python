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


# create a list of colours 
sfcolor = ["white", "blue", "purple", "grey", "magenta"] 

# create a function to create different size snowflakes 
def snowflake(size):   
    # move the pen into starting position 
    elsa.penup() 
    elsa.forward(10*size) 
    elsa.left(45) 
    elsa.pendown() 
    elsa.color(random.choice(sfcolor))   
    # draw branch 8 times to make a snowflake 
    for i in range(8): 
        branch(size)    
        elsa.left(45) 
      
  
# create one branch of the snowflake 
def branch(size): 
    for i in range(3): 
        for i in range(3): 
            elsa.forward(10.0*size/3) 
            elsa.backward(10.0*size/3) 
            elsa.right(45) 
        elsa.left(90) 
        elsa.backward(10.0*size/3) 
        elsa.left(45) 
    elsa.right(90)  
    elsa.forward(10.0*size) 
  
def redraw():
    elsa.reset()
    elsa.speed(0) 
    elsa.hideturtle()
    for i in range(5):
        x = random.randint(-T_X, T_X) 
        y = random.randint(-T_Y, T_Y) 
        sf_size = random.randint(1,5) 
        elsa.penup() 
        elsa.goto(x, y) 
        elsa.pendown() 
        snowflake(sf_size) 
        
tk.Button(master = root, text = "Draw", command = redraw).pack(side = tk.LEFT)
root.mainloop()