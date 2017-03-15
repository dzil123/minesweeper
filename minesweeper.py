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
	def __init__(self, is_mine=, neighbors=None, visible=None):
		if is_mine is None:
			self._is_mine = None
		else:
			self.is_mine = is_mine

		if neighbors is None:
			self._neighbors = None
		else:
			self.neighbors = neighbors # will go through setter

		if visible is None:
			self._visible = None
		else:
			self._visible = visible

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
		#if (isinstance(value, Visibility) is False) or (value is None):
		#	raise ValueError('Must be instance of Visibility enum')

		self._visible = Visibility(value) # automatically does checking for Visibility.x or 1, 2, 3

	@property
	def is_mine(self):
		return self._is_mine
	@is_mine.setter
	def is_mine(self, value):
		if value is None:
			raise ValueError('Must not be None. Must be truthy or falsy value.')
		self._is_mine = bool(value)


class Grid(object):
	USE_CELL = True
	def __init__(self, mines):
		try:
			self._grid, self.x_size, self.y_size = self._parse_args(mines)
		except (AssertionError, WrongException):
			raise TypeError("Sorry, mines didn't parse correctly.")

		# self._grid = (()*self.y_size,)*x_size

		# print('start reindex')

		self.reindex()

	@staticmethod
	def _parse_args(mines):
		try:
			mines = tuple(mines)
			mines = tuple(
				[
					tuple(
						[
							bool(y) for y in x
							]
					)
					for x in mines
					]
			)
		except TypeError:
			raise WrongException('TypeError on parsing mines.')

		# ok so now is 2d tuple of True, False
		# check to see if same dimensions

		assert isinstance(mines, tuple), "Not a tuple"

		# print(mines)

		x_size = len(mines)

		for x in mines:
			assert isinstance(x, tuple), "Not a tuple"
			for y in x:
				assert isinstance(y, bool), "Not a bool %s" % str(y)

		try:
			y_size = len(mines[0])
		except IndexError:
			raise WrongException('IndexError on getting "len" so did not tuple correctly')

		for x in mines:
			assert len(x) == y_size, "Not same length"

		#if Grid.USE_CELL:
		for x in range(x_size):
			for y in range(y_size):
				mines[x][y] = Cell(mines[x][y], None, None)

		return mines, x_size, y_size
	'''
	@property
	def mines(self):
		return self._mines

	@mines.setter
	def mines(self, value):
		return self.__class__(value)  # return new instance instead of change self

	# Grid is Immutable

	@property
	def grid(self):
		return self._grid
	'''

	def grid(self, x, y):
		return self._grid[x][y]

	# @property
	def _str_1margin(self):
		s = ''
		for x in range(self.x_size):
			# print(x)
			s += ' ---' * self.y_size
			s += '\n'
			# print('| '*self.y_size)
			for y in range(self.y_size):
				# print(y)
				s += '| '
				now = self.grid[x][y]
				if now is -1:
					s += 'X'
				elif now is 0:
					s += '0'
				else:
					s += str(now)
				s += ' '
			# s = s + str(('X' if self.grid[x][y] is -1 else self.grid[x][y])) + ' '
			s += '|\n'
		s += ' ---' * self.y_size
		return s  # [:-1]

	def _str_0margin(self):
		s = ''
		for x in range(self.x_size):
			# print(x)
			s += ' -' * self.y_size
			s += '\n'
			# print('| '*self.y_size)
			for y in range(self.y_size):
				# print(y)
				s += '|'
				now = self.grid[x][y]
				if now is -1:
					s += 'X'
				elif now is 0:
					s += ' '
				else:
					s += str(now)
				s += ''
			# s = s + str(('X' if self.grid[x][y] is -1 else self.grid[x][y])) + ' '
			s += '|\n'
		s += ' -' * self.y_size
		return s  # [:-1]

	def _str_numpy(self):
		return str(np.array(self.grid))

	__str__ = _str_0margin

	__repr__ = __str__

	def reindex(self):
		''' # from before Cell
		grid = ()
		for x in range(self.x_size):
			# print('x=%s'%str(x))
			row = ()
			for y in range(self.y_size):
				# print('y=%s'%str(y))
				if (x, y) in ((1, 0), (1, 4)):
					# print()
					pass
				if self.mines[x][y]:
					row += (-1,)
				else:
					row += (self.get_neighbors(x, y),)  # join 2 tuples
			grid += (row,)

		# Todo do sanity checking o n:
		# 2d tuples, same size
		# all ints, -1 to 8
		# edges have -1 to 5
		# corners have -1 to 3

		# print('end reindex')
		# print(grid)
		self._grid = grid
		'''

		for x in range(self.x_size):
			for y in range(self.x_size):
				if not self.grid(x, y):
					self.grid(x, y).neighbors = self.get_neighbors(x, y)

	def get_neighbors(self, x, y) -> list:
		# print('get')
		#assert self.mines[x][y] in (-1, 0)

		neighbors = 0

		for x_ in [-1, 0, 1]:
			# print('_x=%s'%str(x_))
			for y_ in [-1, 0, 1]:
				# print('_y=%s'%str(y_))
				# if not (x_ or y_): # avoid 0, 0 aka center square
				if (x_ is 0) and (y is 0):
					continue
				try:
					X = x_ + x
					Y = y_ + y

					if (X is -1) or (Y is -1):
						raise IndexError  # index is -1, will not
					# throw error normally, but
					#					will wrap-around uninentionally
					#					so stop it from happening

					#neighbor = self.mines[X][Y]
					neighbor = self.grid(x, y)
					neighbors += bool(neighbor)
				except IndexError:
					# We are on edge or corner, so no cell here
					pass

		return neighbors

