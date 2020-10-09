"""
The code below is based entirely on the example from the picamera docs.
You can find it by entering this URL in your browser:
https://picamera.readthedocs.io/en/latest/recipes2.html?highlight=streaming#web-streaming
"""
import io
import logging
import os
import socketserver
from http import server
from threading import Condition

import picamera

# ----- CONSTANTS -----
CAMERA_DIR = os.path.dirname(__file__)
HTML_FILE_PATH = os.path.join(CAMERA_DIR, "../remote_camera.html")
STREAM_FILE = "stream.mjpg"
TITLE = "RPi Remote Camera"
STREAMING_OUTPUT_PATH = os.path.join(CAMERA_DIR, STREAM_FILE)
VIDEO_WIDTH = 1260
VIDEO_HEIGHT = 720


def config_html(title, source_file_path, width, height):
    with open(HTML_FILE_PATH, "r") as html_file:
        html_raw = (
            html_file.read()
            .replace("$TITLE", title)
            .replace("$SRC", source_file_path)
            .replace("$WIDTH", width)
            .replace("$HEIGHT", height)
        )
    return html_raw


PAGE = config_html(TITLE, STREAMING_OUTPUT_PATH, str(VIDEO_WIDTH), str(VIDEO_HEIGHT))


class StreamingOutput(object):
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()

    def write(self, buf):
        if buf.startswith(b"\xff\xd8"):
            self.buffer.truncate()
            with self.condition:
                self.frame = self.buffer.getvalue()
                self.condition.notify_all()
            self.buffer.seek(0)
        return self.buffer.write(buf)


class StreamingHandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_response(301)
            self.send_header("Location", "/index.html")
            self.end_headers()
        elif self.path == "/index.html":
            content = PAGE.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.send_header("Content-Length", len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == f"/{STREAM_FILE}":
            self.send_response(200)
            self.send_header("Age", 0)
            self.send_header("Cache-Control", "no-cache, private")
            self.send_header("Pragma", "no-cache")
            self.send_header(
                "Content-Type", "multipart/x-mixed-replace; boundary=FRAME"
            )
            self.end_headers()
            try:
                while True:
                    with output.condition:
                        output.condition.wait()
                        frame = output.frame
                    self.wfile.write(b"--FRAME\r\n")
                    self.send_header("Content-Type", "image/jpeg")
                    self.send_header("Content-Length", len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b"\r\n")
            except Exception as e:
                logging.warning(
                    "Removed streaming client %s: %s", self.client_address, str(e)
                )
        else:
            self.send_error(404)
            self.end_headers()


class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True


with picamera.PiCamera(
    resolution=f"{VIDEO_WIDTH}x{VIDEO_HEIGHT }", framerate=24
) as camera:
    output = StreamingOutput()
    camera.rotation = 180
    camera.start_recording(output, format="mjpeg")
    try:
        address = ("", 8000)
        server = StreamingServer(address, StreamingHandler)
        server.serve_forever()
    finally:
        camera.stop_recording()
