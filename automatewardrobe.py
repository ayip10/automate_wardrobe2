

import os
import tkinter as tk
import random
from PIL import Image, ImageTk
from playsound import playsound


WINDOW_TITLE = "My Wardrobe"
WINDOW_HEIGHT = 570
WINDOW_WIDTH = 220

IMG_WIDTH=250
IMG_HEIGHT=250
SOUND_EFFECT_FILE_PATH = ''

#importing python os allows us to get all files in specified directory

#tk root widget is a window provided by the window manager. can only be one root widget
#store all tops into a file
ALL_TOPS = [str('tops/') + imagefile for imagefile in os.listdir('tops/') if not imagefile.startswith('.')]
ALL_BOTTOMS = [str('bottoms/') + imagefile for imagefile in os.listdir('bottoms/') if not imagefile.startswith('.')]

class WardrobeApp:
	#self is a class level identifier, represents the instance of the class
	# by using the self keyword we can access the attributes and methods
	#of the class in python

	#__init__ is a constructor and is called when an object is created from the class
	#and allows the classs to initialize the attributes of a class
	def __init__(self,root):
		self.root = root
		#create background
		#show top image in the window
		self.top_images = ALL_TOPS
		self.bottom_images = ALL_BOTTOMS

		#save single top
		self.bottom_image_path = self.bottom_images[0]
		self.top_image_path = self.top_images[0]

		#create and add top image into Frame
		self.tops_frame = tk.Frame(self.root)
		#pack image into tops frame and pack taps frame into root
		self.top_image_label = self.create_photo(self.top_image_path, self.tops_frame)
		self.bottom_frame = tk.Frame(self.root)
		self.bottom_image_label = self.create_photo(self.bottom_image_path, self.bottom_frame)

		self.top_image_label.pack(side=tk.TOP)
		self.bottom_image_label.pack(side=tk.TOP)

		#pack() geometry manager organizes widgets in blocks before placing into 
		#parent widget. tk.BOTH fills horizontally and vertically
		#self.tops_frame.pack(fill=tk.BOTH,expand=tk.YES)

		self.create_background()

	def create_background(self):

		self.root.title(WINDOW_TITLE)
		self.root.geometry('{0}x{1}'.format(WINDOW_WIDTH,WINDOW_HEIGHT))

		self.create_buttons()
		#fill option tells widget wants to fill entire space assigned to it
		#value controls how to fill space, BOTH means widget should expand both 
		#horizontally and vertically
		self.tops_frame.pack(fill=tk.BOTH,expand=tk.YES)
		self.bottom_frame.pack(fill=tk.BOTH,expand=tk.YES)

	#making the buttons
	def create_buttons(self):
		top_prev_button = tk.Button(self.tops_frame, text="Prev", command=self.get_next_top)
		top_prev_button.pack(side=tk.LEFT)

		create_outfit_button = tk.Button(self.bottom_frame, text="CREATE OUTFIT", command = self.create_outfit)
		create_outfit_button.pack(side=tk.LEFT)

		top_next_button = tk.Button(self.tops_frame, text="Next", command = self.get_prev_top)
		top_next_button.pack(side=tk.RIGHT)

		bottom_prev_button = tk.Button(self.bottom_frame, text="Prev", command=self.get_next_bottom)
		bottom_prev_button.pack(side=tk.LEFT)

		bottom_next_button = tk.Button(self.bottom_frame, text="Next", command = self.get_prev_bottom)
		bottom_next_button.pack(side=tk.RIGHT)


		#functions that let us move front and back
	def _get_next_item(self, current_item, category, increment = True):
		item_index = category.index(current_item)
		final_index = len(category) -1
		next_index = 0

		#edge cases
		if increment and item_index==final_index:
			next_index=0
		elif not increment and item_index==0:
			next_index=final_index
		else:
			increment = 1 if increment else -1
			next_index = item_index + increment

		next_image = category[next_index]

		#reset and update image based on next_image path
		if current_item in self.top_images:
			image_label = self.top_image_label
			self.top_image_path = next_image
		else:
			image_label = self.bottom_image_label
			self.bottom_image_path = next_image

		#use update function to change image
		self.update_image(next_image,image_label)

	def update_image(self,new_image_path, image_label):
		#collect and change img to tk photo pbject
		image_file = Image.open(new_image_path)
		image_resized = image_file.resize((IMG_WIDTH, IMG_HEIGHT),Image.ANTIALIAS)
		tk_photo = ImageTk.PhotoImage(image_resized)

		#update based on provided image label
		image_label.configure(image=tk_photo)

		image_label.image = tk_photo

	def get_next_top(self):
		self.get_next_item(self.top_image_path,self.top_images)

	def get_prev_top(self):
		self._get_next_item(self.top_image_path, self.top_images, increment=False)

	def get_next_bottom(self):
		self.get_next_item(self.bottom_image_path, self.bottom_images, increment = True)

	def get_prev_bottom(self):
		self._get_next_item(self.bottom_image_path, self.bottom_images, increment=False)

	def create_photo(self, image_path, frame):
		#open image
		image_file = Image.open(image_path)
		#resize image
		image_resized = image_file.resize((IMG_WIDTH, IMG_HEIGHT), Image.ANTIALIAS)
		#pillow lets us turn the png file into a tk image
		tk_photo = ImageTk.PhotoImage(image_resized)
		#create tk label for photo and connect it to tops frame
		image_label = tk.Label(frame, image=tk_photo, anchor = tk.CENTER)
		#save reference to photo
		image_label.image = tk_photo

		return image_label

	def create_outfit(self):
		#randomly select a top and bottom index
		new_top_index = random.randint(0,len(self.top_images)-1)
		new_bottom_index = random.randint(0,len(self.bottom_images)-1)

		#add clothes onto screen, add tops and bottoms based on randomly selected numbers
		self.update_image(self.top_images[new_top_index], self.top_image_label)
		self.update_image(self.bottom_images[new_bottom_index], self.bottom_image_label)

		#add sound clip
	#	playsound(SOUND_EFFECT_FILE_PATH)

root = tk.Tk()
app = WardrobeApp(root)
root.mainloop()