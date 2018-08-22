from random import choice, random

def fill_maze_no_inner_walls(maze):
	maze.slabs = [[False for i in range(len(maze))] for j in range(len(maze)+1)]
	maze.columns = [[False for i in range(len(maze))] for j in range(len(maze)+1)]

	maze.slabs[0] = [True for i in range(len(maze))]
	maze.slabs[-1] = [True for i in range(len(maze))]

	maze.columns[0] = [True for i in range(len(maze))]
	maze.columns[-1] = [True for i in range(len(maze))]

def fill_maze_all_walls(maze):
	for row in maze.slabs:
		for i in range(len(row)):
			row[i] = True
	for row in maze.columns:
		for i in range(len(row)):
			row[i] = True

class Maze:
	# The maze wasn't meant for you.
	def __init__(self, size=0, generation_func=gen_maze_no_inner_walls):
		self.size = size
		self.gen_func = generation_func # save the func for __repr__
		# take in a size and a generation func and produce the maze
		# using generation_func(size).

		self.slabs, self.columns = generation_func(size)

	def __getitem__(self, key):
		x = key[0]
		y = key[1]
		return {'N':self.slabs[y][x], 'S':self.slabs[y+1][x],
				'W':self.columns[x][y], 'E':self.columns[x+1][y] }

	def __setitem__(self, key, value):
		x = key[0]
		y = key[1]
		letter = key[2]

		if letter == 'N':   self.slabs[y][x] = value
		elif letter == 'S': self.slabs[y+1][x] = value
		elif letter == 'W': self.columns[x][y] = value
		elif letter == 'E': self.columns[x+1][y] = value

	def __str__(self):
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

	def __repr__(self):
		return 'Maze Object with side length ' + str(self.size) + ' and made with ' + str(self.gen_func)

class Node:
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def __eq__(self, other):
		return self.x == other.x and self.y == other.y
	def __getitem__(self, key):
		if key == 0: return self.x
		elif key == 1: return self.y
		raise KeyError("Key:", key, " not recognized. Try [0] or [1].")
	def __str__(self):
		return "(" + str(self.x) + "," + str(self.y) + ")"

	def move_to(self, direction):
		x = self.x
		y = self.y

		if direction == 'N': y -= 1
		elif direction == 'S': y += 1
		elif direction == 'W': x -= 1
		elif direction == 'E': x += 1

		return Node(x,y)

	def copy(self):
		return Node(self.x, self.y)

class Edge:
	def __init__(self, first, second, weight=None):
		self.first = first
		self.second = second
		self.weight = weight

	def __contains__(self, item):
		return self.first == item or self.second == item

	def __eq__(self, other):
		return (self.first == other.first and self.second == other.second) or (self.first == other.second and self.second == other.first)

	def __lt__(self, other):
		return self.weight < other.weight

	def __str__(self):
		return str(self.first) + "-->" + str(self.second)

	def get_direction(self):
		result = None # a None result indicates not an adjacent edge.
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
