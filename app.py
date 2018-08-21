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
from MazeGenerators import *

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
		#animating = not int(self.animation_speed_entry.get()) == 0
		#self.generate_maze(int(self.animation_speed_entry.get()))
		#if not animating:
		#	self.display_maze()

		# select algorithm
		# initialize algorithm
		# initialize drawing
		# loop
		# 	step
		# 	animate start sqaure, stop square, and wall destruction
		# 	pause

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

def main():
	root = tk.Tk()
	root.wm_title('Maze Generation Application')
	root.bind('<Control-c>', quit)
	root.bind('<Control-q>', quit)
	root.bind('<Control-w>', quit)
	app = App(root)
	root.mainloop()

if __name__ == '__main__':
	main()




# def make_depth_first_maze(maze, frame=None, root=None, speed=0): # TODO, change to MGAlgorithm child
# 	animating = not speed == 0

# 	if animating:
# 		sleep_time = 1 / speed
# 		maze_window, drawing = make_maze_display(frame, root)
# 		clear_out_cell((0,0), maze.size, drawing)

# 	# initial state: walls everywhere
# 	fill_maze_all_walls(maze)

# 	# Start in top-left corner. Have a stack for move-memory and a table for squares visited.
# 	move_memory = [(0,0)]
# 	visited = [[False for j in range(maze.size)] for i in range(maze.size)]
# 	visited[0][0] = True

# 	while len(move_memory) > 0:

# 		current_position = move_memory[-1]

# 		move_options = find_unvisited_neighbors(current_position, visited)

# 		if len(move_options) == 0:
# 			move_memory.pop()
# 			continue

# 		move = choice(move_options)

# 		# destroy wall
# 		x = move_memory[-1][0]
# 		y = move_memory[-1][1]
# 		maze[x, y, move] = False

# 		new_position = apply_move(current_position, move)

# 		move_memory.append(new_position)

# 		visited[new_position[0]][new_position[1]] = True

# 		if animating:
# 			remove_wall(current_position, move, maze.size, drawing)
# 			clear_out_cell(new_position, maze.size, drawing)
# 			pause(root, sleep_time)