# https://github.com/Antoniii/Medicine-App/blob/master/README.md

# conda create -n TEST python=3.5
### conda activate TEST

# pip install Pillow
# pip install cx-Freeze

from pathlib import Path
from tkinter import filedialog
from tkinter import *
from PIL import ImageTk, Image, ImageFont, ImageDraw
from time import time

root = Tk()

current_dir = Path.cwd() # путь текущей директории
filename = filedialog.askopenfilename(initialdir = current_dir, # initialdir = "/run/media/rick/DATA/Kazahi"
 title = "Select imagefile", filetypes = (("JPG files", "*.JPG"),("jpeg files", "*.jpeg"),
 										("jpg files", "*.jpg"),("png files", "*.png"),
 										("bmp files", "*.bmp"),("all files", "*.*")))
N_size = 850
size = (N_size, N_size)
radius = 350 # диаметр маски
p_x = 550
p_y = 500
antialias = 3
# percent = 100
# square = 555
diameter = 15 # mm

def prepare_mask(size, antialias = 2):
    mask = Image.new('L', (size[0] * antialias, size[1] * antialias), 0)
    #p = 390
    parametr = (mask.size[0] - p_x, mask.size[1] - p_y)
    ImageDraw.Draw(mask).ellipse((radius, radius) + parametr, fill=255)
    #print(p)
    # print((radius, radius) + parametr)
    return mask.resize(size, Image.ANTIALIAS)

def crop(im, s):
    w, h = im.size
    k = w / s[0] - h / s[1]
    if k > 0: im = im.crop(((w - h) / 2, 0, (w + h) / 2, h))
    elif k < 0: im = im.crop((0, (h - w) / 2, w, (h + w) / 2))
    return im.resize(s, Image.ANTIALIAS)


image = Image.open(filename).convert('L')

k_size = 0.5 # коэффициент сжатия изображения
#print(int(image.size[0]*k_size), int(image.size[1]*k_size))
#image = image.resize((int(image.size[0]*k_size),int(image.size[1]*k_size)))
image = image.resize((536,356))
#print(image.size[0], image.size[1])

root_y = 300
#root.geometry('{}x{}'.format(image.size[0],int(image.size[1]+root_y)))
root.geometry('{}x{}'.format(536,506))
#print(image.size[0], int(image.size[1]+root_y))
#canvas = Canvas(root,width=image.size[0],height=image.size[1])
canvas = Canvas(root,width=536,height=356)
#print(image.size[0], image.size[1])
canvas.pack()

# image = crop(image, size)
# image.putalpha(prepare_mask(size, antialias))
# image = image.convert('L')

pilimage = ImageTk.PhotoImage(image)
# kx_imagesprite = 0.5
# ky_imagesprite = 0.5
#imagesprite = canvas.create_image(int(image.size[0]*kx_imagesprite),int(image.size[1]*ky_imagesprite),image=pilimage)
imagesprite = canvas.create_image(0,0,image=pilimage, anchor=NW)

container = Frame() # создаём контейнер на главном окне для расположения кнопок и полей ввода
container.pack(side='top', fill='both', expand=True)

M = 255 # условие max
L = 0 # min

########################################################################

lbl1 = Label(container, text="Max = ")  
lbl1.grid(column=6, row=1) 

def get_val_motion(event):
	global M
	M = scal.get()
	
scal = Scale(container, orient=HORIZONTAL, length=int(image.size[0]*0.6), from_=0, to=255,
			tickinterval=1, resolution=1)
scal.bind("<B1-Motion>", get_val_motion)
scal.grid(column=7, row=1)

########################################################################

lbl2 = Label(container, text="Min = ")  
lbl2.grid(column=6, row=2) 

def get_val_motion_1(event_1):
	global L
	L = scal1.get()
	
scal1 = Scale(container, orient=HORIZONTAL, length=int(image.size[0]*0.6), from_=0, to=255,
			tickinterval=1, resolution=1)
scal1.bind("<B1-Motion>", get_val_motion_1)
scal1.grid(column=7, row=2)

########################################################################

