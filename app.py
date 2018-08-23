"""Maze Generation program. Call main() to run it."""
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
algo_select_on = True
animation_speed_entry_on = True
button_width = 24
button_height = 1
##########

#Default settings.
##########
max_size = 1000
default_animation_speed = 1000
default_maze_side_length = 200
algorithm_options = [ # be careful with how these are spelled.
"depth first",
"binary tree",
"prims algorithm"
]
##########

item_count = 0

class Button(tk.Button):
	"""An abstraction of tk.Button"""

	def __init__(self, master, f, t, c):
		"""
		Initialize Button.

		Args:
			master (tk.Frame) -- The root frame of the button.
			f (tkFont.Font) -- The desired font for the button.
			t (str) -- The desired text for the button.
			c (function) -- The command called upon button's press.
		"""
		global item_count
		super().__init__(master, font=f, text=t, command=c)
		self.config(height=button_height, width=button_width)
		self.grid(row=item_count, column=0)
		item_count += 1

def create_text_entry(master, f, t, default_text):
	"""
	Create a label and text entry.

	Args:
		f (tkFont.Font) -- The desired font for the label&entry.
		t (str) -- The desired text for the label.
		default_text (str) -- The starting text for the entry.

	Returns:
		(tk.Label, tk.Entry) that have the desired properties.
	"""
	global item_count
	label = tk.Label(master, font=f, text=t)
	label.config(height=button_height, width=button_width)
	label.grid(row=item_count, column=0)

	entry = tk.Entry(master, font=f, width=button_width)
	entry.insert(0, default_text)
	entry.grid(row=item_count, column=1)
	item_count += 1

	return label, entry

def create_dropdown_menu(master, f, label_text, options):
	"""
	Args:
		f (tkFont.Font) -- The desired font for the label&entry.
		label_text (str) -- The text that will be shown on the label.
		options (list) -- The options to be displayed in the menu.

	Returns:
		(tk.OptionMenu, tk.StringVar, tk.Label) that have the desired
		properties.

	"""
	global item_count
	label = tk.Label(master, font=f, text=label_text)
	label.config(height=button_height, width=button_width)
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
	"""Main application class."""

	def __init__(self, master):
		"""
		Initialize App.

		Args:
			master (tk.Tk) -- The root for the App Frame.
		"""
		self.frame = tk.Frame(master)
		self.frame.grid()
		self.root = master
		def return_callback(arg):
			self.generate_and_animate_maze()

		self.root.bind('<Return>', return_callback)
		global item_count

		self.helvetica_font = tkFont.Font(root = master,
										  family='Helvetica', size=18,
										  weight='bold')

		self.default_font = self.helvetica_font

		if algo_select_on:
			self.algo_select, self.selected_algo, \
			self.algo_select_label = create_dropdown_menu(
				self.frame, self.default_font, "Generation Algorithm:",
				algorithm_options
				)

		if animation_speed_entry_on:
			self.animation_speed_label, self.animation_speed_entry \
				= create_text_entry(self.frame, self.default_font,
									'Animation Speed (sqrs/s): ',
									str(default_animation_speed))

		if maze_size_entry_on:
			self.maze_size_label, self.maze_size_entry = \
				create_text_entry(self.frame, self.default_font,
								  'Maze side length',
								  str(default_maze_side_length))

		if generate_and_animate_button_on:
			self.generate_and_animate_button = Button(
				self.frame, self.default_font,
				'Generate maze (animated)',
				self.generate_and_animate_maze)

		self.maze = None

	def draw_whole_maze(self):
		"""Draws entire maze in one go."""
		self.drawing.create_rectangle(offset,offset,
									  window_width+offset,
									  window_height+offset,
									  fill=blank_color)

		for i in range(len(self.maze.slabs)):
			for j in range(len(self.maze.slabs[i])):
				if self.maze.slabs[i][j]:
					x_i = j / len(self.maze) * maze_length + offset
					x_f = (j+1) / len(self.maze) * maze_length + offset
					y_i = i / len(self.maze) * maze_length + offset
					y_f = y_i
					self.drawing.create_line(x_i,y_i, x_f,y_f,
											 fill=default_color,
											 width=3)

		for i in range(len(self.maze.columns)):
			for j in range(len(self.maze.columns[i])):
				if self.maze.columns[i][j]:
					x_i = i / len(self.maze)  * maze_length + offset
					x_f = x_i
					y_i = j / len(self.maze) * maze_length + offset
					y_f = (j+1) / len(self.maze) * maze_length + offset
					self.drawing.create_line(x_i,y_i, x_f,y_f,
											 fill=default_color,
											 width=3)


	def generate_and_animate_maze(self):
		"""Generates and animates maze in real time."""
		# limit maze size.
		maze_size = int(self.maze_size_entry.get()) % max_size
		self.maze = Maze(maze_size) # build a default maze.

		try:
			speed = int(self.animation_speed_entry.get())
		except ValueError:
			speed = default_animation_speed

		if speed == 0:
			sleep_time = 0
		else:
			sleep_time = 1 / speed

		animating = not speed == 0

		algorithm = None

		text = self.selected_algo.get().lower()
		if text == 'depth first':
			algorithm = DepthFirstMazeGenerator(self.maze)
		elif text == 'binary tree':
			algorithm = BinaryTreeMazeGenerator(self.maze)
		elif text == 'prims algorithm':
			algorithm = PrimsAlgorithmMazeGenerator(self.maze)

		self.maze_window, self.drawing = make_maze_display(self.frame)

		move = algorithm.step()

		while move is not None:
			if animating:
				self.draw_move(move)
			move = algorithm.step()
			if animating:
				pause(self.root, sleep_time)

		if not animating:
			self.draw_whole_maze()

	def draw_move(self, move):
		"""
		Draw a move on a drawing.

		Args:
			move (Edge) -- The edge to be drawn
			drawing (tk.Toplevel) -- The canvas to be drawn on.
		"""
		clear_out_cell(move.first, len(self.maze), self.drawing)
		remove_wall(move.first, move.get_direction(), len(self.maze),
					self.drawing)
		clear_out_cell(move.second, len(self.maze), self.drawing)


