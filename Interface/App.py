import tkinter as tk
from tkinter import ttk
import os
import pandas as pd
import subprocess
from PIL import ImageTk, Image
from tkinter import filedialog

from math import ceil
from functools import partial

import NewRender
import DeleteRender
import Config
import PopUP


def joinList(liste) :
    joinStr = ""
    for line in liste :
        print(type(line))
        joinStr += line.decode()
    return joinStr

def getRenderIndex(renderNames) :
    for i in renderNames.index :
        name = renderNames.iloc[i]
        number = int(name[7:])
        renderNames.iloc[i] = number
    renderNames.astype('int64')
    return renderNames

class App(tk.Tk) :
    
    def getRenders(self) :
        if self.SAVEFILE not in os.listdir(path=self.SAVEPATH) :
            renders = pd.DataFrame(data={'RenderName':[],'Username':[],'Ipv4':[],'Config':[],'ON':[]},dtype=str)
            renders.to_csv(self.SAVEPATH+os.path.sep+self.SAVEFILE,index=False)
        else :
            renders = pd.read_csv(self.SAVEPATH+os.path.sep+self.SAVEFILE)
        
        renders.loc[:,('Selected')] = [False for i in range(len(renders))]
        self.select_number.set(0)
        self.select_text.set(f"Sélection : {self.select_number.get()}")
        return renders
    
    def saveRenders(self,renders) :
        renders = renders.loc[:,('RenderName','Username','Ipv4','Config','ON')].copy()
        renders.sort_values(by="RenderName",axis=0,inplace=True,key=getRenderIndex)
        renders.to_csv(self.SAVEPATH+'\\'+self.SAVEFILE,index=False)
        return
    
    def ping(self,ip) :
        try :
            batch = subprocess.check_output('ping '+ip)
            lines = batch.split(b"\n")
            index = lines[2].find(b"octets")
            
            if index >= 0 :
                return True
            else :
                return False
        except :
            pass
        return False
    
    def getStatus(self) :
        for i in range(len(self.renders)) :
            if self.renders.loc[i,"Selected"] :
                ip = self.renders.loc[i,'Ipv4']
                status = self.ping(ip)
                self.renders.loc[i,'ON'] = 1 if status else 0
                print("ping "+ip+" : ","OK" if status else "pas de réponse")
        self.saveRenders(self.renders)
        self.displayRenders()
        return
    
    def displayRenders(self) :
        if self.first_time :
            self.on_frame = ttk.Frame(self,borderwidth=5,relief='solid')
            self.off_frame = ttk.Frame(self,borderwidth=5,relief='solid')
            self.on_frame.grid(column=0, columnspan=6, row=3, sticky=tk.N, padx=5)
            self.off_frame.grid(column=6, columnspan=5, row=3, sticky=tk.NW, padx=5)
            self.first_time = False
        else :
            for widget in self.on_frame.winfo_children() :
                widget.destroy()
            
            for widget in self.off_frame.winfo_children() :
                widget.destroy()
            
            self.renders = self.getRenders()
            
        # on frame
        self.on_frame.rowconfigure(0, weight=1)
        on_columns = 4
        for i in range(on_columns) :
            self.on_frame.columnconfigure(i, weight=1)
        
        on_N = len(self.renders.index[self.renders["Config"] == 1])
        on_N_lines = ceil(on_N/on_columns)
        for i in range(1,on_N_lines+1) :
            self.on_frame.rowconfigure(i, weight=1)
        
        on_label = ttk.Label(self.on_frame, text="Renders configurés ")
        on_label.grid(column=0, columnspan=2, row=0, sticky=tk.NW, padx=3, pady=7)
        
        self.all_on_on_check = tk.IntVar()
        self.all_on_on_check.set(0)
        all_on_on_button = ttk.Checkbutton(self.on_frame, text="Allumés", command=lambda:[self.selectOnlyConfigON() if self.all_on_on_check.get() else self.deselectOnlyConfigON()], variable=self.all_on_on_check)
        all_on_on_button.grid(column=2, row=0, padx=3, sticky=tk.E)
        
        self.all_on_off_check = tk.IntVar()
        self.all_on_off_check.set(0)
        all_on_off_button = ttk.Checkbutton(self.on_frame, text="Éteints", command=lambda:[self.selectOnlyConfigOFF() if self.all_on_off_check.get() else self.deselectOnlyConfigOFF()], variable=self.all_on_off_check)
        all_on_off_button.grid(column=3, row=0, padx=3, sticky=tk.W)
        
        self.all_on_text = tk.StringVar()
        self.all_on_text.set("Tous")
        self.all_on_check = tk.IntVar()
        self.all_on_check.set(0)
        all_on_button = ttk.Checkbutton(self.on_frame, textvariable=self.all_on_text, command=lambda:[self.selectAllConfig() if self.all_on_check.get() else self.deselectAllConfig()], variable=self.all_on_check)
        all_on_button.grid(column=4, row=0, padx=3)
        
    
        
        # off frame
        self.off_frame.rowconfigure(0, weight=1)
        off_columns = 3
        for i in range(off_columns) :
            self.off_frame.columnconfigure(i, weight=1)
        
        off_N = len(self.renders.index[self.renders["Config"] == 0])
        off_N_lines = ceil(off_N/off_columns)
        for i in range(1,off_N_lines+1) :
            self.off_frame.rowconfigure(i, weight=1)
        
        off_label = ttk.Label(self.off_frame, text="Renders non configurés")
        off_label.grid(column=0, columnspan=2, row=0, sticky=tk.NW, padx=3, pady=7)
        
        self.all_off_on_check = tk.IntVar()
        self.all_off_on_check.set(0)
        all_off_on_button = ttk.Checkbutton(self.off_frame, text="Allumés", command=lambda:[self.selectOnlyUnconfigON() if self.all_off_on_check.get() else self.deselectOnlyUnconfigON()], variable=self.all_off_on_check)
        all_off_on_button.grid(column=1, row=0, padx=3, sticky=tk.E)
        
        self.all_off_off_check = tk.IntVar()
        self.all_off_off_check.set(0)
        all_off_off_button = ttk.Checkbutton(self.off_frame, text="Éteints", command=lambda:[self.selectOnlyUnconfigOFF() if self.all_off_off_check.get() else self.deselectOnlyUnconfigOFF()], variable=self.all_off_off_check)
        all_off_off_button.grid(column=2, row=0, padx=3, sticky=tk.W)
        self.all_off_text = tk.StringVar()
        self.all_off_text.set("Tous")
        self.all_off_check = tk.IntVar()
        self.all_off_check.set(0)
        all_off_button = ttk.Checkbutton(self.off_frame, textvariable=self.all_off_text, command=lambda:[self.selectAllUnconfig() if self.all_off_check.get() else self.deselectAllUnconfig()], variable=self.all_off_check)
        all_off_button.grid(column=3, row=0, padx=3)
        
        # display buttons
        self.select_variables = [tk.IntVar() for i in range(len(self.renders))]
        i_on = 0
        i_off = 0
        for i in range(len(self.renders)) :
            self.select_variables[i].set(0)
            
            if self.renders.loc[i,"ON"] == 1 :
                color = self.green
            else :
                color = self.red
                
            if self.renders.loc[i,"Config"] == 1 :
                on_render_label = ttk.Checkbutton(self.on_frame, text=self.renders.loc[i,"RenderName"], command=partial(self.selectOne,i), variable=self.select_variables[i], image=color, compound='left')
                on_render_label.image = color
                on_render_label.grid(column=i_on%on_columns, row=i_on//on_columns+1, padx=10, pady=5, sticky=tk.E)
                i_on += 1
            else :
                off_render_label = ttk.Checkbutton(self.off_frame, text=self.renders.loc[i,"RenderName"], command=partial(self.selectOne,i), variable=self.select_variables[i], image=color, compound='left')
                off_render_label.image = color
                off_render_label.grid(column=i_off%off_columns, row=i_off//off_columns+1, padx=10, pady=5, sticky=tk.E)
                i_off += 1
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
        self.select_text.set(f"Sélection : {self.select_number.get()}")
        return
    
    def deselectAll(self) :
        for i in range(len(self.renders)) :
            self.selectOne(i,False)
        return
    
    def selectAllConfig(self) :
        for i in range(len(self.renders)) :
            if self.renders.loc[i,"Config"] == 1 :
                self.selectOne(i,True)
        self.all_on_check.set(1)
        self.all_on_text.set("Aucun")
        self.all_on_on_check.set(0)
        self.all_on_off_check.set(0)
        return
    
    def deselectAllConfig(self) :
        for i in range(len(self.renders)) :
            if self.renders.loc[i,"Config"] == 1 :
                self.selectOne(i,False)
        self.all_on_check.set(0)
        self.all_on_text.set("Tous")
        self.all_on_on_check.set(0)
        self.all_on_off_check.set(0)
        return
    
    def selectAllUnconfig(self) :
        for i in range(len(self.renders)) :
            if self.renders.loc[i,"Config"] == 0 :
                self.selectOne(i,True)
        self.all_off_check.set(1)
        self.all_off_text.set("Aucun")
        self.all_off_on_check.set(0)
        self.all_off_off_check.set(0)
        return
    
    def deselectAllUnconfig(self) :
        for i in range(len(self.renders)) :
            if self.renders.loc[i,"Config"] == 0 :
                self.selectOne(i,False)
        self.all_off_check.set(0)
        self.all_off_text.set("Tous")
        self.all_off_on_check.set(0)
        self.all_off_off_check.set(0)
        return
    
    def selectOnlyConfigON(self) :
        for i in range(len(self.renders)) :
            if self.renders.loc[i,"Config"] == 1 :
                if self.renders.loc[i,"ON"] == 1 :
                    self.selectOne(i,True)
                else :
                    self.selectOne(i,False)
        self.all_on_on_check.set(1)
        self.all_on_check.set(0)
        self.all_on_text.set("Tous")
        self.all_on_off_check.set(0)
        return
    
    def deselectOnlyConfigON(self) :
        for i in range(len(self.renders)) :
            if self.renders.loc[i,"Config"] == 1 and self.renders.loc[i,"ON"] == 1 :
                self.selectOne(i,False)
        self.all_on_on_check.set(0)
        self.all_on_check.set(0)
        self.all_on_text.set("Tous")
        return
    
    def selectOnlyUnconfigON(self) :
        for i in range(len(self.renders)) :
            if self.renders.loc[i,"Config"] == 0 :
                if self.renders.loc[i,"ON"] == 1 :
                    self.selectOne(i,True)
                else :
                    self.selectOne(i,False)
        self.all_off_on_check.set(1)
        self.all_off_check.set(0)
        self.all_off_text.set("Tous")
        self.all_off_off_check.set(0)
        return
    
    def deselectOnlyUnconfigON(self) :
        for i in range(len(self.renders)) :
            if self.renders.loc[i,"Config"] == 0 and self.renders.loc[i,"ON"] == 1 :
                self.selectOne(i,False)
        self.all_off_on_check.set(0)
        self.all_off_check.set(0)
        self.all_off_text.set("Tous")
        return
    
    def selectOnlyConfigOFF(self) :
        for i in range(len(self.renders)) :
            if self.renders.loc[i,"Config"] == 1 :
                if self.renders.loc[i,"ON"] == 0 :
                    self.selectOne(i,True)
                else :
                    self.selectOne(i,False)
        self.all_on_off_check.set(1)
        self.all_on_check.set(0)
        self.all_on_text.set("Tous")
        self.all_on_on_check.set(0)
        return
    
    def deselectOnlyConfigOFF(self) :
        for i in range(len(self.renders)) :
            if self.renders.loc[i,"Config"] == 1 and self.renders.loc[i,"ON"] == 0 :
                self.selectOne(i,False)
        self.all_on_off_check.set(0)
        self.all_on_check.set(0)
        self.all_on_text.set("Tous")
        return
    
    def selectOnlyUnconfigOFF(self) :
        for i in range(len(self.renders)) :
            if self.renders.loc[i,"Config"] == 0 :
                if self.renders.loc[i,"ON"] == 0 :
                    self.selectOne(i,True)
                else :
                    self.selectOne(i,False)
        self.all_off_off_check.set(1)
        self.all_off_check.set(0)
        self.all_off_text.set("Tous")
        self.all_off_on_check.set(0)
        return
    
    def deselectOnlyUnconfigOFF(self) :
        for i in range(len(self.renders)) :
            if self.renders.loc[i,"Config"] == 0 and self.renders.loc[i,"ON"] == 0 :
                self.selectOne(i,False)
        self.all_off_off_check.set(0)
        self.all_off_check.set(0)
        self.all_off_text.set("Tous")
        return
 
 
    def runProcess(self,renderName,command) :
        index = self.renders.index[self.renders['RenderName'] == renderName][0]
        if self.renders.loc[index,'ON'] == 1 :
            if self.ping(self.renders.loc[index,'Ipv4']) :
                try :
                    batch = subprocess.Popen([command], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    result = batch.stdout.readlines()
                    PopUP.PopUP("Succès",renderName + " : commande effectuée avec succès\n" + joinList(result))
                except :
                    error = joinList(batch.stderr.readlines())
                    PopUP.PopUP("Erreur "+renderName,"ERREUR : " + error,"#FF0000")
            else :
                PopUP.PopUP("Erreur "+renderName,"ERREUR : le render est éteint, ou ne répond pas au ping.","#FF0000")
        else :
            PopUP.PopUP("Erreur "+renderName,"Le render "+renderName+" est considéré éteint. Allumer le render puis actualiser les statuts.","#FF0000")
        return
    
    def commandRender(self, renderName,commandChoice) :
        path = self.SAVEPATH + os.path.sep + renderName
           
        command = f"{path}_{commandChoice}.bat"
        print(command)
        if os.path.isfile(command)  :
            self.runProcess(renderName,command)
        else :
            PopUP.PopUP("Erreur "+renderName,renderName+" pas encore configuré !","#FF0000")
            print("Fichier inexistant")
        return
    
    def commandAllRenders(self,commandChoice) :
        if self.select_number.get() + self.select_number.get() == 0 :
            PopUP.PopUP("Erreur","Aucun Render sélectionné")
        else :
            
            if commandChoice == 'getStatus' :
                self.getStatus()
            else :  
                selected = []
                for i in range(len(self.renders)) :
                    if self.renders.loc[i,"Selected"] :
                        selected.append(self.renders.loc[i,"RenderName"])
                
                for renderName in selected :
                    if commandChoice == 'config' :
                        Config.Config(self,self.SAVEPATH,self.SAVEFILE,self.CONFIGFILE,self.STOPFILE,self.RESTARTFILE,renderName)
                    else :
                        self.commandRender(renderName,commandChoice)
                        self.getStatus()
            self.deselectAll()
            print("End of commands")
        return
    
    def getConfig(self) :
        path = filedialog.askdirectory()
        if path != "" : 
            # path = os.environ['USERPROFILE']+os.path.sep+'Downloads'
            if 'config.csv' not in os.listdir(path=path) :
                PopUP.PopUP("ERROR : échec de l'importation","Il n'y a pas de fichier config.csv dans le dossier sélectionné :\n"+path)
            else :
                renders = self.getRenders()
                renders = renders.loc[:,('RenderName','Username','Ipv4','Config','ON')].copy()
                new_renders = pd.read_csv(path+os.path.sep+'config.csv')
                new_renders.loc[:,'ON'] = [0 for i in range(len(new_renders))]
                concat_renders = pd.concat([renders,new_renders])
                concat_renders = concat_renders.drop_duplicates(subset=['RenderName','Username','Ipv4'],keep='first')
                concat_renders.sort_values(by="RenderName",axis=0,inplace=True,key=getRenderIndex)
                concat_renders.to_csv(self.SAVEPATH+os.path.sep+self.SAVEFILE,index=False)
                
                self.displayRenders()
                PopUP.PopUP("Succès","Le fichier config.csv a été importé avec succès.")
        return
    
    def saveConfig(self) :
        path = filedialog.askdirectory()
        if path != "" : 
            # path = os.environ['USERPROFILE']+os.path.sep+'Downloads'
            if 'config.csv' in os.listdir(path) :
                os.remove(path+os.path.sep+'config.csv')
            self.saveRenders(self.renders)
            renders = self.getRenders()
            renders = renders.loc[:,('RenderName','Username','Ipv4','Config')].copy()
            renders.loc[:,"Config"] = [0 for i in range(len(renders))]
            renders.to_csv(path+os.path.sep+'config.csv',index=False)
            PopUP.PopUP("Succès","La configuration a bien été exportée dans le fichier suivant :\n"+path+os.path.sep+'config.csv')
        return
    
    
    def __init__(self, *args, **kwargs) :
        self.SAVEPATH = '.'+os.path.sep+'_internal'+os.path.sep+'Files'
        self.SAVEFILE = 'saveRenders.csv'
        self.CONFIGFILE = 'connexion_par_cle.bat'
        self.STOPFILE = 'arret_par_cle.bat'
        self.RESTARTFILE = 'restart_par_cle.bat'
        
        tk.Tk.__init__(self, *args, **kwargs)
        
        # Title of the application
        self.wm_title("Interface de commande des Renders")
        
        self.geometry('1200x800')
        self.resizable(1, 1)
        
        # configure the grid
        for i in range(10) :
            self.columnconfigure(i, weight=1)
        for i in range(5) :
            self.rowconfigure(i, weight=1)
        self.rowconfigure(4, weight=3)
        self.rowconfigure(5, weight=1)
        
        # get renders
        self.select_number = tk.IntVar()
        self.select_number.set(0)
        self.select_number = tk.IntVar()
        self.select_number.set(0)
        self.select_text = tk.StringVar()
        self.select_text.set(f"Sélection : {self.select_number.get()+self.select_number.get()}")
        self.renders = self.getRenders()
        
        # import, export, new and delete buttons
        import_button = ttk.Button(self, text="Importer", command=self.getConfig)
        import_button.grid(column=1, row=1, sticky=tk.E, padx=5)
        export_button = ttk.Button(self, text="Exporter", command=self.saveConfig)
        export_button.grid(column=2, row=1, sticky=tk.W, padx=5)
        new_button = ttk.Button(self, text="Nouveau Render", command=partial(NewRender.NewRender,self,self.SAVEPATH,self.SAVEFILE))
        new_button.grid(column=3, columnspan=3, row=1, sticky=tk.EW, padx=5)
        delete_button = ttk.Button(self, text="Supprimer des Renders", command=partial(DeleteRender.DeleteRender,self,self.SAVEPATH,self.SAVEFILE))
        delete_button.grid(column=6, columnspan=3, row=1, sticky=tk.EW, padx=5)
        
        # selection
        selection_label = ttk.Label(self, textvariable=self.select_text)
        selection_label.grid(column=1, columnspan=3, row=2, sticky=tk.W, padx=5)
        
        # status
        image_red=Image.open('_internal\Files\\red.png')
        self.red = ImageTk.PhotoImage(image_red.resize((20,10)))
        self.red.height=10
        self.red.width=10
        image_green=Image.open('_internal\Files\\green.png')
        self.green = ImageTk.PhotoImage(image_green.resize((20,10)))
        self.green.height=10
        self.green.width=10
        self.status_button = ttk.Button(self, text="ACTUALISER",command=partial(self.commandAllRenders,'getStatus'))
        self.status_button.grid(column=2, columnspan=1, sticky=tk.EW, row=2, padx=2)
        
        # actions
        stop_button = ttk.Button(self, text="ARRÊT",command=partial(self.commandAllRenders,'stop'))
        stop_button.grid(column=3, columnspan=2, row=2, sticky=tk.E, padx=2)
        restart_button = ttk.Button(self, text="RESTART",command=partial(self.commandAllRenders,'restart'))
        restart_button.grid(column=5, columnspan=2, row=2, sticky=tk.EW, padx=2)
        config_button = ttk.Button(self, text="PARAMÈTRES",command=partial(self.commandAllRenders,'config'))
        config_button.grid(column=7, columnspan=2, row=2, sticky=tk.EW, padx=2)
        
        # render categorie frames
        self.first_time = True
        self.displayRenders()
        
        def quit() :
            self.renders['ON'] = [0 for i in range(len(self.renders))]
            self.saveRenders(self.renders)
            self.destroy()
        
        # quit button
        quit_button = ttk.Button(self, text="Quitter", command=quit)
        quit_button.grid(column=8, columnspan=2, row=5)

        # configure style
        self.style = ttk.Style(self)
        self.style.configure('TLabel', font=('Helvetica', 12))
        self.style.configure('TButton', font=('Helvetica', 12))
        self.style.configure('TCheckbutton', font=('Helvetica', 12))


if __name__ == "__main__":
    appRoot = App()
    appRoot.mainloop()