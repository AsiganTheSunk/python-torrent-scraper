from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import os
from torrentscraper import scraper_engine as se
from torrentscraper.datastruct.websearch_instance import WebSearchInstance
from simple_option_menu import SimpleOptionMenu
from simple_list_box import SimpleListBox

def label(row, column, text):
    L = Label(root, text=text, anchor='w')
    L.grid(row=row,column=column,sticky="nw",pady=2,padx=3)

def button(root, row, column, text, command):
    B = Button(root, text=text, command=command, width=15, relief='groove', borderwidth=2, bg='#DCDCDC', highlightbackground='#848482')
    B.grid(row=row, column=column, sticky="es", pady=4, padx=3)

def entry(row, column, insert="", show=""):
    E = Entry(root, width=32)
    E.insert(0, insert)
    E.config(show=show)
    E.grid(row=row, column=column)
    return E

def scrap():

    title = var0.get()
    year = var1.get()
    season = var2.get()
    episode = var3.get()
    quality = popupMenu.selection
    header = popupMenu0.selection
    search_type = popupMenu1.selection

    # websearch = WebSearchInstance(title, '', season, episode, quality, '', search_type)
    # scraper_engine = se.ScraperEngine()
    # p2p_instance_list = scraper_engine.search(websearch)
    # dataframe = scraper_engine.create_magnet_dataframe(p2p_instance_list)
    # dataframe = scraper_engine.unique_magnet_dataframe(dataframe)
    # dataframe = scraper_engine.get_dataframe(dataframe, 5)

    magnet = ''
    lista = ['[HorribleSubs] Megalobox Episode - 01 1080p.mkv','[HorribleSubs] Megalobox Episode - 01 720.mkv','[HorribleSubs] Megalobox Episode - 01 480p.mkv']
    # for index in  dataframe.index.tolist():
    #     dn = dataframe.iloc[int(index)]['name']
    #     _hash = dataframe.iloc[int(index)]['hash']
    #     magnet = dataframe.iloc[int(index)]['magnet']
    #     size = dataframe.iloc[int(index)]['size']
    #     seed = dataframe.iloc[int(index)]['seed']
    #     leech = dataframe.iloc[int(index)]['leech']
    #     ratio = dataframe.iloc[int(index)]['ratio']
    #     formato =  '{0:15}'.format(dn)
    #     #formato =  '{0:15} {1:20} {2:7} {3:>4}/{4:4} {5:5}'.format(dn, _hash, str(size), str(seed), str(leech), ratio)
    #     lista.append(formato)

    top = Toplevel()
    top.geometry('830x400')
    top.title("Result")

    list_box = SimpleListBox(top, lista)
    list_box.configure(borderwidth=0, highlightbackground='#848482', bg='#DCDCDC', relief='solid')
    list_box.grid(row=0, column=0, padx=5, pady=5, sticky='nw')

    ttk.Separator(top, orient=VERTICAL).grid(row=2, columnspan=5)

    im = Image.open('./megalobox_placeholder.png')
    photo = ImageTk.PhotoImage(im)
    top.photo = photo
    cv = Canvas(top, width=195, height=265, relief='solid')
    cv.configure(borderwidth=0, highlightbackground='#848482')
    cv.grid(row=0, column=1, padx=5, pady=5)
    cv.create_image(0, 0, image=photo, anchor='nw')

    qicon = Image.open('./display_flags/1080_n.png')
    qphoto = ImageTk.PhotoImage(qicon)
    top.qphoto = qphoto

    cv0 = Canvas(top, width=64, height=50, relief='flat')
    cv0.configure(borderwidth=0)
    cv0.grid(row=1, column=1)
    cv0.create_image(64*.53, 48*.55, image=qphoto, anchor='center')

    qicon0 = Image.open('./display_flags/2.png')
    qphoto0 = ImageTk.PhotoImage(qicon0)
    top.qphoto0 = qphoto0

    cv1 = Label(top, width=64, height=50, relief='flat')
    cv1.configure(borderwidth=0, image=qphoto0)
    cv1.grid(row=1, column=5)
    # cv1.create_image(64*.53, 48*.55, , anchor='center')


    cv2 = Label(top, width=64, height=50, relief='flat')
    cv2.configure(borderwidth=0, image=qphoto0)
    cv2.grid(row=1, column=0)
    button(top, 3, 0, 'Download', yes_no)
    button(top, 3, 1, 'Exit', yes_no())

def yes_no():
    pass

root = Tk()
root.geometry("800x600")
root.style = ttk.Style()
root.style.theme_use("clam")
root.iconbitmap('./cat-grumpy.ico')
root.title("python-torrent-scraper-v0.3.2")

#label(0, 0, 'Title')
# var0 = entry(0, 0,  insert='Title')
var0 = entry(0, 0,  insert='Rick & Morty')

#label(1, 0, 'Year')
var1 = entry(1, 0,  insert='Year')

