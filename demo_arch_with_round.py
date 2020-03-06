from pathlib import Path
from tkinter import filedialog
from PIL import Image, ImageFont, ImageDraw
#from numpy import *
#from pylab import *
from time import time

current_dir = Path.cwd() # путь текущей директории
filename = filedialog.askopenfilename(initialdir = current_dir, # initialdir = "/run/media/rick/DATA/Kazahi"
 title = "Select imagefile", filetypes = (("JPG files", "*.JPG"),("jpeg files", "*.jpeg"),
 										("jpg files", "*.jpg"),("png files", "*.png"),
 										("bmp files", "*.bmp"),("all files", "*.*")))
print(filename) # вывод окна для выбора требуемого видеофайла
'''

img = Image.new("L", (600, 660))
clr = img.getpixel((25, 45))
#img.putpixel((25, 45), 255)
#img.putpixel((25, 47), 251)
#clr1 = img.getpixel((25, 45))
#print(clr, clr1)

for i in range(int(img.size[0])):
	for j in range(int(img.size[1]*0.5)):
		img.putpixel((i, j), 255)

img.show()
img.save("picture3.png")
'''

image = Image.open(filename).convert('L')
#image.show()
#print(str(filename)[-44:-4])
#print(image.mode)

# Подготавливает маску, рисуя её в <antialias> раз больше и
# затем уменьшая, чтобы получилось сглаженно.
def prepare_mask(size, antialias = 2, p = 390):
    mask = Image.new('L', (size[0] * antialias, size[1] * antialias), 0)
    #p = 390
    parametr = (mask.size[0] - p, mask.size[1] - p)
    ImageDraw.Draw(mask).ellipse((radius, radius) + parametr, fill=255)
    print(parametr)
    print((radius, radius) + parametr)
    return mask.resize(size, Image.ANTIALIAS)

# Обрезает и масштабирует изображение под заданный размер.
# Вообще, немногим отличается от .thumbnail, но по крайней мере
# у меня результат получается куда лучше.
def crop(im, s):
    w, h = im.size
    k = w / s[0] - h / s[1]
    if k > 0: im = im.crop(((w - h) / 2, 0, (w + h) / 2, h))
    elif k < 0: im = im.crop((0, (h - w) / 2, w, (h + w) / 2))
    return im.resize(s, Image.ANTIALIAS)

size = (600, 600)
radius = 300

# image = crop(image, size)
# image.putalpha(prepare_mask(size, 6))
#image = prepare_mask(size, 6)
# print(type(image))
# image.save('results/tmp_image_output.png')
# print(type(image))
# image = Image.open('results/tmp_image_output.png').convert('L')

image = crop(image, size)
image.putalpha(prepare_mask(size, 6))
image = image.convert('L')

k_size = 0.5 # коэффициент сжатия изображения
image = image.resize((int(image.size[0]*k_size),int(image.size[1]*k_size)))
# image.save("results/{}.png".format('result6_1'))
# image = crop(image, size)
# image.putalpha(prepare_mask(size, 6))

# image = image.convert('L')
#print(image.mode)
#image.save('results/tmp_image_output.png')

N = 0 # счётчик
M = 255 # условие max
L = 100 # min

new_im = []

start = time()
#print(image.size[0])
for i in range(image.size[0]):
	for j in range(image.size[1]):
		# print(type(image))
		# print(type(image.getpixel((i,j))))
		if (image.getpixel((i,j)) >= L) and (image.getpixel((i,j)) <= M):
			N += 1
			new_im.append((i,j,image.getpixel((i,j))))
#print(image.getpixel((25, 45)))
#print(new_im)
#print(new_im[0][0])
print("N = ", N)
percent = N/(image.size[0]*image.size[1])*100
print("Size = ", image.size[0]*image.size[1])
#print(f"N / {image.size[0]}*{image.size[1]} = {percent:.03f}%")
print("Result = {0:.3f}%".format(percent))

new_image = Image.new("L", (image.size[0], image.size[1]))

for i in range(len(new_im)):
	new_image.putpixel((new_im[i][0], new_im[i][1]), new_im[i][2])

new_image = crop(new_image, size)
new_image.putalpha(prepare_mask(size, 6))
#new_image.show()

draw = ImageDraw.Draw(new_image) # для отрисовки текста на изображении
front_size = int(66*k_size**2)
font = ImageFont.truetype("san-serif.ttf", front_size) # параметры текста
k_x = 0.35
k_y = 0.12
draw.text((int(new_image.size[0]*k_x), int(new_image.size[1]*k_y)),"Result: {0:.3f}%".format(percent), 255,font=font) # наносим текст на изображение
draw.text((int(new_image.size[0]*k_x), int(new_image.size[1]*k_y)+front_size),"(L = {}, M = {})".format(L, M), 255,font=font)
#print(L, M)
new_image.save("results/result_{}.png".format(str(filename)[-11:-4]))

#image.save("results/{}.png".format('result6_1'))
#new_image.save("results/{}.png".format('result7_1'))

print("Time {} s".format(float(round((time()-start)*1e3)/1e3)))