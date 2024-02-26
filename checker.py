#!/usr/bin/python3 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import table as tb
import customtkinter
import os
from tkinter import *
from tkinter import filedialog, ttk

## --- IMPORTANT VARIABLE ----------------------------------
PATH_FILE = ""

TABLE_REKAP = pd.DataFrame([[]])
TABLE_SJWH = pd.DataFrame([[]])
TABLE_STOCK = pd.DataFrame([[]])

TABLE_NAME = ""
FILE_OPEN = False

LIST_FOLDER = []
CURRENT_TABLE_ID = 0

my_tree = ""
TABLE_ORIGINAL = ""
TABLE_OUTPUT = ""

def save_file():
    table = TABLE_REKAP.get_table_original()
    table.drop(labels=['ID', 'Selisih'], axis='columns', inplace=True)

    save_filename = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                             initialdir="C:/",
                                             title="Save",
                                             filetypes=(('Microsoft Excel', "*.xlsx"), ("All Files", "*.*")))

    if save_filename:
        table.to_excel(save_filename)

def save(top, frame, raptor, wh, id):
    global TABLE_REKAP

    TABLE_REKAP.edit_table(raptor=raptor, sjwh=wh, id=int(id))
    show_rekap(frame)
    top.destroy()

def edit(frame):
    selected_item = my_tree.selection()
    data = my_tree.item(selected_item, 'values')
    
    top = Toplevel()
    top.title('Edit')

    width = 260
    height = 200

    screen_width = top.winfo_screenwidth()
    screen_height = top.winfo_screenheight()

    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)

    top.geometry(f"{width}x{height}+{int(x)}+{int(y)}")
    top.resizable(False, False)

    # top_paned = PanedWindow(top,bd=2, relief='groove')
    # top_paned.place(x=5, y=5, width=290, height=190)

    plu_label = Label(top, text='PLU Number')
    plu_label.place(x=10, y=10)
    plu_value = Label(top, text=data[1])
    plu_value.place(x=100, y=10)

    name_label = Label(top, text='Name')
    name_label.place(x=10, y=45)
    name_value = Label(top, text=data[2])
    name_value.place(x=100, y=45)

    raptor_label = Label(top, text='In-Raptor')
    raptor_label.place(x=10, y=80)
    raptor_value = Entry(top, width=20)
    raptor_value.insert(0, data[3])
    raptor_value.place(x=100, y=80)

    wh_label = Label(top, text='In-SJ WH')
    wh_label.place(x=10, y=115)
    wh_value = Entry(top, width=20)
    wh_value.insert(0, data[4])
    wh_value.place(x=100, y=115)

    save_btn = Button(top, 
                      width=10, 
                      text='Save', 
                      command=lambda : save(top=top,
                                            frame=frame,
                                            raptor=raptor_value.get(),
                                            wh=wh_value.get(),
                                            id=data[0]),
                      relief="ridge", 
                      borderwidth=1, 
                      border=1)
    save_btn.place(x=120, y=160)

def popup(event):
    global popup_menu
    # Menampilkan popup hanya jika ada item yang dipilih
    if my_tree.selection():
        popup_menu.post(event.x_root, event.y_root)

