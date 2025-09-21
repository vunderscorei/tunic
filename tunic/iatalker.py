import json
import tkinter as tk
from io import BytesIO
from urllib import request


def get_size(newsgroup: str) -> int:
    root: str = newsgroup.split('.')[0]
    meta_url: str = 'https://archive.org/metadata/usenet-%s/files/%s.mbox.zip' % (root, newsgroup)
    with request.urlopen(meta_url) as resp:
        body: dict = json.loads(resp.read())
    if body and 'result' in body:
        return int(body['result']['size'])
    else:
        return -1


def get_url(newsgroup: str) -> str:
    root: str = newsgroup.split('.')[0]
    return 'https://archive.org/download/usenet-%s/%s.mbox.zip' % (root, newsgroup)


def percent_done(current_size: int, total_size: int) -> int:
    if current_size == 0:
        return 0
    elif current_size >= total_size:
        return 100
    else:
        return int(100.0 * (float(current_size) / float(total_size)))


def download(url: str, target_size: int, cancel_flag: tk.BooleanVar, log_var: tk.StringVar,
             chunk_size: int = 1_000_000) -> BytesIO | None:
    data: BytesIO = BytesIO()
    current_size: int = 0
    # todo: handle error codes
    with request.urlopen(url) as resp:
        while True:
            if cancel_flag.get():
                return None

            buffer: bytes | None = resp.read(chunk_size)
            if not buffer:
                break
            data.write(buffer)
            current_size += len(buffer)
            log_var.set('Downloading... (%d%%)' % percent_done(current_size, target_size))
        return data
