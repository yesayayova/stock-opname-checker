import pandas as pd
import numpy as np
from tkinter import *
from tkinter import filedialog, ttk

class Rekap:
    TABLE_ORIGINAL = pd.DataFrame([[]])
    TABLE_OUTPUT = pd.DataFrame([[]])
    FRAME = ""

    def __init__(self, path, frame):
        self.FRAME = frame

        df = pd.read_excel(path, sheet_name='REKAP MUTASI')

        for i in range(7):
            df.drop(i, inplace=True)
        df.reset_index(drop=True, inplace=True)

        new_columns = df.iloc[0].values
        new_columns[1] = 'PLU Number Barcode'
        new_columns[2] = 'PLU Name Item Menu'
        df.columns = new_columns 
        df.drop(0, inplace=True)
        df.reset_index(drop=True, inplace=True)

        end_point = 0
        list_selisih = []
        list_id = []

        for i in range(df.shape[0]):
            if type(df.iloc[i]['PLU Number Barcode']) != str:
                end_point = i
                break
            list_selisih.append(df.loc[i, 'IN-RAPTOR'] - df.loc[i, 'IN -SJ WH'])
            list_id.append(i)

        
        df = df.iloc[:end_point]
        df['Selisih'] = list_selisih
        df['ID'] = list_id
            
        self.TABLE_ORIGINAL = df
        self.TABLE_OUTPUT = df[['ID', 'PLU Number Barcode', 'PLU Name Item Menu', 'IN-RAPTOR', 'IN -SJ WH', 'Selisih']]

        # ket_selisih = []
        # for i in range(self.TABLE_ORIGINAL.shape[0]):
        #     ket_selisih.append(self.TABLE_ORIGINAL.iloc[i]['IN-RAPTOR'] - self.TABLE_ORIGINAL.iloc[i]['IN -SJ WH'])
        
        # self.TABLE_OUTPUT.loc[:, 'KET SELISIH'] = ket_selisih
    
    def get_table_original(self):
        return self.TABLE_ORIGINAL
    
    def get_table_output(self):
        return self.TABLE_OUTPUT
    
    def edit_table(self, raptor, sjwh, id):
        self.TABLE_ORIGINAL.loc[id, 'IN-RAPTOR'] = raptor
        self.TABLE_ORIGINAL.loc[id, 'IN -SJ WH'] = sjwh
        self.TABLE_OUTPUT.loc[id, 'IN-RAPTOR'] = raptor
        self.TABLE_OUTPUT.loc[id, 'IN -SJ WH'] = sjwh

    def show(self, mode="off"):
        my_tree = ttk.Treeview(self.FRAME)

        # Clear old treeview
        my_tree.delete(*my_tree.get_children())

        # Set up new tree
        my_tree['column'] = list(self.TABLE_OUTPUT.columns)
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
        df_rows = self.TABLE_OUTPUT.to_numpy().tolist()
        
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
        
        def save(id, wh, raptor, top):
            print(wh, raptor)

            id = int(id)
            self.TABLE_ORIGINAL.loc[id, ('IN-RAPTOR')] = raptor
            self.TABLE_ORIGINAL.loc[id, ('IN -SJ WH')] = wh

            self.TABLE_OUTPUT.loc[id, ('IN-RAPTOR')] = raptor
            self.TABLE_OUTPUT.loc[id, ('IN -SJ WH')] = wh

            my_tree = ttk.Treeview(self.FRAME)

            # Clear old treeview
            my_tree.delete(*my_tree.get_children())

            # Set up new tree
            my_tree['column'] = list(self.TABLE_OUTPUT.columns)
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
            df_rows = self.TABLE_OUTPUT.to_numpy().tolist()
            
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

            top.destroy()

        def edit():
            selected_item = my_tree.selection()
            data = my_tree.item(selected_item, 'values')

            top = Toplevel()
            top.title("Edit Data")
            top.geometry("300x200")
            top.resizable(False, False)

            plu_label =    Label(top, text='PLU Number    :')
            plu_label.place(x=10, y=10)
            plu_entry =    Label(top, text=data[1])
            plu_entry.place(x=100, y=10)

            name_label =   Label(top, text='Product Name :')
            name_label.place(x=10, y=45)
            name_entry =   Label(top, text=data[2])
            name_entry.place(x=100, y=45)

            raptor_label = Label(top, text='In-Raptor          :')
            raptor_label.place(x=10, y=80)
            raptor_entry = Entry(top, width=30)
            raptor_entry.insert(0, data[3])
            raptor_entry.place(x=100, y=80)
            
            wh_label =     Label(top, text='SJ - WH             :')
            wh_label.place(x=10, y=115)
            wh_entry = Entry(top, width=30)
            wh_entry.insert(0, data[4])
            wh_entry.place(x=100, y=115)

            save_btn = Button(top, 
                              text="Save", 
                              command=lambda : save(
                                    id=data[0],
                                    wh=wh_entry.get(),
                                    raptor=raptor_entry.get(),
                                    top = top
                              ), 
                              width=10)
            save_btn.place(x=180, y=155)

        def popup(event):
            # Menampilkan popup hanya jika ada item yang dipilih
            if my_tree.selection():
                popup_menu.post(event.x_root, event.y_root)

        popup_menu = Menu(self.FRAME, tearoff=0)
        popup_menu.add_command(label="Edit", command=edit)

        my_tree.bind("<Button-3>", popup)

