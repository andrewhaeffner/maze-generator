"""
MazeGenerators package contains all things for making Mazes.
"""
from random import choice, random

class Maze:
	"""Represents a square Maze, its cells, walls, and all."""

	def __init__(self, size=0, generation_func=fill_maze_no_inner_walls):
		"""
		Initialize Maze object.

		Args:
			size (int) -- The side length of the maze (default: 0).
			generation_func (method) -- The method that will be called to set the initial
				state of the maze (default: fill_maze_no_inner_walls).
		"""
		self.size = size
		self.slabs = None # Represents horizontal cell borders.
		self.columns = None # Represents vertical cell borders.

		generation_func(self)

	def __getitem__(self, key):
		"""
		Compute and return a dict containing info on the borders around a cell.

		Args:
			key (int, int) -- Indicates the cell location.

		Returns:
			A dictionary. For each side of the cell, True indicates the presence
			of a wall and False the lack thereof.
		"""
		x = key[0]
		y = key[1]
		return {'N':self.slabs[y][x], 'S':self.slabs[y+1][x],
				'W':self.columns[x][y], 'E':self.columns[x+1][y] }

	def __setitem__(self, key, value):
		"""
		Set the existence of a wall to value.

		Args:
			key (int, int, str) -- Indicates cell location and direction of a border.
			value (bool) -- The value that the border will take on.
		"""
		x = key[0]
		y = key[1]
		letter = key[2]

		if letter == 'N':   self.slabs[y][x] = value
		elif letter == 'S': self.slabs[y+1][x] = value
		elif letter == 'W': self.columns[x][y] = value
		elif letter == 'E': self.columns[x+1][y] = value

	def __str__(self):
		"""Return a string representation of the maze."""
		result = []

		for i in range(self.size + 1):

			# handle slabs first
			text_row = []
			for j in range(self.size+1):
				text_row.append('+')
				if j < self.size:
					if self.slabs[i][j]:
						symbol = '-'
					else:
						symbol = ' '
					text_row.append(symbol)

			result.append(''.join(text_row))

			# handle columns second
			text_row = []
			if i < self.size:
				for j in range(self.size+1):
					if self.columns[j][i]:
						symbol = '|'
					else:
						symbol = ' '
					text_row.append(symbol)
					if j < self.size:
						text_row.append(' ')

			result.append(''.join(text_row))

		return '\n'.join(result)

	def __len__(self):
		"""Return the side length of the maze."""
		return self.size

	def __repr__(self):
		"""Return a representation of the maze."""
		return 'Maze Object with side length ' + str(self.size)

def fill_maze_no_inner_walls(maze):
	"""Fill maze with just outer walls."""
	maze.slabs = [[False for i in range(len(maze))] for j in range(len(maze)+1)]
	maze.columns = [[False for i in range(len(maze))] for j in range(len(maze)+1)]

	maze.slabs[0] = [True for i in range(len(maze))]
	maze.slabs[-1] = [True for i in range(len(maze))]

	maze.columns[0] = [True for i in range(len(maze))]
	maze.columns[-1] = [True for i in range(len(maze))]

def fill_maze_all_walls(maze):
	"""Fill maze with all possible walls."""
	for row in maze.slabs:
		for i in range(len(row)):
			row[i] = True
	for row in maze.columns:
		for i in range(len(row)):
			row[i] = True

class Node:
	"""A Node represents a location with x,y coordinates."""

	def __init__(self, x, y):
		"""
		Initialize Node object.

		Args:
			x (int) -- x coordinate.
			y (int) -- y coordinate.
		"""
		self.x = x
		self.y = y

	def __eq__(self, other):
		"""
		Evaluate whether or not two nodes are equivalent.

		Args:
			other (Node) -- Node to be compared.

		Returns:
			bool that indicates whether or not self and other are
			equivalent in their x and y values.
		"""
		return self.x == other.x and self.y == other.y

	def __getitem__(self, key):
		"""
		Return x or y value of Node.

		Args:
			key (int) -- Indication of x or y coordinate (0 or 1).

		Returns:
			int that is the desired coordinate value.
		"""
		if key == 0: return self.x
		elif key == 1: return self.y
		raise KeyError("Key:", key, " not recognized. Try [0] or [1].")

	def __str__(self):
		"""Return string representation of Node."""
		return "(" + str(self.x) + "," + str(self.y) + ")"

	def move_to(self, direction):
		"""
		Create and return a Node that is one space over from the
		self Node, in the direction desired.

		Args:
			direction (str) -- Cardinal direction that the new Node will
			be created in.

		Returns:
			A Node that is one space over in the desired direction.
		"""
		x = self.x
		y = self.y

		if direction == 'N': y -= 1
		elif direction == 'S': y += 1
		elif direction == 'W': x -= 1
		elif direction == 'E': x += 1

		return Node(x,y)

	def copy(self):
		"""Return copy of Node."""
		return Node(self.x, self.y)

