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


	def load_maze(self):
		pass

	def save_maze(self):
		pass

	def generate_maze(self):
		pass

	def display_maze(self):
		pass

	def gen_and_display_maze(self):
		pass

def main():
	root = tk.Tk()
	app = App(root)
	root.mainloop()

if __name__ == '__main__':
	main()