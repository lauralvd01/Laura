import tkinter as tk
from tkinter import ttk
import tkinter.font as font
import pandas as pd
import os
import subprocess
from functools import partial

SAVEPATH = '.\Interface\Files'
SAVEFILE = 'saveRenders.csv'
RESTARTFILE = 'restart_par_cle.bat'
STOPFILE = 'arret_par_cle.bat'

COLOR_DEFAULT_BACKGROUND = "#E8E8E8"
COLOR_DEFAULT_BACKGROUND_BTN = "#F5F5F5"
COLOR_DEFAULT_TEXT = "#FFFFFF"

def joinList(liste) :
    joinStr = ""
    for line in liste :
        joinStr += line.decode()
    return joinStr

def popupmsg(title,msg,color_text=COLOR_DEFAULT_TEXT,color_background=COLOR_DEFAULT_BACKGROUND) :
    popup = tk.Tk()
    
    #Titre de la fenêtre
    popup.wm_title(title)
    
    #Couleur de fond
    popup.configure(background=color_background)
    
    #Message
    label_popup = tk.Label(popup, text=msg, font=FONT_LABEL, foreground=color_text, background=color_background)
    
    #Mise en forme standard f_label
    
    label_popup.pack()
    
    #Bouton quitter
    btn_popup_quit = tk.Button(popup, text="OK", font=FONT_POPUP_BTN, background="#7095FF", command=popup.destroy)
    btn_popup_quit.pack()
    
    popup.mainloop()

