import json
from tkinter import *
from anytree import AnyNode
import psycopg2
import copy
from annotation import Annotation
from treelib import Node, Tree
import sqlparse

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


class TreeFrame(Frame):
    def __init__(self, root):
        Frame.__init__(self, root)
        self.canvas = Canvas(self, background='#c5ded2')
        self.canvas.grid(row=0, column=1)

        # label
        # self.query_label = tk.Label(self, text='Click on the\n node to view \n analysis!', font = self.label_font, bg='#c5ded2')
        # self.query_label.grid(sticky=tk.N+ tk.W, row=0, column = 1, padx=12, pady=(12, 0))

        self._on_hover_listener = None
        self._on_click_listener = None
        self._on_hover_end_listener = None

    def draw_tree(self, tree):
        root_node = tree.get_node(tree.root)
        bbox = self._draw_node(root_node, tree, 12, 12)
        self.canvas.configure(
            width=bbox[2] - bbox[0] + 24, height=bbox[3] - bbox[1] + 24)

    def set_on_hover_listener(self, on_hover_listener):
        self._on_hover_listener = on_hover_listener

    def set_on_click_listener(self, on_click_listener):
        self._on_click_listener = on_click_listener

    def set_on_hover_end_listener(self, on_hover_end_listener):
        self._on_hover_end_listener = on_hover_end_listener

    def _on_click(self, node):
        if self._on_click_listener is not None:
            self._on_click_listener(node)

    def _on_hover(self, node):
        if self._on_hover_listener is not None:
            self._on_hover_listener(node)

    def _on_hover_end(self, node):
        if self._on_hover_end_listener is not None:
            self._on_hover_end_listener(node)

    def _draw_node(self, node, tree, x1, y1):
        child_x = x1
        left = x1
        right = -1
        top = y1
        bottom = -1
        button = Button(self.canvas, text=node.tag, padx=12,
                        bg='#7d8ed1', fg='white', anchor='center')
        button.bind('<Button-1>', lambda event: self._on_click(node))
        button.bind('<Enter>', lambda event: self._on_hover(node))
        button.bind('<Leave>', lambda event: self._on_hover_end(node))
        window = self.canvas.create_window(
            (x1, y1), window=button, anchor='nw')
        bbox = self.canvas.bbox(window)
        child_bboxes = []

        children = tree.children(node.identifier)
        if len(children) == 0:
            return bbox
        for child in children:
            child_bbox = self._draw_node(
                child, tree, child_x, y1 + 60)  # (x1, y1, x2, y2)
            child_x = child_bbox[2] + 20
            right = max(right, child_bbox[2])
            bottom = max(bottom, child_bbox[3])
            child_bboxes.append(child_bbox)
        x_mid = (left + right) // 2
        bbox_mid_x = (bbox[0] + bbox[2]) // 2
        self.canvas.move(window, x_mid - bbox_mid_x, 0)
        for child_bbox in child_bboxes:
            child_mid_x = (child_bbox[0] + child_bbox[2]) // 2
            self.canvas.create_line(
                x_mid, bbox[3], child_mid_x, child_bbox[1], width=2, arrow=FIRST)
        return left, top, right, bottom


def run():
    # todo
    inputValue = queryBox.get('1.0', 'end-1c')

    conn = None
    x = None
    try:
        # connect to postgres in this format
        conn = psycopg2.connect(
            host="localhost",
            database="TPC-H",
            user="postgres",
            password="root")

        cur = conn.cursor()
        cur.execute(
            "SET+ checkQueries EXPLAIN (ANALYZE, VERBOSE, FORMAT JSON)" + inputValue)
        rows = cur.fetchall()
        x = json.dumps(rows)

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    print("success")
    plan_QEP = x
    plan_QEP = plan_QEP[2:-2]

    plan_QEP = json.loads(plan_QEP)

    # top_level = tk.Toplevel(root_widget)

    # top_level.title('Visualization')
    # top_level.iconphoto(False, tk.PhotoImage(file='tree.png'))
    inputValue = inputValue.replace('\n', ' ')
    inputValue = sqlparse.format(
        inputValue, reindent=True, keyword_case='upper')

    # query_frame = QueryFrame(top_level)
    # query_frame.set_query(query)

    # query_frame.grid(row=0, column=0, sticky='ew')

    annotation = Annotation()
    treeQEP = Tree()
    treeQEP = annotation.buildTree([plan_QEP[0]['Plan']], treeQEP)
    treeQEP_highlight = annotation.matchNodeToQuery(treeQEP, inputValue)
    treeQEP_annotation = annotation.annotate(treeQEP, inputValue)
    qepGraphicframe.draw_tree(treeQEP)

    def on_click_listener(node):
        if node.identifier in treeQEP_annotation:
            qepAnnotationBox.show_node_annotation(
                treeQEP_annotation[node.identifier])

    def on_hover_listener(node):
        if node.identifier in treeQEP_highlight:
            for pos in treeQEP_highlight[node.identifier]:
                queryBox.tag_add(pos[0], pos[1], node.tag)

    def on_hover_end_listener(node):
        queryBox.tag_remove(node, '1.0', 'end')

    qepGraphicframe.set_on_click_listener(on_click_listener)
    qepGraphicframe.set_on_hover_listener(on_hover_listener)
    qepGraphicframe.set_on_hover_end_listener(on_hover_end_listener)

    return x

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

### ======================================= ###

### Dividers ###
divider = Label(root, text="________", padx=0, pady=0)
divider1 = Label(root, text="________", padx=0, pady=0)
divider2 = Label(root, text="________", padx=0, pady=0)
divider3 = Label(root, text="________", padx=0, pady=0)
divider4 = Label(root, text="________", padx=0, pady=0)
divider5 = Label(root, text="________", padx=0, pady=0)

### ======================================= ###


### Query Plan ###
qepLabel = Label(root, text="Query Execution Plan:", padx=5, pady=1)
qepAnnotationBox = Text(root, width=75, height=4,
                        state="disabled", bg='lightgray')
qepGraphicframe = TreeFrame(root)
# dummyQepButton = Button(qepGraphicframe, text="QEP", fg="red").pack()

aqpLabel = Label(root, text=" Alternate Query Plans:", padx=5, pady=1)
aqpAnnotationBox = Text(root, width=75, height=4,
                        state="disabled", bg='lightgray')
aqpGraphicframe = Frame(root)
dummyAqpButton = Button(aqpGraphicframe, text="AQP", fg="red").pack()

### ======================================= ###

### Grid System ###


runButton.grid(row=1, column=1, columnspan=1)
clearButton.grid(row=2, column=1, columnspan=1)
cb_hj.grid(row=0, column=0, padx=10, pady=1)
cb_mj.grid(row=1, column=0, padx=10, pady=1)
cb_is.grid(row=2, column=0, padx=10, pady=1)
cb_bms.grid(row=3, column=0, padx=10, pady=1)
queryLabel.grid(row=0, column=3, sticky="W")
queryBox.grid(row=1, column=3, rowspan=3, columnspan=3, padx=5, pady=2)

qepLabel.grid(row=5, column=0, columnspan=2, sticky="w")
qepAnnotationBox.grid(row=6, column=0, columnspan=4, padx=5, pady=2)
qepGraphicframe.grid(row=7, column=0, columnspan=4, padx=5, pady=2)

aqpLabel.grid(row=5, column=4, columnspan=2, sticky="w")
aqpAnnotationBox.grid(row=6, column=4, columnspan=3, padx=5, pady=2)
aqpGraphicframe.grid(row=7, column=4, columnspan=3, padx=5, pady=2)

### ======================================= ###


root.mainloop()
