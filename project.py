import json
import tkinter as tk
from tkinter import font, ttk, messagebox
from tkinter import *
from typing import Text
import interface
from node_types import ATTRIBUTE
import sqlparse
import node_types
import psycopg2
import annotation_node

#Function to retrieve SQL query text
def retrieveInput():
    inputValue = query_text.get('1.0', 'end-1c')
    return inputValue


if __name__ == '__main__':
    root = tk.Tk()
    root.title('Input Query')
# root.iconphoto(False, tk.PhotoImage(file='tree.png'))

    button_font = font.Font(family='Google Sans Display', size=12, weight='bold')
    text_font = font.Font(family='Fira Code Retina', size=12)
    label_font = font.Font(family='Google Sans Display', size=12)

    query_label = tk.Label(root, text='Enter your SQL query here', font=label_font)
    query_text = tk.Text(root, font=text_font, height=5, width=60)
    qep_label = tk.Label(root,text='QEP', font=label_font)
    qep_text = tk.Text(root, font=text_font, height=5, width=35)
    aqp_label = tk.Label(root,text='AQP', font=label_font)
    aqp_text = tk.Text(root, font=text_font, height=5, width=35)

# Draw RUN QEP button
    execute_button_QEP = tk.Button(root, text='RUN QEP', padx=0, bg='#FFF', fg='black', font=button_font,
                               anchor='center', command=lambda: interface.get_json(retrieveInput()))

# Draw the RUN AQP button
    execute_button_AQP = tk.Button(root, text='RUN AQP', padx=0, bg='#FFF', fg='black', font=button_font,
                               anchor='center', command=lambda: interface.get_json(retrieveInput(), False))
    
#Styling of Items
    query_label.grid(row=4,rowspan=1, column =1,columnspan=1, sticky='nw', padx=0, pady=0)
    query_text.grid(row=5,rowspan=1, column=1,columnspan=1, padx=0, pady=0, sticky='nw')
    qep_label.grid(row=6,rowspan=1, column =0, columnspan=2, sticky='nw', padx=20, pady=0)
    qep_text.grid(row=7,rowspan=1, column=0,columnspan=2, padx=20, pady=0, sticky='nw')
    aqp_label.grid(row=6,rowspan=1, column =0, columnspan=2, sticky='ne', padx=0, pady=0)
    aqp_text.grid(row=7, rowspan=1,column=0,columnspan=2, padx=0, pady=0, sticky='ne')
    execute_button_QEP.grid(row=3,rowspan=1, column=1,columnspan=1, sticky='nw', padx=0, pady=0)
    execute_button_AQP.grid(row=3,rowspan=1,column=1,columnspan=1, sticky='nw', padx=100, pady=0)

# Button execution to execute function
    execute_button_QEP.bind('<Button-1>', lambda event: interface.execute_query(root, retrieveInput()))
    execute_button_AQP.bind('<Button-2>', lambda event: interface.execute_query_AQP(root, retrieveInput()))

#Scrollbar feature
    # query_scrollbar = tk.Scrollbar(root, orient='vertical', command=query_text.yview)
    # query_text.configure(yscrollcommand=query_scrollbar.set)
    # query_scrollbar.grid(row=5, column=6, sticky='ne', padx=0)

# Checkbox Feature
    def var_states():
        print("HashJoin %d,\nIndexScan %d,\nMergeJoin %d,\BitMapScan %d" % (var1.get(), var2.get(), var3.get(), var4.get()))

    Label(root, text="AQP Configuration").grid(row=4, columnspan=1, sticky=NW, padx=20)
    var1 = IntVar()
    Checkbutton(root, text="enable_hashjoin", variable=var1).grid(row=5,rowspan=1, columnspan=1, sticky=NW, padx=20)
    var2 = IntVar()
    Checkbutton(root, text="enable_indexscan", variable=var2).grid(row=5,rowspan=1,columnspan=1, sticky=NW, padx=20, pady=25)
    var3 = IntVar()
    Checkbutton(root, text="enable_mergejoin", variable=var3).grid(row=5,rowspan=1,columnspan=1,sticky=NW, padx=20, pady=50)
    var4 = IntVar()
    Checkbutton(root, text="enable_bitmapscan", variable=var4).grid(row=5,rowspan=1,columnspan=1, sticky=NW, padx=20, pady=75)

    #Button(root, text='Quit', command=root.quit).grid(row=5, sticky=W, pady=1)
    #Button(root, text='Show', command=var_states).grid(row=6, sticky=W, pady=1)
    
    root.mainloop()

