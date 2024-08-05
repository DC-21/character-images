# Developed By CHOLA KUBOKO(dc_wrld)

# Image Component Extractor

This project is a simple web application built with Flask that allows users to upload an image and extract each individual component from the image. The extracted components are saved as separate PNG files.

## Requirements

- Python 3.x
- Flask
- OpenCV
- Pillow

## Setup Instructions

1. **Install dependencies**:
   extract the project and open it in a compiler, e.g Visual Studio Code and open a terminal then run below command to install dependencies.
   pip install -r requirements.txt

2. **Run the Flask app**:

   ```sh
   python app.py
   ```

3. **Open a web browser** and go to `http://127.0.0.1:5000/` to use the app.

## Usage

1. Open the web application in your browser.
2. Use the file input to upload an image.
3. The application will process the image, extract each individual component, and display the total number of components found.
4. Each extracted component will be saved as a separate PNG file and displayed on the page.

## Notes

- The extracted components are saved in the `static/uploads` directory.
- The application currently supports image formats such as PNG, JPG, JPEG, GIF, and WEBP.

## License

This project is licensed under the MIT License.
