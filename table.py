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

        for i in range(df.shape[0]):
            if type(df.iloc[i]['PLU Number Barcode']) != str:
                end_point = i
                break
        
        df = df.iloc[:end_point]
            
        self.TABLE_ORIGINAL = df
        self.TABLE_OUTPUT = df[['PLU Number Barcode', 'PLU Name Item Menu', 'IN-RAPTOR', 'IN -SJ WH']]
    
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
            else:
                my_tree.column(column, width=70)
        # Set up all rows
        df_rows = self.TABLE_OUTPUT.to_numpy().tolist()
        
        if mode == "off":
            for i, row in enumerate(df_rows):
                if row[2] != row[3]:
                    # print(row)
                    my_tree.insert("", "end", values=row, tags="red")
                else:
                    my_tree.insert("", "end", values=row, tags="white")
        
        elif mode == "on":
            for i, row in enumerate(df_rows):
                if row[2] != row[3]:
                    # print(row)
                    my_tree.insert("", "end", values=row, tags="red")
                else:
                    continue

        my_tree.tag_configure("red", background="#fa9898")
                    
        my_tree.pack(expand=True, fill='both')
        my_tree.place(x=0, y=0, width=585, height=445)
            
        scroll_y = Scrollbar(my_tree, orient='vertical', command=my_tree.yview)
        scroll_y.place(relx=1, rely=0, relheight=1, anchor='ne')

        scroll_x = Scrollbar(my_tree, orient='horizontal', command=my_tree.xview)
        scroll_x.pack(side='bottom', fill='x')

        my_tree.configure(xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

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