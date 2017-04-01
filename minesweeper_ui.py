#!/usr/bin/python3

from minesweeper import *
import minesweeper
from tkinter import *
#from enum import Enum
#import random
import threading
import queue

#class GameThread(threading.Thread, Player):
class GameThread(Player):
	def __init__(self):
		#threading.Thread.__init__(self, args=a, kwargs=k)
		super().__init__()
		#self.game = game
		self.app = None
		self.queue = queue.Queue()
		self.lock = threading.Lock()
		#self.lock1 = threading.Lock()
		#self.daemon = False # i dont know what im doing
	
	#def lose(self, e):
	#	self.app.lose()
	
	#def win(self, e):
	#	self.app.win()
	
	def _move(self, grid):
		#with self.lock:
		self.app.update_grid(grid)
		val = self.queue.get()
		with self.lock:
			return val
	
	#def run(self):
	def send_move(self, move):
		with self.lock:
			self.queue.put(move)
		
		#return self.grid
		
#size = 8
bd = 2
#	  #RGB

color = "#BFBFBF"

# irrelavent

#fg = "#BFBFBF"
#bg = "#BFBFBF" # BFBFBF # color of button

#afg = "#BFBFBF"
#abg = "#BFBFBF" # color when clicked on

#hbg = "#BFBFBF"
#hclr = "#BFBFBF"

# end irrelavent

#pad = 0
#ipad = 1

t = Tk()
#default_image = PhotoImage()

class Images(object):
	blank = PhotoImage()
	i_1 = PhotoImage(file="icons/1.png")
	i_2 = PhotoImage(file="icons/2.png")
	i_3 = PhotoImage(file="icons/3.png")
	#i_4 = PhotoImage(file="icons/4.png")
	#i_5 = PhotoImage(file="icons/5.png")
	#i_6 = PhotoImage(file="icons/6.png")
	#i_7 = PhotoImage(file="icons/7.png")
	#i_8 = PhotoImage(file="icons/8.png")
	flag = PhotoImage(file="icons/flag.png")
	mine = PhotoImage(file="icons/mine.png")
	

#image_1 = PhotoImage(file="1.png")
#image_1 = Images.i_1

#image_1 = PhotoImage(file="icons/1.png")

#image_1	 = PhotoImage(Images.i_1)



