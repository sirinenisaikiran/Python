from tkinter import *

class App:
    def __init__(self, master):
        self.root = master
        frame = Frame(master)
        frame.pack(fill=BOTH, expand=YES)
        self.button = Button( frame, text="QUIT", fg="red", command=self.quit  )
        self.button.pack(side=TOP, fill=BOTH,expand=1)
        self.hi_there = Button(frame, text="Hello", command=self.say_hi)
        self.hi_there.pack(side=TOP, fill=BOTH,expand=1)
        self.w = Label(frame, text="Enter text")
        self.w.pack(side=TOP, anchor=W , fill=BOTH,expand=1)
        
        self.text = StringVar()
        self.input = Entry( frame ,textvariable=self.text)
        self.input.pack(side=TOP, anchor=W, fill=BOTH,expand=1)
        self.text.set("command")
        self.input.bind("<Return>", lambda event: self.say_hi())
    def say_hi(self):
        print("hi there, everyone!", self.text.get())
    def quit(self):
        self.root.destroy()

root = Tk()
app = App(root)
root.mainloop()