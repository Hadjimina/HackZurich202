import os
from app import app
import urllib.request
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import sys
sys.path.insert(1, 'functions/')

from SWcheck import SWcheckMain
from checkFaceTooBig import checkFaceTooBigMain
from checkSightengine import check_sightengine_properties

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def upload_form():
	return render_template('upload.html')

@app.route('/', methods=['POST'])
def upload_image():
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
		#print('upload_image filename: ' + filename)
		#flash('Image successfully uploaded and displayed')

		#Black & White Check
		ret=SWcheckMain(path)
		if ret != 0:
			flash("This image is black and white!")
		else:
			flash("Image is not black and white")

		#Face too big
		ret=checkFaceTooBigMain(path,"haarcascade.xml")
		print(ret)
		if ret[1]:
			flash("This face is too big")
		else:
			flash("Face is good size")

		flash("This image contains "+str(ret[0])+" people")

		#Sightengine
		ret=check_sightengine_properties(path)
		for key in ret:
			# if ret[key]==0:
			# 	flash("Image "+key+"good")
			if ret[key] == 1:
				flash("Image "+key+" too high")
			elif ret[key] == 2:
				flash("Image "+key+" too low")

		return render_template('upload.html', filename=filename)
	else:
		flash('Allowed image types are -> png, jpg, jpeg, gif')
		return redirect(request.url)




@app.route('/display/<filename>')
def display_image(filename):
	#print('display_image filename: ' + filename)

	return redirect(url_for('static', filename='uploads/' + filename), code=301)

if __name__ == "__main__":
    app.run()
