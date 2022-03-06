from ast import walk
from http import HTTPStatus
from typing import Iterable
from flask import Flask, safe_join, send_file, request
import os

from app.video_package import get_file_path, converted_file_format, upload_video

app = Flask(__name__)


@app.get("/videos")
def retrieve():
    # files_list = os.listdir("./videos")
    *_, files_list = next(os.walk("./videos"))

    return {"msg": files_list}, HTTPStatus.OK


@app.get("/videos/play/<filename>")
def play(filename: str):
    filepath = get_file_path(filename)

    return send_file(filepath), HTTPStatus.OK


@app.get("/videos/download/<filename>")
def download(filename: str):
    extension_format = request.args.get("format")
    filepath = get_file_path(filename)

    if extension_format:
        converted_file_format(filename, extension_format)
        return send_file(filepath, as_attachment=True), HTTPStatus.OK

    return send_file(filepath, as_attachment=True), HTTPStatus.OK

@app.post("/videos")
def upload():
    # ImmutableMultiDict Iterable
    files = request.files

    for file in files.values(): 
        upload_video(file)

    return {"msg" : "videos uploaded"}, HTTPStatus.CREATED