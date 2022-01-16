import requests

def get_images_from_request(request, num_files=1):
    """
    Given a request, return the image file.
    Returns a dictionary with the image file or validation errors
    """

    image_params = ["image"] + ["image_" + str(i) for i in range(2, num_files + 1)]
    image_files = []
    for param in image_params:

        img_file = request.files.get(param)
        img_url = request.form.get(f"{param}_url")
        if not img_file and not img_url:
            return {
                "error": f"{param} or {param}_url is required",
                "status": 400,
                "files": None
            }

        # If both are supplied, img_file takes precedence
        if img_file:
            img_format = img_file.filename.split(".")[-1]
            if not img_format in ["jpg", "jpeg", "png"]:
                return {
                    "error": f"invalid format for {param}",
                    "status": 400,
                    "files": None
                }
        else:
            img_file = download_file(img_url)
        
        image_files.append(img_file)
    
    return {
        "error": None,
        "status": 200,
        "files": image_files
    }

def download_file(file_url):
    """
    Given a url, download the file and return the file buffer
    NOTE: I'd secure this function to prevent attacks:
        - Prevent files that are too big
        - Whitelist domains
        - Other potential security issues when downloading arbitrary files?
    """
   
    response = requests.get(file_url, stream=True)
    if response.status_code != 200:
        return None
    return response.raw