def my_callback2(): # главная функция - для расчёта
	N = 0 # счётчик
	new_im = []
	start = time() # для тестирования скорости работы
	for i in range(image.size[0]):
		for j in range(image.size[1]):
			if (image.getpixel((i,j)) >= L) and (image.getpixel((i,j)) <= M):
				N += 1
				new_im.append((i,j,image.getpixel((i,j))))
	#global percent
	percent = N/(image.size[0]*image.size[1])*100
	global diameter
	square_global = 3.141593*(diameter**2)/4.0
	square_local = (square_global * percent) / 100.0
	#print(percent, square_global, square_local)
	print("Time {0:.3f} s".format(float(round((time()-start)*1e3)/1e3))) # для тестирования скорости работы
	global new_image # нужно для возможности сохранения в дальнейшем
	new_image = Image.new("L", (image.size[0], image.size[1]))
	for i in range(len(new_im)):
		new_image.putpixel((new_im[i][0], new_im[i][1]), new_im[i][2])

	#size = (700, 700)
	new_image = crop(new_image, size)
	new_image.putalpha(prepare_mask(size, antialias))

	draw = ImageDraw.Draw(new_image) # для отрисовки текста на изображении
	front_size = int(66*k_size**2)
	font = ImageFont.truetype("san-serif.ttf", front_size) # параметры текста
	k_x = 0.35
	k_y = 0.6
	draw.text((int(new_image.size[0]*k_x), int(new_image.size[1]*k_y)),"Result: {0:.1f}% = {1:.1f} mm^2".format(percent, square_local), 255,font=font) # наносим текст на изображение
	#draw.text((int(new_image.size[0]*k_x), int(new_image.size[1]*k_y)+front_size),"(L = {}, M = {}, N_size = {}, Radius_size = {})".format(L, M, N_size, radius), 255,font=font)
	draw.text((int(new_image.size[0]*k_x), int(new_image.size[1]*k_y)+front_size),"(L = {}, M = {})".format(L, M), 255,font=font)

	global pilimage
	pilimage = ImageTk.PhotoImage(new_image)
	global imagesprite
	#imagesprite = canvas.create_image(int(image.size[0]*kx_imagesprite),int(image.size[1]*kx_imagesprite), image=pilimage)
	imagesprite = canvas.create_image(0,0,image=pilimage, anchor=NW)

button2 = Button(container , text="Result" , command=my_callback2)
button2.grid(row=1 ,column=0)

########################################################################

def my_callback3(): # показывает исходную фотографию
	#print('return button pushed')
	global pilimage
	pilimage = ImageTk.PhotoImage(image)
	global imagesprite
	#imagesprite = canvas.create_image(int(image.size[0]*kx_imagesprite),int(image.size[1]*kx_imagesprite),image=pilimage)
	imagesprite = canvas.create_image(0,0,image=pilimage, anchor=NW)

button3 = Button(container , text="Source" , command=my_callback3)
button3.grid(row=1 ,column=1)

########################################################################

def my_callback4(): # сохраняет результат
	file_name = filedialog.asksaveasfilename(initialdir = current_dir,
							filetypes = (("png files", "*.png"),
 										("jpg files", "*.jpg"), 
 										("bmp files", "*.bmp"),("all files", "*.*")), defaultextension="")
	global new_image
	new_image.save(file_name)

button4 = Button(container , text="Save Result" , command=my_callback4)
button4.grid(row=1 ,column=2)

########################################################################

def my_callback5(): # открыть новое
	global filename
	filename = filedialog.askopenfilename(initialdir = current_dir, # initialdir = "/run/media/rick/DATA/Kazahi"
 				title = "Select imagefile", filetypes = (("JPG files", "*.JPG"),("jpeg files", "*.jpeg"),
 										("jpg files", "*.jpg"),("png files", "*.png"),
 										("bmp files", "*.bmp"),("all files", "*.*")))
	global image
	image = Image.open(filename).convert('L')

	image = crop(image, size)
	image.putalpha(prepare_mask(size, antialias))
	image = image.convert('L')

	# global k_size
	# k_size = 0.6 # коэффициент сжатия изображения

	# image = image.resize((int(image.size[0]*k_size),int(image.size[1]*k_size)))
	# global root
	# root.geometry('{}x{}'.format(image.size[0],int(image.size[1]+root_y)))

	# global canvas
	# canvas = Canvas(root,width=image.size[0],height=image.size[1])
	# canvas.pack()
	global pilimage
	pilimage = ImageTk.PhotoImage(image)
	global imagesprite
	#imagesprite = canvas.create_image(int(image.size[0]*kx_imagesprite),int(image.size[1]*kx_imagesprite),image=pilimage)
	imagesprite = canvas.create_image(0,0,image=pilimage, anchor=NW)

