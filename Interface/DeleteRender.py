import tkinter as tk
from tkinter import ttk
import os
import pandas as pd

from functools import partial
from math import ceil

import PopUP


class DeleteRender(tk.Toplevel):
    
    def getRenders(self) :
        if self.SAVEFILE not in os.listdir(path=self.SAVEPATH) :
            renders = pd.DataFrame(data={'RenderName':[],'Username':[],'Ipv4':[], 'Config':[],'ON':[]},dtype=str)
            renders.to_csv(self.SAVEPATH+os.path.sep+self.SAVEFILE,index=False)
        else :
            renders = pd.read_csv(self.SAVEPATH+os.path.sep+self.SAVEFILE)
            
        renders['Selected'] = [False for i in range(len(renders))]
        self.select_number.set(0)
        self.select_text.set(f"Supprimer : {self.select_number.get()}")
        return renders
    
    def displayRenders(self) :
        if self.first_time :
            self.frame = ttk.Frame(self,borderwidth=5,relief='solid')
            self.frame.grid(column=0, columnspan=7, row=1, padx=5)
            self.first_time = False
        
        else :
            for widget in self.frame.winfo_children() :
                widget.destroy()
            
            self.renders = self.getRenders()
            
        # renders frame
        renders_columns = 3
        for i in range(renders_columns) :
            self.frame.columnconfigure(i, weight=1)
            
        renders_N = len(self.renders)
            
        renders_N_lines = ceil(renders_N/renders_columns)
        for i in range(renders_N_lines+1) :
            self.frame.rowconfigure(i, weight=1)
            
        self.select_variables = [tk.IntVar() for i in range(renders_N)]
        for i in range(renders_N) :
            self.select_variables[i].set(0)
            render_label = ttk.Checkbutton(self.frame, text=self.renders.loc[i,"RenderName"], command=partial(self.selectOne,i), variable=self.select_variables[i])
            render_label.grid(column=i%renders_columns, row=i//renders_columns, padx=10, pady=5)
        
        return
    
    def selectAll(self) :
        if self.all_check.get() :
            for i in range(len(self.renders)) :
                self.selectOne(i,True)
            self.all_text.set("Aucun")
        else :
            for i in range(len(self.renders)) :
                self.selectOne(i,False)
            self.all_text.set("Tous")
        return
    
    def selectOne(self,i,forced_value=None) :
        if self.renders.loc[i,"Selected"] :
            if forced_value is not None and forced_value :
                pass
            else :
                self.renders.loc[i,"Selected"] = False
                self.select_variables[i].set(0)
                self.select_number.set(self.select_number.get()-1)
        else :
            if forced_value is not None and (not forced_value) :
                pass
            else :
                self.renders.loc[i,"Selected"] = True
                self.select_variables[i].set(1)
                self.select_number.set(self.select_number.get()+1)
        self.select_text.set(f"Supprimer : {self.select_number.get()}")
        return
    
    def deleteRender(self, renderName) :
        renders_to_delete = self.renders.index[self.renders.loc[:,'RenderName'] == renderName]
        
        if len(renders_to_delete) > 0 :
            self.renders = self.renders.drop(renders_to_delete,axis=0,inplace=True)
            self.root.saveRenders(self.renders)
            
            # remove bat files
            try :
                path = self.SAVEPATH + os.path.sep + renderName
                command_files = [f"{path}_{commandChoice}.bat" for commandChoice in ['stop', 'restart', 'config']]
                for file in command_files :
                    os.remove(file)
            except :
                pass
            finally :
                self.root.displayRenders()
                self.displayRenders()
                
            PopUP.PopUP("Succès",f"{renderName} a été supprimé")
        else :
            PopUP.PopUP("Erreur "+renderName,"Erreur de suppression de "+renderName,"#FF0000")
        return
    
    def commandAllRenders(self) :
        if self.select_number == 0 :
            PopUP.PopUP("Erreur","Aucun Render sélectionné")
        else :
            selected = []
            for i in range(len(self.renders)) :
                if self.renders.loc[i,"Selected"] :
                    selected.append(self.renders.loc[i,"RenderName"])
            for renderName in selected :
                self.deleteRender(renderName)
        return
    
    
    def __init__(self,root,savepath,savefile):
        super().__init__()

        self.root = root
        self.SAVEPATH = savepath
        self.SAVEFILE = savefile

        self.geometry('700x800')
        self.resizable(1, 1)
        self.title('Supprimer des Renders')

        # configure the grid
        for i in range(7) :
            self.columnconfigure(i, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=3)
        self.rowconfigure(2, weight=1)
        
        # get renders
        self.select_number = tk.IntVar()
        self.select_number.set(0)
        self.select_text = tk.StringVar()
        self.select_text.set(f"Supprimer : {self.select_number.get()}")
        self.renders = self.getRenders()
        
        # selection
        selection_label = ttk.Label(self, textvariable=self.select_text)
        selection_label.grid(column=2, columnspan=2, row=0, sticky=tk.SW, padx=5)
        
        # all button
        self.all_text = tk.StringVar()
        self.all_text.set("Tous")
        self.all_check = tk.IntVar()
        self.all_check.set(0)
        all_button = ttk.Checkbutton(self, textvariable=self.all_text, command=self.selectAll, variable=self.all_check)
        all_button.grid(column=5, row=0, sticky=tk.S, padx=3)

        # liste des renders enregistrés
        self.first_time = True
        self.displayRenders()
        
        # delete button
        delete_button = ttk.Button(self, text="Supprimer", command=self.commandAllRenders)
        delete_button.grid(column=5, row=2, sticky=tk.E)
        
        # quit button
        quit_button = ttk.Button(self, text="Annuler", command=self.destroy)
        quit_button.grid(column=6, row=2)

        # configure style
        self.style = ttk.Style(self)
        self.style.configure('TLabel', font=('Helvetica', 12))
        self.style.configure('TButton', font=('Helvetica', 12))
        self.style.configure('TCheckbutton', font=('Helvetica', 12))


#if __name__ == "__main__":
#    import AppRoot
#    path = os.getcwd() + os.path.sep + 'Interface' + os.path.sep + 'Files'
#    file = 'saveRenders.csv'
#    root = AppRoot.AppRoot()
#    deleteRender = DeleteRender(root,path,file)
#    deleteRender.mainloop()