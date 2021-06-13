import os
from app import app
import urllib.request
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from flask import session
from k_means_scratch import *
from PIL import Image
from io import BytesIO
import numpy as np

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'bmp'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_k_value():
	if request.method == "POST":
		k_value = request.form.get("k_value")
	return k_value

def imageByteSize(img_path):
	img = cv2.imread(img_path)
	img_file = BytesIO()
	image = Image.fromarray(np.uint8(img))
	image.save(img_file, 'bmp')
	return img_file.tell()/1024
	
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
		compressImage(os.path.join(app.config['UPLOAD_FOLDER'], filename), k_value=int(get_k_value()))
		flash('Image successfully uploaded and displayed below', 'success')
		result = request.form['k_value']
		r_value = imageByteSize(os.path.join('static/compressed/recovered_image', f'recovered_image_w_{result}.bmp')) / imageByteSize(os.path.join(app.config['UPLOAD_FOLDER'], filename.split('.')[0] + '.bmp'))
		print(result, r_value)
		return render_template('display.html', filename=filename, result = result , r_value = r_value)
	else:
		flash('Allowed image types are -> png, jpg, jpeg, bmp', 'danger')
		return redirect(request.url)

@app.route('/display/<filename>', methods = ['POST', 'GET'])
def display_image(filename):
	print('Display_image filename: ' + filename)
	return redirect(url_for('static', filename='upload/'+ filename.split('.')[0] + '.bmp'), code=301)

# @app.route('/display_compressed/<filename>', methods = ['POST', 'GET'])
# def display_compressed_file(filename):
# 	return redirect(url_for('static',filename='compressed/bitmap_file/'+ 'compressed_'+ filename + '_bitmap.bmp'), code=302)

@app.route('/display_recovered/<filename>', methods = ['POST', 'GET'])
def display_compressed_image(filename):
	return redirect(url_for('static',filename='compressed/recovered_image/'+ 'recovered_image_w_'+ filename + '.bmp'), code=301)


if __name__ == "__main__":
	app.run(port=30120)
    