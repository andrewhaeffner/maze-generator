##############################
# Filename: generator.py
# Author: Andrew J. Haeffner MIT EECS c/o 2021
# Date: ~August 2018
# Description: This is a maze generator written in python(3)!
##############################

import tkinter as tk
import tkinter.font as tkFont
import sys
from random import random, choice
from time import sleep

#Graphics options.
##########
window_width = 2000
window_height = window_width # square mazes & windows. For now.
maze_length = window_height
offset = 0 # Allows for a rim of blankness around the maze.
default_color = 'black'
blank_color = 'white'
line_width = 5
##########

#UI options.
##########
maze_size_entry_on = True
generate_button_on = True
display_button_on = True
generate_and_animate_button_on = True
algorithm_selection_on = True
animation_speed_entry_on = True
button_width = 24
button_height = 1
##########

#Default settings.
##########
default_animation_speed = 1000
default_maze_side_length = 200
algorithm_options = [ # these options must match the generate_maze entries char for char.
"depth first",
"binary tree",
"prims algorithm",
"random walls (wont animate)"
]
##########

item_count = 0

class Button(tk.Button):
	def __init__(self, master, f, t, c):
		global item_count
		super().__init__(master, font=f, text=t, command=c)
		self.config(height=button_height, width=button_width)
		self.grid(row=item_count, column=0)
		item_count += 1

def create_text_entry(master, f, t, default_text):
	global item_count
	label = tk.Label(master, font=f, text=t)
	label.config(height=button_height, width=button_width) # follow button width. For now.
	label.grid(row=item_count, column=0)

	entry = tk.Entry(master, font=f, width=button_width)
	entry.insert(0, default_text)
	entry.grid(row=item_count, column=1)
	item_count += 1

	return label, entry

def create_dropdown_menu(master, f, label_text, options):
	global item_count
	label = tk.Label(master, font=f, text=label_text)
	label.config(height=button_height, width=button_width) # follow button width. For now.
	label.grid(row=item_count, column=0)

	var = tk.StringVar(master)
	var.set(options[0])
	menu = tk.OptionMenu(master, var, *options)
	menu['font'] = f
	menu['menu']['font'] = f
	menu.config(height=button_height, width=button_width)
	menu.grid(row=item_count, column=1)
	item_count += 1
	return menu, var, label

class App:
	def __init__(self, master):
		self.frame = tk.Frame(master)
		self.frame.grid()
		self.root = master
		def return_callback(arg):
			self.generate_and_animate_maze()

		self.root.bind('<Return>', return_callback)
		global item_count

		helvetica_font = tkFont.Font(root = master, family='Helvetica', size=18, weight='bold')
		default_font = helvetica_font

		if algorithm_selection_on: self.algorithm_selection, self.selected_algorithm, self.algorithm_selection_label = create_dropdown_menu(self.frame, default_font, "Generation Algorithm:", algorithm_options)
		if animation_speed_entry_on: self.animation_speed_label, self.animation_speed_entry = create_text_entry(self.frame, default_font, 'Animation Speed (sqrs/s): ', str(default_animation_speed))
		if maze_size_entry_on: self.maze_size_label, self.maze_size_entry = create_text_entry(self.frame, default_font, 'Maze side length', str(default_maze_side_length))
		if generate_button_on: self.generate_button = Button(self.frame, default_font, 'Generate Maze', self.generate_maze)
		if display_button_on: self.display_button = Button(self.frame, default_font, 'Display Maze', self.display_maze)
		if generate_and_animate_button_on: self.generate_and_animate_button = Button(self.frame, default_font, 'Generate maze (animated)', self.generate_and_animate_maze)

		self.maze = None # represents the Maze that is currently loaded.

	def generate_maze(self, speed=0, algorithm=None, max_size=1000):
		maze_size = int(self.maze_size_entry.get()) % max_size # maze size in length of a side. max of 1000 b/c performance.
		self.maze = Maze(maze_size) # default maze with a standard border

		if algorithm is None:
			text = self.selected_algorithm.get().lower()
			if text == 'depth first':
				algorithm = make_depth_first_maze
			elif text == 'binary tree':
				algorithm = make_binary_tree_maze
			elif text == 'prims algorithm':
				algorithm = make_prims_algorithm_maze
			elif text == 'random walls (wont animate)':
				algorithm = make_random_walls

		algorithm(self.maze, self.frame, self.root, speed)

	def display_maze(self):
		if self.maze is None:
			print('Cannot display a maze that does not exist.')
			return

		maze_window, drawing = make_maze_display(self.frame, self.root)
		drawing.create_rectangle(offset,offset, window_width+offset,window_height+offset, fill=blank_color)

		for i in range(len(self.maze.slabs)):
			for j in range(len(self.maze.slabs[i])):
				if self.maze.slabs[i][j]:
					x_i = (j / self.maze.size) * maze_length + offset
					x_f = ((j+1) / self.maze.size) * maze_length + offset
					y_i = (i / self.maze.size) * maze_length + offset
					y_f = y_i
					drawing.create_line(x_i,y_i, x_f,y_f, fill=default_color, width=3)

		for i in range(len(self.maze.columns)):
			for j in range(len(self.maze.columns[i])):
				if self.maze.columns[i][j]:
					x_i = i / self.maze.size  * maze_length + offset
					x_f = x_i
					y_i = (j / self.maze.size) * maze_length + offset
					y_f = ((j+1) / self.maze.size) * maze_length + offset
					drawing.create_line(x_i,y_i, x_f,y_f, fill=default_color, width=3)

	def generate_and_animate_maze(self):
		animating = not int(self.animation_speed_entry.get()) == 0
		self.generate_maze(int(self.animation_speed_entry.get()))
		if not animating:
			self.display_maze()

