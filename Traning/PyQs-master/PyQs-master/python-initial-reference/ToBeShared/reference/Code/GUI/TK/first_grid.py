from tkinter import *

sticky=W+S+N+E

class App:
    def __init__(self, master):
        self.root = master
        frame = Frame(master)
        #frame is 1x1
        frame.grid(sticky=sticky)
        frame.master.rowconfigure( 0, weight = 1 )
        frame.master.columnconfigure( 0, weight = 1 )
        #create 2x2
        frame.rowconfigure( 0, weight = 1 )
        frame.columnconfigure( 0, weight = 1 )
        frame.rowconfigure( 1, weight = 1 )
        frame.columnconfigure( 1, weight = 1 )
        
        #Create now 
        self.button = Button( frame, text="QUIT", fg="red", command=self.quit  )
        self.button.grid(row=0,column=0,sticky=sticky)
        self.hi_there = Button(frame, text="Hello", command=self.say_hi)
        self.hi_there.grid(row=0,column=1,sticky=sticky)
        self.w = Label(frame, text="Enter text")
        self.w.grid(row=1,column=0,sticky=sticky)
        self.text = StringVar()
        self.input = Entry( frame ,textvariable=self.text)
        self.input.grid(row=1, column=1,sticky=sticky)
        self.text.set("command")
        self.input.bind("<Return>", lambda event: self.say_hi())
    def say_hi(self):
        print("hi there, everyone!", self.text.get())
    def quit(self):
        self.root.destroy()

root = Tk()
app = App(root)
root.mainloop()