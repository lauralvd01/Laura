import tkinter as tk
from tkinter import ttk
import os
import pandas as pd

import PopUP

def getRenderIndex(renderNames) :
    for i in renderNames.index :
        name = renderNames.iloc[i]
        number = int(name[7:])
        renderNames.iloc[i] = number
    renderNames.astype('int64')
    return renderNames

class NewRender(tk.Toplevel):
    
    def getRenders(self) :
        if self.SAVEFILE not in os.listdir(path=self.SAVEPATH) :
            renders = pd.DataFrame(data={'RenderName':[],'Username':[],'Ipv4':[], 'Config':[]},dtype=str)
            renders.to_csv(self.SAVEPATH+os.path.sep+self.SAVEFILE,index=False)
        else :
            renders = pd.read_csv(self.SAVEPATH+os.path.sep+self.SAVEFILE)
        return renders
    
    def add(self) :
        renderName = self.render_entry.get().strip("\t").strip("\n")
        username = self.user_entry.get().strip("\t").strip("\n")
        ip = self.ip_entry.get().strip("\t").strip("\n")
        
        if "Render "+renderName not in [self.renders.loc[i,"RenderName"] for i in range(len(self.renders))] and renderName != "" and username != "" and ip != "" and ip != "render-" :
            #Adding to the csv
            N = len(self.renders.index)
            self.renders.loc[N] = ["Render "+renderName,username,ip,0]
            self.renders.sort_values(by="RenderName",axis=0,inplace=True,key=getRenderIndex)
            self.renders.to_csv(self.SAVEPATH+'\\'+self.SAVEFILE,index=False)
            
            #Update renders showed in the app
            self.root.displayRenders()
            
            #Clear entries
            self.render_entry.delete(0,len(renderName))
            self.user_entry.delete(0,len(username))
            self.ip_entry.delete(0,len(ip))
            self.user_entry.insert(0,("backburner"))
            self.ip_entry.insert(0,("render-"))
            
            PopUP.PopUP("Succès !",f"Render {renderName} : {username}@{ip} enregistré.\nIl faudra le configurer pour pouvoir l'utiliser.")
        else :
            PopUP.PopUP("Erreur","Il faut remplir tous les champs et donner un nom de Render qui n'existe pas encore.")
        return
    
    def __init__(self,root,savepath,savefile):
        super().__init__()
        
        self.root = root
        self.SAVEPATH = savepath
        self.SAVEFILE = savefile
        self.renders = self.getRenders()

        self.geometry('450x180')
        self.resizable(0, 0)
        self.title('Nouveau Render')

        # UI options
        paddings = {'padx': 5, 'pady': 5}
        entry_font = {'font': ('Helvetica', 11)}

        # configure the grid
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        
        # render n°
        render_label = ttk.Label(self, text="N° du Render :")
        render_label.grid(column=0, row=0, sticky=tk.W, **paddings)
        
        renderName_label = ttk.Label(self, text="Render      ")
        renderName_label.grid(column=1, row=0, sticky=tk.W)

        self.render_entry = ttk.Entry(self, **entry_font)
        self.render_entry.grid(column=2, row=0, columnspan=1, sticky=tk.E, **paddings)
        self.render_entry.focus()

        # user
        user_label = ttk.Label(self, text="Nom de l'utilisateur :     ")
        user_label.grid(column=0, row=2, sticky=tk.W, **paddings)

        self.user_entry = ttk.Entry(self, **entry_font)
        self.user_entry.insert(0,("backburner"))
        self.user_entry.grid(column=1, row=2, columnspan=2, sticky=tk.EW, **paddings)
        
        # ip
        ip_label = ttk.Label(self, text="Adresse ip :")
        ip_label.grid(column=0, row=3, sticky=tk.W, **paddings)

        self.ip_entry = ttk.Entry(self, **entry_font)
        self.ip_entry.insert(0,("render-"))
        self.ip_entry.grid(column=1, row=3, columnspan=2, sticky=tk.EW, **paddings)
        

        # add button
        add_button = ttk.Button(self, text="Ajouter", command=self.add)
        add_button.grid(column=2, row=4, sticky=tk.E, **paddings)
        self.bind('<Return>',lambda event : self.add())
        
        # quit button
        quit_button = ttk.Button(self, text="Annuler", command=self.destroy)
        quit_button.grid(column=3, row=4, sticky=tk.EW, **paddings)

        # configure style
        self.style = ttk.Style(self)
        self.style.configure('TLabel', font=('Helvetica', 11))
        self.style.configure('TButton', font=('Helvetica', 11))


#if __name__ == "__main__":
#    import AppRoot
#    path = os.getcwd() + os.path.sep + 'Interface' + os.path.sep + 'Files'
#    file = 'saveRenders.csv'
#    newRender = NewRender(AppRoot.AppRoot(),path,file)
#    newRender.mainloop()