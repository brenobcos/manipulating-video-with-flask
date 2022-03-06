import os
from flask import safe_join
from datetime import datetime as dt
from werkzeug.utils import secure_filename

VIDEOS_DIRECTORY = os.getenv("VIDEOS_DIRECTORY")


def get_file_path(filename: str):
    abs_path = os.path.abspath(VIDEOS_DIRECTORY)
    filepath = safe_join(abs_path, filename)

    return filepath


def converted_file_format(filename: str, ext_format: str):
    filename_base = filename.split(".")[0]
    converted_filename = filename_base + "." + ext_format
    # converted_filename = ".".join([filename_base, extension_format])

    filepath = get_file_path(converted_filename)
    imput_path = get_file_path(filename)

    command = f"ffmpeg -i {imput_path} {filepath}"

    os.system(command)


# file -> Objeto do tipo FileStorage
def upload_video(file):
    filename = generate_random_filename(file.filename)
    filepath = get_file_path(filename)

    file.save(filepath)


def generate_random_filename(filename: str):
    filename_user = filename.split(".")[0]
    extension = filename.split(".")[-1]
    random_filename = str(dt.now().timestamp())

    random_filename += filename_user + "." + extension
    # random_filename = ".".join([filename_user, random_filename, extension])

    return secure_filename(random_filename)
