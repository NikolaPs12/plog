import os
import secrets
from PIL import Image
from flask import current_app

def save_picture(picture_file):

    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(picture_file.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(picture_file)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn