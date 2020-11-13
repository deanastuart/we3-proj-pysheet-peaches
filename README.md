# PySheet
a simple python spread sheet.

It uses [https://docs.python.org/3/library/tkinter.html](TKinter) as a ways to runs windows, cells, I/O, etc.

Implement this code; make a working spreadsheet.

Figure out why you need a ChainMap and what it does.

### What's it supposed to do?

You can click on cells to edit their formulae and move around with the arrow keys. Formulae are evaluated once you press Return or navigate way from a cell. 

Every cell is evaluated as a Python expression. This means you don't do the Excel thing of having formulae start with =. Everything is a formula. So the formula in A2 in the screenshot above is valid and will evaluate to 1 once focus moves away from the cell. The math module is imported by default, so you can use sin and cos and so on. 

It uses a very cheap and nasty call of **eval()** to make it all work, which you should never do for production code. (wanna guess why?)

Other than using **eval()**, it also plays a little fast and loose with the way objects are allowed to touch each other in the code. 
It should allow each cell to access all their siblings directly instead of going through an intermediary. (Wait, what's a sibling in a spreadsheet sense).

It probably also breaks a couple of other OO rules along the way with the way the cells propagate their calculations when they are changed.

Think through WHY and HOW when you change a single cell's formula, it needs to both re-calculate itself, and all other cells that depend on it, and how when references to other cells change within a cells, how that will propagate and cause a series of re-calculations.

You will probably also want to comment out stuff to get it running to get a feel for how it will work WITHOUT and "logic" behind each cell.
So, get it to a point where you can edit a cell, but when you type "return" no calculations happen (yet).

Is there any way to unit test ANY of this code?

How could you test this code?

### Load/Save

are extra credit. You *may* have to learn more about tkinter to be able to create the UI needed to implement those.