'''
def l_press(x, y):
	print("Left: (%s, %s)" % (str(x), str(y)))
	#self.buttons[x][y].config(state=DISABLED, image=image_1)

def r_press(x, y):
	print("Right: (%s, %s)" % (str(x), str(y)))
'''
class Tile(Button):
	#IMAGE_1 = PhotoImage(file="1.png")
	size = 6 # Find size, bd that makes reasonable final_size
	bd = 3 # for every +1 bd, do -1 size for same width, height
	final_size = 16 # 16 is closest to xp minesweeper
	color = "#BFBFBF" # color of button
	grid_color = "#888" # color of 1 px grid line
	def __init__(self, master, x, y, app=None):
		#'''
		self.frame = Frame(master, bd=0, relief=FLAT, \
						   bg=self.grid_color, \
						   width=self.final_size, height=self.final_size)
						   # Button size in px is 2*self.size
						   # Make Frame same size as Button
						   # bg = color of 1 px grid line
						   # bd, relief so Frame is invisible
		self.frame.grid(row=x, column=y, padx=0, pady=0, ipadx=0, \
						ipady=0, sticky=N+S+E+W)
						# Sticky so fill all space, pad so invisible
		self.frame.grid_propagate(False) # Keep width, height size'''
		
		#self.frame = master
		
		super().__init__(self.frame, image=Images.blank, \
						 compound=CENTER, width=self.size, \
						 height=self.size, bd=self.bd, relief=RAISED, \
						 bg=self.color, activebackground=self.color, \
						 activeforeground=self.color, takefocus=False)
						 # image, compound so small size
						 # Images.blank is blank
		
		self.grid(row=x, column=y, padx=0, pady=0, ipadx=1, ipady=1, \
				  sticky=E+S)
		
		self.x, self.y = x, y
		
		if app is None:
			app = master
		
		self.app = app
		self.state = False
		self.open = False
		self.click = False
		
		self.register_events()
	
	def generate_callback(self):
		def callback(event):
			#print('(' + str(x) + ', ' + str(y) + ') ' + str(type(event.type)))
			
			if self.open:
				return 'break'
			
			if event.type == EventType.Leave:
				self.config(bd=self.bd, width=self.size, height=self.size)
				
				self.state = False
				return
			if event.type == EventType.Enter and self.click:
				self.config(bd=0, width=self.final_size-1, height=self.final_size-1) # bd=0 so same as relief=FLAT, final_size-1 so 1 px line
				
				self.state = True
				return
			if (event.type == EventType.ButtonPress) and (event.num == 1):
				self.config(bd=0, relief=FLAT, width=self.final_size-1, height=self.final_size-1) # Same as above Enter
				
				self.click = True
				self.state = True
				return
			if event.type == EventType.ButtonRelease and event.num == 1 and self.state:
				self.config(bd=self.bd, relief=FLAT, width=self.size-1, height=self.size-1)
				
				self.state = False
				self.click = False
				self.open = True
				self.app.l_press(self.x, self.y)
				return
			if event.type == EventType.ButtonRelease and event.num == 1:
				self.config(bd=self.bd, width=self.size, height=self.size)
				self.state = False
				self.click = False
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
	def __init__(self, tk, player, grid):
		super().__init__(tk, bg=color) # "#888"
		self.x_size, self.y_size = 9, 9
		self.player = player
		self._grid = grid
		self.load_images()
		self.make_widgets()
		self.player.app = self
	
	#def move(self, grid):
	#	assert grid.x_size == 9
	#	assert grid.y_size == 9
	#	
	#	self.grid = grid
	
	def redraw(self):
		class Event(object):
			type = EventType.ButtonRelease
			num = 1
		
		for x in range(self.x_size):
			for y in range(self.y_size):
				self.buttons[x][y]["image"] = self.get_image(x, y)
				if self._grid.grid(x, y).visible == Visibility.open:
					self.buttons[x][y].state = True
					self.buttons[x][y].generate_callback()(Event())
	
	def load_images(self):
		pass
	
	def make_widgets(self):
		self.make_button_grid()
	
	def get_image(self, x, y):
		# This is where you get appropriate image from Game, or grid, or whatever
		cell = self._grid.grid(x, y)
		if cell.visible == Visibility.hidden:
			return Images.blank
		if cell.visible == Visibility.flag:
			return Images.flag
		m, n = cell.is_mine, cell.neighbors
		if m:
			return Images.mine
		if n == 0:
			return Images.blank
		if n == 1:
			return Images.i_1
		if n == 2:
			return Images.i_2
		if n == 3:
			return Images.i_3
		return Images.flag
	
	def update_grid(self, grid):
		self._grid = grid
		self.redraw()
	
	def l_press(self, x, y):
		print("Left: (%s, %s)" % (str(x), str(y)))
		
		#self.redraw()
		
		#image = self.get_image(x, y)
		#self.buttons[x][y].config(image=image)
		#self.buttons[x][y].grid(ipadx=1, ipady=1)
		
		self.player.send_move([MoveType.open, x, y])
	
	def r_press(self, x, y):
		print("Right: (%s, %s)" % (str(x), str(y)))
		self.player.send_move([MoveType.flag, x, y])
	
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

class Game2(threading.Thread):
	def __init__(self, game):
		self.game = game
		super().__init__()
	
	def run(self):
		self.game.mainloop()

def main():
	#tk = Tk()
	#image = PhotoImage()
	grid_generator = RandomGridGenerator(9, 9, 10)
	print(grid_generator)
	grid = grid_generator.next()
	print(grid)
	grid = minesweeper.Grid(grid)
	print(grid)
	player = GameThread()
	game = Game(grid, player)
	app = App(t, player, grid)
	app.grid()
	Game2(game).start()
	t.mainloop()

if __name__ == "__main__":
	main()
