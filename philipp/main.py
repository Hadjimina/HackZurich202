import os
from app import app
import urllib.request
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import sys
from PIL import Image
sys.path.insert(1, 'functions/')

from SWcheck import SWcheckMain
from checkFaceTooBig import checkFaceTooBigMain
from checkSightengine import check_sightengine_properties
from checkBackground import checkBackgroundEdges

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
USE_SIGHTENGINE = False
SHOW_POSITIVE_MESSAGES = False
SKIP_OTHER = True

def checkResolution(path):
	im = Image.open(path)
	width, height = im.size
	if width < 300 or height < 300:
		messages.append(tuple(("Image is too small. Try uploading a bigger picture", "error")))
		error_count+=1

	else:
		if SHOW_POSITIVE_MESSAGES:
			messages.append(tuple(("Image Resolution good","information")))

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def upload_form():
	return render_template('upload.html')

@app.route('/', methods=['POST'])

def upload_image():
	messages =[]
	error_count = 0
	warning_count = 0

	if 'file' not in request.files:
		flash('No file part')
		return redirect(request.url)
	file = request.files['file']
	if file.filename == '':
		flash('No image selected for uploading')
		return redirect(request.url)
	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename)
		path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
		file.save(path)


		#Black & White Check
		ret=SWcheckMain(path)
		if ret != 0:
			messages.append(tuple(("This image is black and white. Try uploading an image with colors","error")))
			error_count+=1
		else:
			if SHOW_POSITIVE_MESSAGES:
				messages.append(tuple(("Image is not black and white","information")))

		#Face too big
		# messages.append(tuple(("FACE TOO BIG OFF","error")))

		ret=checkFaceTooBigMain(path,"haarcascade.xml")

		if ret[1]:
			messages.append(tuple(("A face in the image is too big. Try moving your camera further away from you","error")))
			error_count+=1
		else:
			if SHOW_POSITIVE_MESSAGES:
				messages.append(tuple(("Face is good size","information")))

		if ret[0] >3:
			messages.append(tuple(("The image contains "+str(ret[0])+" people. Try having no more than 3","warning")))
			warning_count+=1
		else:
			if SHOW_POSITIVE_MESSAGES:
				messages.append(tuple(("This image contains "+str(ret[0]),"information")))

		#Sightengine
		if USE_SIGHTENGINE:

			offensive_objects_counter = 0;
			returnSignt=check_sightengine_properties(path)

			for key,value in returnSignt.items():
				# if value==0:
				# 	messages.append(tuple(("Image "+key+"good")))

				if key == "weapon" or key == "alcohol" or key == "drugs" or key == "nudity":
					if value == 1:
						offensive_objects_counter +=1
						if offensive_objects_counter < 2:
							messages.append(tuple(("It seems your picture shows alcohol, drug, nudity or weapons. Please change your picture","error")))
							error_count+=1
					elif value == 0 and offensive_objects_counter==0:
						if SHOW_POSITIVE_MESSAGES:
							messages.append(tuple(("Image does not contain alcohol, drug, nudity or weapons", "information")))
				elif key == "sharpness":
					if value==1:
						if SHOW_POSITIVE_MESSAGES:
							messages.append(tuple(("Image does not contain alcohol, drug, nudity or weapons", "information")))
					else:
						messages.append(tuple(("The picture seems to be out of focus. Try focusing on the subject when taking a picture", "warning")))
						warning_count+=1

				elif key == "brightness":
					if value==1:
						messages.append(tuple(("Puuh, that's bright. Try taking a picture in a darker environment", "warning")))
						warning_count+=1
					elif value==2:
						messages.append(tuple(("That's a bit dark. Try taking a picture in a brighter environment", "warning")))
						warning_count+=1
					else:
						if SHOW_POSITIVE_MESSAGES:
							messages.append(tuple(("brightness ok", "information")))
				elif key == "contrast":
					if value==1:
						messages.append(tuple(("To get the best quality of pictures we suggest decrasing the contrast", "warning")))
						warning_count+=1
					elif value==2:
						messages.append(tuple(("To get the best quality of pictures we suggest increasing the contrast", "warning")))
						warning_count+=1
					else:
						if SHOW_POSITIVE_MESSAGES:
							messages.append(tuple(("contrast ok", "information")))
				elif key == "offensive":
					if value==1:
						messages.append(tuple(("We detected some offensive imagery in your picture. Please change your image.","error")))
						error_count+=1
					else:
						if SHOW_POSITIVE_MESSAGES:
							messages.append(tuple(("offensive ok", "information")))
				elif key == "minor":
					if value==1:
						messages.append(tuple(("We detect a minor in your image. Please change your image","error")))
						error_count+=1
					else:
						if SHOW_POSITIVE_MESSAGES:
							messages.append(tuple(("minor ok", "information")))
				elif key == "sunglasses":
					if value==1:
						messages.append(tuple(("Nice shades! However, for the most appealing pictures, we suggest removing them.","warning")))
						warning_count+=1
					else:
						if SHOW_POSITIVE_MESSAGES:
							messages.append(tuple(("shades ok", "information")))
				else:
					if not SKIP_OTHER:
						messages.append(tuple(("There has been a problem with your image. Try uploading another one. "+key,"error")))
						error_count+=1
		else:
			messages.append(tuple(("SIGHTENGINE OFF","error")))

		if error_count == 0:
			if warning_count > 0:
				messages.append(tuple(("Nice! Your picture looks pretty good. Check below for some editing suggestions","information")))
			else:
				messages.append(tuple(("Awesome! Your picture looks perfect.","information")))

		#Check resolution
		checkResolution(path)


		edgesReturn = checkBackgroundEdges(path)
		if edgesReturn == 0:
			if SHOW_POSITIVE_MESSAGES:
				messages.append(tuple(("Background not too wild","information")))
		else:
			messages.append(tuple(("The image background feels nervous. Maybe try a more even one","warning")))


		messages.reverse()

		for msg in messages:
		 	flash(msg[0],msg[1])

		return render_template('upload.html', filename=filename)
	else:
		flash('Allowed image types are -> png, jpg, jpeg, gif')
		return redirect(request.url)

@app.route('/display/<filename>')

def display_image(filename):
	#print('display_image filename: ' + filename)

	return redirect(url_for('static', filename='uploads/' + filename), code=301)

if __name__ == "__main__":
    app.run(threaded=False)