def commandRender(renderName,commandChoice) :
    path = SAVEPATH + '\\' + renderName
    command = f"{path}_{commandChoice}.bat"
    (command)
    batch = subprocess.Popen([command], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    result = batch.stdout.readlines()
    if result == []:
        error = joinList(batch.stderr.readlines())
        popupmsg("Erreur","ERREUR : " + error,"#FF0000")
    else :
        popupmsg("Succès",renderName + ":" + joinList(result))
    return

def commandAllRender(renderNames,commandChoice) :
    for renderName in renderNames :
        path = SAVEPATH + '\\' + renderName
        command = f"{path}_{commandChoice}.bat"
        (command)
        batch = subprocess.Popen([command], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result = batch.stdout.readlines()
        if result == []:
            error = joinList(batch.stderr.readlines())
            popupmsg("Erreur","ERREUR : " + error,"#FF0000")
        else :
            popupmsg("Succès",renderName + ":" + joinList(result))
    return

def popupRender(renderName,username,ip) :
    popupRender = tk.Tk()

    popupRender.wm_title(renderName)
    popupRender.configure(background=COLOR_DEFAULT_BACKGROUND)
    
    label_render = tk.Label(popupRender, text=f"{renderName} : {username}@{ip}", font=FONT_LABEL, foreground=COLOR_DEFAULT_TEXT, background=COLOR_DEFAULT_BACKGROUND)
    label_render.pack()
    
    btn_stop = tk.Button(popupRender,text="STOP", font=FONT_BTN, background=COLOR_DEFAULT_BACKGROUND_BTN, command=partial(commandRender,renderName,"stop"))
    btn_restart = tk.Button(popupRender,text="RESTART", font=FONT_BTN, background=COLOR_DEFAULT_BACKGROUND_BTN, command=partial(commandRender,renderName,"restart"))
    btn_stop.pack()
    btn_restart.pack()
    
    btn_popup_quit = tk.Button(popupRender, text="OK", font=FONT_POPUP_BTN, background="#7095FF",command=popupRender.destroy)
    btn_popup_quit.pack()
    
    popupRender.mainloop()

def getRenders(frame) :
    files = os.listdir(path=SAVEPATH)
    btn_renders = []
    if SAVEFILE not in files :
        df = pd.DataFrame(data={'RenderName':[],'Username':[],'Ipv4':[]},dtype=str)
        df.to_csv(SAVEPATH+'\\'+SAVEFILE,index=False)
    else :
        savedRenders = pd.read_csv(SAVEPATH+'\\'+SAVEFILE)
        for i in savedRenders.index :
            #(savedRenders["RenderName"][i] + " : " + savedRenders["Username"][i] + "@" + savedRenders["Ipv4"][i])
            btn_render = tk.Button(frame,text=savedRenders["RenderName"][i], font=FONT_BTN, background=COLOR_DEFAULT_BACKGROUND_BTN, command=partial(popupRender,savedRenders["RenderName"][i],savedRenders["Username"][i],savedRenders["Ipv4"][i]))
            btn_renders.append(btn_render)
    return btn_renders

def add(entry_render,entry_name,entry_ip) :
    renderName = entry_render.get()
    username = entry_name.get()
    ip = entry_ip.get()
    savedRenders = pd.read_csv(SAVEPATH+'\\'+SAVEFILE)
    if renderName not in [savedRenders["RenderName"][i] for i in range(len(savedRenders))] and renderName != "" and username != "" and ip != "" :
        #Adding to the csv
        new = pd.DataFrame({'RenderName':[renderName],'Username':[username],'Ipv4':[ip]})
        new.to_csv(SAVEPATH+'\\'+SAVEFILE,mode='a',header=False,index=False)
        
        #Creating restart.bat file
        source_restart_file = open(SAVEPATH+'\\'+RESTARTFILE,'r')
        i = 0
        new = ""
        for line in source_restart_file :
            if i == 6 :
                new_line = "set name=" + username +'\n'
            elif i == 7 :
                new_line = "set ip=" + ip +'\n'
            else :
                new_line = line
            new += new_line
            i += 1
        source_restart_file.close()
        
        restart_file = open(SAVEPATH+'\\'+renderName+'_restart.bat','w')
        restart_file.write(new)
        restart_file.close()
        
        #Creating stop.bat file
        source_stop_file = open(SAVEPATH+'\\'+STOPFILE,'r')
        i = 0
        new = ""
        for line in source_stop_file :
            if i == 6 :
                new_line = "set name=" + username +'\n'
            elif i == 7 :
                new_line = "set ip=" + ip +'\n'
            else :
                new_line = line
            new += new_line
            i += 1
        source_stop_file.close()
        
        stop_file = open(SAVEPATH+'\\'+renderName+'_stop.bat','w')
        stop_file.write(new)
        stop_file.close()
        
        global renders
        global frame_renders
        for render in renders :
            render.pack_forget()
        renders = getRenders(frame_renders)
        for render in renders :
            render.pack()
        popupmsg("Succès !",f"{renderName} : {username}@{ip}\najouté à la liste des renders")
    else :
        popupmsg("Erreur","Il faut remplir tous les champs et donner un nom de Render qui n'existe pas encore.")
    return

def newRender() :
    new = tk.Tk()
    new.wm_title("Nouveau Render")
    label = tk.Label(new, text="Rentrer les caractéristiques du Render :", font=FONT_LABEL, foreground=COLOR_DEFAULT_TEXT, background=COLOR_DEFAULT_BACKGROUND)
    label.pack()
    
    label_render = tk.Label(new, text="Nom du Render", font=FONT_LABEL, foreground=COLOR_DEFAULT_TEXT, background=COLOR_DEFAULT_BACKGROUND)
    label_name = tk.Label(new, text="Username", font=FONT_LABEL, foreground=COLOR_DEFAULT_TEXT, background=COLOR_DEFAULT_BACKGROUND)
    label_ip = tk.Label(new, text="Adresse ipv4", font=FONT_LABEL, foreground=COLOR_DEFAULT_TEXT, background=COLOR_DEFAULT_BACKGROUND)
    entry_render = tk.Entry(new,background="#FFFFFF",font=FONT_LABEL, foreground=COLOR_DEFAULT_TEXT)
    entry_name = tk.Entry(new,background="#FFFFFF",font=FONT_LABEL, foreground=COLOR_DEFAULT_TEXT)
    entry_ip = tk.Entry(new,background="#FFFFFF",font=FONT_LABEL, foreground=COLOR_DEFAULT_TEXT)
    label_render.pack()
    entry_render.pack()
    label_name.pack()
    entry_name.pack()
    label_ip.pack()
    entry_ip.pack()
    
    btn_ok = tk.Button(new, text="Ajouter", font=FONT_BTN, background="#D0F301", command=partial(add,entry_render,entry_name,entry_ip))
    btn_ok.pack()
    
    #Bouton quitter
    btn_popup_quit = tk.Button(new, text="OK", font=FONT_POPUP_BTN, background="#7095FF", command=new.destroy)
    btn_popup_quit.pack()
        
    new.mainloop()

def deleteRender(entry_render) :
    renderName = entry_render.get()
    savedRenders = pd.read_csv(SAVEPATH+'\\'+SAVEFILE)
    renders_to_delete = savedRenders.index[savedRenders.loc[:,'RenderName'] == renderName]
    
    if len(renders_to_delete) > 0 :
        savedRenders.drop(renders_to_delete,axis=0,inplace=True)
        savedRenders.to_csv(SAVEPATH+'\\'+SAVEFILE,index=False)
        
        os.remove(SAVEPATH+'\\'+renderName+'_restart.bat')
        os.remove(SAVEPATH+'\\'+renderName+'_stop.bat')
        
        global renders
        global frame_renders
        for render in renders :
            render.pack_forget()
        renders = getRenders(frame_renders)
        for render in renders :
            render.pack()
        popupmsg("Succès",f"Tous les Renders du nom {renderName} ont été supprimés")
    else :
        popupmsg("Erreur","Il n'y a pas de Render de ce nom")
    return

def delRender() :
    delete = tk.Tk()
    delete.wm_title("Supprimer un Render")
    label = tk.Label(delete, text="Rentrer les caractéristiques du Render :", font=FONT_LABEL, foreground=COLOR_DEFAULT_TEXT, background=COLOR_DEFAULT_BACKGROUND)
    label.pack()
    
    label_render = tk.Label(delete, text="Nom du Render à supprimer", font=FONT_LABEL, foreground=COLOR_DEFAULT_TEXT, background=COLOR_DEFAULT_BACKGROUND)
    entry_render = tk.Entry(delete,background="#FFFFFF",font=FONT_LABEL, foreground=COLOR_DEFAULT_TEXT)
    label_render.pack()
    entry_render.pack()
    
    
    btn_ok = tk.Button(delete, text="Supprimer", font=FONT_BTN, background="#F36001", command=partial(deleteRender,entry_render))
    btn_ok.pack()
    
    #Bouton quitter
    btn_popup_quit = tk.Button(delete, text="OK", font=FONT_POPUP_BTN, background="#7095FF", command=delete.destroy)
    btn_popup_quit.pack()
        
    delete.mainloop()

def all() :
    popupAllRender = tk.Tk()

    popupAllRender.wm_title("Agir sur tous les Renders")
    popupAllRender.configure(background=COLOR_DEFAULT_BACKGROUND)
    
    savedRenders = pd.read_csv(SAVEPATH+'\\'+SAVEFILE)
    renderNames = [savedRenders["RenderName"][i] for i in range(len(savedRenders))]
    
    btn_stop = tk.Button(popupAllRender,text="STOP", font=FONT_BTN, background=COLOR_DEFAULT_BACKGROUND_BTN, command=partial(commandAllRender,renderNames,"stop"))
    btn_restart = tk.Button(popupAllRender,text="RESTART", font=FONT_BTN, background=COLOR_DEFAULT_BACKGROUND_BTN, command=partial(commandAllRender,renderNames,"restart"))
    btn_stop.pack()
    btn_restart.pack()
    
    btn_popup_quit = tk.Button(popupAllRender, text="OK", font=FONT_POPUP_BTN, background="#7095FF",command=popupAllRender.destroy)
    btn_popup_quit.pack()
    
    popupAllRender.mainloop()


### MAIN

interface = tk.Tk()

FONT_LABEL = font.Font(family='Times New Roman', size=22)
FONT_BTN = font.Font(family='Times New Roman', size=16, weight="bold")
FONT_POPUP_BTN = font.Font(family='Times New Roman', size=12, weight="bold")

interface.title("Interface de commande des Renders")
interface.configure(background=COLOR_DEFAULT_BACKGROUND)

# Agir sur tous les renders
btn_all = tk.Button(text="Tous", font=FONT_BTN, background="#9BFFE4", command=all)
btn_all.pack()

frame_renders = tk.Frame(interface)
frame_renders.pack()
renders = getRenders(frame_renders)
for render in renders :
    render.pack()

# Ajouter un nouveau render
btn_new = tk.Button(text="Nouveau Render", font=FONT_BTN, background="#D0F301", command=newRender)
btn_new.pack()

# Supprimer un render
btn_del = tk.Button(text="Supprimer un Render", font=FONT_BTN, background="#F36001", command=delRender)
btn_del.pack()

# Quitter
btn_quit = tk.Button(text="Quitter", font=FONT_BTN, background="#7095FF", command=interface.destroy)
btn_quit.pack()

interface.mainloop()