class Mask(object):
	def __init__(self, grid):
		assert isinstance(grid, Grid)
		self._original_grid = grid
		self._mines, self._grid, self.x_size, self.y_size = self.original_grid.mines, self.original_grid.grid, self.original_grid.x_size, self.original_grid.y_size
		self.mask = [[0]*self.y_size]*self.x_size

	@property
	def original_grid(self):
		return self._original_grid

	@property
	def mines(self):
		return self._mines

	@property
	def mask(self):
		return self._grid

def get_random() -> random.Random: # assume random module is imported as random
	return random.random.__self__ # __self__ gets instance a bound method belongs to. Basically, get default random.Random()

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

	#random.shuffle(l)

	l = rand.sample(l, mines)

	#mines = []
	for x in range(mines):
		grid[l[x][0]][l[x][1]] = True

	#for x in grid:
	#	print(x)

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
		#while True:
		#	yield randomize(self.x, self.y, self.mines, self.rand)
		return randomize(self.x, self.y, self.mines, self.rand)

class Game(object):
	def __init__(self, grid, player):
		assert isinstance(player, Grid)
		assert isinstance(player, Player)
		self.grid = grid
		self.player = player
		self.x_size = self.grid.x_size
		self.y_size = self.grid.y_size

		self.mask = Grid(self.grid.mines) # Create copy

class Move(object):
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
				raise Explosion(x, y)
		elif self.type == MoveType.flag:
			if cell.visible == Visibility.open:
				return # invalid command. Cannot flag if opened
			elif cell.visible == Visibility.flagged: # unflag if flagged
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
		self.x, self.y = x, y
		super().__init__(*a, **k)

class MoveType(Enum):
	open = 1
	flag = 2
	#unflag = 3

class Player(object):
	def __init__(self):
		pass
	
	def move(self, grid):
		if not isinstance(grid, Grid):
			raise TypeError()
		

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
	# print(g.mines)
	# print(g.grid)
	print(np.array(g.grid))
	'''
	#g = Grid(randomize(9,9,10))

	while True:
		i = input("? ")
		i = int(i)

		r = RandomGridGenerator(9, 9, 10, state=i)

		for x in range(3):
			g = Grid(r.next())
			print(np.array(g.grid))
			print()

if __name__ == "__main__":
	main()
