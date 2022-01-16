
from flask import Flask, render_template, request, send_file

import services.image as image_service

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")

@app.route('/api-examples/<api_name>')
def api_examples(api_name):
    """API Examples html"""

    if api_name in ['center-crop', 'image-difference', 'image-hash']:
        return render_template(f"api_examples/{api_name}.html")
    else:
        return "No API example found for " + api_name, 404


@app.route("/api/center-crop", methods=["POST"])
def center_crop():
    """
    Given width, height and an image. Crop it from the center with width and height
    """
    # Validate parameters
    width = request.form.get("width")
    height = request.form.get("height")
    if not width or not height:
        return "width and height are required", 400
    try:
        width = int(width)
        height = int(height)
    except ValueError:
        return "width and height must be integers", 400

    img_file = request.files.get("image")
    if not img_file:
        return "image file is required", 400

    img_format = img_file.filename.split(".")[-1]
    if not img_format in ["jpg", "jpeg", "png"]:
        return "invalid format", 400

    img_buf = image_service.center_crop(img_file, width, height)

    return send_file(img_buf, mimetype="image/" + img_format)

@app.route("/api/image-difference", methods=["POST"])
def image_difference():
    """
    Given two images, return the difference between them
    """
    img_file_1 = request.files.get("image1")
    if not img_file_1:
        return "image1 is required", 400

    img_file_2 = request.files.get("image2")
    if not img_file_2:
        return "image2 is required", 400

    img_format_1 = img_file_1.filename.split(".")[-1]
    if not img_format_1 in ["jpg", "jpeg", "png"]:
        return "invalid format for image1", 400
    
    img_format_2 = img_file_2.filename.split(".")[-1]
    if not img_format_2 in ["jpg", "jpeg", "png"]:
        return "invalid format for image2", 400

    img_buf = image_service.image_difference(img_file_1, img_file_2)

    return send_file(img_buf, mimetype="image/" + img_format_1)

@app.route("/api/image-hash", methods=["POST"])
def image_hash():
    """
    Given an image, return the hash of the image
    """
    img_file = request.files.get("image")
    if not img_file:
        return "image is required", 400

    img_format = img_file.filename.split(".")[-1]
    if not img_format in ["jpg", "jpeg", "png"]:
        return "invalid format", 400

    img_hash = image_service.image_hash(img_file)

    # Return the hash as a string in json, so it can be parsed by javascript
    return f'{{"hash": "{img_hash}"}}'


if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host="0.0.0.0", debug=True, port=80)
