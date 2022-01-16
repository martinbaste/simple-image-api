from PIL import Image
from PIL.ImageChops import difference
from io import BytesIO

def center_crop(img_file, width, height):
    """
    Given width, height and an image. Crop it from the center with specified width and height.
    """
    #img_format = img_file.filename.split(".")[-1]
    img = Image.open(img_file)
    img_format = img.format
    img_width, img_height = img.size
    left = (img_width - width) / 2
    top = (img_height - height) / 2
    right = img_width - left
    bottom = img_height - top
    img = img.crop((left, top, right, bottom))
    img_buf = BytesIO()
    img.save(img_buf, img_format)
    img_buf.seek(0)
    return img_buf, img_format

def image_difference(img_file_1, img_file_2):
    """
    Given two images, return the difference between them.
    It substracts the pixel values of the two images and returns the difference.

    Assumes that the images are the same size and format.
    Useful when used to identify 'raw' change between images, 
    for example to quantify growth of a plant, movement, etc.

    Returns image in the same format as img_file_1.
    """
    img_1 = Image.open(img_file_1)
    img_format = img_1.format
    img_1 = img_1.convert('RGB')
    img_2 = Image.open(img_file_2).convert('RGB')
    dif_img = difference(img_1, img_2)
    img_buf = BytesIO()
    dif_img.save(img_buf, img_format)
    img_buf.seek(0)
    return img_buf, img_format

def image_hash(img_file):
    """
    Given an image, return the hash of the image
    We can't get the hash of the image file because the timestamp can be different for each image.
    Using this solution: https://stackoverflow.com/questions/49689550/simple-hash-of-pil-image
    Basically, reduce the image to a 10x10 pixel image, and then calculate the average pixel value.
    Then get an string of 1/0 values, where 1 is a pixel with a value greater than the average, 
    and 0 is a pixel with a value less than the average.
    Finally, convert the binary string into hex representation, and return it.
    """
    img = Image.open(img_file)

    img = img.resize((10, 10), Image.ANTIALIAS)
    img = img.convert('L')
    pixel_data = list(img.getdata())
    avg_pixel = sum(pixel_data)/len(pixel_data)
    bits = "".join(['1' if (px >= avg_pixel) else '0' for px in pixel_data])
    hex_representation = str(hex(int(bits, 2)))[2:][::-1].upper()

    return hex_representation