def make_maze_display(frame):
	"""
	Create a display for a maze.

	Args:
		frame (tk.Frame) -- The frame the maze will be drawn on.

	Returns:
		(tk.Toplevel, tk.Canvas) that are the window and drawing
		objects to be used for the new maze animation.
	"""
	maze_window = tk.Toplevel(frame)
	maze_window.grid()

	def destroy(arg):
		maze_window.destroy()

	maze_window.bind('<Control-w>', destroy)
	maze_window.bind('<Control-q>', quit)

	drawing = tk.Canvas(maze_window, width=window_width+2*offset,
						height=window_height+2*offset)
	drawing.grid()

	drawing.create_rectangle(offset,offset, window_width+offset,
							 window_height+offset, fill=default_color)

	return maze_window, drawing

def clear_out_cell(position, size, drawing):
	"""
	Draws out a square in the desired position on the drawing.

	Args:
		position (Node) -- Indicates cell to be drawn out.
		size (int) -- The pixel side length of the maze.
		drawing (tk.Canvas) -- The object to be drawn upon.
	"""
	x = position[0]
	y = position[1]

	x_i = (x / size) * maze_length + (line_width / 2) + offset
	x_f = ((x+1) / size) * maze_length - (line_width / 2) + offset

	y_i = (y / size) * maze_length + (line_width / 2) + offset
	y_f = ((y+1) / size) * maze_length - (line_width / 2) + offset

	drawing.create_rectangle(x_i,y_i, x_f,y_f, fill=blank_color,
							 outline=blank_color)

def remove_wall(position, move, size, drawing): # TODO: change to Edge?
	"""
	Removes a wall in the desired location on a drawing.

	Args:
		position (Edge) -- Indicates central cell for the wall.
		move (str) -- Indicate the direction in which the wall is.
		size (int) -- The pixel side length of the maze.
		drawing (tk.Canvas) -- The object to be drawn upon.
	"""
	x = position[0]
	y = position[1]
	if move == 'N':
		line_crawl = line_width / 2
		x_i = (x / size) * maze_length + line_crawl + offset
		x_f = ((x+1) / size) * maze_length - line_crawl + offset + 1

		y_i = (y / size) * maze_length + offset
		y_f = y_i
		drawing.create_line(x_i,y_i, x_f,y_f, fill=blank_color,
							width=line_width)

	if move == 'S': remove_wall((x,y+1), 'N', size, drawing)

	if move == 'W':
		line_crawl = line_width / 2

		x_i = x / size  * maze_length + offset
		x_f = x_i

		y_i = (y / size) * maze_length + line_crawl + offset
		y_f = ((y+1) / size) * maze_length - line_crawl + 1 + offset
		drawing.create_line(x_i,y_i, x_f,y_f, fill=blank_color,
							width=line_width)

	if move == 'E': remove_wall((x+1,y), 'W', size, drawing)

def pause(root, t):
	"""
	Pause the app for t seconds.

	Args:
		root (tk.Tk) -- The root of the application.
		t (int) -- The amount of time to sleep for.
	"""
	root.update()
	sleep(t)

def main():
	"""main function for the app."""
	root = tk.Tk()
	root.wm_title('Maze Generation Application')
	root.bind('<Control-q>', quit)
	root.bind('<Control-w>', quit)
	app = App(root)
	root.mainloop()

if __name__ == '__main__':
	main()