def gen_maze_no_inner_walls(size):
	slabs = [[False for i in range(size)] for j in range(size+1)]
	columns = [[False for i in range(size)] for j in range(size+1)]

	slabs[0] = [True for i in range(size)]
	slabs[-1] = [True for i in range(size)]

	columns[0] = [True for i in range(size)]
	columns[-1] = [True for i in range(size)]

	return slabs, columns

def random_bool():
	return random() > .5

def make_random_walls(maze, frame=None, root=None, speed=0):
	for sequence in maze.slabs:
		for i in range(len(sequence)):
			if random_bool():
				sequence[i] = True

	for sequence in maze.columns:
		for i in range(len(sequence)):
			if random_bool():
				sequence[i] = True

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

def apply_move(current_position, move):
	x = current_position[0]
	y = current_position[1]

	if move == 'N': y -= 1
	elif move == 'S': y += 1
	elif move == 'W': x -= 1
	elif move == 'E': x += 1

	return Node(x, y)


def make_maze_display(frame, root):
	maze_window = tk.Toplevel(frame)
	maze_window.grid()

	def destroy(arg):
		maze_window.destroy()

	maze_window.bind('<Control-w>', destroy)
	maze_window.bind('<Control-q>', quit)

	drawing = tk.Canvas(maze_window, width=window_width+2*offset, height=window_height+2*offset)
	drawing.grid()

	drawing.create_rectangle(offset,offset, window_width+offset,window_height+offset, fill=default_color)

	return maze_window, drawing

def clear_out_cell(position, size, drawing):
	x = position[0]
	y = position[1]

	x_i = (x / size) * maze_length + (line_width / 2) + offset
	x_f = ((x+1) / size) * maze_length - (line_width / 2) + offset

	y_i = (y / size) * maze_length + (line_width / 2) + offset
	y_f = ((y+1) / size) * maze_length - (line_width / 2) + offset

	drawing.create_rectangle(x_i,y_i, x_f,y_f, fill=blank_color,outline=blank_color)

def remove_wall(position, move, size, drawing):
	x = position[0]
	y = position[1]
	if move == 'N':
		line_crawl = line_width / 2
		x_i = (x / size) * maze_length + line_crawl + offset
		x_f = ((x+1) / size) * maze_length - line_crawl + offset + 1

		y_i = (y / size) * maze_length + offset
		y_f = y_i
		drawing.create_line(x_i,y_i, x_f,y_f, fill=blank_color, width=line_width)

	if move == 'S': remove_wall((x,y+1), 'N', size, drawing)

	if move == 'W':
		line_crawl = line_width / 2

		x_i = x / size  * maze_length + offset
		x_f = x_i

		y_i = (y / size) * maze_length + line_crawl + offset
		y_f = ((y+1) / size) * maze_length - line_crawl + 1 + offset
		drawing.create_line(x_i,y_i, x_f,y_f, fill=blank_color, width=line_width)

	if move == 'E': remove_wall((x+1,y), 'W', size, drawing)

def pause(root, t):
	root.update()
	sleep(t)

