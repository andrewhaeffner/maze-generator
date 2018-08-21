from random import choice

def gen_maze_no_inner_walls(size): # TODO - change to fill_maze_no_inner_walls .. And change arg to maze and mutate maze.
	slabs = [[False for i in range(size)] for j in range(size+1)]
	columns = [[False for i in range(size)] for j in range(size+1)]

	slabs[0] = [True for i in range(size)]
	slabs[-1] = [True for i in range(size)]

	columns[0] = [True for i in range(size)]
	columns[-1] = [True for i in range(size)]

	return slabs, columns

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
		return self.y
	def __str__(self):
		return "(" + str(self.x) + "," + str(self.y) + ")"

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

def get_move(start, finish): # TODO, merge with Edge functionality. Change args to self.
	char = 'error in get move'
	if finish.y > start.y:
		char = 'S'
	elif finish.y < start.y:
		char = 'N'
	elif finish.x > start.x:
		char = 'E'
	elif finish.x < start.x:
		char = 'W'
	return char

def apply_move(current_position, move): # TODO, consider in relation to Node and Edge. Simplify.
	x = current_position.x
	y = current_position.y

	if move == 'N': y -= 1
	elif move == 'S': y += 1
	elif move == 'W': x -= 1
	elif move == 'E': x += 1

	return Node(x, y)

class MGAlgorithm:
	def __init__(self, maze):
		self.starting_square = Node(0,0)
	def step(self, maze):
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
		self.maze = maze
		fill_maze_all_walls(self.maze)

		self.move_memory = [(0,0)]
		self.visited = [[False for j in range(self.maze.size)] for i in range(self.maze.size)]
		self.visited[0][0] = True

	def step(self):
		while True:
			if len(self.move_memory) == 0:
				return None

			current_position = self.move_memory[-1]

			move_options = find_unvisited_neighbors(current_position, self.visited)

			if len(move_options) == 0:
				self.move_memory.pop()
				continue

			move = choice(move_options)

			self.maze[current_position.x, current_position.y, move] = False

			new_position = apply_move(current_position, move)

			self.move_memory.append(new_position)

			self.visited[new_position.x][new_position.y] = True

			return Edge(current_position, new_position)			

class BinaryTreeMazeGenerator(MGAlgorithm):
	def __init__(self, maze):
		self.maze = maze
		fill_maze_all_walls(self.maze)
		self.starting_square = Node(0, self.maze.size-1)

		self.visited = [[False for j in range(maze.size)] for i in range(maze.size)]


		self.root_position = Node(0, self.maze.size-1)
		self.wandering_position = self.root_position.copy()
		self.finished = False
		self.traversing = False

	def traverse(self):
		x = self.wandering_position[x]
		y = self.wandering_position[y]
		if self.visited[x][y]:
			return None

		options = ['N', 'W']
		if y == 0: options.remove('N')
		if x == 0: options.remove('W')

		if len(options) == 0:
			return None # i.e.: top left corner has been reached.

		direction = choice(options)
		self.maze[x, y, direction] = False # remove wall

		new_position = apply_move(self.wandering_position, direction)
		result = Edge(self.wandering_position, new_position)
		self.wandering_position = new_position

		return result

	def increment(self):
		self.root_position.x += 1
		if self.root_position.x >= len(self.maze):
			self.root_position.x = 0
			self.root_position.y -= 1


	def step(self):
		if self.finished:
			return None

		While True:
			if not self.traversing:
				self.increment()
				wandering_position = root_position.copy()
				if root_position.y < 0:
					self.finished = True
					return None
				traversing = True

			move = self.traverse()
			if move is not None:
				return move

			self.traversing = False


def make_random_walls(maze, frame=None, root=None, speed=0): # TODO, change to MGAlgorithm child.
	for sequence in maze.slabs:
		for i in range(len(sequence)):
			if random_bool():
				sequence[i] = True

	for sequence in maze.columns:
		for i in range(len(sequence)):
			if random_bool():
				sequence[i] = True

def random_bool():
	return random() > .5

def random_integer(max): # TODO, remove
	return int(random() * max) + 1

