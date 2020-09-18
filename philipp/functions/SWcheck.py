from PIL import Image
import numpy as np
import sys
import math

#imgColor = Image.open("/home/david/Downloads/veloCOLOR.jpeg")
#print(np.array(imgColor).shape)

def check_BW(image):
	array_img = np.array(image)
	num_of_dimensions = len(array_img.shape)
	total_pixel = array_img.shape[0] * array_img.shape[1]
	if total_pixel < 10000:
		step_i = 1
		step_j = 1
	else:
		step_i = array_img.shape[0] // 100
		step_j = array_img.shape[1] // 100
	if num_of_dimensions < 3:
		return True
	BW_pixel = 0
	count = 0
	for i in range(0, array_img.shape[0], step_i):
		for j in range(0, array_img.shape[1], step_j):
			pixel = array_img[i,j]
			avg = sum(pixel[0:3] / 3)
			count += 1
			if abs(pixel[1] - avg) < 2:
				BW_pixel += 1
	if BW_pixel / count > 0.9:
		return True
	else:
		return False


def SWcheckMain(path):
	image_path = path
	try:
		img = Image.open(image_path)
	except:
		print("Black-White-Check could no read image.")
		return
	is_BW = check_BW(img)
	if is_BW:
		print ("The image is black and white...")
	else:
		return 0

if __name__ == "__main__":
	main()
