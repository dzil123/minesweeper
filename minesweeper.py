#!/usr/bin/python3

import random
import numpy as np
from enum import Enum


class Visibility(Enum):
	hidden = 0
	flag = 1
	visible = 2
	
	open = visible
	flagged = flag
	unopened = hidden


class Cell(object):
	MINE_STR = 'X'
	ZERO_STR = '_'
	
	def __init__(self, is_mine, neighbors=None, visible=None):
		self.is_mine = is_mine
		
		if neighbors is None:
			self._neighbors = None
		else:
			self.neighbors = neighbors  # will go through setter
		
		if visible is None:
			self._visible = None
		else:
			self._visible = visible
	
	def copy(self, reset_visibility=True):
		visible = self.visible
		if reset_visibility:
			visible = Visibility.hidden
		return self.__class__(self.is_mine, self.neighbors, visible)
	
	__copy__ = copy
	__deepcopy__ = copy
	
	def __bool__(self):
		return self.is_mine
	
	__nonzero__ = __bool__
	
	@property
	def neighbors(self):
		return self._neighbors
	
	@neighbors.setter
	def neighbors(self, value):
		value = int(value)
		if 0 <= value <= 8:
			self._neighbors = value
		else:
			raise ValueError('Neighbors must be between 0 and 8')
	
	@property
	def visible(self):
		return self._visible
	
	@visible.setter
	def visible(self, value):
		self._visible = Visibility(value)  # automatically does checking for Visibility.x or 1, 2, 3
	
	@property
	def is_mine(self):
		return self._is_mine
	
	@is_mine.setter
	def is_mine(self, value):
		if value is None:
			raise ValueError('Must not be None. Must be truthy or falsy value.')
		self._is_mine = bool(value)
	
	def print(self):
		if self.is_mine:
			return Cell.MINE_STR
		if self.neighbors is None:
			error = NotImplementedError('Incorrectly initialized Cell')
			# error.x, error.y = self. #oops cells don't know their x, y
			raise error
		if self.neighbors is 0:
			return Cell.ZERO_STR
		return str(self.neighbors)
	
	def __str__(self):
		if self.visible is Visibility.hidden:
			return ' '
		if self.visible is Visibility.flagged:
			return '⚑'
		return self.print()
	
	def __repr__(self):
			return str(self) + ' ' + str(self.neighbors) + ' ' + str(self.visible)
	

class Grid(object):  # Todo: join mines and grid creation in one loop
	USE_CELL = True  # Implement __deepcopy__ for Grid and Cell
	
	def __init__(self, mines):
		self._grid, self.x_size, self.y_size = self._parse_args(mines)
		
		self.reindex()
	
	@staticmethod
	def _parse_args(mines):
		try:
			x_size = len(mines)  # Total num. of objects in mine
			y_size = len(mines[0])  # Num. of objects in first object in mine
			
			grid = []
			for x in range(x_size):
				assert len(mines[x]) == y_size  # make sure equal num of objects in every object of mine
				row = []
				for y in range(y_size):
					tmp = bool(mines[x][y])
					row.append(Cell(is_mine=tmp, visible=Visibility.hidden))
				grid.append(row)
		
		except (TypeError, IndexError, AssertionError):
			# If any error, then raise error, so everything can be in one big try
			raise ValueError('Could not parse mines.')
		
		return grid, x_size, y_size
	
	@property
	def mines(self):
		return [[bool(y) for y in x] for x in self.grid()]
	
	def grid(self, x=None, y=None):
		if None in (x, y):
			return self._grid
		return self._grid[x][y]
	
	def _str_1margin(self):
		s = ''
		for x in range(self.x_size):
			if x is 0:
				s += ' ' + ('----' * self.y_size)[:-1]
			else:
				s += '|' + ('----' * self.y_size)[:-1] + '|'
			s += '\n'
			
			for y in range(self.y_size):
				s += '| ' + str(self.grid(x, y)) + ' '
			s += '|\n'
		s += ' ' + ('----' * self.y_size)[:-1]
		return s
	
	def _str_0margin(self):
		s = ''
		for x in range(self.x_size):
			s += ' -' * self.y_size
			s += '\n'
			for y in range(self.y_size):
				s += '|'
				now = str(self.grid(x, y))
				s += now
				s += ''
			s += '|\n'
		s += ' -' * self.y_size
		return s
	
	def _str_numpy(self):
		return str(np.array(self.grid()))
	
	__str__ = _str_1margin  # This is changed
	
	__repr__ = __str__
	
	def copy(self, reset_visibility=True):
		new = self.__class__.__new__(self.__class__)
		
		new._grid = [[self.grid(x, y).copy(reset_visibility) for y in range(self.y_size)] for x in range(self.x_size)]
		new.x_size = self.x_size # bypasses long parse_args
		new.y_size = self.y_size
		
		return new
	
	def reindex(self):
		for x in range(self.x_size):
			for y in range(self.x_size):
				if not self.grid(x, y).is_mine:
					self.grid(x, y).neighbors = self.get_neighbors(x, y)
	
	def get_neighbors(self, x, y) -> list:
		neighbors = 0
		
		for x_ in [-1, 0, 1]:
			# print('_x=%s'%str(x_))
			for y_ in [-1, 0, 1]:
				if (x_ is 0) and (y is 0):  # faster than if not (x_ or y_)
					continue  # avoid 0, 0 aka center square
				try:
					X = x_ + x
					Y = y_ + y
					
					if (X is -1) or (Y is -1):
						raise IndexError  # -1 index is invalid, so just skip this (x, y) pair
					
					neighbor = self.grid(X, Y).is_mine
					neighbors += bool(neighbor)
				except IndexError:
					# We are on edge or corner, so no cell here
					pass
		
		return neighbors
	
	def print(self):
		g = str(self)
		g = g.split('\n')
		g = iter(g)

		print('  ', end='')
		for y in range(self.y_size):
			print('  %s ' % str(y), end='')
		print()

		for x in range(self.x_size):  # only works with 1 char margins
			print('  ' + next(g))
			print(str(x) + ' ' + next(g))
		print('  ' + next(g))
		print()
	
	@property
	def open(self):
		o = []
		for x in range(self.x_size):
			for y in range(self.y_size):
				if self.grid(x, y).visible is Visibility.open:
					o.append(self.grid(x, y))
		
		return o
	
	@property
	def unopened(self):
		o = []
		for x in range(self.x_size):
			for y in range(self.y_size):
				cell = self.grid(x, y)
				if not (cell.visible is Visibility.open) and (cell.is_mine == False):
					o.append(self.grid(x, y))

		return o
	
	@property
	def total(self):
		return self.x_size * self.y_size
	
	@property
	def mines(self):
		o = []
		for x in range(self.x_size):
			for y in range(self.y_size):
				cell = self.grid(x, y)
				if cell.is_mine == True:
					o.append(self.grid(x, y))

		return o

