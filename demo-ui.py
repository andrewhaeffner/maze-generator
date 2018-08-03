import tkinter as tk
import tkinter.font as tkFont



class App:
	def __init__(self, master):
		self.frame = tk.Frame(master)
		self.frame.grid()

		helvetica_font = tkFont.Font(root = master, family='Helvetica', size=16, weight='bold')
		button_width = 18

		self.save_button = tk.Button(self.frame, text='Save to File', command=self.save_maze)
		self.load_button = tk.Button(self.frame, text='Load from File', command=self.load_maze)
		self.generate_button = tk.Button(self.frame, text='Generate Maze', command=self.load_maze)
		self.display_button = tk.Button(self.frame, text='Display Maze', command=self.load_maze)
		self.gen_and_display_button = tk.Button(self.frame, text='Gen & Display Maze', command=self.gen_and_display_maze)

		self.save_button.config(height=1, width=button_width) # h and w are in characters.
		self.load_button.config(height=1, width=button_width)
		self.generate_button.config(height=1, width=button_width)
		self.display_button.config(height=1, width=button_width)
		self.gen_and_display_button.config(height=1, width=button_width)

		self.save_button['font'] = helvetica_font
		self.load_button['font'] = helvetica_font
		self.generate_button['font'] = helvetica_font
		self.display_button['font'] = helvetica_font
		self.gen_and_display_button['font'] = helvetica_font


		self.save_button.grid(row=1, column=0)
		self.load_button.grid(row=2, column=0)
		self.generate_button.grid(row=3, column=0)
		self.display_button.grid(row=4, column=0)
		self.gen_and_display_button.grid(row=5, column=0)
		#self.save_button.pack(side=tk.LEFT)
		#self.load_button.pack(side=tk.LEFT)
		#self.generate_button.pack(side=tk.LEFT)
		#self.display_button.pack(side=tk.LEFT)
		#self.gen_and_display_button.pack(side=tk.LEFT)


		self.maze_size_label = tk.Label(self.frame, font=helvetica_font, text='Maze side length:')
		self.maze_size_label.config(height=1, width=16)

		self.maze_size_entry = tk.Entry(self.frame, font=helvetica_font)
		self.maze_size_entry.insert(0, "10")

		self.maze_size_label.grid(row=0, column=0)
		self.maze_size_entry.grid(row=0, column=1)

		# to get current entry (e)'s text: s = e.get()

		#self.maze_size_entry.pack(side=tk.LEFT)

		self.maze = None # represents the Maze that is currently loaded.



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
		# Provide info on the object.
		return 'Maze Object with side length ' + str(self.size) + ' and made with ' + str(self.gen_func)

def main():
	root = tk.Tk()
	app = App(root)
	root.mainloop()

def debug():
	print('Here are some empty mazes for you.')
	for i in range(1,10):
		m = Maze(i, gen_maze_no_inner_walls)
		print(m)
		print(m[0,0])
		m[0, 0, 'S'] = True
		m[0, 0, 'E'] = True
		print(m)

if __name__ == '__main__':
	main()
	#debug()
