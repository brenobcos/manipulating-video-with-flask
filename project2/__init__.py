from ast import walk
from http import HTTPStatus
from flask import Flask, safe_join, send_file, request
import os

from project2.video_handler.video_service import get_file_path

app = Flask(__name__)
VIDEOS_DIRECTORY = os.getenv("VIDEOS_DIRECTORY")


@app.get("/videos")
def retrieve():
    # *_, files_list = list(os.walk("./videos"))[0]
    *_, files_list = next(os.walk("./videos"))

    return {"msg": files_list}, HTTPStatus.OK


@app.get("/videos/play/<filename>")
def play(filename: str):
    abs_path = os.path.abspath(VIDEOS_DIRECTORY)
    filepath = safe_join(abs_path, filename)

    # TODO: verificar se filepath é diferente de None video41min

    return send_file(filepath), HTTPStatus.OK


@app.get("/videos/download/<filename>")
def download(filename: str):
    extension_format = request.args.get("format")
    filepath = get_file_path(VIDEOS_DIRECTORY, filename)

    if extension_format:
        filename_base = filename.split(".")[0]
        converted_filename = filename_base + "." + extension_format
        # converted_filename = ".".join([filename_base, extension_format])

        filepath = get_file_path(VIDEOS_DIRECTORY, converted_filename)
        imput_path = get_file_path(VIDEOS_DIRECTORY, filename)

        command = f"ffmpeg -i {imput_path} {filepath}"

        os.system(command)

        return send_file(filepath, as_attachment=True), HTTPStatus.OK

    return send_file(filepath, as_attachment=True), HTTPStatus.OK
