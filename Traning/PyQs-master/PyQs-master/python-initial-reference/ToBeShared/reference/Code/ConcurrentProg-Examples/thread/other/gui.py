from tkinter import *
import tkinter.scrolledtext as tkst
from tkinter import filedialog
from tkinter import messagebox

from functools import partial 
import os,subprocess,time,sys

MOCK = FALSE
DEBUG = FALSE 

def printIfDebug(*args, **kargs):
    if DEBUG:
        print(*args, **kargs)
        

class App(Frame):
    def __init__( self , master=None,after_ms=10):
        super().__init__(master)
        self.master.title( "Grid Demo" )
        #one row for Frame parent 
        self.master.rowconfigure( 0, weight = 1 )
        self.master.columnconfigure( 0, weight = 1 )
        
        
        #6x6 for Frame 
        row,col=6,6
        for i in range(row):
            self.rowconfigure( i, weight = 1 )
        for i in range(col):
            self.columnconfigure( i, weight = 1 )
        #for Frame 
        self.grid(row=0,column=0, sticky = W+E+N+S )
        
        #create widgets 
        self.vInput = StringVar()
        self.input = Entry( self ,textvariable=self.vInput)
        self.input.grid( row=0,column=0, rowspan=1, columnspan=5, sticky = W+E+N+S )
        self.vInput.set("http://")
        self.input.bind("<Return>", lambda event: self.startProcess())
        #copy and paste is default for Entry
        #self.input.bind("<Control-C>", lambda event: self.handleControl(1))
        #self.input.bind("<Control-V>", lambda event: self.handleControl(2))

        #create pid 
        self.pid = 0
        self.get = Button( self, text = "GET" )
        self.get["command"] = self.startProcess
        self.get.grid( row = 0, column = 5, rowspan=1, columnspan=1, sticky = W+E+N+S )
        
        self.vOutput = ""
        self.output = tkst.ScrolledText(self,  wrap=WORD, relief=SUNKEN, bg="#EFEFEF", font=("Helvetica", 11),fg="red")
        self.output.grid( row = 1, column = 0, rowspan = 5, columnspan=6, sticky = W+E+N+S )
        #schedule callback
        self.master.after(after_ms, self.UpdateOutput, after_ms)
        
        #Add menu 
        menubar = Menu(self)
        # create a pulldown menu, and add it to the menu bar
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Save", command=self.save)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=root.destroy)
        menubar.add_cascade(label="File", menu=filemenu)
        # display the menu
        self.master.config(menu=menubar)
    
    def handleControl(self, which):
        if which == 1:  #c 
            self.master.withdraw()
            self.master.clipboard_clear()
            self.master.clipboard_append(self.vInput.get())
            self.master.update() 
        else :     # V 
            clipboard = self.master.clipboard_get()
            self.vInput.set(clipboard)
        
    def UpdateOutput(self, after_ms):
        self.master.after(after_ms, self.UpdateOutput, after_ms)
        printIfDebug("UpdateOutput", self.pid, file=sys.stderr)
        if not self.pid:
            return
        self.vOutput += self.getOutput()
        self.output.config(state=NORMAL)
        self.output.delete('1.0',END)
        self.output.insert(INSERT, self.vOutput)
        self.output.see(END)
        self.output.config(state=DISABLED)
        
    def reset(self):
        self.pid = 0
        self.get["text"] = "GET"
        self.input.config(state=NORMAL)        
    
    def getOutput(self):      
        #printIfDebug("getOutput", file=sys.stderr)
        output = ""
        if self.pid:
            if self.pid.poll() == None: #still running 
                output = self.pid.stdout.readline()
            else : #ended 
                output = self.pid.stdout.read()  #read fully 
                self.reset()
        printIfDebug("getOutput<",output,">",sep="",file=sys.stderr)
        return output        
        
    def checkURL(self):
        from urllib.parse import urlparse
        result = urlparse(self.vInput.get())
        check = all([result.scheme, result.netloc, result.path]) if not MOCK else True
        return check 
        
    def getProcessName(self):
        if MOCK:
            name = [self.vInput.get()]  #
        else:
            name =["python", "recurseDown_t.py", self.vInput.get()]
        return name
        
    def startProcess(self):
        if not self.checkURL():
            messagebox.showinfo("URL ERORR","Can you check the correctness of URL?")
            return  
        if not self.pid :
            self.get["text"] = "Cancel"
            self.input.config(state=DISABLED)            
            try:
                name = self.getProcessName()
                printIfDebug("Command:", name, file=sys.stderr)
                #stderr=subprocess.STDOUT
                self.pid = subprocess.Popen(name, stdout=subprocess.PIPE, bufsize=1, universal_newlines=True ) #read line by line
                #empty now 
                self.vOutput = ""
                #printIfDebug("PID", self.pid, file=sys.stderr)
            except Exception as ex:
                messagebox.showinfo("Execution ERORR",str(ex))
                self.pid = 0                
        else:
            self.pid.kill() if self.pid else ""
            #sleep some time 
            time.sleep(1)
            self.reset()      
        return TRUE   
        
    def save(self):
        my_filetypes = [('all files', '.*'), ('text files', '.txt')]
        filename = filedialog.asksaveasfilename(parent=self,
                                      initialdir=os.getcwd(),
                                      title="Please select a file name for saving:",
                                      filetypes=my_filetypes)
        with open(filename, "wt") as f:
            f.write(self.vOutput)
        printIfDebug("saved",filename, file=sys.stderr)
        

root = Tk()
root.geometry('700x400')
app = App(master=root)
app.mainloop()