import os
from flask import Flask, request, jsonify, send_file, render_template
from werkzeug.utils import secure_filename
from rembg import remove
from io import BytesIO
from PIL import Image

app = Flask(__name__)

# Folder to store uploaded files
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Function to check if the file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route to serve the index.html
@app.route('/')
def index():
    return render_template('index.html')

# API route to handle image uploads and background removal
@app.route('/api/remove-bg', methods=['POST'])
def remove_background():
    # Check if the request contains a file part
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']

    # Check if a file was selected
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Save and process the file if it's allowed
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Remove the background
        with open(file_path, 'rb') as f:
            input_image = f.read()

        output_image = remove(input_image)  # Background removed

        # Send the processed image as a response
        return send_file(BytesIO(output_image), mimetype='image/png')

    else:
        return jsonify({'error': 'File type not allowed'}), 400

if __name__ == '__main__':
    app.run(debug=True)
