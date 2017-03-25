#!/usr/bin/python3

from Tkinter import *
#from minesweeper import *

class App(Frame):
	def __init__(self, tk, grid, x_size=9, y_size=9):
		Frame.__init__(self, tk)
		self.Tk = tk
		self._grid = None
		self.x_size, self.y_size = x_size, y_size
		self._buttons = []
		
		for x in range(10, self.x_size+10):
			row = []
			for y in range(10, self.y_size+10):
				row.append(self.make_button(x, y))
			self._buttons.append(row)
		
		#self.grid = grid
		
				
	def make_button(self, x, y):
		b = Button(self, text=' ')
		b.grid(row=x, column=y, padx=1, pady=1)
		return b
	
	@property
	def grid(self, value):
		assert isinstance(value, Grid)
		assert self.x_size == value.x_size
		assert self.y_size == value.y_size
		
		for x in range(self.x_size):
			for y in range(self.y_size):
				self.set_button(x, y, str(value.grid(x, y)))

def main():
	tk = Tk()
	app = App(tk, [])
	app.grid(0, 0, padx=5, pady=5)
	tk.mainloop()

if __name__ == "__main__":
	main()
