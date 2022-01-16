
from flask import Flask, render_template, request, send_file

import services.image as image_service
from services.utils import get_images_from_request

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

    # Get image from request
    validated = get_images_from_request(request)
    if validated['files'] is None:
        return validated['error'], validated['status']

    img_buf, img_format = image_service.center_crop(validated['files'][0], width, height)
    return send_file(img_buf, mimetype="image/" + img_format)

@app.route("/api/image-difference", methods=["POST"])
def image_difference():
    """
    Given two images, return the difference between them
    """
    # Get images from request
    validated = get_images_from_request(request, 2)
    if validated['files'] is None:
        return validated['error'], validated['status']

    img_buf, img_format = image_service.image_difference(validated["files"][0], validated["files"][1])

    return send_file(img_buf, mimetype="image/" + img_format)

@app.route("/api/image-hash", methods=["POST"])
def image_hash():
    """
    Given an image, return the hash of the image
    """
    # Get image from request
    validated = get_images_from_request(request)
    if validated['files'] is None:
        return validated['error'], validated['status']

    img_hash = image_service.image_hash(validated['files'][0])

    # Return the hash as a string in json, so it can be parsed by javascript
    return f'{{"hash": "{img_hash}"}}'


if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host="0.0.0.0", debug=True, port=80)
