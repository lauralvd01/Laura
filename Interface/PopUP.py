import tkinter as tk
from tkinter import ttk

class PopUP(tk.Tk):
    def __init__(self, title, msg, color="#000000"):
        super().__init__()

        self.geometry('800x600')
        self.resizable(1, 1)
        self.title(title)

        # UI options
        paddings = {'padx': 5, 'pady': 5}

        # configure the grid
        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=1)
        
        # display the message
        msg_label = ttk.Label(self, text=msg, foreground=color)
        msg_label.grid(column=0, row=0, sticky=tk.W, **paddings)
        
        # quit button
        quit_button = ttk.Button(self, text="OK", command=self.destroy)
        quit_button.grid(column=1, row=1, sticky=tk.E, **paddings)
        self.bind('<Return>',lambda event : self.destroy())

        # configure style
        self.style = ttk.Style(self)
        self.style.configure('TLabel', font=('Helvetica', 11))


#if __name__ == "__main__":
#    popUP = PopUP("Titre","ERROR Message","#FF0000")
#    popUP.mainloop()