def get_random() -> random.Random:  # assume random module is imported as random
	return random.random.__self__  # Gets default random.Random() 


def randomize(x_size, y_size, mines, rand=None):
	if rand is None:
		rand = get_random()
	
	l = []
	grid = []
	for x in range(x_size):
		m = []
		for y in range(y_size):
			m.append(False)
			l.append((x, y))
		grid.append(m)
	
	l = rand.sample(l, mines)  # better than random.shuffle(l); l = l[:mines]
	
	# mines = []
	for x in range(mines):
		grid[l[x][0]][l[x][1]] = True
	
	return grid


class RandomGridGenerator(object):
	def __init__(self, x, y, mines, state=None):
		self.rand = random.Random(state) # If state==None, then will make random seed
		
		self.x, self.y, self.mines = x, y, mines
	
	def __iter__(self):
		return self
	
	def __next__(self):
		return self.next()
	
	def next(self):
		return randomize(self.x, self.y, self.mines, self.rand)


class Game(object):  # NOT IMPLEMENTED
	def __init__(self, grid, player):
		assert isinstance(grid, Grid)
		assert isinstance(player, Player)
		
		self.grid = grid.copy()  # Should make copy.deepcopy of grid
		self.player = player
		self.x_size = self.grid.x_size
		self.y_size = self.grid.y_size
		
		#print(self.total, self.need_to_open, self.open)
	
	def move(self):
		self.check_win()
		
		move = self.player.move(self.grid) # TODO: add already visited to move.apply
		opened = move.apply(self.grid) # will not apply explosion for now
		
		self.check_win()
	
	def check_win(self, error=True):
		if len(self.grid.open) < 0 or len(self.grid.open) > (self.grid.total1 0 - len(self.grid.mines)):
			raise NotImplementedError("open: %s need: %s" % \
				str(len(self.grid.open)), str(len(self.grid.unopened))) # sanity check
		
		if len(self.grid.unopened) == 0:
			if error:
				raise Win(self)
			return True
		
		return False
	
	def mainloop(self):
		self.check_win() # can't play if already won
		
		try:
			while True:
				self.move()
		except Explosion as e:
			self.player.lose(e)
		except Win as e:
			self.player.win(e)

