from PIL import Image
import os

def convert_to_favicon(image_path, output_favicorn_path, size=(16, 16)):
    """
    Converts an image to a favicon.

    Args:
    image_path (str): Path to the input image file.
    output_path (str): Path to save the converted favicon.
    size (tuple): Tuple specifying the dimensions of the favicon. Default is (16, 16).

    Returns:
    None
    """
    try:
        # Open the image
        img = Image.open(image_path)

        if not img:
            raise Exception('Image not found')
        else:
        # Resize the image to favicon size
            img = img.resize(size, Image.ANTIALIAS)

        # Save as ICO format
        img.save(output_favicorn_path, format="ICO")

        print("Favicon created successfully!")

    except Exception as e:
        print(f"Error converting to favicon: {e}")

# Example usage:
image_path = os.path.abspath('/backend/imagefile.png')
output_favicon_path = "output_favicon.ico"
convert_to_favicon(image_path, output_favicon_path)
