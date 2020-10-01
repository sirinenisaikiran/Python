from tkinter import *
import tkinter.scrolledtext as tkst

sticky=W+S+N+E

class App:
    def __init__(self, master):
        self.root = master
        frame = Frame(master)
        #frame is 1x1
        frame.grid(sticky=sticky)
        self.conf(frame.master,range(1),range(1))
        #create 3x2
        self.conf(frame,range(3),range(2))  #self.conf(frame,range(2),range(2))
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
        self.output = tkst.ScrolledText(frame, wrap=WORD, relief=SUNKEN,bg='misty rose', width=30,height=5)
        self.output.grid( row = 2, column = 0,columnspan=2,sticky = sticky)
        self.output.insert(INSERT, ("Scrolled text "*3+"\n")*100)
        #self.txFrame, self.output = self.createXYScrolledText(master,  wrap=WORD, relief=SUNKEN,bg='misty rose', width=30,height=5)
        #self.txFrame.grid( row = 2, column = 0, columnspan=2, sticky = sticky)
        #self.output.insert(INSERT, ("Scrolled text "*3+"\n")*100)             
        #schedule 
        self.root.after(1000,self.update)
    def update(self):
        self.output.delete(1.0, 2.0)
        nn = len(self.output.get(1.0, END).splitlines())
        print(nn)
        self.text.set(str(nn))
        self.root.after(1000,self.update)
    def conf(self, frame, row, col):
        for r in row:
            frame.rowconfigure( r, weight = 1 )
        for c in col:
            frame.columnconfigure( c, weight = 1 )     
    def say_hi(self):
        print("hi there, everyone!", self.text.get())
    def quit(self):
        self.root.destroy()
    def createXYScrolledText(self,master, **options):
        frame = Frame(master, bd=2, relief=SUNKEN)  #bd=brorderwidth
        #1x1 , distribute all empty spaces to row=0,col=0 ie text widgest
        self.conf(frame, range(1),range(1))
        xscrollbar = Scrollbar(frame, orient=HORIZONTAL)
        xscrollbar.grid(row=1, column=0, sticky=E+W)
        yscrollbar = Scrollbar(frame,orient=VERTICAL))
        yscrollbar.grid(row=0, column=1, sticky=N+S)
        options.update( dict(wrap=NONE, bd=0,xscrollcommand=xscrollbar.set,yscrollcommand=yscrollbar.set) )
        text = Text(frame, **options)
        text.grid(row=0, column=0, sticky=N+S+E+W)
        xscrollbar.config(command=text.xview)
        yscrollbar.config(command=text.yview)
        return frame,text

root = Tk()
app = App(root)
root.mainloop()