class Move(object):  # All grid manipulation logic here
	def __init__(self, move_type, x, y):
		self.type = MoveType(move_type)
		x, y = int(x), int(y)
		if (x < 0) or (y < 0):
			raise IndexError('Out of range ints')
		self.x, self.y = x, y
	
	def apply(self, grid, visit=[]):
		if not isinstance(grid, Grid):
			raise TypeError('grid must be type Grid')
		if (self.x >= grid.x_size) or (self.y >= grid.y_size):
			raise ValueError('Coordinates out of bounds for Grid')
		
		cell = grid.grid(self.x, self.y)
		
		if self.type == MoveType.open:
			#self.visited = []
			if cell.visible in (Visibility.visible, Visibility.flag):
				return visit # Not going to open already open or flagged
			cell.visible = Visibility.visible
			if cell.is_mine:
				raise Explosion(self.x, self.y, grid)
			visit.append(cell)
			if cell.neighbors == 0 and cell.is_mine == False:
				#visit = []
				print("Starting", self.x, self.y)
				for X in [-1, 0, 1]:
					for Y in [-1, 0, 1]:
						x, y = self.x + X, self.y + Y
						if (x, y) == (0, 0) or x < 0 or y < 0:
							continue
						print(x, y)
						try:
							a = grid.grid(x, y)
						except IndexError:
							continue
						if [x, y] in visit:
							continue
						if grid.grid(x, y).is_mine:
							continue
						#visit.append([x, y])
						visit = Move(MoveType.open, x, y).apply(grid, visit)
						print("yes")
						#visit.append([x, y])
				
			return visit
		
		elif self.type == MoveType.flag:
			if cell.visible == Visibility.open:
				return  # invalid command. Cannot flag if opened
			elif cell.visible == Visibility.flagged:  # unflag if flagged
				cell.visible = Visibility.hidden
			elif cell.visible == Visibility.hidden:
				cell.visible = Visibility.flag
			else:
				raise NotImplementedError()
		else:
			raise NotImplementedError()
		return


class Explosion(Exception):
	def __init__(self, x, y, move, *a, **k):
		self.x, self.y = x, y  # Store (x, y) for Game to use
		self.move = move
		super().__init__(*a, **k)

class Win(Exception):
	def __init__(self, grid, *a, **k):
		self.grid = grid
		super().__init__(*a, **k)

class MoveType(Enum):
	open = 1
	flag = 2


class Player(object): # Override every function
	def __init__(self):
		pass
	
	def lose(self, e):
		x, y = str(e.x), str(e.y)
		print("You Lose: (%s, %s)" % (x, y))
	
	def win(self, e):
		x, y = e.grid.x_size, e.grid.y_size
		x, y = str(x), str(y)
		print("You Win: (%sx%s)" % (x, y))
	
	def _move(self, grid):
		raise NotImplementedError()
	
	def move(self, grid):  # Do Not Override
		if not isinstance(grid, Grid):
			raise TypeError()
		choice = self._move(grid)
		
		return Move(*choice)


class HumanPlayer(Player):
	def __init__(self):
		super().__init__()
		print("Move types:")
		print("    Open = 1")
		print("    Flag = 2")
	
	def _move(self, grid):
		grid.print()
		
		while True:
			try:
				i = input("M, X, Y? ")
				i = i.split()
				
				i[0], i[1], i[2] = int(i[0]), int(i[1]), int(i[2])
				assert i[0] in (1, 2)
				
				assert 0 <= i[1] <= grid.x_size
				assert 0 <= i[2] <= grid.y_size
				
			except (AssertionError, ValueError, IndexError):
				pass
			
			else:
				break
		print(i)
		#return Move(MoveType(i[0]), i[1], i[2])
		return i

'''
def main():
	import sys
	while True:
		try:
			i = input(">>> ")
			i = "print(" + i + ")"
			exec(i)
		except:
			#print("exception")
			print(sys.exc_info())



def main():
	g = Grid([[0, 0, 0, 0, 0, 0, 0, 0, 1], [0, 0, 0, 1, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 1, 0],
			  [0, 0, 0, 0, 1, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0, 0],
			  [0, 0, 1, 0, 0, 1, 0, 0, 0], [0, 0, 1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]])
	g = Grid(randomize(9,9,10))
	
	
	while True:
		i = input("? ")
		i = int(i)
		
		r = RandomGridGenerator(9, 9, 10, state=i)
		
		for x in range(3):
			g = Grid(r.next())  # print(np.array(g.grid()))
			# g = Grid([[0, 0, 1, 0], [1, 1, 0, 0], [0, 0, 0, 0], [1, 0, 0, 0]])
			print(g)
			print('\n')
'''

def main():
	h = Grid(RandomGridGenerator(9, 9, 10).next())	
	
	g = Game(h, HumanPlayer())
	g.mainloop()
	

if __name__ == "__main__":
	main()
