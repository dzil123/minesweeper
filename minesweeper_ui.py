#!/usr/bin/python3

from minesweeper import *
from tkinter import *

size = 7.5
bd = 2
#	  #RGB

color = "#BFBFBF"

# irrelavent

fg = "#BFBFBF"
bg = "#BFBFBF" # BFBFBF # color of button

afg = "#BFBFBF"
abg = "#BFBFBF" # color when clicked on

hbg = "#BFBFBF"
hclr = "#BFBFBF"

# end irrelavent

pad = 0

t = Tk()
image = PhotoImage()

class App(Frame):
	def __init__(self, tk):
		super().__init__(tk, bg=color)
		self.make_widgets()
		self.state = [[False]*9]*9
	
	def make_widgets(self):
		self.make_button_grid()
	
	def l_press(self, x, y):
		print("Left: (%s, %s)" % (str(x), str(y)))
	
	def r_press(self, x, y):
		print("Right: (%s, %s)" % (str(x), str(y)))
	
	def generate_callback(self, x, y):
		def callback(event):
			#print('(' + str(x) + ', ' + str(y) + ') ' + str(type(event.type)))
			
			if event.type == EventType.Leave:
				self.buttons[x][y].config(bd=2)
				self.state[x][y] = False
			if (event.type == EventType.ButtonPress) and (event.num == 1):
				self.buttons[x][y].config(bd=0)
				self.state[x][y] = True
			if event.type == EventType.ButtonRelease and self.state[x][y]:
				self.buttons[x][y].config(bd=2)
				self.state[x][y] = False
				self.l_press(x, y)
			if (event.type == EventType.ButtonPress) and (event.num == 3):
				self.state[x][y] = False
				self.r_press(x, y)
			
		return callback
	
	def register_events(self, button, x, y): # Button-3, 
		callback = self.generate_callback(x, y)
		
		button.bind("<ButtonPress-1>", callback)
		button.bind("<ButtonRelease-1>", callback)
		button.bind("<Leave>", callback)
		button.bind("<ButtonPress-3>", callback)
	
	def make_button_grid(self, x_size=9, y_size=9, x_offset=None, y_offset=None):
		x_size, y_size = int(x_size), int(y_size)		
		
		if (x_offset is None):
			x_offset = 0
		x_offset = int(x_offset)
		if x_offset < 0:
			x_offset = 0
		
		if y_offset is None:
			y_offset = x_offset
		y_offset = int(y_offset)
		if y_offset < 0:
			y_offset = 0
		
		buttons = []
		for x in range(x_size):
			row = []
			for y in range(y_size):
				b = Button(self, image=image, compound=CENTER, text=' ', width=size, \
				height=size, bd=2, relief=RAISED, fg=color, bg=color, activebackground=color, activeforeground=color, takefocus=False)
				self.register_events(b, x, y)
				b.grid(row=x+x_offset, column=y+y_offset, padx=pad, pady=pad)#, ipadx=0, ipady=0)
				row.append(b)
			buttons.append(row)
		self.buttons = buttons
	

def main():
	#tk = Tk()
	#image = PhotoImage()
	app = App(t)
	app.grid()
	t.mainloop()

if __name__ == "__main__":
	main()
