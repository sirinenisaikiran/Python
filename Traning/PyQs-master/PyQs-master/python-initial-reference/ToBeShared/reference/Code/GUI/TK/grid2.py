#6x6
#(Widget, start_row, start_col, row_span, column_span):
#1.("Button 0", 6, 0, 1, 1)
#2.("Button 1", 6, 1, 1, 1)
#3.("Button 2", 6, 2, 1, 1)
#4.("Button 3", 6, 3, 1, 1)
#5.("Button 4", 6, 4, 1, 1)
#6.("Frame1", 0, 0, 3, 2)
#7.("Frame2", 2, 0, 3, 2)
#8.("Frame3", 0, 3, 6, 3)

#Set all rows, column , rowconfigure/columnconfigure are must  


from tkinter import *

class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()
        self.master.title("Grid Manager")

        for r in range(6):
            self.master.rowconfigure(r, weight=1)    
        for c in range(5):
            self.master.columnconfigure(c, weight=1)
            Button(master, text="Button {0}".format(c)).grid(row=6,column=c,sticky=E+W)

        Frame1 = Frame(master, bg="red")
        Frame1.grid(row = 0, column = 0, rowspan = 3, columnspan = 2, sticky = W+E+N+S) 
        Frame2 = Frame(master, bg="blue")
        Frame2.grid(row = 3, column = 0, rowspan = 3, columnspan = 2, sticky = W+E+N+S)
        Frame3 = Frame(master, bg="green")
        Frame3.grid(row = 0, column = 2, rowspan = 6, columnspan = 3, sticky = W+E+N+S)

root = Tk()
root.geometry('400x400')
app = Application(master=root)
app.mainloop()


