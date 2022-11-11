import json
from tkinter import *
import node_types
from annotation import Annotation
from treelib import Tree
import sqlparse
from preprocessing import Preprocessing


def init_ui():
    root = Tk()
    root.title('Project 2: Query Plan')
    root.geometry('1280x900')
    root.resizable(False, False)

    ###  GUI for Query ###
    class QueryFrame(Frame):
        def __init__(self, root):
            Frame.__init__(self, root)
            self.text = Text(self, width=130, height=6)
            self.text.grid(row=0, column=0)
            self.scrollbar = Scrollbar(
                self, orient='vertical', command=self.text.yview)
            self.scrollbar.grid(row=0, column=1, sticky='ns')
            self.text.configure(yscrollcommand=self.scrollbar.set)

            self.text.tag_configure(
                'OTHER', background='#fbef7f', foreground='black')

            self.index_map = {}
            self.query = None

        def set_query(self, query):
            self.query = query
            self.text.delete('1.0', 'end')
            self.text.insert('end', query)

            self.index_map = {}
            line = 1
            column = 0
            index = 0
            while index <= len(query):
                self.index_map[index] = f'{line}.{column}'
                if index < len(query) and query[index] == '\n':
                    line += 1
                    column = 0
                else:
                    column += 1
                index += 1

        def highlight_text(self, start, end, node_type):
            if node_type in node_types.NODE_TYPES:
                self.text.tag_add(
                    node_type, self.index_map[start], self.index_map[end])
            else:
                self.text.tag_add(
                    'OTHER', self.index_map[start], self.index_map[end])

        def clear_highlighting(self):
            for node_type in node_types.NODE_TYPES + ['OTHER']:
                self.text.tag_remove(node_type, '1.0', 'end')

        def get_text(self):
            return self.text.get('1.0', 'end-1c')

        def clear_text(self):
            self.text.delete('1.0', END)

    ### ======================================= ###

    ###  GUI for annotation ###

    class AnnotationFrame(Frame):
        def __init__(self, root):
            Frame.__init__(self, root)
            Font_tuple = ("Calibri", 12, "bold")
            self.text = Text(self, width=75, height=5)

            self.text.grid(row=1, column=0)
            self.scrollbar = Scrollbar(
                self, orient='vertical', command=self.text.yview)
            self.scrollbar.grid(row=1, column=1, sticky='ns')
            self.text.configure(yscrollcommand=self.scrollbar.set,
                                state="disabled", bg='grey', fg='white', font=Font_tuple)

            self.text.tag_configure(
                'OTHER', background='#fbef7f', foreground='black')

            self.index_map = {}
            self.query = None

        def show_node_annotation(self, annotation):
            self.text.configure(state="normal")
            self.text.delete('1.0', 'end')
            print(annotation)
            self.text.insert(INSERT, annotation)
            self.text.configure(state="disabled")

        def clear_text(self):
            print("executed clear annottation")
            self.text.configure(state="normal")
            self.text.delete('1.0', 'end-1c')
            self.text.configure(state="disabled")

    ### ======================================= ###

    ###  GUI for Query Graphic ###
    class QueryGraphicFrame(Frame):
        def __init__(self, root):
            Frame.__init__(self, root)
            self.canvas = Canvas(self, background='#a3b9cd')
            self.canvas.grid(row=0, column=1)
            self.canvas.config(width=500, height=500)
            self.scrollbar = Scrollbar(
                self, orient='vertical', command=self.canvas.yview)
            self.scrollbar.grid(row=0, column=2, sticky='e')

            self._on_hover_listener = None
            self._on_click_listener = None
            self._on_hover_end_listener = None

        def draw_tree(self, tree, highlight, annotation, annotationBox):
            root_node = tree.get_node(tree.root)
            bbox = self._draw_node(root_node, tree, highlight,
                                   annotation, annotationBox, 12, 12)
            self.canvas.configure(
                width=bbox[2] - bbox[0] + 24, height=bbox[3] - bbox[1] + 24)

        def set_on_hover_listener(self, on_hover_listener, highlight):
            self._on_hover_listener = on_hover_listener

        def set_on_click_listener(self, on_click_listener, annotation, annotationBox):
            self._on_click_listener = on_click_listener

        def set_on_hover_end_listener(self, on_hover_end_listener):
            self._on_hover_end_listener = on_hover_end_listener

        def _on_click(self, node, annotation, annotationBox):
            if self._on_click_listener is not None:
                self._on_click_listener(node, annotation, annotationBox)

        def _on_hover(self, node, highlight):
            if self._on_hover_listener is not None:
                self._on_hover_listener(node, highlight)

        def _on_hover_end(self, node):
            if self._on_hover_end_listener is not None:
                self._on_hover_end_listener(node)

        def _draw_node(self, node, tree, highlight, annotation, annotationBox, x1, y1):
            child_x = x1
            left = x1
            right = -1
            top = y1
            bottom = -1
            button = Button(self.canvas, text=node.tag, padx=12,
                            bg='#7d8ed1', fg='white', anchor='center')
            button.bind('<Button-1>', lambda event: self._on_click(node,
                        annotation, annotationBox))
            button.bind(
                '<Enter>', lambda event: self._on_hover(node, highlight))
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
                    child, tree, highlight, annotation, annotationBox, child_x, y1 + 60)  # (x1, y1, x2, y2)
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

    ### ======================================= ###

    ###  Utility Functions ###

    def getAQPConfig():
        result = {'enable_hashjoin': enable_hashjoin.get(), 'enable_mergejoin': enable_mergejoin.get(),
                  'enable_indexscan': enable_indexscan.get(), 'enable_seqscan': enable_seqscan.get()}

        return result

    def clear_nodes():
        for widgets in qepGraphicframe.winfo_children():
            widgets.destroy()
        for widgets in aqpGraphicframe.winfo_children():
            widgets.destroy()
        qepGraphicframe.__init__(root)
        aqpGraphicframe.__init__(root)
        qepGraphicframe.grid(row=7, column=0, columnspan=4, padx=5, pady=2)
        aqpGraphicframe.grid(row=7, column=4, columnspan=3, padx=5, pady=2)

    def run():
        inputValue = queryBox.get_text()
        if (len(inputValue.strip()) == 0):
            return
        qepAnnotationBox.clear_text()
        aqpAnnotationBox.clear_text()
        clear_nodes()
        json_QEP, json_AQP = Preprocessing.get_json(inputValue, getAQPConfig())

        plan_QEP = json_QEP
        plan_QEP = plan_QEP[2:-2]

        plan_QEP = json.loads(plan_QEP)

        plan_AQP = json_AQP
        plan_AQP = plan_AQP[2:-2]

        plan_AQP = json.loads(plan_AQP)

        inputValue = inputValue.replace('\n', ' ')
        inputValue = sqlparse.format(
            inputValue, reindent=True, keyword_case='upper')

        queryBox.set_query(inputValue)

        annotation = Annotation()
        treeQEP = Tree()
        treeQEP = annotation.buildTree([plan_QEP[0]['Plan']], treeQEP)
        treeQEP_highlight = annotation.matchNodeToQuery(treeQEP, inputValue)
        treeQEP_annotation = annotation.annotate(treeQEP, inputValue)
        qepGraphicframe.draw_tree(
            treeQEP, treeQEP_highlight, treeQEP_annotation, qepAnnotationBox)

        treeAQP = Tree()
        treeAQP = annotation.buildTree([plan_AQP[0]['Plan']], treeAQP)
        treeAQP_highlight = annotation.matchNodeToQuery(treeAQP, inputValue)
        treeAQP_annotation = annotation.annotate(treeAQP, inputValue)
        aqpGraphicframe.draw_tree(
            treeAQP, treeAQP_highlight, treeAQP_annotation, aqpAnnotationBox)

        def on_click_listener(node, annotation, annotationBox):
            if node.identifier in annotation:
                annotationBox.show_node_annotation(
                    annotation[node.identifier])

        def on_hover_listener(node, highlight):
            if node.identifier in highlight:
                for pos in highlight[node.identifier]:
                    queryBox.highlight_text(pos[0], pos[1], node.tag)

        def on_hover_end_listener(node):
            queryBox.clear_highlighting()

        qepGraphicframe.set_on_click_listener(
            on_click_listener, treeQEP_annotation, qepAnnotationBox)
        qepGraphicframe.set_on_hover_listener(
            on_hover_listener, treeQEP_highlight)
        qepGraphicframe.set_on_hover_end_listener(on_hover_end_listener)

        aqpGraphicframe.set_on_click_listener(
            on_click_listener, treeAQP_annotation, aqpAnnotationBox)
        aqpGraphicframe.set_on_hover_listener(
            on_hover_listener, treeAQP_highlight)
        aqpGraphicframe.set_on_hover_end_listener(on_hover_end_listener)

    def clear():
        queryBox.clear_text()
        qepAnnotationBox.clear_text()
        aqpAnnotationBox.clear_text()
        clear_nodes()
        pass

    ### ======================================= ###

    ### Checkbuttons ###

    enable_hashjoin = IntVar(value=1)
    cb_hj = Checkbutton(root, text="enable_hashjoin", variable=enable_hashjoin)

    enable_mergejoin = IntVar(value=1)
    cb_mj = Checkbutton(root, text="enable_mergejoin",
                        variable=enable_mergejoin)

    enable_indexscan = IntVar(value=1)
    cb_is = Checkbutton(root, text="enable_indexscan",
                        variable=enable_indexscan)

    enable_seqscan = IntVar(value=1)
    cb_bms = Checkbutton(root, text="enable_seqscan", variable=enable_seqscan)

    ### ======================================= ###

    ### Execution Buttons ###

    runButton = Button(root, text="Run", command=run)
    clearButton = Button(root, text="Clear", command=clear)

    ### ======================================= ###

    ### Inputs ###
    queryLabel = Label(root, text="Query:", padx=5, pady=0)
    queryBox = QueryFrame(root)
    qepAnnotationBox = AnnotationFrame(root)
    aqpAnnotationBox = AnnotationFrame(root)
    ### ======================================= ###

    ### Query Plan ###
    qepLabel = Label(root, text="Query Execution Plan:", padx=5, pady=1)
    qepGraphicframe = QueryGraphicFrame(root)

    aqpLabel = Label(root, text=" Alternate Query Plans:", padx=5, pady=1)
    aqpGraphicframe = QueryGraphicFrame(root)

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
