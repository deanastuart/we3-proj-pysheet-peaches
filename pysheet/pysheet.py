
import pickle
import tkinter as tk
import re
from collections import ChainMap
import math
import yaml
import json

from tkinter.filedialog import asksaveasfile


#from numpy import save

Nrows = 5
Ncols = 5

cellre = re.compile(r'\b[A-Z][0-9]\b')


def cellname(i, j):
    return f'{chr(ord("A") + j)}{i + 1}'
    # returns a string translates col 0, row 0 to 'A1'


class Cell():
    def __init__(self, i, j, siblings, parent):
        # save off instance variables from arguments
        self.row = i
        self.col = j
        self.siblings = siblings
        # and also
        # set name to cellname(i, j)
        self.name = cellname(i, j)
        # set value of cell to zero
        self.value = 0
        # set formula to a str(value)
        self.formula = str(self.value)
        # Set of Dependencies - must be updated if this cell changes
        # make deps empty
        self.deps = set()
        # Set of Requirements - values required for this cell to calculate
        # make reqs empty
        self.reqs = set()

        # be happy you get this machinery for free.
        self.var = tk.StringVar()
        entry = self.widget = tk.Entry(parent,
                                       textvariable=self.var,
                                       justify='right')
        entry.bind('<FocusIn>', self.edit)
        entry.bind('<FocusOut>', self.update)
        entry.bind('<Return>', self.update)
        entry.bind('<Up>', self.move(-1, 0))
        entry.bind('<Down>', self.move(+1, 0))
        entry.bind('<Left>', self.move(0, -1))
        entry.bind('<Right>', self.move(0, 1))
        # set this cell's var to cell's value
        self.var.set(self.value)
        # and you're done.



    def move(self, rowadvance, coladvance):
        targetrow = (self.row + rowadvance) % Nrows
        targetcol = (self.col + coladvance) % Ncols

        def focus(self, event):
            targetwidget = self.siblings[cellname(targetrow, targetcol)].widget
            targetwidget.focus()

        return focus

    def calculate(self):
        # find all the cells mentioned in the formula.
        #  put them all into a tmp set currentreqs
        currentreqs = set(cellre.findall(self.formula))
        # Add this cell to the new requirement's dependents
        # removing all the reqs that we might no longer need
        # for each in currentreqs - self.reqs
        #    my siblings[].deps.add(self.name)
        for e in currentreqs - self.reqs:
            self.siblings[e].deps.add(self.name)
        # Add remove this cell from dependents no longer referenced
        # for each in self.reqs - currentreqs:
        #    my siblings[r].deps.remove(self.name)
        for e in self.reqs - currentreqs:
            self.siblings[e].deps.remove(self.name)

        # Look up the values of our required cells
        # reqvalues = a comprehension of r, self.siblings[r].value for r in currentreqs
        reqvalues = {r: self.siblings[r].value for r in currentreqs}
        # Build an environment with these values and basic math functions
        environment = ChainMap(math.__dict__, reqvalues)
        # Note that eval is DANGEROUS and should not be used in production
        self.value = eval(self.formula, {}, environment)
        # save currentreqs in self.reqs
        # set this cell's var to cell's value
        self.reqs = currentreqs
        self.var.set(self.value)

    def propagate(self):
        # for each of your deps
        #     calculate
        #     propogate
        for e in self.deps:
            self.siblings[e].calculate()
            self.siblings[e].propagate()

    def edit(self, event):
        # make sure to update the cell with the formula
        self.var.set(self.formula)
        self.widget.select_range(0, tk.END)

    def update(self, event):
        # get the value of this cell and put it in formula
        # calculate all dependencies
        # propogate to all dependecnies
        self.formula = self.var.get()
        self.calculate()
        self.propagate()
        # If this was after pressing Return, keep showing the formula
        if hasattr(event, 'keysym') and event.keysym == "Return":
            self.var.set(self.formula)

    def load(self, filename):
        pass


class SpreadSheet(tk.Frame):
    def __init__(self, rows=5, cols=5, master=None):
        super().__init__(master)
        self.rows = rows
        self.cols = cols
        self.cells = {}

        self.pack()
        self.create_widgets()

    def save1(self, filename):
        print(self.cells)
        data = {}
        for key in self.cells:
            data[key] = self.cells[key].value

        with open(filename, 'w') as outfile:
            yaml.dump(data, outfile)

    def create_widgets(self):
        # Frame for all the cells
        # tk.Button(text='Fetch').grid()
        self.cellframe = tk.Frame(self)
        self.cellframe.pack(side='top')

        # self.B = tk.Butt


        """files = [('All Files', '*.*'),
                 ('Python Files', '*.py'),
                 ('Text Document', '*.txt')]
"""

        self.B = tk.Button(root, text="Save", command=lambda: self.save1('test.yaml'))
        # Cell.save1(self, [self.rows, self.cols] , 'test.pickle'
        # (asksaveasfile(filetypes=files, defaultextension=files))
        self.C = tk.Button(root, text="Load")

        self.B.pack()
        self.C.pack()



        # Column labels
        blank = tk.Label(self.cellframe)
        blank.grid(row=0, column=0)
        for j in range(self.cols):
            label = tk.Label(self.cellframe, text=chr(ord('A') + j))
            label.grid(row=0, column=j + 1)

        # Fill in the rows
        for i in range(self.rows):
            rowlabel = tk.Label(self.cellframe, text=str(i + 1))
            rowlabel.grid(row=1 + i, column=0)
            for j in range(self.cols):
                cell = Cell(i, j, self.cells, self.cellframe)
                self.cells[cell.name] = cell
                cell.widget.grid(row=1 + i, column=1 + j)




root = tk.Tk()
app = SpreadSheet(Nrows, Ncols, master=root)



app.mainloop()