class Edge:
	"""Represents an edge between two Nodes."""

	def __init__(self, first, second, weight=None):
		"""
		Initialize Edge object.

		Args:
			first (Node) -- The first node in the Edge.
			second (Node) -- The second node in the Edge.
			weight (int) -- The weight of the edge (default: None).
		"""
		self.first = first
		self.second = second
		self.weight = weight

	def __contains__(self, item):
		"""
		Determine whether or not item is a member of Edge.

		Args:
			item (Node) -- Node to search for in the Edge.

		Returns:
			bool indicating whether or not item is a member of Edge.
		"""
		return self.first == item or self.second == item

	def __eq__(self, other):
		"""
		Determine whether or not self and other are equivalent edges,
		without regard for Node order.

		Args:
			other (Edge) -- The Edge self will be compared to.

		Returns:
			bool indicating whether or not the two edges are equivalent.
		"""
		return (self.first == other.first and self.second == other.second) or (self.first == other.second and self.second == other.first)

	def __lt__(self, other):
		"""
		Determine whether or not self has a lower weight than other.

		Args:
			other (Edge) -- Edge that will have its weight compared to that of self.

		Returns:
			bool indicating whether or not self has a lower weight than other.
		"""
		return self.weight < other.weight

	def __str__(self):
		"""Return string representation of Edge."""
		return str(self.first) + "-->" + str(self.second)

	def get_direction(self):
		"""
		Determine the cardinal direction that Edge points in.

		Returns:
			str indicating the cardinal direction that Edge points in.
		"""
		result = None
		if self.second.y > self.first.y:
			result = 'S'
		elif self.second.y < self.first.y:
			result = 'N'
		elif self.second.x > self.first.x:
			result = 'E'
		elif self.second.x < self.first.x:
			result = 'W'
		return result

def find_unvisited_neighbors(pos, visited):
	"""
	Determine all unvisited neighbors for a position.

	Args:
		pos (Node) -- The position around which neighbors will be searched for.
		visited ([bool][bool]) -- A 2D bool table indicating visited Nodes.

	Returns:
		list of str's indicating which cardinal directions have unvisited Nodes.
	"""
	size = len(visited)
	good_neighbors = []

	# Check for the edge cases and check if the square in that direction
	# has been visited or not. If not, add it to the list of good_neighbors.
	if pos.x > 0 and not visited[pos.x - 1][pos.y]: good_neighbors.append('W')
	if pos.x < size - 1 and not visited[pos.x + 1][pos.y]: good_neighbors.append('E')
	if pos.y > 0 and not visited[pos.x][pos.y - 1]: good_neighbors.append('N')
	if pos.y < size - 1 and not visited[pos.x][pos.y + 1]: good_neighbors.append('S')

	return good_neighbors

class MGAlgorithm:
	def __init__(self, maze):
		self.maze = maze
		fill_maze_all_walls(self.maze)
		self.visited = [[False for j in range(self.maze.size)] for i in range(self.maze.size)]

	def step(self):
		return None # or return an edge.