def make_depth_first_maze(maze, frame=None, root=None, speed=0):
	animating = not speed == 0

	if animating:
		sleep_time = 1 / speed
		maze_window, drawing = make_maze_display(frame, root)
		clear_out_cell((0,0), maze.size, drawing)

	# initial state: walls everywhere
	for row in maze.slabs:
		for i in range(len(row)):
			row[i] = True
	for row in maze.columns:
		for i in range(len(row)):
			row[i] = True

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

def make_binary_tree_maze(maze, frame=None, root=None, speed=0):
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
	for row in maze.slabs:
		for i in range(len(row)):
			row[i] = True
	for row in maze.columns:
		for i in range(len(row)):
			row[i] = True

	visited = [[False for j in range(maze.size)] for i in range(maze.size)]

	# Traverse every single square iteratively.
	for i in range(maze.size-1, -1, -1):
		for j in range(0, maze.size, 1):
			traverse(j,i)

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

class Edge:
	def __init__(self, first, second, weight):
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

class PriorityQueue:
	# reconsider the whole class given that None is the 0th element.
	def __init__(self):
		self.queue = [None]

	def insert(self, item):
		if type(item) is list:
			for element in item:
				self += item
		else:
			self += item

	def pop(self, index):
		result = self.queue.pop(index+1)
		if len(self) - index > 1:
			self.queue.insert(index+1, self.queue.pop(len(self)))
			self.percolate_down(index+1)

		return result

	def __iadd__(self, item):
		self.queue.append(item)
		self.percolate_up(len(self))
		return self

	def __len__(self):
		return len(self.queue) - 1

	def peek(self):
		if len(self) > 0:
			return self.queue[1]
		else:
			raise IndexError("queue is empty")

	def get_min(self):
		return self.pop(0)

	def percolate_up(self, index):
		if index == 1:
			return

		current = self.queue[index]
		parent = self.queue[index // 2]
		if current < parent:
			temp = current
			self.queue[index] = parent
			self.queue[index // 2] = temp
			self.percolate_up(index // 2)

	def percolate_down(self, index):
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


class EdgePriorityQueue(PriorityQueue):
	def remove(self, key):
		i = 0
		while i < len(self):
			if key in self.queue[i+1]:
				self.pop(i)
				continue
			i += 1

def random_integer(max):
	return int(random() * max) + 1

def get_move(start, finish):
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

def make_prims_algorithm_maze(maze, frame=None, root=None, speed=0):
	animating = not speed == 0
	if animating:
		sleep_time = 1 / speed
		maze_window, drawing = make_maze_display(frame, root)


	# initial state: walls everywhere
	for row in maze.slabs:
		for i in range(len(row)):
			row[i] = True
	for row in maze.columns:
		for i in range(len(row)):
			row[i] = True

	visited = [[False for j in range(maze.size)] for i in range(maze.size)]

	max = 1000

	queue = EdgePriorityQueue()
	seed = (maze.size // 2, maze.size // 2)
	start = Node(seed[0], seed[1])
	visited[start.x][start.y] = True
	neighbors = [Edge(start, apply_move(start, direction), random_integer(max)) for direction in find_unvisited_neighbors(start, visited)]
	queue.insert(neighbors)
	if animating: clear_out_cell(start, maze.size, drawing)

	while queue.len() > 0:
		move = queue.get_min()
		queue.remove(move.second)
		if animating: clear_out_cell(move.second, maze.size, drawing)
		direct = get_move(move.first, move.second)
		if animating: remove_wall(move.first, direct, maze.size, drawing)
		visited[move.second.x][move.second.y] = True
		maze[move.first.x, move.first.y, direct] = False
		neighbors = [Edge(move.second, apply_move(move.second, direction), random_integer(max)) for direction in find_unvisited_neighbors(move.second, visited)]
		queue.insert(neighbors)
		pause(root, sleep_time)

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

def main():
	root = tk.Tk()
	root.wm_title('Maze Generation Application')
	root.bind('<Control-c>', quit)
	root.bind('<Control-q>', quit)
	root.bind('<Control-w>', quit)
	app = App(root)
	root.mainloop()

def debug():
	m = Maze(5, gen_maze_no_inner_walls)
	make_random_walls(m)
	print(m)

def draw():
	def quit():
		root.quit()
	root = tk.Tk()
	root.bind('<control-c>', quit)
	app = App(root)
	app.generate_maze()
	app.display_maze()
	root.mainloop()

if __name__ == '__main__':
	main()
	#debug()
	#draw()
