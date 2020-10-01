from tkinter import *
import tkinter.scrolledtext as tkst


def createB(master, n=5, row=0,sticky=N+W+E):
    for c in range(n):
        Button(master, text="Button {0}".format(c)).grid(row=row,column=c,sticky=sticky)

def conf(master, row=1,column=1):
    for r in range(row):
        master.rowconfigure(r, weight=1)    
    for c in range(column):
        master.columnconfigure(c, weight=1)

root = Tk()
root.geometry('900x600+0+0')

master = root 
conf(master,8,5)

Frame1 = Frame(master, bg="red")
Frame1.grid(row = 0, column = 0, rowspan = 3, columnspan = 2, sticky = W+E+N+S) 
Frame2 = Frame(master, bg="blue")
Frame2.grid(row = 3, column = 0, rowspan = 3, columnspan = 2, sticky = W+E+N+S)

Frame3 = Frame(master, bg="green")
Frame3.grid(row = 0, column = 2, rowspan = 6, columnspan = 3, sticky = W+E+N+S)
conf(Frame3,2,5)#child 1x5
createB(Frame3, 5,sticky=N+W+E+S)

#Add one scrolledText for displaying 
output = tkst.ScrolledText(Frame3,  wrap=WORD, relief=SUNKEN, font=("Helvetica", 11),fg="black", bg='misty rose',width=50)
output.grid( row = 1, column = 2, columnspan=3,sticky = N+E+S )
#schedule callback
def updateOutput():
    output.insert(INSERT, ("Scrolled text "*3+"\n")*3)
    root.after(1000, updateOutput)
    
root.after(1000, updateOutput)


#
Frame4 = Frame(master, bg="violet")
Frame4.grid(row = 6, column = 0, rowspan = 2, columnspan = 5, sticky = W+E+N+S)
conf(Frame4,2,5)  #child 2x5



Frame5 = Frame(Frame4, bg="red")
Frame5.grid(row = 0, column = 0, rowspan = 2, columnspan = 3, sticky = W+E+N+S)
conf(Frame5,1,3)#child 1x3
createB(Frame5, 3)

Frame6 = Frame(Frame4,bg="violet")
Frame6.grid(row = 0, column = 3, rowspan = 2, columnspan = 2, sticky = W+E+N+S)
conf(Frame6,1,3)#child 1x3
createB(Frame6, 3)

#Update all and call minsize
#note update must not be called inside command handler 
root.update()
# now root.geometry() returns valid size/placement
#root.minsize(root.winfo_width(), root.winfo_height())
root.mainloop()
