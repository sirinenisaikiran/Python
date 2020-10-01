import turtle
turtle.color('red', 'yellow')
turtle.begin_fill()
while True:
    turtle.forward(200) #draw line upto 200 pixel
    turtle.left(170)    #rotate 170 deg
    x = turtle.pos()    #x, y, current cordinates  
    print(x, abs(x)) #abs = sqrt(x*x+y*y)
    if abs(x) < 1:
        break

turtle.end_fill()
turtle.done()  # or turtle.mainloop()