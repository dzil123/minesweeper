#!/usr/bin/python3

from minesweeper import *
from tkinter import *
import random

size = 8
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
ipad = 1

t = Tk()
default_image = PhotoImage()
image_1 = PhotoImage(file="1.png")
'''
def l_press(x, y):
	print("Left: (%s, %s)" % (str(x), str(y)))
	#self.buttons[x][y].config(state=DISABLED, image=image_1)

def r_press(x, y):
	print("Right: (%s, %s)" % (str(x), str(y)))
'''
class Tile(Button):
	IMAGE_1 = PhotoImage(file="1.png")
	def __init__(self, master, x, y, app=None):
		
		self.frame = Frame(master, bd=0, relief=FLAT, bg="#888", width=16, height=16)
		self.frame.grid(row=x, column=y, padx=0, pady=0, ipadx=0, ipady=0, sticky=N+S+E+W)
		self.frame.grid_propagate(False)
		
		super().__init__(self.frame, image=default_image, compound=CENTER, \
			width=size, height=size, bd=2, relief=RAISED, bg=color, \
			activebackground=color, activeforeground=color, takefocus=False)
		
		self.grid(row=0, column=0, padx=0, pady=0, ipadx=ipad, ipady=ipad, sticky=E+S)
		
		self.x, self.y = x, y
		
		if app is None:
			app = master
		
		self.app = app
		self.state = False
		self.open = False
		
		self.register_events()
	
	def generate_callback(self):
		def callback(event):
			#print('(' + str(x) + ', ' + str(y) + ') ' + str(type(event.type)))
			
			if self.open:
				return 'break'
			
			if event.type == EventType.Leave:
				self.config(bd=2, width=size, height=size)
				#self.frame.grid(ipadx=0, ipady=0)
				#self.frame.config(width=16, height=16)
				if self.state:
					self.state = 0
				else:
					self.state = False
				return
			if event.type == EventType.Enter and self.state is 0:
				self.config(bd=0, relief=FLAT, width=size+3, height=size+3)
				self.state = True
				return
			if (event.type == EventType.ButtonPress) and (event.num == 1):
				self.config(bd=0, relief=FLAT, width=size+3, height=size+3)
				#self.frame.grid(ipadx=1, ipady=1)
				#self.frame.config(width=14, height=14)
				self.state = True
				return
			if event.type == EventType.ButtonRelease and self.state:
				#self.config(bd=2, relief=RIDGE, width=size-1, height=size-1)
				#self.frame.grid(ipadx=0, ipady=0)
				#self.frame.config(width=16, height=16)
				self.state = False
				self.open = True
				self.app.l_press(self.x, self.y)
				return
			if event.type == EventType.ButtonRelease:
				self.config(bd=2, width=size, height=size)
				self.state = False
				return
			if (event.type == EventType.ButtonPress) and (event.num == 3):
				self.state = False
				self.app.r_press(self.x, self.y)
				return
			
		return callback
	
	def register_events(self):
		callback = self.generate_callback()
		
		for x in ["<ButtonPress-1>", "<ButtonRelease-1>", "<Leave>", "<ButtonPress-3>", "<Enter>"]:
			self.bind(x, callback)

class App(Frame):
	def __init__(self, tk):
		super().__init__(tk, bg=color) # "#888"
		self.make_widgets()
		self.state = [[False]*9]*9
	
	def make_widgets(self):
		self.make_button_grid()
	
	def l_press(self, x, y):
		print("Left: (%s, %s)" % (str(x), str(y)))
		#if not random.randint(0, 3):
		i = image_1
		#else:
		#	i = default_image
		self.buttons[x][y].config(relief=FLAT, image=i)
		self.buttons[x][y].grid(ipadx=1, ipady=1)
	
	def r_press(self, x, y):
		print("Right: (%s, %s)" % (str(x), str(y)))
	
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
				b = self.make_button(x + x_offset, y + y_offset)
				row.append(b)
			buttons.append(row)
		self.buttons = buttons
	
	def make_button(self, x, y):
		return Tile(self, x, y)
		

def main():
	#tk = Tk()
	#image = PhotoImage()
	app = App(t)
	app.grid()
	t.mainloop()

if __name__ == "__main__":
	main()
