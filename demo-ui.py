import tkinter as tk

class App:
	def __init__(self, master):
		self.frame = tk.Frame(master)
		self.frame.pack()

		self.save_button = tk.Button(self.frame, text='Save to File', command=self.save_maze)
		self.load_button = tk.Button(self.frame, text='Load from File', command=self.load_maze)
		self.generate_button = tk.Button(self.frame, text='Generate Maze', command=self.load_maze)
		self.display_button = tk.Button(self.frame, text='Display Maze', command=self.load_maze)
		self.gen_and_display_button = tk.Button(self.frame, text='Gen & Display Maze', command=self.gen_and_display_maze)

		self.save_button.pack(side=tk.LEFT)
		self.load_button.pack(side=tk.LEFT)
		self.generate_button.pack(side=tk.LEFT)
		self.display_button.pack(side=tk.LEFT)
		self.gen_and_display_button.pack(side=tk.LEFT)


		self.maze_size_entry = tk.Entry(self.frame)
		self.maze_size_entry.insert(0, "10")
		# to get current entry (e)'s text: s = e.get()

		self.maze_size_entry.pack(side=tk.LEFT)

		self.maze = None # represents the Maze that is currently loaded. default = None.



	def load_maze(self):
		# Come up with a decent way to save a maze as a file. define walls, maybe?
		pass

	def save_maze(self):
		pass

	def generate_maze(self):
		maze_size = int(self.maze_size_entry.get()) # maze size in length of a side.
		pass

	def display_maze(self):
		# Use a tk.Canvas object.
		pass

	def gen_and_display_maze(self):
		self.generate_maze()
		self.display_maze()


def gen_maze_no_inner_walls(size):
	slabs = [[False for i in range(size)] for j in range(size+1)]
	columns = [[False for i in range(size)] for j in range(size+1)]

	slabs[0] = [True for i in range(size)]
	slabs[-1] = [True for i in range(size)]

	columns[0] = [True for i in range(size)]
	columns[-1] = [True for i in range(size)]

	return slabs, columns

class Maze:
	# The maze wasn't meant for you.
	def __init__(self, size=0, generation_func=None):
		self.size = size
		self.gen_func = generation_func # save the func for __repr__
		# take in a size and a generation func and produce the maze
		# using generation_func(size).

		self.slabs, self.columns = generation_func(size)
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
		# It would be convenient to have a console debug tr srepresentation of a maze.
	def __repr__(self):
		# Provide info on the object.

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

		return 'Maze Object with size ' + str(self.size) + ' and made with ' + str(self.gen_func)

def main():
	root = tk.Tk()
	app = App(root)
	root.mainloop()

def debug():
	print('Here are some empty mazes for you.')
	for i in range(10):
		m = Maze(i, gen_maze_no_inner_walls)
		print(m)

if __name__ == '__main__':
	#main()
	debug()
