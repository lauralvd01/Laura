import tkinter as tk
from tkinter import ttk
import os
import pandas as pd
import subprocess
from PIL import ImageTk, Image
# from threading import Thread,Event

from math import ceil
from functools import partial

import NewRender
import DeleteRender
import Config
import PopUP

# class Controller(object) :
#     def __init__(self,nbThreads) -> None:
#         self.nbThreads = nbThreads
#         self.threads = [None for i in range(nbThreads)]
#         self.stop = Event()
#         print(self.threads)

# import sys
# cmd = [sys.executable or "python", "-u", "-c", """
# import itertools, time
# for i in itertools.count():
#     print(i)
#     time.sleep(0.5)
# """]




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

class App(tk.Tk) :
    
    def getRenders(self) :
        if self.SAVEFILE not in os.listdir(path=self.SAVEPATH) :
            renders = pd.DataFrame(data={'RenderName':[],'Username':[],'Ipv4':[],'Config':[]},dtype=str)
            renders.to_csv(self.SAVEPATH+os.path.sep+self.SAVEFILE,index=False)
        else :
            renders = pd.read_csv(self.SAVEPATH+os.path.sep+self.SAVEFILE)
        
        renders['Selected'] = ['0' for i in range(len(renders))]
        renders['ON'] = [False for i in range(len(renders))]
        self.select_number.set(0)
        self.select_text.set(f"Sélection : {self.select_number.get()}")
        return renders
    
    def ping(self,ip) :
        # print("ping "+ip)
        try :
            batch = subprocess.check_output('ping '+ip)
            lines = batch.split(b"\n")
            # print(lines[2])
            index = lines[2].find(b"attente")
            
            if index < 0 :
                # print("Connected")
                return True
            else :
                # print("Not connected")
                return False
        except :
            pass
            # print("ping impossible pour "+ip)
        return False
    
    def getStatus(self) :
        for i in range(len(self.renders)) :
            status = self.ping(self.renders.loc[i,'Ipv4'])
            self.renders.loc[i,'ON'] = status
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
            self.getStatus()
            
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
        all_on_on_button = ttk.Checkbutton(self.on_frame, text="Allumés", command=partial(self.selectAll,"on","on"), variable=self.all_on_on_check)
        all_on_on_button.grid(column=2, row=0, padx=3, sticky=tk.E)
        
        self.all_on_off_check = tk.IntVar()
        self.all_on_off_check.set(0)
        all_on_off_button = ttk.Checkbutton(self.on_frame, text="Éteints", command=partial(self.selectAll,"on","off"), variable=self.all_on_off_check)
        all_on_off_button.grid(column=3, row=0, padx=3, sticky=tk.W)
        
        self.all_on_text = tk.StringVar()
        self.all_on_text.set("Tous")
        self.all_on_check = tk.IntVar()
        self.all_on_check.set(0)
        all_on_button = ttk.Checkbutton(self.on_frame, textvariable=self.all_on_text, command=partial(self.selectAll,"on"), variable=self.all_on_check)
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
        all_off_on_button = ttk.Checkbutton(self.off_frame, text="Allumés", command=partial(self.selectAll,"off","on"), variable=self.all_off_on_check)
        all_off_on_button.grid(column=1, row=0, padx=3, sticky=tk.E)
        
        self.all_off_off_check = tk.IntVar()
        self.all_off_off_check.set(0)
        all_off_off_button = ttk.Checkbutton(self.off_frame, text="Éteints", command=partial(self.selectAll,"off","off"), variable=self.all_off_off_check)
        all_off_off_button.grid(column=2, row=0, padx=3, sticky=tk.W)
        self.all_off_text = tk.StringVar()
        self.all_off_text.set("Tous")
        self.all_off_check = tk.IntVar()
        self.all_off_check.set(0)
        all_off_button = ttk.Checkbutton(self.off_frame, textvariable=self.all_off_text, command=partial(self.selectAll,"off"), variable=self.all_off_check)
        all_off_button.grid(column=3, row=0, padx=3)
        
        # display buttons
        self.select_variables = [tk.IntVar() for i in range(len(self.renders))]
        i_on = 0
        i_off = 0
        for i in range(len(self.renders)) :
            self.select_variables[i].set(0)
            
            if self.renders.loc[i,"ON"] :
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
    
    def selectAll(self,mode,status=None) :
        if status is None :
            if mode == "on" :
                if self.all_on_check.get() : # All from configured
                    for i in range(len(self.renders)) :
                        if self.renders.loc[i,"Config"] == 1 :
                            self.selectOne(i,'1')
                    self.all_on_text.set("Aucun")
                else : # None from configured
                    for i in range(len(self.renders)) :
                        if self.renders.loc[i,"Config"] == 1 :
                            self.selectOne(i,'0')
                    self.all_on_text.set("Tous ")
                self.all_on_on_check.set(0)
                self.all_on_off_check.set(0)
            else :
                if self.all_off_check.get() : # All from not configured
                    for i in range(len(self.renders)) :
                        if self.renders.loc[i,"Config"] == 0 :
                            self.selectOne(i,'1')
                    self.all_off_text.set("Aucun")
                else : # None from not configured
                    for i in range(len(self.renders)) :
                        if self.renders.loc[i,"Config"] == 0 :
                            self.selectOne(i,'0')
                    self.all_off_text.set("Tous ")
                self.all_off_on_check.set(0)
                self.all_off_off_check.set(0)
        elif status == "on" :
            if mode == "on" : 
                if self.all_on_on_check.get() : # Select only connected from configured
                    for i in range(len(self.renders)) :
                        if self.renders.loc[i,"Config"] == 1 :
                            if self.renders.loc[i,"ON"] :
                                self.selectOne(i,'1')
                            else :
                                self.selectOne(i,'0')
                else : # Unselect only connected from configured
                    for i in range(len(self.renders)) :
                        if self.renders.loc[i,"Config"] == 1 :
                            if self.renders.loc[i,"ON"] :
                                self.selectOne(i,'0')
                self.all_on_off_check.set(0)
            else :
                if self.all_off_on_check.get() : # Select only connected from not configured
                    for i in range(len(self.renders)) :
                        if self.renders.loc[i,"Config"] == 0 :
                            if self.renders.loc[i,"ON"] :
                                self.selectOne(i,'1')
                            else :
                                self.selectOne(i,'0')
                else : # Unselect only connected from not configured
                    for i in range(len(self.renders)) :
                        if self.renders.loc[i,"Config"] == 0 :
                            if self.renders.loc[i,"ON"] :
                                self.selectOne(i,'0')
                self.all_off_off_check.set(0)
        else :
            if mode == "on" :
                if self.all_on_off_check.get() : # Select only not connected from configured
                    for i in range(len(self.renders)) :
                        if self.renders.loc[i,"Config"] == 1 :
                            if not self.renders.loc[i,"ON"] :
                                self.selectOne(i,'1')
                            else :
                                self.selectOne(i,'0')
                else : # Unselect only not connected from configured
                    for i in range(len(self.renders)) :
                        if self.renders.loc[i,"Config"] == 1 :
                            if not self.renders.loc[i,"ON"] :
                                self.selectOne(i,'0')
                self.all_on_on_check.set(0)
            else :
                if self.all_off_off_check.get() : # Select only not connected from not configured
                    for i in range(len(self.renders)) :
                        if self.renders.loc[i,"Config"] == 0 :
                            if not self.renders.loc[i,"ON"] :
                                self.selectOne(i,'1')
                            else :
                                self.selectOne(i,'0')
                else : # Unselect only not connected from not configured
                    for i in range(len(self.renders)) :
                        if self.renders.loc[i,"Config"] == 0 :
                            if not self.renders.loc[i,"ON"] :
                                self.selectOne(i,'0')
                self.all_off_on_check.set(0)
        return
    
    def selectOne(self,i,forced_value=None) :
        if self.renders.loc[i,"Selected"] == '0':
            if forced_value is None or forced_value == '1' :
                self.renders.loc[i,"Selected"] = '1'
                self.select_variables[i].set(1)
                self.select_number.set(self.select_number.get()+1)
        else :
            if forced_value is None or forced_value == '0' :
                self.renders.loc[i,"Selected"] = '0'
                self.select_variables[i].set(0)
                self.select_number.set(self.select_number.get()-1)
        self.select_text.set(f"Sélection : {self.select_number.get()}")
        return
    
    def createBat(self,renderName) :
        render = {}
        for i in range(len(self.renders)) :
            if self.renders.loc[i,"RenderName"] == renderName :
                render = {'RenderName': self.renders.loc[i,"RenderName"],'Username': self.renders.loc[i,"Username"],'Ipv4': self.renders.loc[i,"Ipv4"], 'Config': self.renders.loc[i,"Config"]}
        
        if len(render) > 0 and render['Config'] == 0 :
            
            #Creating config.bat file
            source_config_file = open(self.SAVEPATH+os.path.sep+self.CONFIGFILE,'r')
            i = 0
            new = ""
            for line in source_config_file :
                if i == 12 :
                    new_line = "set name=" + render['Username'] +'\n'
                elif i == 13 :
                    new_line = "set ip=" + render['Ipv4'] +'\n'
                else :
                    new_line = line
                new += new_line
                i += 1
            source_config_file.close()
            
            config_file = open(self.SAVEPATH+os.path.sep+renderName+'_config.bat','w')
            config_file.write(new)
            config_file.close()
            
            #Creating stop.bat file
            source_stop_file = open(self.SAVEPATH+os.path.sep+self.STOPFILE,'r')
            i = 0
            new = ""
            for line in source_stop_file :
                if i == 6 :
                    new_line = "set name=" + render['Username'] +'\n'
                elif i == 7 :
                    new_line = "set ip=" + render['Ipv4'] +'\n'
                else :
                    new_line = line
                new += new_line
                i += 1
            source_stop_file.close()
            
            stop_file = open(self.SAVEPATH+os.path.sep+renderName+'_stop.bat','w')
            stop_file.write(new)
            stop_file.close()
            
            #Creating restart.bat file
            source_restart_file = open(self.SAVEPATH+os.path.sep+self.RESTARTFILE,'r')
            i = 0
            new = ""
            for line in source_restart_file :
                if i == 6 :
                    new_line = "set name=" + render['Username'] +'\n'
                elif i == 7 :
                    new_line = "set ip=" + render['Ipv4'] +'\n'
                else :
                    new_line = line
                new += new_line
                i += 1
            source_restart_file.close()
            
            restart_file = open(self.SAVEPATH+os.path.sep+renderName+'_restart.bat','w')
            restart_file.write(new)
            restart_file.close()
        
        else :
            PopUP.PopUP("Erreur",renderName+" est déjà configuré.")
            
        return
    
    def stopOperations(self) :
        # if self.running :
        #     self.running = False
        #     print("STOP")
        # else :
        #     PopUP.PopUP("Erreur","Aucune opération en cours.")
        return
    
    def runProcessO(self,renderName,command) :
    #     command = cmd
        
    #     index = self.renders.index[self.renders['RenderName'] == renderName]
    #     if self.renders.loc[index[0],'ON'] :
    #         try :
    #             error = ""
    #             batch = subprocess.Popen([command], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                
    #             while batch.poll() == None :
    #                 print("Trying "+command+" ...")
    #                 if not self.running :
    #                     batch.terminate()
    #                     print("Stop "+command)
    #                     PopUP.PopUP("Arrêt de l'opération",command+" : processus arrêté avec succès.")
                
    #             # if self.running :
    #             if True :
    #                 result = batch.stdout.readlines()
    #                 if result == []:
    #                     error = joinList(batch.stderr.readlines())
    #                     PopUP.PopUP("Erreur "+renderName,"ERREUR : " + error,"#FF0000")
    #                 else :
    #                     PopUP.PopUP("Succès",renderName + " :\n" + joinList(result))
    #             else :
    #                 PopUP.PopUP("Arrêt des opérations","Arrêt de l'opération sur le "+renderName)
    #         except :
    #             PopUP.PopUP("Erreur "+renderName,"Une erreur s'est produite lors de l'envoi de la commande","#FF0000")
    #     else :
    #         PopUP.PopUP("Erreur "+renderName,"Le render "+renderName+" est considéré éteint. Allumer le render puis actualiser les statuts.","#FF0000")
        return
        
    def runProcess(self,renderName,command) :
        index = self.renders.index[self.renders['RenderName'] == renderName]
        if self.renders.loc[index[0],'ON'] :
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
        else :
            PopUP.PopUP("Erreur "+renderName,"Le render "+renderName+" est considéré éteint. Allumer le render puis actualiser les statuts.","#FF0000")
        return
    
    def commandRender(self, renderName,commandChoice) :
        path = self.SAVEPATH + os.path.sep + renderName
        
        if commandChoice == 'config' :
            # creation of bat files
            self.createBat(renderName)
            
        command = f"{path}_{commandChoice}.bat"
        print(command)
        if os.path.isfile(command)  :
            self.runProcess(renderName,command)
        else :
            PopUP.PopUP("Erreur "+renderName,renderName+" pas encore configuré !","#FF0000")
        return
    
    def commandAllRenders(self,commandChoice) :
        if self.select_number.get() + self.select_number.get() == 0 :
            PopUP.PopUP("Erreur","Aucun Render sélectionné")
        else :
            # self.running = True
            # print(self.running)
            
            selected = []
            for i in range(len(self.renders)) :
                if self.renders.loc[i,"Selected"] == '1' :
                    selected.append(self.renders.loc[i,"RenderName"])
            
            for renderName in selected :
                # if not self.running :
                #     break
                
                if commandChoice != "config" :
                    self.commandRender(renderName,commandChoice)
                else :
                    Config.Config(self,self.SAVEPATH,self.SAVEFILE,self.CONFIGFILE,self.STOPFILE,self.RESTARTFILE,renderName)
        
            print("End of commands")
            # self.stopOperations()
        self.selectAll("off")
        return
    
    def getConfig(self) :
        if 'config.csv' not in os.listdir(path=self.SAVEPATH) :
            PopUP.PopUP("ERROR : échec de l'importation","Il n'y a pas de fichier config.csv à l'endroit prévu.\nDéplacez le fichier config.csv à importer dans :\n"+self.SAVEPATH+os.path.sep+"\nou vérifiez l'orthographe du fichier.")
        else :
            renders = self.getRenders().drop("Selected",axis=1).drop("ON",axis=1)
            new_renders = pd.read_csv(self.SAVEPATH+os.path.sep+'config.csv')
            concat_renders = pd.concat([renders,new_renders]).drop_duplicates(subset=['RenderName','Username','Ipv4'],keep='first')
            concat_renders.sort_values(by="RenderName",axis=0,inplace=True,key=getRenderIndex)
            concat_renders.to_csv(self.SAVEPATH+os.path.sep+self.SAVEFILE,index=False)
            self.getRenders()
            self.displayRenders()
            PopUP.PopUP("Succès","Le fichier config.csv a été importé avec succès.")
        return
    
    def saveConfig(self) :
        renders = self.renders.drop("Selected",axis=1)
        renders = self.renders.drop("ON",axis=1)
        renders["Config"] = [0 for i in range(len(renders))]
        renders.to_csv(self.SAVEPATH+os.path.sep+'config.csv',index=False)
        PopUP.PopUP("Succès","La configuration a bien été exportée dans le fichier suivant :\n"+self.SAVEPATH+os.path.sep+'config.csv')
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
        
        # stop operations
        # self.running = False
        # self.stop_op_button = ttk.Button(self, text="STOP",command=self.stopOperations)
        # self.stop_op_button.grid(column=2, columnspan=1, sticky=tk.W, row=3, padx=2)
        
        # status
        image_red=Image.open('_internal\Files\\red.png')
        self.red = ImageTk.PhotoImage(image_red.resize((20,10)))
        self.red.height=10
        self.red.width=10
        image_green=Image.open('_internal\Files\\green.png')
        self.green = ImageTk.PhotoImage(image_green.resize((20,10)))
        self.green.height=10
        self.green.width=10
        self.status_button = ttk.Button(self, text="ACTUALISER",command=self.displayRenders)
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
            # self.running = False
            self.destroy()
        
        
        # # stop button
        # stop_button = ttk.Button(self, text="Annuler les opérations", command=self.stopOperations)
        # stop_button.grid(column=1, columnspan=2, row=5, sticky=tk.EW)
        
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
    #control = Controller(2)