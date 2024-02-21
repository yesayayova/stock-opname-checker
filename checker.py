#!/usr/bin/python3 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import filedialog, ttk

## --- IMPORTANT VARIABLE ----------------------------------
PATH_FOLDER = ""
PATH_FILE = ""

def dummy():
    pass

def open_file():
    global PATH_FILE

    if PATH_FILE == "":
        filename = filedialog.askopenfilename(initialdir="C:/",
                                              title="Open File",
                                              filetypes=(('Excel Files', '*.xl*'), ('All Files', '*.*')))
        PATH_FILE = r"{}".format(filename)
    return PATH_FILE

def open_folder():
    global PATH_FOLDER

    if PATH_FOLDER == "":
        foldername = filedialog.askdirectory(initialdir="C:/",
                                             title="Open Folder",
                                             mustexist=True)
        PATH_FOLDER = foldername
    return PATH_FOLDER

def show_tables():
    pass

def main():
    ## --- ROOT APPS -------------------------------------------
    root = Tk()
    root.title('Stock Opname Checker')

    width = 1200
    height = 510

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)

    root.geometry(f"{width}x{height}+{int(x)}+{int(y)}")
    root.resizable(False, False)
    # root.iconbitmap('icon.ico')

    rekap_paned = PanedWindow(bd=2, relief="groove")
    rekap_paned.place(x=10, y=10, width=600, height=490)
    rekap_frame = Frame(rekap_paned, width=585, height=420, background='#cccbca', relief="groove", border=1)
    rekap_frame.place(x=5, y=10)
    rekap_label = Label(root, text='Rekap Mutasi')
    rekap_label.place(x=20, y=0)

    next_btn = Button(rekap_paned, 
                      text='>', 
                      width=2, 
                      command=dummy, 
                      relief="ridge", 
                      borderwidth=1, 
                      border=1)
    next_btn.place(x=555, y=450)
    
    prev_btn = Button(rekap_paned, 
                      text='<', 
                      width=2, 
                      command=dummy, 
                      relief="ridge", 
                      borderwidth=1, 
                      border=1)
    prev_btn.place(x=530, y=450)
    
    openfolder_btn = Button(rekap_paned, 
                      text='Open Folder', 
                      width=10, 
                      command=open_folder, 
                      relief="ridge", 
                      borderwidth=1, 
                      border=1)
    openfolder_btn.place(x=5, y=450)

    summarize_btn = Button(rekap_paned, 
                      text='Summarize', 
                      width=10, 
                      command=dummy, 
                      relief="ridge", 
                      borderwidth=1, 
                      border=1)
    summarize_btn.place(x=90, y=450)

    wh_paned = PanedWindow(bd=2, relief="groove")
    wh_paned.place(x=615, y=10, width=575, height=240)
    wh_frame = Frame(wh_paned, width=560, height=218, background='#cccbca', relief="groove", border=1)
    wh_frame.place(x=5, y=10)
    wh_label = Label(root, text="SJ WH")
    wh_label.place(x=625, y=0)

    stock_paned = PanedWindow(bd=2, relief="groove")
    stock_paned.place(x=615, y=260, width=575, height=240)
    stock_frame = Frame(stock_paned, width=560, height=218, background='#cccbca', relief="groove", border=1)
    stock_frame.place(x=5, y=10)
    stock_label = Label(root, text="Stock Transaction")
    stock_label.place(x=625, y=250)

    ## --- MENU BAR --------------------------------------------------------
    my_menu = Menu(root)

    file_menu = Menu(my_menu, tearoff=False)
    my_menu.add_cascade(label='File', menu=file_menu)

    file_menu.add_command(label='Open File ...        ', command=open_file)
    file_menu.add_command(label='Open Folder ...      ', command=open_folder)
    file_menu.add_separator()
    file_menu.add_command(label='Exit                 ', command=root.quit)

    edit_menu = Menu(my_menu, tearoff=False)
    my_menu.add_cascade(label='Help', menu=edit_menu)

    edit_menu.add_command(label='About             ', command=dummy)
    edit_menu.add_command(label='Documentation     ', command=dummy)

    root.config(menu=my_menu)

    # side_paned = PanedWindow(bd=2, relief="groove")
    # side_paned.place(x=10, y=10, width=125, height=490)
    # openfile_btn  = Button(side_paned,
    #                        text='Open File',
    #                        width=13,
    #                        command=dummy,
    #                        relief='ridge',
    #                        borderwidth=1,
    #                        border=1,
    #                        anchor=W)
    # openfile_btn.place(x=10, y=5)
    # openfolder_btn  = Button(side_paned,
    #                         text='Open Folder',
    #                         width=13,
    #                         command=dummy,
    #                         relief="ridge",
    #                         borderwidth=1,
    #                         border=1,
    #                         anchor=W)
    # openfolder_btn.place(x=10, y=35)
    # summarize_btn  = Button(side_paned,
    #                         text='Summarize',
    #                         width=13,
    #                         command=dummy,
    #                         relief="ridge",
    #                         borderwidth=1,
    #                         border=1,
    #                         anchor=W)
    # summarize_btn.place(x=10, y=75)
    # visualize_btn  = Button(side_paned,
    #                         text='Visualize',
    #                         width=13,
    #                         command=dummy,
    #                         relief="ridge",
    #                         borderwidth=1,
    #                         border=1,
    #                         anchor=W)
    # visualize_btn.place(x=10, y=105)

    ## --- FOOTER ---------------------------------------
    footer = Label(root, text='Version 1.0.0')
    footer.place(x=1110, y=485)

    root.mainloop()

if __name__ == "__main__":
    main()