def find_unvisited_neighbors(current_position, visited):
	x_i = current_position[0]
	y_i = current_position[1]
	size = len(visited)
	good_neighbors = []

	# Check for the edge cases and check if the square in that direction
	# has been visited or not. If not, add it to the list of good_neighbors.
	if x_i > 0 and not visited[x_i - 1][y_i]: good_neighbors.append('W')
	if x_i < size - 1 and not visited[x_i + 1][y_i]: good_neighbors.append('E')
	if y_i > 0 and not visited[x_i][y_i - 1]: good_neighbors.append('N')
	if y_i < size - 1 and not visited[x_i][y_i + 1]: good_neighbors.append('S')

	return good_neighbors

def make_depth_first_maze(maze, frame=None, root=None, speed=0): # TODO, change to MGAlgorithm child
	animating = not speed == 0

	if animating:
		sleep_time = 1 / speed
		maze_window, drawing = make_maze_display(frame, root)
		clear_out_cell((0,0), maze.size, drawing)

	# initial state: walls everywhere
	fill_maze_all_walls(maze)

	# Start in top-left corner. Have a stack for move-memory and a table for squares visited.
	move_memory = [(0,0)]
	visited = [[False for j in range(maze.size)] for i in range(maze.size)]
	visited[0][0] = True

	while len(move_memory) > 0:

		current_position = move_memory[-1]

		move_options = find_unvisited_neighbors(current_position, visited)

		if len(move_options) == 0:
			move_memory.pop()
			continue

		move = choice(move_options)

		# destroy wall
		x = move_memory[-1][0]
		y = move_memory[-1][1]
		maze[x, y, move] = False

		new_position = apply_move(current_position, move)

		move_memory.append(new_position)

		visited[new_position[0]][new_position[1]] = True

		if animating:
			remove_wall(current_position, move, maze.size, drawing)
			clear_out_cell(new_position, maze.size, drawing)
			pause(root, sleep_time)

def make_binary_tree_maze(maze, frame=None, root=None, speed=0): # TODO, change to MGAlgorithm child
	animating = not speed == 0

	if animating:
		sleep_time = 1 / speed
		maze_window, drawing = make_maze_display(frame, root)

	def traverse(x, y):
		if not visited[x][y]:

			visited[x][y] = True

			if animating: clear_out_cell((x,y), maze.size, drawing)

			options = ['N', 'W']
			if y == 0: options.remove('N')
			if x == 0: options.remove('W')

			if len(options) == 0: return # i.e.: top left corner has been reached.

			direction = choice(options)
			maze[x, y, direction] = False

			if animating:
				remove_wall((x,y), direction, maze.size, drawing)
				pause(root, sleep_time)

			new_position = apply_move((x,y), direction)
			traverse(new_position[0], new_position[1]) # recurse, going along the path.

	# initial state: walls everywhere
	fill_maze_all_walls(maze)


	visited = [[False for j in range(maze.size)] for i in range(maze.size)]

	# Traverse every single square iteratively.
	for i in range(maze.size-1, -1, -1):
		for j in range(0, maze.size, 1):
			traverse(j,i)

def make_prims_algorithm_maze(maze, frame=None, root=None, speed=0): # TODO, change to MGAlgorithm child
	animating = not speed == 0
	if animating:
		sleep_time = 1 / speed
		maze_window, drawing = make_maze_display(frame, root)

	fill_maze_all_walls(maze)

	visited = [[False for j in range(maze.size)] for i in range(maze.size)]

	max = 1000

	queue = PriorityQueue()
	create_weighted_edges = lambda position, visited : [Edge(position, apply_move(position, direction), random_integer(max)) for direction in find_unvisited_neighbors(position, visited)]

	start = Node(maze.size // 2, maze.size // 2)
	visited[start.x][start.y] = True
	queue.insert(create_weighted_edges(start, visited))

	if animating: clear_out_cell(start, maze.size, drawing)

	while len(queue) > 0:
		move = queue.get_min()

		if visited[move.second.x][move.second.y]:
			continue

		move_direction = get_move(move.first, move.second)

		visited[move.second.x][move.second.y] = True
		maze[move.first.x, move.first.y, move_direction] = False # remove wall

		neighbors = create_weighted_edges(move.second, visited)
		queue.insert(neighbors)

		if animating:
			clear_out_cell(move.second, maze.size, drawing)
			remove_wall(move.first, move_direction, maze.size, drawing)
			pause(root, sleep_time)

