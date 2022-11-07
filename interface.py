from tkinter import *

root = Tk()
root.title('Project 2: Query Plan')
root.geometry('1280x800')

ENABLE_HASHJOIN_QUERY = "query to append for enable"
DISABLE_HASHJOIN_QUERY = "query to append for disable"
ENABLE_MERGEJOIN_QUERY = "query to append for enable"
DISABLE_MERGEJOIN_QUERY = "query to append for disable"
ENABLE_INDEXSCAN_QUERY = "query to append for enable"
DISABLE_INDEXSCAN_QUERY = "query to append for disable"
ENABLE_BITMAPSCAN_QUERY = "query to append for enable"
DISABLE_BITMAPSCAN_QUERY = "query to append for disable"

# Function for run


def run():
    label = Label(root, text=enable_hashjoin.get())
    # label.pack()
    print(enable_hashjoin.get())
    # todo
    return

# Function for clear


def clear():
    # todo
    return

    ### Checkbuttons ###


enable_hashjoin = StringVar()
enable_hashjoin.set(ENABLE_HASHJOIN_QUERY)
cb_hj = Checkbutton(root, text="enable_hashjoin", variable=enable_hashjoin,
                    onvalue=ENABLE_HASHJOIN_QUERY, offvalue=DISABLE_HASHJOIN_QUERY)

enable_mergejoin = StringVar()
enable_mergejoin.set(ENABLE_MERGEJOIN_QUERY)
cb_mj = Checkbutton(root, text="enable_mergejoin", variable=enable_mergejoin,
                    onvalue=ENABLE_MERGEJOIN_QUERY, offvalue=DISABLE_MERGEJOIN_QUERY)

enable_indexscan = StringVar()
enable_indexscan.set(ENABLE_INDEXSCAN_QUERY)
cb_is = Checkbutton(root, text="enable_indexscan", variable=enable_indexscan,
                    onvalue=ENABLE_INDEXSCAN_QUERY, offvalue=DISABLE_INDEXSCAN_QUERY)

enable_bitmapscan = StringVar()
enable_bitmapscan.set(ENABLE_BITMAPSCAN_QUERY)
cb_bms = Checkbutton(root, text="enable_bitmapscan", variable=enable_bitmapscan,
                     onvalue=ENABLE_BITMAPSCAN_QUERY, offvalue=DISABLE_BITMAPSCAN_QUERY)

### ======================================= ###

### Execution Buttons ###

runButton = Button(root, text="Run", command=run)
clearButton = Button(root, text="Clear", command=clear)

### ======================================= ###

### Inputs ###
queryLabel = Label(root, text="Query:", padx=5, pady=0)
queryBox = Text(root, width=130, height=5)
annotationLabel = Label(root, text="Annotation:", padx=5, pady=0)
annotationBox = Text(root, width=155, height=5,
                     state="disabled", bg='lightgray')

### ======================================= ###

### Grid System ###


runButton.grid(row=1, column=1, columnspan=1)
clearButton.grid(row=2, column=1, columnspan=1)
cb_hj.grid(row=0, column=0, padx=10, pady=1)
cb_mj.grid(row=1, column=0, padx=10, pady=1)
cb_is.grid(row=2, column=0, padx=10, pady=1)
cb_bms.grid(row=3, column=0, padx=10, pady=1)
queryLabel.grid(row=0, column=3, sticky="W")
queryBox.grid(row=1, column=3, rowspan=3, padx=5, pady=2)
annotationLabel.grid(row=4, column=0, columnspan=4, sticky="W")
annotationBox.grid(row=5, column=0, columnspan=4, padx=5, pady=2)

### ======================================= ###

root.mainloop()