def show_rekap(frame, mode="off"):
        global TABLE_REKAP, my_tree, popup_menu

        table = TABLE_REKAP.get_table_output()
        my_tree = ttk.Treeview(frame)

        # Clear old treeview
        my_tree.delete(*my_tree.get_children())

        # Set up new tree
        my_tree['column'] = list(table.columns)
        my_tree['show'] = "headings"
            
        # Set up all column names
        for column in my_tree['column']:        
            my_tree.heading(column, text=column, anchor=W)
            if 'PLU' in column:
                my_tree.column(column, width=140)
            elif 'ID' in column:
                my_tree.column(column, width=20)
            else:
                my_tree.column(column, width=70)
        # Set up all rows
        df_rows = table.to_numpy().tolist()
        
        if mode == "off":
            for i, row in enumerate(df_rows):
                if (row[3] != row[4]) and (row[5]> 0):
                    # print(row)
                    my_tree.insert("", "end", values=row, tags="red")
                elif (row[3] != row[4]) and (row[5]< 0):
                    my_tree.insert("", "end", values=row, tags="yellow")
                else:
                    my_tree.insert("", "end", values=row, tags="white")
        
        elif mode == "on":
            for i, row in enumerate(df_rows):
                if (row[3] != row[4]) and (row[5]> 0):
                    # print(row)
                    my_tree.insert("", "end", values=row, tags="red")
                elif (row[3] != row[4]) and (row[5]< 0):
                    my_tree.insert("", "end", values=row, tags="yellow")
                else:
                    continue

        my_tree.tag_configure("red", background="#fa9898")
        my_tree.tag_configure("yellow", background="#e8f28f")

        my_tree.pack(expand=True, fill='both')
        my_tree.place(x=0, y=0, width=585, height=445)
            
        scroll_y = Scrollbar(my_tree, orient='vertical', command=my_tree.yview)
        scroll_y.place(relx=1, rely=0, relheight=1, anchor='ne')

        scroll_x = Scrollbar(my_tree, orient='horizontal', command=my_tree.xview)
        scroll_x.pack(side='bottom', fill='x')

        my_tree.configure(xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        popup_menu = Menu(frame, tearoff=0)
        popup_menu.add_command(label="Edit", command=lambda : edit(frame))

        my_tree.bind("<Button-3>", popup)

def dummy():
    pass

def open_file(path = "", frame_rekap="", frame_stock="", frame_sjwh=""):
    global PATH_FILE, TABLE_REKAP, TABLE_SJWH, TABLE_STOCK, TABLE_NAME, FILE_OPEN, CURRENT_TABLE_ID, switch

    if path == "":
        filename = filedialog.askopenfilename(initialdir="C:/",
                                                title="Open File",
                                                filetypes=(('Excel Files', '*.xl*'), ('All Files', '*.*')))
        PATH_FILE = r"{}".format(filename)
    else:
        PATH_FILE = path

    # print(PATH_FILE)

    try:
        TABLE_REKAP = tb.Rekap(PATH_FILE, frame=frame_rekap)
        show_rekap(frame_rekap)
        # TABLE_REKAP.show()

        TABLE_SJWH = tb.SJWH(PATH_FILE, frame=frame_sjwh)
        TABLE_SJWH.show()

        TABLE_STOCK = tb.Stock(PATH_FILE, frame=frame_stock)
        TABLE_STOCK.show()

        TABLE_NAME.config(text="Table : " + PATH_FILE.split('/')[-1])

        FILE_OPEN = True
        switch_btn.configure(state=ACTIVE)
    except:
        return 0

def open_folder(frame_rekap, frame_stock, frame_sjwh):
    global LIST_FOLDER, CURRENT_TABLE_ID

    foldername = filedialog.askdirectory(initialdir="C:/",
                                            title="Open Folder",
                                            mustexist=True)
    for filename in os.listdir(foldername):
        LIST_FOLDER.append(str(foldername + '/' + filename))

    # print(CURRENT_TABLE)

    open_file(path=LIST_FOLDER[CURRENT_TABLE_ID], 
              frame_rekap=frame_rekap, 
              frame_sjwh=frame_sjwh,
              frame_stock=frame_stock)
    
def next(frame_rekap, frame_stock, frame_sjwh):
    global CURRENT_TABLE_ID

    if len(LIST_FOLDER) == 0:
        return 0
    else:
        if CURRENT_TABLE_ID == len(LIST_FOLDER)-1:
            print('test')
            return 0
        else:
            CURRENT_TABLE_ID += 1
            path = LIST_FOLDER[CURRENT_TABLE_ID]
            open_file(path=path, 
                frame_rekap=frame_rekap, 
                frame_sjwh=frame_sjwh,
                frame_stock=frame_stock)
        print(path)

def prev(frame_rekap, frame_stock, frame_sjwh):
    global CURRENT_TABLE_ID

    if len(LIST_FOLDER) == 0:
        return 0
    else:
        if CURRENT_TABLE_ID == 0:
            return 0
        else:
            CURRENT_TABLE_ID -= 1
            path = LIST_FOLDER[CURRENT_TABLE_ID]
            open_file(path=path, 
                frame_rekap=frame_rekap, 
                frame_sjwh=frame_sjwh,
                frame_stock=frame_stock)
        print(path)
        
def search(frame, seach_value=""):
    global TABLE_SJWH, FILE_OPEN

    if FILE_OPEN:
        TABLE_SJWH.show(seach_value)
        # print(seach_value)
    else:
        return 0

def main():
    global TABLE_NAME, switch_btn, log

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
                      command=lambda : next(frame_rekap=rekap_frame, 
                                            frame_sjwh=wh_frame, 
                                            frame_stock=stock_frame
                                            ),
                      relief="ridge", 
                      borderwidth=1, 
                      border=1)
    next_btn.place(x=555, y=10)
    
    prev_btn = Button(rekap_paned, 
                      text='<', 
                      width=2, 
                      command=lambda : prev(frame_rekap=rekap_frame, 
                                            frame_sjwh=wh_frame, 
                                            frame_stock=stock_frame
                                            ), 
                      relief="ridge", 
                      borderwidth=1, 
                      border=1)
    prev_btn.place(x=530, y=10)
    
    openfile_btn = Button(rekap_paned, 
                      text='Open File', 
                      width=10, 
                      command=lambda : open_file(frame_rekap=rekap_frame, 
                                                 frame_sjwh=wh_frame, 
                                                 frame_stock=stock_frame), 
                      relief="ridge", 
                      borderwidth=1, 
                      border=1)
    openfile_btn.place(x=10, y=495)

    openfolder_btn = Button(rekap_paned, 
                      text='Open Folder', 
                      width=10, 
                      command=dummy, 
                      relief="ridge", 
                      borderwidth=1, 
                      border=1)
    openfolder_btn.place(x=95, y=495)

    def switch():
        global FILE_OPEN
        
        if FILE_OPEN: 
            show_rekap(mode=switch_var.get(), frame=rekap_frame)
        else:
            return 0

    switch_var = customtkinter.StringVar(value='off')
    switch_btn = customtkinter.CTkSwitch(rekap_paned,
                                         text = "",
                                         command=switch,
                                         onvalue='on',
                                         offvalue='off',
                                         variable=switch_var,
                                         state=DISABLED
                                         )
    switch_btn.place(x=530, y= 495)

    wh_paned = PanedWindow(bd=2, relief="groove")
    wh_paned.place(x=615, y=10, width=575, height=260)
    wh_frame = Frame(wh_paned, width=560, height=210, background='#cccbca', relief="groove", border=1)
    wh_frame.place(x=5, y=10)
    wh_label = Label(root, text="SJ WH")
    wh_label.place(x=1130, y=0)
    wh_filter_label = Label(wh_paned, text='Filter  : ')
    wh_filter_label.place(x=10, y=228)
 
    wh_search = Entry(wh_paned, width=20)
    wh_search.place(x=60, y=228)
    wh_search_btn = Button(wh_paned, 
                           text='Search', 
                           width=6, 
                           command=lambda : search(frame=wh_frame, seach_value=str(wh_search.get())), 
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

    def combo_click(event):
        global TABLE_STOCK, FILE_OPEN

        filter_value = str(stock_combobox.get())
        if FILE_OPEN:
            TABLE_STOCK.show(filter=filter_value)
        else:
            return 0

    stock_combobox_options = ['', 'Adjust In ', 'Adjust Out ', 'Sold ', 'Uknown']
    stock_combobox = ttk.Combobox(stock_paned, values=stock_combobox_options)
    stock_combobox.current(0)
    stock_combobox.bind("<<ComboboxSelected>>",combo_click)
    stock_combobox.place(x=60, y=225)

    my_tree = ttk.Treeview(rekap_frame)

    ## --- MENU BAR --------------------------------------------------------
    my_menu = Menu(root)

    file_menu = Menu(my_menu, tearoff=False)
    my_menu.add_cascade(label='File', menu=file_menu)
    file_menu.add_command(label='Open File ...        ', 
                          command=lambda : open_file(frame_rekap=rekap_frame, 
                                                     frame_sjwh=wh_frame, 
                                                     frame_stock=stock_frame
                                                    ))
    file_menu.add_command(label='Open Folder ...      ', command=lambda : open_folder(frame_rekap=rekap_frame,
                                                                                      frame_sjwh=wh_frame,
                                                                                      frame_stock=stock_frame))
    file_menu.add_separator()
    file_menu.add_command(label='Save                 ', command=save_file)
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