#label(2, 0, 'Season')
# var2 = entry(2, 0,  insert='Season')
var2 = entry(2, 0,  insert='03')

#label(3, 0, 'Episode')
#var3 = entry(3, 0,  insert='Episode')
var3 = entry(3, 0,  insert='08')

quality = {'1080p':'1080p', '720p':'720p', 'HDTV':'HDTV', 'WEBRip': 'WEBRip'}
popupMenu = SimpleOptionMenu(root, '[Choose Quality]', *quality)
#Label(root, text="[Choose a Quality]: ").grid(row=4, column=0, sticky='W')
popupMenu.grid(row=4, column=0, columnspan=2, sticky='W')

header = {'[HorribleSubs]':'HorribleSubs'}
popupMenu0 = SimpleOptionMenu(root, '[Choose Header]', *header)
#Label(root, text="[Choose a Quality]: ").grid(row=5, column=0, sticky='W')
popupMenu0.grid(row=5, column=0, columnspan=2, sticky='W')

search_type = {'SHOW':'SHOW', 'MOVIE':'MOVIE', 'ANIME':'ANIME'}
popupMenu1 = SimpleOptionMenu(root, '[Choose Search Type]', *search_type)
#Label(root, text="[Choose a Search Type]: ").grid(row=6, column=0, sticky='W')
popupMenu1.grid(row=6, column=0, columnspan=2, sticky='W')

label(10, 0, '')
button(root, 17, 0, 'Scrap', scrap)
button(root, 17, 1, 'Quit', root.quit)
root.mainloop()


# from tkinter import *
#
# canvas_width = 300
# canvas_height =80
#
# master = Tk()
# canvas = Canvas(master,
#            width=canvas_width,
#            height=canvas_height)
# canvas.pack()
#
# bitmaps = ["error", "gray75", "gray50", "gray25", "gray12", "hourglass", "info", "questhead", "question", "warning"]
# nsteps = len(bitmaps)
# step_x = int(canvas_width / nsteps)
#
# for i in range(0, nsteps):
#    canvas.create_bitmap((i+1)*step_x - step_x/2,50, bitmap=bitmaps[i])
#
# mainloop()

# global quality_selection
#
# class SimpleOptionMenu(OptionMenu):
#     def __init__(self, master, status, *options):
#         self.var = StringVar(master)
#         self.var.set(status)
#         self.var.trace('w', self.get_item)
#         OptionMenu.__init__(self, master, self.var, *options)
#         self.config(font=('calibri', (10)), width=12)
#         self['menu'].config(font=('calibri', (10)), bg='white')
#
#     def get_item(self, *args):
#         quality_selection = self.var.get()
#         print(quality_selection)
#         return quality_selection
#
# root = Tk()
# root.title("Tk dropdown example")
# root.geometry('600x400')
# root.iconbitmap('./cat-grumpy.ico')


#root.overrideredirect(True)
#root.attributes("-toolwindow", 1)




# #!/usr/bin/python
# import tkinter as tk
#
# class App(tk.Frame):
#     def __init__(self, parent, *args, **kwargs):
#         tk.Frame.__init__(self, parent)
#
#         self.parent = parent
#
#         self.initUI()
#
#     def initUI(self):
#
#         self.parent.title("Fullscreen Application")
#
#         self.pack(fill="both", expand=True, side="top")
#
#         self.parent.wm_state("zoomed")
#
#         self.parent.bind("<F11>", self.fullscreen_toggle)
#         self.parent.bind("<Escape>", self.fullscreen_cancel)
#
#         self.fullscreen_toggle()
#
#         self.label = tk.Label(self, text="Fullscreen", font=("default",120), fg="black")
#         self.label.pack(side="top", fill="both", expand=True)
#
#     def fullscreen_toggle(self, event="none"):
#
#         self.parent.focus_set()
#         self.parent.overrideredirect(True)
#         self.parent.overrideredirect(False) #added for a toggle effect, not fully sure why it's like this on Mac OS
#         self.parent.attributes("-fullscreen", True)
#         self.parent.wm_attributes("-topmost", 1)
#
#     def fullscreen_cancel(self, event="none"):
#
#         self.parent.overrideredirect(False)
#         self.parent.attributes("-fullscreen", False)
#         self.parent.wm_attributes("-topmost", 0)
#
#         self.centerWindow()
#
#     def centerWindow(self):
#
#         sw = self.parent.winfo_screenwidth()
#         sh = self.parent.winfo_screenheight()
#
#         w = sw*0.7
#         h = sh*0.7
#
#         x = (sw-w)/2
#         y = (sh-h)/2
#
#         self.parent.geometry("%dx%d+%d+%d" % (w, h, x, y))
#
# if __name__ == "__main__":
#     root = tk.Tk()
#     App(root).pack(side="top", fill="both", expand=True)
#     root.mainloop()