class PriorityQueue:
	def __init__(self):
		self.queue = [None]

	def insert(self, item):
		if type(item) is not list:
			self.insert([item])
			return
		for element in item:
			self.queue.append(element)
			self.percolate_up(len(self))

	def pop(self, index):
		result = self.queue.pop(index+1)
		if len(self) - index > 1:
			self.queue.insert(index+1, self.queue.pop(len(self)))
			self.percolate_down(index+1)

		return result

	def __len__(self):
		return len(self.queue) - 1

	def get_min(self):
		return self.pop(0)

	def percolate_up(self, index): # change to iterative percolate
		if index == 1:
			return

		current = self.queue[index]
		parent = self.queue[index // 2]
		if current < parent:
			temp = current
			self.queue[index] = parent
			self.queue[index // 2] = temp
			self.percolate_up(index // 2)

	def percolate_down(self, index): # change to iterative percolate
		current = self.queue[index]

		if index > len(self) / 2:
			return

		child = index * 2
		if index * 2 + 1 < len(self):
			challenger = index * 2 + 1
			if self.queue[child] < self.queue[challenger]:
				child = challenger

		if self.queue[child] < current:
			temp = current
			self.queue[index] = self.queue[child]
			self.queue[child] = temp
			self.percolate_down(child)

class DepthFirstMazeGenerator(MGAlgorithm):
	def __init__(self, maze):
		# make a super call !!!!!!!!!!!!!!!
		super().__init__(maze)

		self.start = Node(0,0)

		self.visited[self.start.x][self.start.y] = True

		self.move_memory = [self.start.copy()]

	def step(self):
		while True:
			if len(self.move_memory) == 0:
				return None

			current_position = self.move_memory[-1]

			move_options = find_unvisited_neighbors(current_position, self.visited)

			if len(move_options) == 0:
				self.move_memory.pop()
				continue

			direction = choice(move_options)

			self.maze[current_position.x, current_position.y, direction] = False

			new_position = current_position.move_to(direction)

			self.move_memory.append(new_position)

			self.visited[new_position.x][new_position.y] = True

			return Edge(current_position, new_position)			

class BinaryTreeMazeGenerator(MGAlgorithm):
	def __init__(self, maze):
		# make a super call !!!!!!!!!
		super().__init__(maze)


		self.root_position = Node(0, self.maze.size-1)
		self.wandering_position = self.root_position.copy()
		self.finished = False
		self.traversing = True

	def traverse(self):
		x = self.wandering_position.x
		y = self.wandering_position.y
		if self.visited[x][y]:
			return None

		self.visited[x][y] = True

		options = ['N', 'W']
		if y == 0: options.remove('N')
		if x == 0: options.remove('W')

		if len(options) == 0:
			return None # i.e.: top left corner has been reached.

		direction = choice(options)
		self.maze[x, y, direction] = False # remove wall

		new_position = self.wandering_position.move_to(direction)
		result = Edge(self.wandering_position, new_position)
		self.wandering_position = new_position

		return result

	def increment(self):
		self.root_position.x += 1
		if self.root_position.x >= self.maze.size:
			self.root_position.x = 0
			self.root_position.y -= 1


	def step(self):
		if self.finished:
			return None

		while True:
			if not self.traversing:
				self.increment()
				self.wandering_position = self.root_position.copy()
				if self.root_position.y < 0:
					self.finished = True
					return None
				self.traversing = True

			move = self.traverse()
			if move is not None:
				return move

			self.traversing = False

class PrimsAlgorithmMazeGenerator(MGAlgorithm):
	def __init__(self, maze):
		super().__init__(maze)


		self.start = Node(self.maze.size // 2, self.maze.size // 2)

		max = 1000
		self.queue = PriorityQueue()

		random_integer = lambda max : int(random() * max) + 1

		self.create_weighted_edges = lambda position : [Edge(position, position.move_to(direction), random_integer(max)) for direction in find_unvisited_neighbors(position, self.visited)]

		self.visited[self.start.x][self.start.y] = True
		self.queue.insert(self.create_weighted_edges(self.start))


	def step(self):
		while True:
			if len(self.queue) == 0:
				return None
			move = self.queue.get_min()
			if self.visited[move.second.x][move.second.y]:
				continue

			self.visited[move.second.x][move.second.y] = True
			self.maze[move.first.x, move.first.y, move.get_direction()] = False # remove wall

			neighbors = self.create_weighted_edges(move.second)
			self.queue.insert(neighbors)

			return move
