#!/usr/bin/python3

import random
import numpy as np
from enum import Enum


class WrongException(Exception):
	pass


class Visibility(Enum):
	hidden = 0
	flag = 1
	visible = 2
	
	open = visible
	flagged = flag
	unopened = hidden


class Cell(object):
	MINE_STR = 'X'
	ZERO_STR = ' '
	
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
	
	def __bool__(self):
		return self.is_mine
	
	__nonzero__ = __bool__
	
	def __str__(self):
		if self.is_mine:
			return Cell.MINE_STR
		if self.neighbors is None:
			error = NotImplementedError('Incorrectly initialized Cell')
			# error.x, error.y = self. #oops cells don't know their x, y
			raise error
		if self.neighbors is 0:
			return Cell.ZERO_STR
		return str(self.neighbors)
	
	__repr__ = __str__
	
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


class Grid(object): # Todo: join mines and grid creation in one loop
	USE_CELL = True # Implement __deepcopy__ for Grid and Cell
	
	def __init__(self, mines):
		try:
			self._mines, self._grid, self.x_size, self.y_size = self._parse_args(mines)
		except (AssertionError, WrongException):
			raise TypeError("Sorry, mines didn't parse correctly.")
		
		self.reindex()
		
		self._visible = False
	
	@staticmethod
	def _parse_args(mines):
		try:
			mines = list(mines)
			mines = [[bool(y) for y in x] for x in mines]
		except TypeError:
			raise WrongException('TypeError on parsing mines.')
		
		# ok so now is 2d tuple of True, False
		# check to see if same dimensions
		
		assert isinstance(mines, list), "Not a tuple"
		
		# print(mines)
		
		x_size = len(mines)
		
		for x in mines:
			assert isinstance(x, list), "Not a list"
			for y in x:
				assert isinstance(y, bool), "Not a bool %s" % str(y)
		
		try:
			y_size = len(mines[0])
		except IndexError:
			raise WrongException('IndexError on getting "len" so did not tuple correctly')
		
		for x in mines:
			assert len(x) == y_size, "Not same length"
		# Done sanity checking # might not be necessary
		
		grid = []
		for x in range(x_size):
			row = []
			for y in range(y_size):
				temp = mines[x][y]
				temp = bool(temp)
				temp = Cell(is_mine=temp, visible=False)
				row.append(temp)
			# grid[x][y] = temp
			grid.append(row)
		
		return mines, grid, x_size, y_size
	
	@property
	def mines(self):
		return self._mines
	
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


def get_random() -> random.Random:  # assume random module is imported as random
	return random.random.__self__  # __self__ gets instance a bound method belongs to. Basically, get default random.Random()


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
		if state:
			self.rand = random.Random(state)
		else:
			self.rand = get_random()
		
		self.x, self.y, self.mines = x, y, mines
	
	def __iter__(self):
		return self
	
	def __next__(self):
		return self.next()
	
	def next(self):
		return randomize(self.x, self.y, self.mines, self.rand)


class Game(object):  # NOT IMPLEMENTED
	def __init__(self, grid, player):
		raise NotImplementedError()
		assert isinstance(grid, Grid)
		assert isinstance(player, Player)
		self.grid = grid # Should make copy.deepcopy of grid
		self.player = player
		self.x_size = self.grid.x_size
		self.y_size = self.grid.y_size
		
		self.mask = Grid(self.grid.mines)  # Create copy


class Move(object):  # All grid manipulation logic here
	def __init__(self, move_type, x, y):
		self.type = MoveType(move_type)
		x, y = int(x), int(y)
		if (x < 0) or (y < 0):
			raise ValueError('Out of range ints')
		self.x, self.y = x, y
	
	def apply(self, grid):
		if not isinstance(grid, Grid):
			raise TypeError('grid must be type Grid')
		if (self.x >= grid.x_size) or (self.y >= grid.y_size):
			raise ValueError('Coordinates out of bounds for Grid')
		
		cell = grid.grid(self.x, self.y)
		
		if self.type == MoveType.open:
			cell.visible = Visibility.visible
			if cell.is_mine:
				raise Explosion(self.x, self.y)
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
	def __init__(self, x, y, *a, **k):
		self.x, self.y = x, y  # Store (x, y) for Game to use
		super().__init__(*a, **k)


class MoveType(Enum):
	open = 1
	flag = 2


class Player(object):
	def __init__(self):  # Override me
		pass
	
	def _move(self, grid):
		raise NotImplementedError()  # Override me
	
	def move(self, grid):  # Do Not Override
		if not isinstance(grid, Grid):
			raise TypeError()
		choice = self._move(grid)
		
		return MoveType(choice)


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
'''


def main():
	'''g = Grid([[0, 0, 0, 0, 0, 0, 0, 0, 1], [0, 0, 0, 1, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 1, 0],
			  [0, 0, 0, 0, 1, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0, 0],
			  [0, 0, 1, 0, 0, 1, 0, 0, 0], [0, 0, 1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]])
	g = Grid(randomize(9,9,10))
	'''
	
	while True:
		i = input("? ")
		i = int(i)
		
		r = RandomGridGenerator(9, 9, 10, state=i)
		
		for x in range(3):
			g = Grid(r.next())			#print(np.array(g.grid()))
			#g = Grid([[0, 0, 1, 0], [1, 1, 0, 0], [0, 0, 0, 0], [1, 0, 0, 0]])
			print(g)
			print('\n')
		#break


if __name__ == "__main__":
	main()
	input()
