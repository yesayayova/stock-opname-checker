#!/usr/bin/python3 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import table as tb
from tkinter import *
from tkinter import filedialog, ttk

## --- IMPORTANT VARIABLE ----------------------------------
PATH_FOLDER = ""
PATH_FILE = ""
TABLE_REKAP = ""
TABLE_SJWH = ""
TABLE_STOCK = ""
TABLE_NAME = ""

def dummy():
    pass

def combo_click(event):
    pass

def open_file(frame_rekap="", frame_stock="", frame_sjwh=""):
    global PATH_FILE, TABLE_REKAP, TABLE_SJWH, TABLE_STOCK, TABLE_NAME

    filename = filedialog.askopenfilename(initialdir="C:/",
                                              title="Open File",
                                              filetypes=(('Excel Files', '*.xl*'), ('All Files', '*.*')))
    PATH_FILE = r"{}".format(filename)
    
    TABLE_REKAP = tb.Rekap(PATH_FILE, frame=frame_rekap)
    TABLE_REKAP.show()

    TABLE_SJWH = tb.SJWH(PATH_FILE, frame=frame_sjwh)
    TABLE_SJWH.show()

    TABLE_STOCK = tb.Stock(PATH_FILE, frame=frame_stock)
    TABLE_STOCK.show()

    TABLE_NAME.config(text="Table : " + PATH_FILE.split('/')[-1])


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
    global TABLE_NAME

    ## --- ROOT APPS -------------------------------------------
    root = Tk()
    root.title('Stock Opname Checker')

    width = 1200
    height = 560

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)

    root.geometry(f"{width}x{height}+{int(x)}+{int(y)}")
    root.resizable(False, False)
    # root.iconbitmap('icon.ico')

    rekap_paned = PanedWindow(bd=2, relief="groove")
    rekap_paned.place(x=10, y=10, width=600, height=530)
    rekap_frame = Frame(rekap_paned, width=585, height=445, background='#cccbca', relief="groove", border=1)
    rekap_frame.place(x=5, y=45)
    rekap_label = Label(root, text='Rekap Mutasi')
    rekap_label.place(x=517, y=0)

    TABLE_NAME = Label(rekap_paned, text="Table : ")
    TABLE_NAME.place(x=10, y=10)

    next_btn = Button(rekap_paned, 
                      text='>', 
                      width=2, 
                      command=dummy, 
                      relief="ridge", 
                      borderwidth=1, 
                      border=1)
    next_btn.place(x=555, y=10)
    
    prev_btn = Button(rekap_paned, 
                      text='<', 
                      width=2, 
                      command=dummy, 
                      relief="ridge", 
                      borderwidth=1, 
                      border=1)
    prev_btn.place(x=530, y=10)
    
    openfolder_btn = Button(rekap_paned, 
                      text='Open Folder', 
                      width=10, 
                      command=open_folder, 
                      relief="ridge", 
                      borderwidth=1, 
                      border=1)
    openfolder_btn.place(x=10, y=495)

    summarize_btn = Button(rekap_paned, 
                      text='Summarize', 
                      width=10, 
                      command=dummy, 
                      relief="ridge", 
                      borderwidth=1, 
                      border=1)
    summarize_btn.place(x=95, y=495)

    wh_paned = PanedWindow(bd=2, relief="groove")
    wh_paned.place(x=615, y=10, width=575, height=260)
    wh_frame = Frame(wh_paned, width=560, height=210, background='#cccbca', relief="groove", border=1)
    wh_frame.place(x=5, y=10)
    wh_label = Label(root, text="SJ WH")
    wh_label.place(x=1130, y=0)
    wh_filter_label = Label(wh_paned, text='Filter  : ')
    wh_filter_label.place(x=10, y=228)
    # wh_combobox_options = ['']
    # wh_combobox = ttk.Combobox(wh_paned, values=wh_combobox_options)
    # wh_combobox.current(0)
    # wh_combobox.bind("<<ComboboxSelected>>", combo_click)
    # wh_combobox.place(x=60, y=225)
    wh_search = Entry(wh_paned, width=20)
    wh_search.place(x=60, y=228)
    wh_search_btn = Button(wh_paned, 
                           text='Search', 
                           width=6, 
                           command=dummy, 
                           relief="ridge", 
                           borderwidth=1, 
                           border=1)
    wh_search_btn.place(x=190, y=226)

    stock_paned = PanedWindow(bd=2, relief="groove")
    stock_paned.place(x=615, y=280, width=575, height=260)
    stock_frame = Frame(stock_paned, width=560, height=210, background='#cccbca', relief="groove", border=1)
    stock_frame.place(x=5, y=10)
    stock_label = Label(root, text="Stock Transaction")
    stock_label.place(x=1070, y=270)
    stock_filter_label = Label(stock_paned, text='Filter  : ')
    stock_filter_label.place(x=10, y=225)
    # stock_combobox_options = ['']
    # stock_combobox = ttk.Combobox(stock_paned, values=stock_combobox_options)
    # stock_combobox.current(0)
    # stock_combobox.bind("<<ComboboxSelected>>", combo_click)
    # stock_combobox.place(x=60, y=225)
    stock_search = Entry(stock_paned, width=20)
    stock_search.place(x=60, y=228)
    stock_search_btn = Button(stock_paned, 
                           text='Search', 
                           width=6, 
                           command=dummy, 
                           relief="ridge", 
                           borderwidth=1, 
                           border=1)
    stock_search_btn.place(x=190, y=226)

    ## --- MENU BAR --------------------------------------------------------
    my_menu = Menu(root)

    file_menu = Menu(my_menu, tearoff=False)
    my_menu.add_cascade(label='File', menu=file_menu)

    file_menu.add_command(label='Open File ...        ', 
                          command=lambda : open_file(frame_rekap=rekap_frame, 
                                                     frame_sjwh=wh_frame, 
                                                     frame_stock=stock_frame
                                                    ))
    file_menu.add_command(label='Open Folder ...      ', command=open_folder)
    file_menu.add_separator()
    file_menu.add_command(label='Exit                 ', command=root.quit)

    edit_menu = Menu(my_menu, tearoff=False)
    my_menu.add_cascade(label='Help', menu=edit_menu)

    edit_menu.add_command(label='About             ', command=dummy)
    edit_menu.add_command(label='Documentation     ', command=dummy)

    root.config(menu=my_menu)

    ## --- FOOTER ---------------------------------------
    footer = Label(root, text='Version 1.0.0')
    footer.place(x=1110, y=515)

    ## --- LOG LABEL -----------------------------------
    log = Label(root, text="Welcome!", font=("Arial", 8, "italic"))
    log.place(x=20, y=540)

    root.mainloop()

if __name__ == "__main__":
    main()