class SJWH:
    TABLE = pd.DataFrame([[]])
    FRAME = ""

    def __init__(self, path, frame):
        self.FRAME = frame

        df = pd.read_excel(path, sheet_name='8SJ WH')
        df = df.iloc[:, 1:8]
        df['Sales No.'] = df['Sales No.'].astype(str)

        id_not_digit = []

        for i in range(df.shape[0]):
            value = df.iloc[i]['Sales No.']
            
            if not(value.isdigit()):
                id_not_digit.append(i)

        for i in id_not_digit:
            df.drop(i, inplace=True)

        df.reset_index(drop=True, inplace=True)
        df = df.fillna("-")

        self.TABLE = df
    
    def show(self, search=""):
        my_tree = ttk.Treeview(self.FRAME)

        # Clear old treeview
        my_tree.delete(*my_tree.get_children())

        # Set up new tree
        my_tree['column'] = list(self.TABLE.columns)
        my_tree['show'] = "headings"
        
        # Set up all column names
        for column in my_tree['column']:        
            my_tree.heading(column, text=column, anchor=W)
            if 'No. From Customer' in column:
                my_tree.column(column, width=220)
            else:
                my_tree.column(column, width=50)
        # Set up all rows
        df_rows = self.TABLE.to_numpy().tolist()

        if search == "":
            for row in df_rows:
                my_tree.insert("", "end", values=row, tags="row")

        else:
            for row in df_rows:
                if search.upper() in row[2]:
                    my_tree.insert("", "end", values=row, tags="row")
                else:
                    continue
                        
        my_tree.pack(expand=True, fill='both')
        my_tree.place(x=0, y=0, width=560, height=215)
            
        scroll_y = Scrollbar(my_tree, orient='vertical', command=my_tree.yview)
        scroll_y.place(relx=1, rely=0, relheight=1, anchor='ne')

        scroll_x = Scrollbar(my_tree, orient='horizontal', command=my_tree.xview)
        scroll_x.pack(side='bottom', fill='x')

        my_tree.configure(xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
    
    def get_filter_options(self):
        return list(self.TABLE["No. From Customer"].unique())

class Stock:
    TABLE = pd.DataFrame([[]])
    FRAME = ""

    def __init__(self, path, frame):
        self.FRAME = frame

        df = pd.read_excel(path, sheet_name='6st pos1')

        for i in range(8):
            df.drop(i, inplace=True)
        df.reset_index(drop=True, inplace=True)

        df = df.iloc[:, :11]

        df.columns = df.iloc[0].values
        df.drop(0, inplace=True)
        df.fillna("Uknown", inplace=True)

        self.TABLE = df
    
    def show(self, filter=""):
        my_tree = ttk.Treeview(self.FRAME)

        # Clear old treeview
        my_tree.delete(*my_tree.get_children())

        # Set up new tree
        my_tree['column'] = list(self.TABLE.columns)
        my_tree['show'] = "headings"
            
        # Set up all column names
        for column in my_tree['column']:        
            my_tree.heading(column, text=column, anchor=W)
            if 'PLU' in column:
                my_tree.column(column, width=140)
            else:
                my_tree.column(column, width=70)
        # Set up all rows
        df_rows = self.TABLE.to_numpy().tolist()

        if filter == "":
            for row in df_rows:
                my_tree.insert("", "end", values=row, tags="row")
        else:
            for row in df_rows:
                if row[3] == filter:
                    my_tree.insert("", "end", values=row, tags="row")
                else:
                    continue
                    
        my_tree.pack(expand=True, fill='both')
        my_tree.place(x=0, y=0, width=560, height=215)
            
        scroll_y = Scrollbar(my_tree, orient='vertical', command=my_tree.yview)
        scroll_y.place(relx=1, rely=0, relheight=1, anchor='ne')

        scroll_x = Scrollbar(my_tree, orient='horizontal', command=my_tree.xview)
        scroll_x.pack(side='bottom', fill='x')

        my_tree.configure(xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

    def get_filter_options(self):
        return list(self.TABLE["Trans Type"].unique())