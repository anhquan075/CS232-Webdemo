import os
from app import app
import urllib.request
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from flask import session
from k_means_scratch import *

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'bmp'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def compressImage(img_path, clusters=8):
	img = read_image(img_path)
	
	points, means = initialize_means(img, clusters)
	means, index = k_means(points, means, clusters)
	compress_image(means, index, img, clusters)

def get_k_value():
	if request.method == "POST":
		k_value = request.form.get("k_value")
	return k_value

	
@app.route('/')
def upload_form():
	return render_template('upload.html')

@app.route('/', methods=['POST'])
def upload_image():
	if 'file' not in request.files:
		flash('No file part', 'warning')
		return redirect(request.url)
	file = request.files['file']
	if file.filename == '':
		flash('No image selected for uploading', 'warning')
		return redirect(request.url)

	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		print('upload_image filename: ' + filename)
		compressImage(os.path.join(app.config['UPLOAD_FOLDER'], filename), clusters=int(get_k_value()))
		flash('Image successfully uploaded and displayed below', 'success')
		result = request.form['k_value']
		return render_template('display.html', filename=filename, result = result )
	else:
		flash('Allowed image types are -> png, jpg, jpeg, bmp', 'danger')
		return redirect(request.url)

@app.route('/display/<filename>', methods = ['POST', 'GET'])
def display_image(filename):
	print('Display_image filename: ' + filename)
	# return redirect(url_for('static', filename='upload/' + 'compressed_' + str(get_k_value()) + '_bitmap.bmp'), code=301)
	return redirect(url_for('static', filename='upload/'+ filename), code=301)

@app.route('/display_compressed/<filename>', methods = ['POST', 'GET'])
def display_image_compressed(filename):
	return redirect(url_for('static',filename='compressed/'+ 'compressed_'+filename+'_bitmap.bmp'), code=301)


if __name__ == "__main__":
    app.run(port=30120, debug=True)