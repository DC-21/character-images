from flask import Flask, request, redirect, url_for, render_template, send_from_directory
import os
import cv2
import logging
import uuid

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
app.config['EXTRACT_FOLDER'] = 'static/extracts/'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

# Set up logging
logging.basicConfig(level=logging.DEBUG)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def extract_sprites(image_path, rows, columns, extract_folder):
    sprite_sheet = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    sheet_height, sheet_width, _ = sprite_sheet.shape
    sprite_height = sheet_height // rows
    sprite_width = sheet_width // columns

    if not os.path.exists(extract_folder):
        os.makedirs(extract_folder)

    sprite_counter = 0
    sprites = []
    for row in range(rows):
        for col in range(columns):
            x = col * sprite_width
            y = row * sprite_height
            sprite = sprite_sheet[y:y + sprite_height, x:x + sprite_width]
            sprite_filename = os.path.join(extract_folder, f"sprite_{sprite_counter}.png")
            cv2.imwrite(sprite_filename, sprite)
            sprites.append(f"sprite_{sprite_counter}.png")
            sprite_counter += 1
    
    return sprites

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            logging.error("No file part in the request")
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            logging.error("No file selected for uploading")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = file.filename
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            logging.debug(f"File {filename} uploaded successfully")
            
            # Create a unique folder for the extracted sprites
            unique_id = str(uuid.uuid4())
            extract_folder = os.path.join(app.config['EXTRACT_FOLDER'], unique_id)
            
            rows = int(request.form.get('rows', 6))
            columns = int(request.form.get('columns', 5))
            sprites = extract_sprites(file_path, rows, columns, extract_folder)
            logging.debug(f"Extracted sprites: {sprites}")
            return render_template('index.html', filename=filename, sprites=sprites, extract_folder=unique_id)
    return render_template('index.html', sprites=None)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/extracts/<folder>/<filename>')
def extracted_file(folder, filename):
    extract_folder = os.path.join(app.config['EXTRACT_FOLDER'], folder)
    return send_from_directory(extract_folder, filename)

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    if not os.path.exists(app.config['EXTRACT_FOLDER']):
        os.makedirs(app.config['EXTRACT_FOLDER'])
    app.run(debug=True)
