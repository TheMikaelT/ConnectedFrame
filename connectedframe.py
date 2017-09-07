#!/usr/bin/env python

from Tkinter import *
from os import putenv, getenv, system
from PIL import Image, ImageTk 
from glob import glob

dropbox_link = getenv("DROPBOX_LINK")
download_interval = int(getenv("DOWNLOAD_INTERVAL_HOURS")) * 60 * 60 * 1000
carousel_interval = int(getenv("CAROUSEL_INTERVAL_SECONDS")) * 1000
frame_owner = getenv("FRAME_OWNER")
ifttt_key = getenv("IFTTT_KEY")

base_path = "/usr/src/app/images/"
carrousel_status = True
image_index = 0
image_list = []
initial_init = True

def download_images(url):
	archive = base_path + "temp.zip"

	remove = "sudo rm -rf " + base_path + "*"
	download = "wget -q  "+ url + " -O " + archive
	extract = "unzip -o " + archive + " -d " + base_path

	system(remove)
	system(download)
	system(extract)

def resize_images():
	images = list_images()

	for file in images:
		img = Image.open(file)
		img = img.resize((1920, 1080), Image.ANTIALIAS)
		img.save(file, "JPEG")

def list_images():
	images = []

	dir = base_path + "*.jpg"

	images = glob(dir)

	return images


def carrousel():
	if(carrousel_status):
		next_image()

	root.after(carousel_interval, carrousel)

def update_image(image_path):
	img = ImageTk.PhotoImage(Image.open(image_path))
	center_label.configure(image=img)
	center_label.image = img

	img = ImageTk.PhotoImage(Image.open("/usr/src/app/icons/like.png"))
	like_button.configure(image=img)
	like_button.image = img

def initialize():
	global image_list, carrousel_status, initial_init
	current_carrousel_status = carrousel_status
	carrousel_status = False

	download_images(dropbox_link)
	resize_images()
	image_list = list_images()

	carrousel_status = current_carrousel_status

	if(initial_init):
		initial_init = False
		root.after(1000, initialize)
	else:
		root.after(download_interval, initialize)


root = Tk()
root.title('Connected Frame')
root.geometry('{}x{}'.format(800, 480))
root.attributes("-fullscreen", True)
root.config(cursor='none')

initialize()



center_image = Image.open(image_list[0])
center_photo = ImageTk.PhotoImage(center_image)
center_label = Label(center_column, image=center_photo)

carrousel()

root.mainloop()
