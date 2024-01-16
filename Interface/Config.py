import tkinter as tk
from tkinter import ttk
import os
import pandas as pd
import subprocess

import PopUP

def joinList(liste) :
    joinStr = ""
    for line in liste :
        joinStr += line.decode()
    return joinStr

def getRenderIndex(renderNames) :
    for i in renderNames.index :
        name = renderNames.iloc[i]
        number = int(name[7:])
        renderNames.iloc[i] = number
    renderNames.astype('int64')
    return renderNames

class Config(tk.Toplevel):
    
    def getRenders(self) :
        if self.SAVEFILE not in os.listdir(path=self.SAVEPATH) :
            renders = pd.DataFrame(data={'RenderName':[],'Username':[],'Ipv4':[],'Config':[]},dtype=str)
            renders.to_csv(self.SAVEPATH+os.path.sep+self.SAVEFILE,index=False)
        else :
            renders = pd.read_csv(self.SAVEPATH+os.path.sep+self.SAVEFILE)
        return renders
    
    def displayRender(self, renderName) :
        if not self.firstime :
            self.renderName_label.grid_forget()
            self.user_label.grid_forget()
            self.ip_label.grid_forget()
        
        self.render = {}
        for i in range(len(self.renders)) :
            if self.renders.loc[i,"RenderName"] == renderName :
                self.render = {'Index': i, 'RenderName': self.renders.loc[i,"RenderName"],'Username': self.renders.loc[i,"Username"],'Ipv4': self.renders.loc[i,"Ipv4"], 'Config': self.renders.loc[i,"Config"]}

        assert(len(self.render) > 0)
        self.renderName_label = ttk.Label(self, text=self.render['RenderName'])
        self.renderName_label.grid(column=3, row=0, sticky=tk.E)
        self.user_label = ttk.Label(self, text=self.render['Username'])
        self.user_label.grid(column=3, row=2, sticky=tk.E)
        self.ip_label = ttk.Label(self, text=self.render['Ipv4'])
        self.ip_label.grid(column=3, row=3, sticky=tk.E)
        
        self.firstime = False
        return
            
    def modifyRender(self) :
        num = self.num_entry.get()
        username = self.user_entry.get()
        ip = self.ip_entry.get()
        
        modif = True
        
        if  not (num == "" and username == "" and ip == "") :
            
            if modif and num != "" :
                if "Render "+num not in [self.renders.loc[i,"RenderName"] for i in range(len(self.renders))] or "Render "+num == self.render['RenderName']:
                    self.renders.loc[self.render['Index'],"RenderName"] = "Render "+num
                else :
                    modif = False
                    PopUP.PopUP("Erreur","Render déjà existant avec ce n°")
            
            if modif and username != "" :
                self.renders.loc[self.render['Index'],"Username"] = username
            
            if modif and ip != "" :
                self.renders.loc[self.render['Index'],"Ipv4"] = ip
            
            if modif :
                self.renders.loc[self.render['Index'],"Config"] = 0
                
                self.renders.sort_values(by="RenderName",axis=0,inplace=True,key=getRenderIndex)
                self.renders.to_csv(self.SAVEPATH+os.path.sep+self.SAVEFILE,index=False)
                
                #Update renders showed in the app
                self.renders = self.getRenders()
                self.displayRender(self.render['RenderName'] if num == "" else "Render "+num)
                self.root.displayRenders()
                
                #Clear entries
                self.num_entry.delete(0,len(num))
                self.user_entry.delete(0,len(username))
                self.ip_entry.delete(0,len(ip))
                
                # remove bat files
                try :
                    path = self.SAVEPATH + os.path.sep + self.render['RenderName']
                    command_files = [f"{path}_{commandChoice}.bat" for commandChoice in ['stop', 'restart', 'config']]
                    for file in command_files :
                        os.remove(file)
                except :
                    pass
                finally :
                    PopUP.PopUP("Succès !",f"Render supprimé et \n{self.render['RenderName']} : {self.render['Username']}@{self.render['Ipv4']} enregistré.\nIl faudra le configurer pour pouvoir l'utiliser.")
                
        else :
            PopUP.PopUP("Erreur","Il faut remplir au moins un champ.")
        return
    
    def createBat(self) :
        #Creating config.bat file
        source_config_file = open(self.SAVEPATH+os.path.sep+self.CONFIGFILE,'r')
        i = 0
        new = ""
        for line in source_config_file :
            if i == 12 :
                new_line = "set name=" + self.render['Username'] +'\n'
            elif i == 13 :
                new_line = "set ip=" + self.render['Ipv4'] +'\n'
            else :
                new_line = line
            new += new_line
            i += 1
        source_config_file.close()
            
        config_file = open(self.SAVEPATH+os.path.sep+self.render['RenderName']+'_config.bat','w')
        config_file.write(new)
        config_file.close()
            
        #Creating stop.bat file
        source_stop_file = open(self.SAVEPATH+os.path.sep+self.STOPFILE,'r')
        i = 0
        new = ""
        for line in source_stop_file :
            if i == 6 :
                new_line = "set name=" + self.render['Username'] +'\n'
            elif i == 7 :
                new_line = "set ip=" + self.render['Ipv4'] +'\n'
            else :
                new_line = line
            new += new_line
            i += 1
        source_stop_file.close()
            
        stop_file = open(self.SAVEPATH+os.path.sep+self.render['RenderName']+'_stop.bat','w')
        stop_file.write(new)
        stop_file.close()
            
        #Creating restart.bat file
        source_restart_file = open(self.SAVEPATH+os.path.sep+self.RESTARTFILE,'r')
        i = 0
        new = ""
        for line in source_restart_file :
            if i == 6 :
                new_line = "set name=" + self.render['Username'] +'\n'
            elif i == 7 :
                new_line = "set ip=" + self.render['Ipv4'] +'\n'
            else :
                new_line = line
            new += new_line
            i += 1
        source_restart_file.close()
            
        restart_file = open(self.SAVEPATH+os.path.sep+self.render['RenderName']+'_restart.bat','w')
        restart_file.write(new)
        restart_file.close()
        return
    
    def config(self) :
        if self.render['Config'] == 1 :
            PopUP.PopUP("Erreur","Render déjà configuré")
        else :
            self.createBat()
            
            path = self.SAVEPATH + os.path.sep + self.render['RenderName']
            command = f"{path}_config.bat"
            try :
                batch = subprocess.Popen([command], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                result = batch.stdout.readlines()
                if result == []:
                    error = joinList(batch.stderr.readlines())
                    PopUP.PopUP("Erreur "+self.render['RenderName'],"ERREUR : " + error,"#FF0000")
                else :
                    PopUP.PopUP("Succès",self.render['RenderName'] + " :\n" + joinList(result))
            except :
                PopUP.PopUP("Erreur "+self.render['RenderName'],self.render['RenderName']+" mal configuré !","#FF0000")
            
            self.render['Config'] == 1
            self.renders.loc[self.render['Index'],"Config"] = 1
            self.renders.to_csv(self.SAVEPATH+os.path.sep+self.SAVEFILE,index=False)
            self.root.displayRenders()
        return
    
    def __init__(self,root,savepath,savefile,configfile,stopfile,restartfile,renderName):
        super().__init__()
        
        self.root = root
        self.SAVEPATH = savepath
        self.SAVEFILE = savefile
        self.CONFIGFILE = configfile
        self.STOPFILE = stopfile
        self.RESTARTFILE = restartfile
        self.renders = self.getRenders()

        self.geometry('580x270')
        self.resizable(1, 1)
        self.title('Modifier les informations du Render')

        # UI options
        paddings = {'padx': 5, 'pady': 5}
        entry_font = {'font': ('Helvetica', 11)}
        
        # render informations
        self.firstime = True
        self.displayRender(renderName)
        
        modify_label = ttk.Label(self, text="Modifier :",style='Heading.TLabel')
        modify_label.grid(column=0, columnspan=2, row=3, sticky=tk.W, padx=10)
        
        # new render n°
        new_num_label = ttk.Label(self, text="N° du Render :")
        new_num_label.grid(column=0, row=4, sticky=tk.W, **paddings)
        
        renderName_label = ttk.Label(self, text="Render ")
        renderName_label.grid(column=1, row=4, sticky=tk.W)

        self.num_entry = ttk.Entry(self, **entry_font)
        self.num_entry.grid(column=2, row=4, columnspan=2, sticky=tk.EW, **paddings)
        self.num_entry.focus()

        # user
        new_user_label = ttk.Label(self, text="Nom de l'utilisateur :")
        new_user_label.grid(column=0, row=6, sticky=tk.W, **paddings)

        self.user_entry = ttk.Entry(self, **entry_font)
        self.user_entry.grid(column=1, row=6, columnspan=3, sticky=tk.EW, **paddings)
        
        # ip
        new_ip_label = ttk.Label(self, text="Adresse ip :")
        new_ip_label.grid(column=0, row=7, sticky=tk.W, **paddings)

        self.ip_entry = ttk.Entry(self, **entry_font)
        self.ip_entry.grid(column=1, row=7, columnspan=3, sticky=tk.EW, **paddings)
        

        # save button
        add_button = ttk.Button(self, text="Modifier", command=self.modifyRender)
        add_button.grid(column=2, row=8, sticky=tk.E, **paddings)
        
        # config button
        config_button = ttk.Button(self, text="Configurer", command=self.config)
        config_button.grid(column=3, row=8, **paddings)
        
        # quit button
        quit_button = ttk.Button(self, text="Annuler", command=self.destroy)
        quit_button.grid(column=4, row=8, sticky=tk.EW, **paddings)

        # configure style
        self.style = ttk.Style(self)
        self.style.configure('TLabel', font=('Helvetica', 12))
        self.style.configure('TButton', font=('Helvetica', 12))
        self.style.configure('Heading.TLabel', font=('Helvetica', 13, 'bold'))


#if __name__ == "__main__":
#    import AppRoot
#    path = os.getcwd() + os.path.sep + 'Interface' + os.path.sep + 'Files'
#    savefile = 'saveRenders.csv'
#    configfile = 'connexion_par_cle.bat'
#    stopfile = 'arret_par_cle.bat'
#    restartfile = 'restart_par_cle.bat'
#    config = Config(AppRoot.AppRoot(),path,savefile,configfile,stopfile,restartfile,"Render 1")
#    config.mainloop()