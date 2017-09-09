# Simulated Computer with a 6502 CPU
# https://github.com/wynand1004/6502_Assembly_Simulator
# By wynand1004 & 18melissa40

import tkinter
import random

from cpu_6502 import CPU

root = tkinter.Tk()
root.title("6502 Assembler Simulator")

class Display(object):
	def __init__(self, start_of_video_memory, start_of_character_memory):
		self.canvas = tkinter.Canvas(root, width=320, height=240)
		self.canvas.pack()

		self.label = tkinter.Label(root, width=40, height=5, bg="black", fg="white")
		self.label.pack()		
		
		self.start_of_video_memory = start_of_video_memory
		self.start_of_character_memory = start_of_character_memory
		# Color list based on C64 color chart REF: http://sta.c64.org/cbm64col.html
		self.colors = ["black", "white", "red", "cyan", "purple", "green", "blue", "yellow", "orange", "brown", "pink", "darkgrey", "grey", "lightgreen", "lightblue", "lightgrey"]
		
	def update(self, memory):

		# Update Graphics Canvas
		# Clear canvas
		self.canvas.delete("all") 	
	
		# Draw 32 x 24 Squares (10 x 10 pixels)
		for x in range(0, 32):
			for y in range(0, 24):
				m = self.start_of_video_memory + (y * 32) + (x)
				color = self.colors[memory[m]]
				self.canvas.create_rectangle(x * 10, y * 10, x * 10 + 10, y * 10 + 10, fill=color)	

		# Update text label (40 x 5 Characters)
		text = ""
		for i in range(self.start_of_character_memory, self.start_of_character_memory + 200):
			text += chr(memory[i])
			# Check for eol
			if (i - (self.start_of_character_memory - 1)) % 40 == 0:
				text += "\r"
		
		# Update label
		self.label["text"]=text

		# Update
		root.update()

# Create the display
display = Display(1024, 2048)

# Memory (Simple list of integers 65kb))
memory = []
for _ in range(0, 65536):
	memory.append(0)

# CPU
# Set start of execution memory to 0x1000 / 4096
cpu = CPU(0x1000)

# Add code for testing
memory[4096] = 0xa9 # LDA #0x02
memory[4097] = 0x02
memory[4098] = 0x8d # STA 0x400
memory[4099] = 0x00
memory[4100] = 0x04
memory[4101] = 0xee # INC 0x1003 (4099)
memory[4102] = 0x03 
memory[4103] = 0x10 
memory[4104] = 0x4c  # JMP 0x1000
memory[4105] = 0x00
memory[4106] = 0x10

while True:
	# Clock tick
	cpu.tick(memory)	

	# Update the display
	display.update(memory)
	

root.mainloop()