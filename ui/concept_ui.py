import tkinter as tk
from tkinter import messagebox
from tkinter import *

def open_ui():
	top = tk.Tk()

	top.geometry("400x200")
	top.update()

	B1 = Button(top, text = "Go To Drawings", command = get_selected_drawing)

	B1.place(x = 200-(B1.winfo_width() / 2), y = 133-(B1.winfo_height()/2))
	B1.update()
	B1.place(x = 200-(B1.winfo_width() / 2), y = 133-(B1.winfo_height()/2))

	E1 = Entry(top, bd = 5)

	E1.pack( side = RIGHT )
	E1.place(x = 200-(E1.winfo_width() / 2), y = 80-(E1.winfo_height() / 2))
	E1.update()
	E1.place(x = 200-(E1.winfo_width() / 2), y = 80-(E1.winfo_height() / 2))

	top.mainloop()