button5 = Button(container , text="Open New Image" , command=my_callback5)
button5.grid(row=1 ,column=3)

########################################################################

def my_callback6(): # открыть новое маленькое изображение
	global filename
	filename = filedialog.askopenfilename(initialdir = current_dir, # initialdir = "/run/media/rick/DATA/Kazahi"
 				title = "Select imagefile", filetypes = (("JPG files", "*.JPG"),("jpeg files", "*.jpeg"),
 										("jpg files", "*.jpg"),("png files", "*.png"),
 										("bmp files", "*.bmp"),("all files", "*.*")))
	global image
	image = Image.open(filename).convert('L')
	# global k_size
	# k_size = 0.6 # коэффициент сжатия изображения

	image = image.resize((536,356))
	# global root
	# root.geometry('{}x{}'.format(800,800))

	# global canvas
	# canvas = Canvas(root,width=image.size[0],height=image.size[1])
	# canvas.pack()
	global pilimage
	pilimage = ImageTk.PhotoImage(image)
	global imagesprite
	#imagesprite = canvas.create_image(int(image.size[0]*kx_imagesprite),int(image.size[1]*kx_imagesprite),image=pilimage)
	imagesprite = canvas.create_image(0,0,image=pilimage, anchor=NW)

button6 = Button(container , text="Open Small Image" , command=my_callback6)
button6.grid(row=2 ,column=0)

########################################################################

def my_callback7(): # главная функция - для расчёта маленького изображения
	N = 0 # счётчик
	new_im = []
	start = time() # для тестирования скорости работы
	for i in range(image.size[0]):
		for j in range(image.size[1]):
			if (image.getpixel((i,j)) >= L) and (image.getpixel((i,j)) <= M):
				N += 1
				new_im.append((i,j,image.getpixel((i,j))))
	#global percent
	percent = N/(image.size[0]*image.size[1])*100
	#global diameter
	#square_global = 3.141593*(diameter**2)/4.0
	#square_local = (square_global * percent) / 100.0
	#print(percent, square_global, square_local)
	print("Time {0:.3f} s".format(float(round((time()-start)*1e3)/1e3))) # для тестирования скорости работы
	global new_image # нужно для возможности сохранения в дальнейшем
	new_image = Image.new("L", (image.size[0], image.size[1]))
	for i in range(len(new_im)):
		new_image.putpixel((new_im[i][0], new_im[i][1]), new_im[i][2])

	#size = (700, 700)
	#new_image = crop(new_image, size)
	#new_image.putalpha(prepare_mask(size, antialias))

	draw = ImageDraw.Draw(new_image) # для отрисовки текста на изображении
	front_size = int(66*k_size**2)
	font = ImageFont.truetype("san-serif.ttf", front_size) # параметры текста
	k_x = 0.35
	k_y = 0.6
	draw.text((int(new_image.size[0]*k_x), int(new_image.size[1]*k_y)),"Result: {0:.1f}%".format(percent), 255,font=font) # наносим текст на изображение
	#draw.text((int(new_image.size[0]*k_x), int(new_image.size[1]*k_y)+front_size),"(L = {}, M = {}, N_size = {}, Radius_size = {})".format(L, M, N_size, radius), 255,font=font)
	draw.text((int(new_image.size[0]*k_x), int(new_image.size[1]*k_y)+front_size),"(L = {}, M = {})".format(L, M), 255,font=font)

	global pilimage
	pilimage = ImageTk.PhotoImage(new_image)
	global imagesprite
	#imagesprite = canvas.create_image(int(image.size[0]*kx_imagesprite),int(image.size[1]*kx_imagesprite), image=pilimage)
	imagesprite = canvas.create_image(0,0,image=pilimage, anchor=NW)

button7 = Button(container , text="SmallResult" , command=my_callback7)
button7.grid(row=2 ,column=1)

########################################################################

lbl7 = Label(container, text="Calibration (current diameter = 15 mm):")  # калибровка
lbl7.grid(column=0, row=3) 

lbl8 = Label(container, text="Diameter = ")
lbl8.grid(column=0, row=4) 

txt8 = Entry(container,width=5)  
txt8.grid(column=1, row=4) 

lbl8 = Label(container, text="mm")  
lbl8.grid(column=2, row=4)

def clicked8():
    global diameter
    diameter = float(txt8.get())
    print(diameter)
    
btn8 = Button(container, text="Input diameter", command=clicked8)
btn8.grid(column=3, row=4)

root.mainloop()